import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import { ToastProvider } from '@/components/Toast';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const jetbrains = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains',
  display: 'swap',
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'https://autoreplyai.com'),
  title: 'AutoReplyAI - AI Customer Support That Never Sleeps',
  description:
    'Deploy an AI support agent trained on your knowledge base in under 5 minutes. Resolve 90% of tickets automatically, 24/7. Trusted by 2,000+ businesses worldwide.',
  keywords:
    'AI customer support, chatbot, customer service automation, support widget, AI chat, customer support software, help desk AI',
  openGraph: {
    title: 'AutoReplyAI - AI Customer Support That Never Sleeps',
    description:
      'Deploy an AI support agent trained on your knowledge base in under 5 minutes. Resolve 90% of tickets automatically, 24/7.',
    url: 'https://autoreplyai.com',
    siteName: 'AutoReplyAI',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'AutoReplyAI - AI Customer Support Platform',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AutoReplyAI - AI Customer Support That Never Sleeps',
    description:
      'Deploy an AI support agent trained on your knowledge base in under 5 minutes. Resolve 90% of tickets automatically, 24/7.',
    images: ['/twitter-image.jpg'],
    creator: '@autoreplyai',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrains.variable} scroll-smooth`}>
      <body className="font-sans antialiased">
        <ToastProvider>{children}</ToastProvider>
      </body>
    </html>
  );
}
