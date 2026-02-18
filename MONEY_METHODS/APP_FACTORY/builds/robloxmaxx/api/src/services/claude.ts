import Anthropic from '@anthropic-ai/sdk';

// BYOK architecture: We never store or use our own Anthropic API key.
// Every AI call uses the user's API key, passed in the request.
// This means zero API cost risk for us.

export interface GenerateRequest {
  prompt: string;
  mode: 'code' | 'question' | 'scaffold';
  genre: string;
  context: string;
  systemPrompt: string;
}

export async function generateWithUserKey(
  userApiKey: string,
  req: GenerateRequest,
  model: string = 'claude-sonnet-4-5-20250929'
): Promise<string> {
  const client = new Anthropic({ apiKey: userApiKey });

  const userMessage =
    req.context && req.context.length > 0
      ? `CURRENT GAME CODE:\n${req.context}\n\nUSER REQUEST: ${req.prompt}`
      : `USER REQUEST (empty game, create from scratch): ${req.prompt}`;

  const message = await client.messages.create({
    model,
    max_tokens: 8192,
    system: req.systemPrompt,
    messages: [{ role: 'user', content: userMessage }],
  });

  const textBlock = message.content.find((b) => b.type === 'text');
  return textBlock ? textBlock.text : '';
}

export async function generateScaffoldWithUserKey(
  userApiKey: string,
  gameDescription: string,
  genre: string,
  systemPrompt: string,
  model: string = 'claude-sonnet-4-5-20250929'
): Promise<string> {
  const client = new Anthropic({ apiKey: userApiKey });

  const message = await client.messages.create({
    model,
    max_tokens: 16384,
    system: systemPrompt,
    messages: [
      {
        role: 'user',
        content: `Generate a COMPLETE ${genre} Roblox game from this description: ${gameDescription}\n\nCreate all scripts, folders, UI, and systems needed for a fully playable game. Include monetization hooks (gamepasses, dev products). Return the JSON array of actions.`,
      },
    ],
  });

  const textBlock = message.content.find((b) => b.type === 'text');
  return textBlock ? textBlock.text : '';
}
