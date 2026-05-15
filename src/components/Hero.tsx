'use client';

import React from 'react';
import Link from 'next/link';

export default function Hero() {
  return (
    <section className="container-journal animate-fade-in" style={{ padding: '12rem 0 8rem', textAlign: 'center' }}>
      <div style={{ marginBottom: '3rem' }}>
        <span className="badge">Verified Intelligence 2026</span>
      </div>
      
      <h1 style={{ fontSize: '5.5rem', marginBottom: '2.5rem', lineHeight: '1', color: 'hsl(var(--nh-slate))', letterSpacing: '-0.02em' }}>
        Unlocking the <br />
        <span style={{ color: 'hsl(var(--nh-gold))' }}>New Hampshire</span> Advantage.
      </h1>
      
      <p style={{ fontSize: '1.5rem', color: '#475569', marginBottom: '4rem', maxWidth: '750px', margin: '0 auto 4rem', fontWeight: 400, lineHeight: '1.6' }}>
        The authoritative source for NH home financing. We provide the data, transparency, and strategies required to secure your legacy in the Granite State.
      </p>
      
      <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center', marginBottom: '6rem' }}>
        <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none' }}>Launch Rate Engine</Link>
        <Link href="/guides" style={{ 
            padding: '1rem 2.5rem', 
            background: 'white', 
            color: 'hsl(var(--nh-slate))', 
            fontWeight: 600, 
            border: '1px solid #e2e8f0', 
            borderRadius: '8px', 
            textDecoration: 'none', 
            transition: 'all 0.2s',
            fontSize: '0.9rem',
            textTransform: 'uppercase',
            letterSpacing: '0.05em'
        }}>
          Market Analysis
        </Link>
      </div>

      <div style={{ padding: '4rem', borderTop: '1px solid #f1f5f9', display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'center', gap: '4rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', textAlign: 'left' }}>
          <div style={{ 
              width: '70px', 
              height: '70px', 
              borderRadius: '8px', 
              background: 'hsl(var(--nh-slate))', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              fontSize: '1.8rem', 
              color: 'white', 
              fontWeight: 900,
              fontFamily: 'var(--font-display)'
          }}>MG</div>
          <div>
            <div style={{ fontWeight: 900, fontSize: '1.2rem', color: 'hsl(var(--nh-slate))', fontFamily: 'var(--font-display)' }}>Matt Gill</div>
            <div style={{ fontSize: '0.75rem', color: 'hsl(var(--nh-gold))', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 800 }}>Lead Intelligence Analyst</div>
          </div>
        </div>
        <div style={{ height: '50px', width: '1px', background: '#e2e8f0' }} className="hide-mobile"></div>
        <p style={{ maxWidth: '450px', fontSize: '1.1rem', color: '#64748b', textAlign: 'left', fontStyle: 'italic', lineHeight: '1.6' }}>
          "In 2026, the NH market rewards the informed. Our engine is engineered to provide local buyers a sovereign edge in high-stakes negotiations."
        </p>
      </div>
    </section>
  );
}
