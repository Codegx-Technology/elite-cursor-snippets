import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Layout from "@/components/Layout";

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Root layout with Kenya-first design system and enterprise styling
// [GOAL]: Proper CSS loading and layout wrapper for entire application
// [TASK]: Import global styles and wrap with Layout component

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Shujaa Studio - Kenya-First AI Video Platform",
  description: "Empowering African storytellers with cutting-edge AI video generation technology",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Layout>{children}</Layout>
      </body>
    </html>
  );
}
