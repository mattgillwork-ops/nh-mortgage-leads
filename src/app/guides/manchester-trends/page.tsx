import React from 'react';
import Link from 'next/link';

export default function ManchesterTrendsGuide() {
  return (
    <main style={{ padding: '8rem 15%', minHeight: '100vh', background: 'white', color: 'hsl(var(--nh-slate))', lineHeight: '1.8' }}>
      <Link href="/guides" style={{ color: 'hsl(var(--nh-gold))', textDecoration: 'none', marginBottom: '2rem', display: 'inline-block', fontWeight: 600 }}>← Back to Resources</Link>
      
      <h1 className="display-font" style={{ fontSize: '3.5rem', marginBottom: '2rem', letterSpacing: '-0.04em' }}>
        2026 <span style={{ color: 'hsl(var(--nh-gold))' }}>Manchester</span> Real Estate ROI Trends
      </h1>
      
      <div style={{ padding: '3rem', marginBottom: '4rem', border: '1px solid #f1f5f9', borderRadius: '24px', background: '#f8fafc' }}>
        <h2 style={{ color: 'hsl(var(--nh-gold))', marginBottom: '1.5rem' }}>1. The North End Appreciation Spike</h2>
        <p>
          Manchester's <strong>North End</strong> continues to lead the state in equity growth. Our 2026 data shows a 
          <strong> 8.4% year-over-year appreciation</strong>, driven by the expansion of the tech corridor and 
          increased demand for historic properties. For investors, this represents a unique window for high-LTV 
          refinancing to fund additional NH acquisitions.
        </p>
      </div>

      <h2 className="display-font" style={{ fontSize: '2rem', marginBottom: '1.5rem' }}>2. Multi-Family Opportunities in the West Side</h2>
      <p style={{ marginBottom: '2.5rem' }}>
        The <strong>West Side</strong> is emerging as a "Cash-Flow King" for 2026. With the new transit-oriented development 
        zoning, multi-family properties are seeing a 12% increase in rental yield. Our engine can help you 
        analyze the specific debt-service coverage ratio (DSCR) for Manchester multi-families.
      </p>

      <div style={{ padding: '3rem', border: '1px solid #f1f5f9', borderRadius: '24px', background: 'hsla(var(--nh-gold), 0.05)' }}>
        <h2 style={{ marginBottom: '1.5rem' }}>3. Manchester's Interest Rate Micro-Climate</h2>
        <p>
          Because Manchester is a designated "Hub City," specific local lenders offer <strong>0.25% rate discounts</strong> 
          for properties within city limits to encourage urban density. We track these Manchester-specific 
          incentives in real-time.
        </p>
      </div>

      <div style={{ marginTop: '4rem', textAlign: 'center' }}>
        <h3 className="display-font" style={{ fontSize: '1.5rem', marginBottom: '2rem' }}>Ready to calculate your actual NH ROI?</h3>
        <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none' }}>Launch Rate Engine</Link>
      </div>
    </main>
  );
}
