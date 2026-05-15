'use client';

import React from 'react';
import Link from 'next/link';

export default function Hero() {
  return (
    <section className="hero-container" style={{ padding: '10rem 2rem 6rem', display: 'flex', justifyContent: 'center', background: 'white' }}>
      <div className="animate-fade-in" style={{ maxWidth: '900px', textAlign: 'center' }}>
        <div style={{ marginBottom: '2.5rem' }}>
          <span className="badge" style={{ background: 'hsla(var(--nh-ice), 0.1)', color: 'hsl(var(--nh-ice))', border: '1px solid hsla(var(--nh-ice), 0.2)' }}>
            Statewide Intelligence Report
          </span>
        </div>
        
        <h1 style={{ fontSize: '4.5rem', marginBottom: '1.5rem', lineHeight: '1.05', color: 'hsl(var(--nh-slate))', letterSpacing: '-0.04em' }}>
          Unlocking the <br />
          <span style={{ color: 'hsl(var(--nh-gold))' }}>New Hampshire</span> Advantage.
        </h1>
        
        <p style={{ fontSize: '1.4rem', color: 'hsl(var(--nh-granite))', marginBottom: '3.5rem', maxWidth: '700px', margin: '0 auto 3.5rem', fontWeight: 400, lineHeight: '1.6' }}>
          The local authority on NH home financing. We provide the data, transparency, and strategies you need to secure your legacy in the Granite State.
        </p>
        
        <div style={{ display: 'flex', gap: '1.5rem', justifyContent: 'center', marginBottom: '5rem' }}>
          <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none', padding: '1rem 2.5rem', fontSize: '1.1rem' }}>Get Your Market Rate</Link>
          <Link href="/guides" style={{ padding: '1rem 2.5rem', background: 'white', color: 'hsl(var(--nh-slate))', fontWeight: 600, border: '1px solid #e2e8f0', borderRadius: '12px', cursor: 'pointer', textDecoration: 'none', transition: 'all 0.2s' }}>
            Read the Guides
          </Link>
        </div>

        <div style={{ padding: '3rem', borderTop: '1px solid #f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '3rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', textAlign: 'left' }}>
            <div style={{ width: '60px', height: '60px', borderRadius: '50%', background: 'linear-gradient(135deg, #fbbf24 0%, #d97706 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', color: 'white', fontWeight: 700 }}>MG</div>
            <div>
              <div style={{ fontWeight: 700, fontSize: '1.1rem', color: 'hsl(var(--nh-slate))' }}>Matt Gill</div>
              <div style={{ fontSize: '0.85rem', color: 'hsl(var(--nh-granite))', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Lead Intelligence Analyst</div>
            </div>
          </div>
          <div style={{ height: '40px', width: '1px', background: '#e2e8f0' }}></div>
          <p style={{ maxWidth: '400px', fontSize: '0.95rem', color: 'hsl(var(--nh-granite))', textAlign: 'left', fontStyle: 'italic' }}>
            "In 2026, the NH market rewards the informed. Our engine is built to give local buyers a sovereign edge."
          </p>
        </div>
      </div>
    </section>
  );
}
