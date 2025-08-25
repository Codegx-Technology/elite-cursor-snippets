import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../globals.css";
import Layout from "@/components/Layout";
import ClientBoot from "@/components/ClientBoot";
import { PlanGuardProvider } from "@/context/PlanGuardContext";
import { AuthProvider } from "@/context/AuthContext";
import { ErrorProvider } from "@/context/ErrorContext";
import ErrorNotification from "@/components/ErrorNotification";
import { ToastProvider } from "@/components/ui/use-toast";

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

export default function LocaleLayout({
  children,
  params: {lang}
}: Readonly<{
  children: React.ReactNode;
  params: {lang: string};
}>) {
  return (
    <html lang={lang}>
      <body className={inter.className}>
        <ToastProvider>
          <ErrorProvider>
            <AuthProvider>
              <PlanGuardProvider>
                <Layout>{children}</Layout>
              </PlanGuardProvider>
            </AuthProvider>
            <ClientBoot />
            <ErrorNotification />
          </ErrorProvider>
        </ToastProvider>
      </body>
    </html>
  );
}
