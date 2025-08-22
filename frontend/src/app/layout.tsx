import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Layout from "@/components/Layout";
import ClientBoot from "@/components/ClientBoot";
import { PlanGuardProvider } from "@/context/PlanGuardContext"; // New import
import { AuthProvider } from "@/context/AuthContext"; // New import for AuthProvider
import { ErrorProvider } from "@/context/ErrorContext"; // Re-added ErrorProvider
import ErrorNotification from "@/components/ErrorNotification"; // Re-added ErrorNotification

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Root layout with Kenya-first design system and enterprise styling
// [GOAL]: Proper CSS loading and layout wrapper for entire application
// [TASK]: Import global styles and wrap with Layout component

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Shujaa Studio - Kenya-First AI Video Platform",
  description: "Empowering African storytellers with cutting-edge AI video generation technology",
  keywords: "AI video generation, Kenya, Africa, storytelling, content creation, artificial intelligence",
  authors: [{ name: "Shujaa Studio Team" }],
  creator: "Shujaa Studio",
  publisher: "Shujaa Studio",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://shujaa.studio'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: "Shujaa Studio - Kenya-First AI Video Platform",
    description: "Empowering African storytellers with cutting-edge AI Video Platform",
    url: 'https://shujaa.studio',
    siteName: 'Shujaa Studio',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Shujaa Studio - Kenya-First AI Video Platform',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: "Shujaa Studio - Kenya-First AI Video Platform",
    description: "Empowering African storytellers with cutting-edge AI Video Platform",
    images: ['/twitter-image.png'],
    creator: '@ShujaaStudio',
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
  manifest: '/manifest.json',
  icons: {
    icon: [
      { url: '/icon-32x32.png', sizes: '32x32', type: 'image/png' },
      { url: '/icon-192x192.png', sizes: '192x192', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'Shujaa Studio',
  },
  verification: {
    google: 'your-google-verification-code',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes" />
        <meta name="theme-color" content="#00A651" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Shujaa Studio" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="msapplication-TileColor" content="#00A651" />
        <meta name="msapplication-config" content="/browserconfig.xml" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="//fonts.googleapis.com" />
        <link rel="dns-prefetch" href="//fonts.gstatic.com" />
      </head>
      <body className={inter.className} suppressHydrationWarning={true}>
        <ErrorProvider> {/* Wrap with ErrorProvider */}
          <AuthProvider> {/* Wrap with AuthProvider */}
            <PlanGuardProvider> {/* Wrap with PlanGuardProvider */}
              <Layout>{children}</Layout>
            </PlanGuardProvider>
          </AuthProvider>
          <ClientBoot />
          <ErrorNotification /> {/* Render ErrorNotification */}
        </ErrorProvider>
      </body>
    </html>
  );
}
