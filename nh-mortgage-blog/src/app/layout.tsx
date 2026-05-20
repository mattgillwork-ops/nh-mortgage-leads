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
  title: "New Hampshire Mortgage Blog & Homeowner Guide",
  description: "Your trusted source for New Hampshire mortgage guides, local interest rate updates, NHHFA home start qualifications, and closing cost breakdowns.",
  keywords: ["NH Mortgage", "New Hampshire mortgage rates", "NHHFA Home Start", "NH closing costs", "lender reviews"],
  authors: [{ name: "Anti-Gravity Financial Editorial" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${outfit.variable} h-full antialiased`}>
      <head>
        {/* Lemonade Affiliate Verification */}
        <meta name="fo-verify" content="201efa5d-8e8e-40dc-bc9f-cbcab045d651" />
      </head>
      <body className="min-h-full flex flex-col bg-[#f8fafc] text-[#0f172a]">{children}</body>
    </html>
  );
}
