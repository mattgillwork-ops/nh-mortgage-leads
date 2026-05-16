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
    <main style={{ minHeight: '100vh', background: 'hsl(var(--background))' }}>
      <div className="nh-blue-box gliding-box" style={{ 
        margin: '0 auto', 
        minHeight: '100vh', 
        padding: '8rem 4rem',
      }}>
        <div style={{ marginBottom: '6rem', textAlign: 'center' }}>
          <h1 className="display-font" style={{ fontSize: '4.5rem', marginBottom: '1.5rem' }}>Market <span className="gold-gradient">Intelligence</span></h1>
          <p style={{ opacity: 0.7, fontSize: '1.3rem', maxWidth: '750px', margin: '0 auto', lineHeight: '1.7' }}>
              Exclusive resources for the New Hampshire homeowner. Real data. Local expertise. No placeholders.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2.5rem', maxWidth: '1000px', margin: '0 auto' }}>
          {GUIDES.map((guide, i) => (
            <div key={i} className="glass-panel" style={{ padding: '3.5rem', transition: 'transform 0.3s ease' }}>
              <div style={{ fontSize: '3rem', marginBottom: '1.5rem' }}>{guide.icon}</div>
              <h2 className="display-font" style={{ fontSize: '1.8rem', marginBottom: '1rem', color: 'white' }}>{guide.title}</h2>
              <p style={{ opacity: 0.6, lineHeight: '1.8', marginBottom: '2.5rem', fontSize: '1.05rem' }}>{guide.excerpt}</p>
              <Link href={`/guides/${guide.slug}`} className="btn-primary" style={{ width: '100%', textDecoration: 'none', display: 'block', textAlign: 'center' }}>Read Full Guide</Link>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
