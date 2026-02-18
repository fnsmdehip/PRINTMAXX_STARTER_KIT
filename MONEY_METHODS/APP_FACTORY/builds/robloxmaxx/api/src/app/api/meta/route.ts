import { NextRequest, NextResponse } from 'next/server';

const GENRE_META = [
  {
    name: 'simulator',
    health: 'WARM',
    trend: 'stable',
    saturation: 'HIGH',
    revenue_potential: 'MEDIUM-HIGH',
    recommendation:
      'Only enter with genuine innovation. Pet sims oversaturated but garden/cooking/fishing sims have space.',
    hot_mechanics: ['rare drops', 'trading economy', 'idle progression'],
    avoid: ['generic click-to-earn', 'copy of existing top games'],
  },
  {
    name: 'tycoon',
    health: 'WARM',
    trend: 'declining',
    saturation: 'VERY HIGH',
    revenue_potential: 'MEDIUM',
    recommendation:
      'Dropper tycoons are dead. Hybrid tycoons (tycoon + simulator or tycoon + RPG) still work if the theme is fresh.',
    hot_mechanics: ['hybrid genre mashups', 'narrative-driven progression', 'cooperative tycoons'],
    avoid: ['generic dropper tycoons', 'military base tycoons', 'any tycoon without a unique hook'],
  },
  {
    name: 'obby',
    health: 'COOL',
    trend: 'declining',
    saturation: 'EXTREME',
    revenue_potential: 'LOW-MEDIUM',
    recommendation:
      'Basic obbies are dead. Tower of Hell style random obbies and horror obbies still draw players. Need strong social or competitive element.',
    hot_mechanics: ['randomized stages', 'multiplayer races', 'horror obby hybrid'],
    avoid: ['basic checkpoint obbies', 'rainbow obby clones', 'obbies under 50 stages'],
  },
  {
    name: 'rpg',
    health: 'HOT',
    trend: 'growing',
    saturation: 'MEDIUM',
    revenue_potential: 'HIGH',
    recommendation:
      'Strong demand. Anime-inspired RPGs dominate. Focus on satisfying combat feel and deep progression. Dungeon crawlers and roguelikes are underexplored.',
    hot_mechanics: ['anime combat', 'roguelike runs', 'gacha-style character collection', 'dungeon finder'],
    avoid: ['slow turn-based combat', 'empty open worlds', 'generic fantasy without art direction'],
  },
  {
    name: 'horror',
    health: 'HOT',
    trend: 'growing',
    saturation: 'LOW-MEDIUM',
    revenue_potential: 'MEDIUM-HIGH',
    recommendation:
      'Strong niche with loyal audience. Multiplayer horror (Doors-style) prints. Single-player story horror has lower retention but high video/streaming appeal.',
    hot_mechanics: ['procedural rooms', 'entity catalog', 'co-op survival', 'proximity voice chat'],
    avoid: ['static jumpscare-only games', 'granny clones', 'games under 15 min playtime'],
  },
  {
    name: 'fps',
    health: 'HOT',
    trend: 'growing',
    saturation: 'MEDIUM',
    revenue_potential: 'HIGH',
    recommendation:
      'Roblox FPS audience is expanding fast with PS5 launch. Weapon skin economies and ranked modes drive spending. Arsenal/Rivals-style games set the bar.',
    hot_mechanics: ['weapon skin economy', 'ranked competitive', 'battle pass seasons', 'custom loadouts'],
    avoid: ['bad hit registration', 'no anti-cheat', 'games without matchmaking'],
  },
  {
    name: 'social',
    health: 'HOT',
    trend: 'growing',
    saturation: 'LOW',
    revenue_potential: 'VERY HIGH',
    recommendation:
      'Fashion/social games monetize extremely well through avatar cosmetics. Dress to Impress proved the model. Social deduction games also strong.',
    hot_mechanics: ['fashion competitions', 'avatar customization', 'social deduction', 'house decoration'],
    avoid: ['empty hangout games', 'social games without activities', 'copycats without unique cosmetics'],
  },
  {
    name: 'survival',
    health: 'WARM',
    trend: 'stable',
    saturation: 'MEDIUM',
    revenue_potential: 'MEDIUM-HIGH',
    recommendation:
      'Natural disasters and zombie survival still perform. Base building + wave defense is underexplored on Roblox.',
    hot_mechanics: ['base building', 'wave defense', 'crafting systems', 'natural disaster events'],
    avoid: ['generic survival with no goal', 'survival games without progression saves'],
  },
];

const TRENDING_NOW = [
  'calm farming sims',
  'hybrid genres',
  'social fashion',
  'FPS with ranked modes',
  'anime combat RPGs',
  'procedural horror',
  'dress-up competitions',
  'idle factory games',
];

const DYING = [
  'generic dropper tycoons',
  'basic obbies',
  'adopt me clones',
  'static hangout games',
  'generic click simulators',
  'copy-paste military tycoons',
];

const PLATFORM_UPDATES = [
  '4D Generation open beta - AI-assisted 3D asset creation in Studio',
  'Rewarded ads expansion - now available to more developers',
  'PS5 launch - new controller-first audience entering platform',
  'Creator Store overhaul - better asset discovery and sales',
  'Subscriptions API - recurring revenue option for developers',
  'Enhanced social features - voice chat improvements, party system upgrades',
];

export async function GET() {
  return NextResponse.json({
    genres: GENRE_META,
    trending_now: TRENDING_NOW,
    dying: DYING,
    platform_updates: PLATFORM_UPDATES,
    updated_at: new Date().toISOString().split('T')[0],
  });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => ({}));
    const { genre } = body as { genre?: string };

    if (genre && typeof genre === 'string') {
      const match = GENRE_META.find(
        (g) => g.name.toLowerCase() === genre.toLowerCase()
      );
      if (match) {
        return NextResponse.json({
          genres: [match],
          trending_now: TRENDING_NOW,
          dying: DYING,
          platform_updates: PLATFORM_UPDATES,
          updated_at: new Date().toISOString().split('T')[0],
        });
      }
      return NextResponse.json(
        { error: `Unknown genre: ${genre}. Available: ${GENRE_META.map((g) => g.name).join(', ')}` },
        { status: 400 }
      );
    }

    return NextResponse.json({
      genres: GENRE_META,
      trending_now: TRENDING_NOW,
      dying: DYING,
      platform_updates: PLATFORM_UPDATES,
      updated_at: new Date().toISOString().split('T')[0],
    });
  } catch (error) {
    console.error('[/api/meta] Error:', error);
    return NextResponse.json({ error: 'Failed to fetch meta data' }, { status: 500 });
  }
}
