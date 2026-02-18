import { NextRequest, NextResponse } from 'next/server';
import { generateWithUserKey } from '@/services/claude';
import { authenticateRequest } from '@/services/auth';
import { incrementUsage } from '@/services/db';
import { buildSystemPrompt } from '@/prompts/system';

// Genre meta context injected into every generation for meta-awareness
const GENRE_META_CONTEXT: Record<string, string> = {
  simulator: `CURRENT META: Simulator genre is WARM with HIGH saturation. Pet sims oversaturated. Garden/cooking/fishing sims have space. Hot mechanics: rare drops, trading economy, idle progression. AVOID generic click-to-earn and copies of top games.`,
  tycoon: `CURRENT META: Tycoon genre is WARM but DECLINING. Dropper tycoons are dead. Hybrid tycoons (tycoon+simulator or tycoon+RPG) work if theme is fresh. Hot mechanics: hybrid genre mashups, narrative-driven progression, cooperative tycoons. AVOID generic dropper tycoons.`,
  obby: `CURRENT META: Obby genre is COOL with EXTREME saturation. Basic obbies are dead. Tower-of-Hell-style random obbies and horror obbies still draw players. Need strong social or competitive element. Hot mechanics: randomized stages, multiplayer races, horror obby hybrid. AVOID basic checkpoint obbies.`,
  rpg: `CURRENT META: RPG genre is HOT and GROWING with MEDIUM saturation. Strong demand. Anime-inspired RPGs dominate. Focus on satisfying combat feel and deep progression. Dungeon crawlers and roguelikes are underexplored. Hot mechanics: anime combat, roguelike runs, gacha-style character collection. AVOID slow turn-based combat and empty open worlds.`,
  horror: `CURRENT META: Horror genre is HOT and GROWING with LOW-MEDIUM saturation. Multiplayer horror (Doors-style) prints. Single-player story horror has lower retention but high streaming appeal. Hot mechanics: procedural rooms, entity catalog, co-op survival, proximity voice chat. AVOID static jumpscare-only games.`,
  fps: `CURRENT META: FPS genre is HOT and GROWING. PS5 launch bringing new controller audience. Weapon skin economies and ranked modes drive spending. Hot mechanics: weapon skin economy, ranked competitive, battle pass seasons. AVOID bad hit registration and lack of anti-cheat.`,
  social: `CURRENT META: Social genre is HOT with LOW saturation and VERY HIGH revenue potential. Fashion/social games monetize extremely well through avatar cosmetics. Dress to Impress proved the model. Hot mechanics: fashion competitions, avatar customization, social deduction. AVOID empty hangout games.`,
  survival: `CURRENT META: Survival genre is WARM with MEDIUM saturation. Natural disasters and zombie survival still perform. Base building + wave defense is underexplored. Hot mechanics: base building, wave defense, crafting systems. AVOID generic survival with no goal.`,
};

function getMetaContext(genre: string): string {
  const normalized = genre.toLowerCase();
  if (GENRE_META_CONTEXT[normalized]) {
    return GENRE_META_CONTEXT[normalized];
  }
  return `CURRENT META: Trending now on Roblox: calm farming sims, hybrid genres, social fashion, FPS with ranked modes, anime combat RPGs, procedural horror. Dying: generic dropper tycoons, basic obbies, adopt me clones. Platform updates: 4D Generation open beta, Rewarded ads expansion, PS5 launch, Subscriptions API.`;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { token, prompt, mode, genre, context, pluginVersion, apiKey } = body;

    // API key is required (BYOK model)
    const userApiKey = apiKey || request.headers.get('x-api-key');
    if (!userApiKey) {
      return NextResponse.json(
        { error: 'API key required. Bring your own Claude/Anthropic API key.' },
        { status: 400 }
      );
    }

    if (!prompt) {
      return NextResponse.json(
        { error: 'Missing prompt' },
        { status: 400 }
      );
    }

    // Authenticate (optional for basic generation, required for Pro features)
    let userId: number | null = null;
    if (token) {
      const auth = authenticateRequest(token);
      if (auth) {
        userId = auth.userId;
      }
    }

    // Build system prompt with meta context injection
    const baseSystemPrompt = buildSystemPrompt(mode || 'code', genre || 'general');
    const metaContext = getMetaContext(genre || 'general');
    const systemPrompt = baseSystemPrompt + '\n\n## Current Roblox Meta (Auto-injected)\n' + metaContext;

    // Generate with the user's own API key (BYOK - zero cost to us)
    const response = await generateWithUserKey(userApiKey, {
      prompt,
      mode: mode || 'code',
      genre: genre || 'general',
      context: context || '',
      systemPrompt,
    });

    // Track usage for analytics only (no limits enforced)
    if (userId) {
      incrementUsage(userId, 'generate', genre || 'general', mode || 'code', response.length);
    }

    return NextResponse.json({ response });
  } catch (error) {
    console.error('[/api/generate] Error:', error);

    // Surface Anthropic API errors clearly (bad key, rate limit, etc)
    const errMsg = error instanceof Error ? error.message : 'Generation failed';
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
