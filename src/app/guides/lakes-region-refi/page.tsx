import React from 'react';
import Link from 'next/link';

export default function LakesRegionRefiGuide() {
  return (
    <main className="container-journal animate-fade-in" style={{ padding: '8rem 0' }}>
      <Link href="/guides" style={{ color: 'hsl(var(--nh-gold))', textDecoration: 'none', marginBottom: '3rem', display: 'inline-block', fontWeight: 600, fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        ← Back to Resources
      </Link>
      
      <h1 style={{ fontSize: '4rem', marginBottom: '3rem', lineHeight: '1.1' }}>
        Unlock Equity: <span style={{ color: 'hsl(var(--nh-gold))' }}>Lakes Region</span> Refinance Guide
      </h1>
      
      <section className="journal-card" style={{ marginBottom: '3rem' }}>
        <h2 style={{ color: 'hsl(var(--nh-gold))', marginBottom: '1.5rem', fontSize: '1.8rem' }}>1. Leveraging Lakefront Appreciation</h2>
        <p style={{ fontSize: '1.15rem', color: '#334155' }}>
          Properties in the <strong>Lakes Region</strong> (Winnipesaukee, Squam, Winnisquam) have seen unprecedented 
          equity growth over the last 36 months. A <strong>Cash-Out Refinance</strong> today can unlock hundreds of 
          thousands in capital for property improvements, boat slips, or debt consolidation, often at rates 
          significantly lower than HELOCs.
        </p>
      </section>

      <section style={{ padding: '2rem 0', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2.2rem', marginBottom: '1.5rem' }}>2. Seasonal Income Considerations</h2>
        <p style={{ fontSize: '1.15rem', color: '#334155' }}>
            Refinancing a second home or short-term rental in the Lakes Region requires a specialized underwriting 
            approach. Our engine understands the <strong>seasonal rental income</strong> models common in <strong>Meredith</strong> 
            and <strong>Wolfeboro</strong>, allowing you to use that income to qualify for higher loan amounts.
        </p>
      </section>

      <section className="journal-card" style={{ background: 'hsla(var(--nh-gold), 0.02)', borderColor: 'hsla(var(--nh-gold), 0.1)' }}>
        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.8rem' }}>3. Jumbo Loan Refinancing in Belknap County</h2>
        <p style={{ fontSize: '1.15rem', color: '#334155' }}>
          High-value lakefront properties often fall into the <strong>Jumbo Loan</strong> category. In 2026, 
          Jumbo rates have stabilized, making it an ideal time to move from an adjustable-rate mortgage (ARM) 
          to a secure, low-rate fixed 30-year term.
        </p>
      </section>

      <div style={{ marginTop: '6rem', textAlign: 'center', padding: '4rem', background: '#f8fafc', borderRadius: '24px' }}>
        <h3 style={{ fontSize: '2rem', marginBottom: '2rem' }}>Ready to calculate your actual NH ROI?</h3>
        <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none' }}>Launch Rate Engine</Link>
      </div>
    </main>
  );
}
