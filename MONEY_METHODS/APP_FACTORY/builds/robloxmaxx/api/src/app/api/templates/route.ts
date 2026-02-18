import { NextRequest, NextResponse } from 'next/server';
import { GAME_TEMPLATES } from '@/templates/index';

export async function GET(request: NextRequest) {
  const genre = request.nextUrl.searchParams.get('genre');

  if (genre && genre in GAME_TEMPLATES) {
    const template = GAME_TEMPLATES[genre as keyof typeof GAME_TEMPLATES];
    return NextResponse.json({ template });
  }

  // Return all template summaries
  const summaries = Object.entries(GAME_TEMPLATES).map(([key, val]) => ({
    genre: key,
    name: val.name,
    description: val.description,
    scriptCount: val.scripts.length,
  }));

  return NextResponse.json({ templates: summaries });
}
