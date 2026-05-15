'use client';

import React from 'react';
import Link from 'next/link';

export default function Navbar() {
  return (
    <nav style={{ 
      position: 'fixed', 
      top: 0, 
      width: '100%', 
      background: 'rgba(255,255,255,0.95)', 
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid #f1f5f9',
      zIndex: 1000,
      padding: '1.5rem 0'
    }}>
      <div className="container-journal" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link href="/" style={{ textDecoration: 'none' }}>
          <div style={{ fontFamily: "'Playfair Display', serif", fontSize: '1.6rem', fontWeight: 900, letterSpacing: '-0.02em', color: 'hsl(var(--nh-slate))' }}>
            NH <span style={{ color: 'hsl(var(--nh-gold))' }}>Mortgage</span> Journal
          </div>
        </Link>
        
        <div style={{ display: 'flex', gap: '3rem', alignItems: 'center' }}>
          <Link href="/guides" className="nav-link">Market Intelligence</Link>
          <Link href="/funnel" className="btn-primary" style={{ padding: '0.6rem 1.5rem', fontSize: '0.8rem' }}>Get Your Rate</Link>
        </div>
      </div>
    </nav>
  );
}
