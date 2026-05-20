import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://nh-mortgage-leads.onrender.com"),
  title: "NH Mortgage Journal | New Hampshire Home Financing Intelligence",
  description: "The local authority on New Hampshire home financing. Get sovereign mortgage strategies, real-time market rates, and a personalized wealth intelligence report for NH buyers.",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "NH Mortgage Journal | New Hampshire Home Financing Intelligence",
    description: "The local authority on New Hampshire home financing. Get sovereign mortgage strategies, real-time market rates, and a personalized wealth intelligence report for NH buyers.",
    url: "https://nh-mortgage-leads.onrender.com",
    siteName: "NH Mortgage Journal",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "NH Mortgage Journal | New Hampshire Home Financing Intelligence",
    description: "The local authority on New Hampshire home financing. Get sovereign mortgage strategies, real-time market rates, and a personalized wealth intelligence report for NH buyers.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <head>
        {/* Impact.com Affiliate Verification */}
        <meta name="impact-site-verification" content="cd7c222f-cec2-474f-87c4-586f0847f263" />
        {/* Lemonade Affiliate Verification */}
        <meta name="fo-verify" content="fcd8eaaf-2125-48a5-8c02-e632cf2c1555" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": ["LocalBusiness", "FinancialService"],
              "@id": "https://nh-mortgage-leads.onrender.com/#localbusiness",
              "name": "NH Mortgage Journal",
              "description": "The local authority on New Hampshire home financing. Get sovereign mortgage strategies, real-time market rates, and a personalized wealth intelligence report for NH buyers.",
              "url": "https://nh-mortgage-leads.onrender.com",
              "telephone": "877-411-0123",
              "address": {
                "@type": "PostalAddress",
                "streetAddress": "20 Trafalgar Square Ste 304",
                "addressLocality": "Nashua",
                "addressRegion": "NH",
                "postalCode": "03063",
                "addressCountry": "US"
              },
              "areaServed": [
                {
                  "@type": "State",
                  "name": "New Hampshire"
                },
                {
                  "@type": "City",
                  "name": "Manchester"
                },
                {
                  "@type": "City",
                  "name": "Nashua"
                },
                {
                  "@type": "City",
                  "name": "Concord"
                },
                {
                  "@type": "City",
                  "name": "Portsmouth"
                }
              ],
              "knowsAbout": [
                "Mortgage pre-approval",
                "Home purchase loans",
                "Refinancing",
                "FHA loans",
                "VA loans",
                "Conventional loans"
              ]
            })
          }}
        />
      </head>
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
