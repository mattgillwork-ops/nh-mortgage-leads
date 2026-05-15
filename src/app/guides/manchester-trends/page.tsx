import React from 'react';
import Link from 'next/link';

export default function ManchesterTrendsGuide() {
  return (
    <main className="container-journal animate-fade-in" style={{ padding: '8rem 0' }}>
      <Link href="/guides" style={{ color: 'hsl(var(--nh-gold))', textDecoration: 'none', marginBottom: '3rem', display: 'inline-block', fontWeight: 600, fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        ← Back to Resources
      </Link>
      
      <h1 style={{ fontSize: '4rem', marginBottom: '3rem', lineHeight: '1.1' }}>
        2026 <span style={{ color: 'hsl(var(--nh-gold))' }}>Manchester</span> Real Estate ROI Trends
      </h1>
      
      <section className="journal-card" style={{ marginBottom: '3rem' }}>
        <h2 style={{ color: 'hsl(var(--nh-gold))', marginBottom: '1.5rem', fontSize: '1.8rem' }}>1. The North End Appreciation Spike</h2>
        <p style={{ fontSize: '1.15rem', color: '#334155' }}>
          Manchester's <strong>North End</strong> continues to lead the state in equity growth. Our 2026 data shows a 
          <strong> 8.4% year-over-year appreciation</strong>, driven by the expansion of the tech corridor and 
          increased demand for historic properties. For investors, this represents a unique window for high-LTV 
          refinancing to fund additional NH acquisitions.
        </p>
      </section>

      <section style={{ padding: '2rem 0', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2.2rem', marginBottom: '1.5rem' }}>2. Multi-Family Opportunities in the West Side</h2>
        <p style={{ fontSize: '1.15rem', color: '#334155' }}>
          The <strong>West Side</strong> is emerging as a "Cash-Flow King" for 2026. With the new transit-oriented development 
          zoning, multi-family properties are seeing a 12% increase in rental yield. Our engine can help you 
          analyze the specific debt-service coverage ratio (DSCR) for Manchester multi-families.
        </p>
      </section>

      <section className="journal-card" style={{ background: 'hsla(var(--nh-gold), 0.02)', borderColor: 'hsla(var(--nh-gold), 0.1)' }}>
        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.8rem' }}>3. Manchester's Interest Rate Micro-Climate</h2>
        <p style={{ fontSize: '1.15rem', color: '#334155' }}>
          Because Manchester is a designated "Hub City," specific local lenders offer <strong>0.25% rate discounts</strong> 
          for properties within city limits to encourage urban density. We track these Manchester-specific 
          incentives in real-time.
        </p>
      </section>

      <div style={{ marginTop: '6rem', textAlign: 'center', padding: '4rem', background: '#f8fafc', borderRadius: '24px' }}>
        <h3 style={{ fontSize: '2rem', marginBottom: '2rem' }}>Ready to calculate your actual NH ROI?</h3>
        <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none' }}>Launch Rate Engine</Link>
      </div>
    </main>
  );
}
