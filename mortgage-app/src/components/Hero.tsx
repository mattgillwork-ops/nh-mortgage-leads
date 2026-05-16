'use client';

import React from 'react';
import Link from 'next/link';

export default function Hero() {
  return (
    <section className="hero-container" style={{ padding: '10rem 2rem 6rem', display: 'flex', justifyContent: 'center' }}>
      <div className="animate-fade-in" style={{ maxWidth: '900px', textAlign: 'center' }}>
        <div style={{ marginBottom: '2.5rem' }}>
          <span className="badge">
            Statewide Intelligence Report
          </span>
        </div>
        
        <h1 style={{ fontSize: '5rem', marginBottom: '1.5rem', lineHeight: '1', letterSpacing: '-0.04em' }}>
          Unlocking the <br />
          <span className="gold-gradient">New Hampshire</span> Advantage.
        </h1>
        
        <p style={{ fontSize: '1.3rem', opacity: 0.7, marginBottom: '3.5rem', maxWidth: '750px', margin: '0 auto 3.5rem', fontWeight: 400, lineHeight: '1.7', color: 'var(--foreground)' }}>
          The local authority on NH home financing. We provide the data, transparency, and strategies you need to secure your legacy in the Granite State.
        </p>
        
        <div style={{ display: 'flex', gap: '1.5rem', justifyContent: 'center', marginBottom: '6rem' }}>
          <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none', padding: '1.1rem 3rem', fontSize: '1.1rem' }}>Get Your Market Rate</Link>
          <Link href="/guides" className="glass-panel" style={{ padding: '1.1rem 3rem', color: 'var(--foreground)', fontWeight: 600, textDecoration: 'none', transition: 'all 0.2s', fontSize: '1.1rem' }}>
            Read the Guides
          </Link>
        </div>

        <div style={{ padding: '4rem', borderTop: '1px solid rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.2rem', textAlign: 'left' }}>
            <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'linear-gradient(135deg, #D4AF37 0%, #B8860B 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', color: 'hsl(var(--nh-slate))', fontWeight: 800, border: '4px solid rgba(255,255,255,0.1)' }}>MG</div>
            <div>
              <div style={{ fontWeight: 700, fontSize: '1.2rem' }}>Matt Gill</div>
              <div style={{ fontSize: '0.8rem', opacity: 0.5, textTransform: 'uppercase', letterSpacing: '0.1em' }}>Lead Intelligence Analyst</div>
            </div>
          </div>
          <div style={{ height: '50px', width: '1px', background: 'rgba(255,255,255,0.1)' }}></div>
          <p style={{ maxWidth: '400px', fontSize: '1rem', opacity: 0.6, textAlign: 'left', fontStyle: 'italic', lineHeight: '1.6' }}>
            "In 2026, the NH market rewards the informed. Our engine is built to give local buyers a sovereign edge."
          </p>
        </div>
      </div>
    </section>
  );
}
