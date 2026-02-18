import { NextResponse } from 'next/server';
import { readFileSync } from 'fs';
import { join } from 'path';

export async function GET() {
  try {
    const pluginPath = join(process.cwd(), '..', 'plugin', 'RobloxMaxxPlugin.lua');
    const content = readFileSync(pluginPath, 'utf-8');

    return new NextResponse(content, {
      status: 200,
      headers: {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': 'attachment; filename="RobloxMaxxPlugin.lua"',
      },
    });
  } catch {
    return NextResponse.json(
      { error: 'Plugin file not found' },
      { status: 404 }
    );
  }
}
