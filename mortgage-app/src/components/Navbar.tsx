'use client';

import React from 'react';
import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="glass-panel" style={{ 
      position: 'fixed', 
      top: '1.5rem', 
      left: '50%', 
      transform: 'translateX(-50%)', 
      width: '90%', 
      maxWidth: '1200px',
      padding: '1rem 2rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      zIndex: 1000,
      borderRadius: '16px'
    }}>
      <Link href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
        <div style={{ fontWeight: 800, fontSize: '1.4rem', letterSpacing: '-0.04em', color: 'white' }} className="display-font">
          NH <span style={{ color: 'hsl(var(--nh-gold))' }}>MORTGAGE</span> JOURNAL
        </div>
      </Link>
      <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
        <Link href="/guides" className="nav-link" style={{ fontSize: '0.95rem', fontWeight: 500, color: 'rgba(255,255,255,0.8)' }}>Market Intelligence</Link>
        <Link href="/funnel" className="btn-primary" style={{ padding: '0.6rem 1.5rem', fontSize: '0.9rem', textDecoration: 'none' }}>Get Your Rate</Link>
      </div>
    </nav>
  );
}
