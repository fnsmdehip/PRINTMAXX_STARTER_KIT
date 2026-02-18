import { NextRequest, NextResponse } from 'next/server';
import { authenticateRequest } from '@/services/auth';
import { incrementUsage } from '@/services/db';
import Anthropic from '@anthropic-ai/sdk';

const SCAN_SYSTEM_PROMPT = `You are a Roblox game quality auditor. Analyze the provided game scripts and score them across 5 categories:

1. SECURITY (0-25): Client trust violations, unvalidated RemoteEvents, exploitable physics, exposed secrets
2. DATA PERSISTENCE (0-20): DataStore usage, save-on-leave, BindToClose, pcall wrapping, defaults
3. MONETIZATION (0-25): Gamepasses, DevProducts, ProcessReceipt, purchase prompts, value visibility
4. ENGAGEMENT (0-15): Core loop speed, progression visibility, variable rewards, social features, idle elements
5. MOBILE (0-15): Touch-friendly UI, screen scaling, no keyboard-only inputs, performance

Score generously for what IS present. Deduct for what is MISSING or BROKEN.
Focus on actionable issues with specific fixes.

Return ONLY a JSON object (no markdown, no backticks) with this exact structure:
{
  "score": <number 0-100>,
  "security": { "score": <number 0-25>, "issues": [<string>], "fixes": [<string>] },
  "persistence": { "score": <number 0-20>, "issues": [<string>], "fixes": [<string>] },
  "monetization": { "score": <number 0-25>, "issues": [<string>], "fixes": [<string>] },
  "engagement": { "score": <number 0-15>, "issues": [<string>], "fixes": [<string>] },
  "mobile": { "score": <number 0-15>, "issues": [<string>], "fixes": [<string>] },
  "deprecated_apis": [<string>],
  "summary": "<1-2 sentence overall assessment>"
}`;

interface ScriptInput {
  name: string;
  path: string;
  source: string;
}

interface ScanRequest {
  scripts: ScriptInput[];
  genre?: string;
  token?: string;
  apiKey?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { scripts, genre, token, apiKey: bodyApiKey } = body as ScanRequest;

    // BYOK: API key required
    const userApiKey = bodyApiKey || request.headers.get('x-api-key');
    if (!userApiKey) {
      return NextResponse.json(
        { error: 'API key required. Bring your own Claude/Anthropic API key.' },
        { status: 400 }
      );
    }

    // Auth optional (for usage tracking)
    let userId: number | null = null;
    if (token) {
      const auth = authenticateRequest(token);
      if (auth) {
        userId = auth.userId;
      }
    }

    // Validate scripts input
    if (!scripts || !Array.isArray(scripts) || scripts.length === 0) {
      return NextResponse.json(
        { error: 'scripts array is required and must not be empty' },
        { status: 400 }
      );
    }

    if (scripts.length > 50) {
      return NextResponse.json(
        { error: 'Maximum 50 scripts per scan' },
        { status: 400 }
      );
    }

    // Validate each script entry
    for (const script of scripts) {
      if (
        !script ||
        typeof script.name !== 'string' ||
        typeof script.source !== 'string'
      ) {
        return NextResponse.json(
          { error: 'Each script must have name (string) and source (string)' },
          { status: 400 }
        );
      }
    }

    // Build the scripts content for analysis
    const scriptsText = scripts
      .map(
        (s) =>
          `--- SCRIPT: ${s.name} (${s.path || 'unknown path'}) ---\n${s.source}`
      )
      .join('\n\n');

    // Truncate if too long
    const maxChars = 80000;
    const truncatedScripts =
      scriptsText.length > maxChars
        ? scriptsText.slice(0, maxChars) + '\n\n[TRUNCATED - too many scripts to analyze at once]'
        : scriptsText;

    const genreContext = genre
      ? `\nGame genre: ${genre}. Score monetization and engagement relative to ${genre} genre expectations.`
      : '';

    const userMessage = `Analyze these Roblox game scripts for quality issues:${genreContext}\n\n${truncatedScripts}`;

    // Use the user's API key (BYOK - zero cost to us)
    const client = new Anthropic({ apiKey: userApiKey });
    const message = await client.messages.create({
      model: 'claude-3-5-haiku-20241022',
      max_tokens: 4096,
      system: SCAN_SYSTEM_PROMPT,
      messages: [{ role: 'user', content: userMessage }],
    });

    const textBlock = message.content.find((b) => b.type === 'text');
    const responseText = textBlock ? textBlock.text : '';

    // Track usage for analytics only (no limits enforced)
    if (userId) {
      incrementUsage(userId, 'scan', genre || 'general', 'scan', responseText.length);
    }

    // Parse the JSON response
    let scanResult;
    try {
      // Strip any markdown code fences if present
      const cleaned = responseText
        .replace(/^```json?\s*/i, '')
        .replace(/\s*```$/i, '')
        .trim();
      scanResult = JSON.parse(cleaned);
    } catch {
      // If parsing fails, return the raw text with a warning
      return NextResponse.json({
        warning: 'AI returned non-JSON response. Raw analysis included.',
        raw_analysis: responseText,
        score: 0,
      });
    }

    return NextResponse.json(scanResult);
  } catch (error) {
    console.error('[/api/scan-game] Error:', error);

    const errMsg = error instanceof Error ? error.message : 'Game scan failed';
    const status = errMsg.includes('401') || errMsg.includes('authentication')
      ? 401
      : errMsg.includes('429')
        ? 429
        : 500;

    return NextResponse.json(
      { error: errMsg },
      { status }
    );
  }
}
