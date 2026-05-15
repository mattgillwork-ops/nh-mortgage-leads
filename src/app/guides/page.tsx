import React from 'react';
import Link from 'next/link';

const GUIDES = [
  {
    title: "NH First-Time Homebuyer Guide",
    excerpt: "Learn about state-level advantages like NH Housing 'Home Start' and how to save $150/mo on PMI.",
    icon: "🏠",
    slug: "nh-first-time-buyer"
  },
  {
    title: "Manchester Trends 2026",
    excerpt: "ROI audit of the North End appreciation spike and West Side multi-family cash-flow opportunities.",
    icon: "📈",
    slug: "manchester-trends"
  },
  {
    title: "Lakes Region Refinance Guide",
    excerpt: "Unlock equity in lakefront properties and navigate seasonal income models for Winnipesaukee homes.",
    icon: "🌊",
    slug: "lakes-region-refi"
  }
];

export default function GuidesPage() {
  return (
    <main style={{ padding: '8rem 8%', minHeight: '100vh', background: 'hsl(var(--background))' }}>
      <div style={{ marginBottom: '4rem', textAlign: 'center' }}>
        <h1 className="display-font" style={{ fontSize: '3.5rem', marginBottom: '1rem' }}>Market <span className="gold-gradient">Intelligence</span></h1>
        <p style={{ opacity: 0.6, fontSize: '1.2rem', maxWidth: '700px', margin: '0 auto' }}>
            Exclusive resources for the New Hampshire homeowner. Real data. Local expertise. No placeholders.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
        {GUIDES.map((guide, i) => (
          <div key={i} style={{ padding: '2.5rem', background: 'white', border: '1px solid #f1f5f9', borderRadius: '24px', transition: 'all 0.3s shadow' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '1.5rem' }}>{guide.icon}</div>
            <h2 className="display-font" style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'hsl(var(--nh-slate))' }}>{guide.title}</h2>
            <p style={{ color: 'hsl(var(--nh-granite))', lineHeight: '1.6', marginBottom: '2rem' }}>{guide.excerpt}</p>
            <Link href={`/guides/${guide.slug}`} className="btn-primary" style={{ width: '100%', textDecoration: 'none', display: 'block', textAlign: 'center' }}>Read Full Guide</Link>
          </div>
        ))}
      </div>
    </main>
  );
}
