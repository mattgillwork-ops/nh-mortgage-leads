import React from 'react';
import Link from 'next/link';

export default function LakesRegionRefiGuide() {
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
          Unlock Equity: <span className="gold-gradient">Lakes Region</span> Refinance Guide
        </h1>
        
        <div className="glass-panel" style={{ padding: '3rem', marginBottom: '4rem' }}>
          <h2 style={{ color: 'hsl(var(--nh-gold))', marginBottom: '1.5rem' }}>1. Leveraging Lakefront Appreciation</h2>
          <p style={{ opacity: 0.85 }}>
            Properties in the <strong>Lakes Region</strong> (Winnipesaukee, Squam, Winnisquam) have seen unprecedented 
            equity growth over the last 36 months. A <strong>Cash-Out Refinance</strong> today can unlock hundreds of 
            thousands in capital for property improvements, boat slips, or debt consolidation, often at rates 
            significantly lower than HELOCs.
          </p>
        </div>

        <h2 className="display-font" style={{ fontSize: '2rem', marginBottom: '1.5rem', color: 'white' }}>2. Seasonal Income Considerations</h2>
        <p style={{ marginBottom: '2.5rem', opacity: 0.85 }}>
          Refinancing a second home or short-term rental in the Lakes Region requires a specialized underwriting 
          approach. Our engine understands the <strong>seasonal rental income</strong> models common in <strong>Meredith</strong> 
          and <strong>Wolfeboro</strong>, allowing you to use that income to qualify for higher loan amounts.
        </p>

        <div className="glass-panel" style={{ padding: '3rem', background: 'rgba(212,175,55,0.05)', border: '1px solid rgba(212,175,55,0.15)' }}>
          <h2 style={{ marginBottom: '1.5rem', color: 'hsl(var(--nh-gold))' }}>3. Jumbo Loan Refinancing in Belknap County</h2>
          <p style={{ opacity: 0.85 }}>
            High-value lakefront properties often fall into the <strong>Jumbo Loan</strong> category. In 2026, 
            Jumbo rates have stabilized, making it an ideal time to move from an adjustable-rate mortgage (ARM) 
            to a secure, low-rate fixed 30-year term.
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
