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
    <main className="container-journal animate-fade-in" style={{ padding: '10rem 0' }}>
      <div style={{ marginBottom: '6rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '4.5rem', marginBottom: '1.5rem', letterSpacing: '-0.02em' }}>
            Market <span style={{ color: 'hsl(var(--nh-gold))' }}>Intelligence</span>
        </h1>
        <p style={{ opacity: 0.6, fontSize: '1.3rem', maxWidth: '700px', margin: '0 auto', lineHeight: '1.6' }}>
            Exclusive resources for the New Hampshire homeowner. Real data. Local expertise. Verified publication.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '3rem' }}>
        {GUIDES.map((guide, i) => (
          <div key={i} className="journal-card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <div style={{ fontSize: '3rem', marginBottom: '2rem' }}>{guide.icon}</div>
            <h2 style={{ fontSize: '1.8rem', marginBottom: '1.5rem', lineHeight: '1.2' }}>{guide.title}</h2>
            <p style={{ color: '#475569', fontSize: '1.05rem', marginBottom: '3rem', flexGrow: 1 }}>{guide.excerpt}</p>
            <Link 
                href={`/guides/${guide.slug}`} 
                className="btn-primary" 
                style={{ width: '100%', textDecoration: 'none', display: 'block', textAlign: 'center' }}
            >
                Read Analysis
            </Link>
          </div>
        ))}
      </div>
    </main>
  );
}
