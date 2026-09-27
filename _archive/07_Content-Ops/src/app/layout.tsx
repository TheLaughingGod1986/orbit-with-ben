import type { Metadata } from "next";
import { Fraunces, Space_Grotesk } from "next/font/google";
import "./globals.css";
import { AppShell } from "@/components/AppShell";
import { DryRunBanner } from "@/components/DryRunBanner";

const display = Fraunces({
  variable: "--font-orbit-display",
  subsets: ["latin"],
});

const sans = Space_Grotesk({
  variable: "--font-orbit-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Orbit Content Ops",
  description: "Multi-platform distribution studio for Orbit with Ben",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${sans.variable} antialiased font-sans`}>
        <DryRunBanner />
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
