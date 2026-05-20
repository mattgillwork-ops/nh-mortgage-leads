import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import "./globals.css";

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "Top 10 Best Mortgage Lenders in NH (2026 Reviews) | NH Financial Review",
  description: "Compare the top 10 mortgage lenders in New Hampshire for 2026. See our top picks for first-time buyers, refinancing, and fast local closings.",
  keywords: ["best mortgage lenders NH", "NH mortgage reviews", "lender comparison NH", "loan officer NH"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${outfit.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-[#f8fafc] text-[#0f172a]">{children}</body>
    </html>
  );
}
