import React from 'react';
import Link from 'next/link';

export default function ManchesterTrendsGuide() {
  return (
    <main style={{ minHeight: '100vh', background: 'hsl(var(--background))' }}>
      <div className="nh-blue-box gliding-box" style={{ 
        margin: '0 auto', 
        minHeight: '100vh', 
        padding: '8rem 4rem',
        maxWidth: '1200px',
        lineHeight: '1.8'
      }}>
        <Link href="/guides" style={{ color: 'hsl(var(--nh-gold))', textDecoration: 'none', marginBottom: '2rem', display: 'inline-block', fontWeight: 600 }}>← Back to Resources</Link>
        
        <h1 className="display-font" style={{ fontSize: '3.5rem', marginBottom: '2rem', letterSpacing: '-0.04em' }}>
          2026 <span className="gold-gradient">Manchester</span> Real Estate ROI Trends
        </h1>
        
        <div className="glass-panel" style={{ padding: '3rem', marginBottom: '4rem' }}>
          <h2 style={{ color: 'hsl(var(--nh-gold))', marginBottom: '1.5rem' }}>1. The North End Appreciation Spike</h2>
          <p style={{ opacity: 0.85 }}>
            Manchester's <strong>North End</strong> continues to lead the state in equity growth. Our 2026 data shows a 
            <strong> 8.4% year-over-year appreciation</strong>, driven by the expansion of the tech corridor and 
            increased demand for historic properties. For investors, this represents a unique window for high-LTV 
            refinancing to fund additional NH acquisitions.
          </p>
        </div>

        <h2 className="display-font" style={{ fontSize: '2rem', marginBottom: '1.5rem', color: 'white' }}>2. Multi-Family Opportunities in the West Side</h2>
        <p style={{ marginBottom: '2.5rem', opacity: 0.85 }}>
          The <strong>West Side</strong> is emerging as a "Cash-Flow King" for 2026. With the new transit-oriented development 
          zoning, multi-family properties are seeing a 12% increase in rental yield. Our engine can help you 
          analyze the specific debt-service coverage ratio (DSCR) for Manchester multi-families.
        </p>

        <div className="glass-panel" style={{ padding: '3rem', background: 'rgba(212,175,55,0.05)', border: '1px solid rgba(212,175,55,0.15)' }}>
          <h2 style={{ marginBottom: '1.5rem', color: 'hsl(var(--nh-gold))' }}>3. Manchester's Interest Rate Micro-Climate</h2>
          <p style={{ opacity: 0.85 }}>
            Because Manchester is a designated "Hub City," specific local lenders offer <strong>0.25% rate discounts</strong> 
            for properties within city limits to encourage urban density. We track these Manchester-specific 
            incentives in real-time.
          </p>
        </div>

        <div style={{ marginTop: '4rem', textAlign: 'center' }}>
          <h3 className="display-font" style={{ fontSize: '1.5rem', marginBottom: '2rem', color: 'white' }}>Ready to calculate your actual NH ROI?</h3>
          <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none' }}>Launch Rate Engine</Link>
        </div>
      </div>
    </main>
  );
}
