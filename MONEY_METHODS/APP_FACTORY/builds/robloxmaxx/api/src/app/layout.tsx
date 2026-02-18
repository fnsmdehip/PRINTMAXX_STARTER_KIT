import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'RobloxMaxx - AI Game Builder for Roblox',
  description:
    'Build complete Roblox games from natural language. Tycoons, obbys, simulators, RPGs, horror games. AI generates production-ready Luau code directly in Roblox Studio.',
  keywords: [
    'roblox',
    'ai game builder',
    'roblox studio plugin',
    'luau code generator',
    'roblox tycoon builder',
    'roblox obby maker',
    'roblox simulator maker',
    'roblox ai',
  ],
  openGraph: {
    title: 'RobloxMaxx - AI Game Builder for Roblox',
    description:
      'Describe your game in plain English. RobloxMaxx generates production-ready Luau code, tests it, and deploys to your game. Tycoons, obbys, simulators, RPGs, horror.',
    type: 'website',
    siteName: 'RobloxMaxx',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'RobloxMaxx - AI Game Builder for Roblox',
    description:
      'Build complete Roblox games from natural language. 250 free actions/month.',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <nav className="navbar">
          <div className="nav-inner">
            <Link href="/" className="nav-logo">
              RobloxMaxx
            </Link>
            <div className="nav-links">
              <Link href="/docs" className="nav-link">Docs</Link>
              <Link href="/#pricing" className="nav-link">Pricing</Link>
              <Link href="/login" className="nav-link">Log in</Link>
              <Link href="/signup" className="nav-link nav-cta">Sign up</Link>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
