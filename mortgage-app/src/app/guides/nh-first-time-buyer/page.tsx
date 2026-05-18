import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: "First-Time Homebuyer NH Programs & Loans | NH Mortgage Journal",
  description: "Complete guide to NH Housing Finance Authority (NHHFA) 'Home Start' advantages, FHA loans, and zero down payment programs for NH first-time buyers.",
};

export default function FirstTimeBuyerGuide() {
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
          The <span className="gold-gradient">Sovereign</span> NH First-Time Buyer Guide
        </h1>
        
        <div className="glass-panel" style={{ padding: '3rem', marginBottom: '4rem' }}>
          <h2 style={{ color: 'hsl(var(--nh-gold))', marginBottom: '1.5rem' }}>1. The NH Housing "Home Start" Advantage</h2>
          <p style={{ opacity: 0.85 }}>
            New Hampshire offers unique state-level advantages that retail banks often overlook. The <strong>Home Start</strong> program 
            provides below-market interest rates for low-to-moderate income households in cities like <strong>Manchester</strong> and <strong>Nashua</strong>. 
            Unlike standard FHA loans, NH Housing programs often allow for lower mortgage insurance premiums (PMI), which can save you up to <strong>$150/month</strong> 
            on a standard $400,000 home.
          </p>
        </div>

        <h2 className="display-font" style={{ fontSize: '2rem', marginBottom: '1.5rem', color: 'white' }}>2. Navigating the Seacoast Market</h2>
        <p style={{ marginBottom: '2.5rem', opacity: 0.85 }}>
          Inventory in Rockingham County is currently at a 10-year low. To win in this environment, your "Lead Intelligence" must be 
          fully verified before you make an offer. Our engine doesn't just give you a rate; it prepares a <strong>Sovereign Pre-Approval</strong> 
          that NH sellers trust.
        </p>

        <div className="glass-panel" style={{ padding: '3rem', background: 'rgba(212,175,55,0.05)', border: '1px solid rgba(212,175,55,0.15)' }}>
          <h2 style={{ marginBottom: '1.5rem', color: 'hsl(var(--nh-gold))' }}>3. The ROI of "Local-First" Financing</h2>
          <p style={{ opacity: 0.85 }}>
            By choosing a local NH-focused engine over a national "big-box" lender, you avoid the $1,200+ junk fees often hidden in 
            closing costs. Our data shows that NH homeowners using local specialized engines save an average of <strong>0.375%</strong> 
            on their APR over the life of the loan.
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
