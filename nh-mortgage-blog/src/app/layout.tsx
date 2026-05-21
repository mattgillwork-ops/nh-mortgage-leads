import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import "./globals.css";

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://nh-mortgage-blog.onrender.com"),
  title: "New Hampshire Mortgage Blog & Homeowner Guide | Buying a home in NH",
  description: "Your trusted source for New Hampshire mortgage guides, local interest rate updates, an accurate NH mortgage calculator, and closing cost breakdowns.",
  keywords: ["NH Mortgage", "New Hampshire mortgage rates", "NHHFA Home Start", "NH closing costs", "lender reviews", "buying a home in NH", "NH mortgage calculator", "first-time homebuyer programs NH"],
  authors: [{ name: "Anti-Gravity Financial Editorial" }],
  other: {
    "fo-verify": "201efa5d-8e8e-40dc-bc9f-cbcab045d651",
  },
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
