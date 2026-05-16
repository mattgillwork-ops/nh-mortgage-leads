'use client';

import React from 'react';
import Link from 'next/link';

export default function Hero() {
  return (
    <section className="hero-container nh-blue-box gliding-box" style={{ 
      minHeight: '80vh', 
      display: 'flex', 
      flexDirection: 'column',
      justifyContent: 'center', 
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Localized Intelligence Backdrop */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundImage: 'url(/images/nh-hero.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        opacity: 0.4,
        zIndex: 0,
        maskImage: 'linear-gradient(to bottom, black 60%, transparent 100%)',
        WebkitMaskImage: 'linear-gradient(to bottom, black 60%, transparent 100%)'
      }} />

      <div className="animate-fade-in" style={{ 
        position: 'relative', 
        zIndex: 1, 
        padding: '6rem 4rem', 
        textAlign: 'center',
        maxWidth: '900px',
        margin: '0 auto'
      }}>
        <div style={{ marginBottom: '2.5rem' }}>
          <span className="badge" style={{ background: 'hsla(var(--nh-gold), 0.15)', border: '1px solid hsla(var(--nh-gold), 0.3)' }}>
            2026 NH Market Intelligence
          </span>
        </div>
        
        <h1 style={{ fontSize: '5.5rem', marginBottom: '1.5rem', lineHeight: '0.95', letterSpacing: '-0.05em' }}>
          Unlocking the <br />
          <span className="gold-gradient">NH Advantage.</span>
        </h1>
        
        <p style={{ fontSize: '1.4rem', opacity: 0.8, marginBottom: '4rem', fontWeight: 400, lineHeight: '1.7', maxWidth: '700px', margin: '0 auto 4rem' }}>
          The local authority on New Hampshire home financing. We provide the data, transparency, and sovereign strategies you need to secure your legacy.
        </p>
        
        <div className="flex-stack" style={{ display: 'flex', gap: '2rem', justifyContent: 'center', marginBottom: '6rem' }}>
          <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none', padding: '1.2rem 3.5rem', fontSize: '1.15rem' }}>Get Your Market Rate</Link>
          <Link href="/guides" className="glass-panel" style={{ padding: '1.2rem 3.5rem', color: 'white', fontWeight: 600, textDecoration: 'none', fontSize: '1.15rem' }}>
            Browse Intelligence
          </Link>
        </div>

        <div className="flex-stack" style={{ padding: '4rem', borderTop: '1px solid rgba(255,255,255,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '5rem', background: 'rgba(255,255,255,0.02)' }}>
          <div className="flex-stack" style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', textAlign: 'left' }}>
            <div style={{ flexShrink: 0, width: '68px', height: '68px', borderRadius: '50%', background: 'linear-gradient(135deg, #D4AF37 0%, #B8860B 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.6rem', color: '#0B0F19', fontWeight: 900, border: '4px solid rgba(255,255,255,0.15)' }}>SA</div>
            <div>
              <div style={{ fontWeight: 700, fontSize: 'clamp(1rem, 4vw, 1.4rem)', letterSpacing: '-0.02em' }}>Sovereign Mortgage Architect</div>
              <div style={{ fontSize: '0.8rem', opacity: 0.5, textTransform: 'uppercase', letterSpacing: '0.15em', marginTop: '0.2rem' }}>NH Principal Intelligence</div>
            </div>
          </div>
          <div style={{ height: '60px', width: '1px', background: 'rgba(255,255,255,0.15)' }}></div>
          <p style={{ maxWidth: '380px', fontSize: '1.1rem', opacity: 0.7, textAlign: 'left', fontStyle: 'italic', lineHeight: '1.6' }}>
            "In 2026, the NH market rewards the informed. Our engine is built to provide local buyers with a sovereign edge."
          </p>
        </div>
      </div>
    </section>
  );
}
