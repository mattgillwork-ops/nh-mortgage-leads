import React from 'react';
import Link from 'next/link';

export default function FirstTimeBuyerGuide() {
  return (
    <main style={{ padding: '8rem 15%', minHeight: '100vh', background: 'white', color: 'hsl(var(--nh-slate))', lineHeight: '1.8' }}>
      <Link href="/guides" style={{ color: 'hsl(var(--nh-gold))', textDecoration: 'none', marginBottom: '2rem', display: 'inline-block', fontWeight: 600 }}>← Back to Resources</Link>
      
      <h1 className="display-font" style={{ fontSize: '3.5rem', marginBottom: '2rem', letterSpacing: '-0.04em' }}>
        The <span style={{ color: 'hsl(var(--nh-gold))' }}>Sovereign</span> NH First-Time Buyer Guide
      </h1>
      
      <div style={{ padding: '3rem', marginBottom: '4rem', border: '1px solid #f1f5f9', borderRadius: '24px', background: '#f8fafc' }}>
        <h2 style={{ color: 'hsl(var(--nh-gold))', marginBottom: '1.5rem' }}>1. The NH Housing "Home Start" Advantage</h2>
        <p>
          New Hampshire offers unique state-level advantages that retail banks often overlook. The <strong>Home Start</strong> program 
          provides below-market interest rates for low-to-moderate income households in cities like <strong>Manchester</strong> and <strong>Nashua</strong>. 
          Unlike standard FHA loans, NH Housing programs often allow for lower mortgage insurance premiums (PMI), which can save you up to <strong>$150/month</strong> 
          on a standard $400,000 home.
        </p>
      </div>

      <h2 className="display-font" style={{ fontSize: '2rem', marginBottom: '1.5rem' }}>2. Navigating the Seacoast Market</h2>
      <p style={{ marginBottom: '2.5rem' }}>
        Inventory in Rockingham County is currently at a 10-year low. To win in this environment, your "Lead Intelligence" must be 
        fully verified before you make an offer. Our engine doesn't just give you a rate; it prepares a <strong>Sovereign Pre-Approval</strong> 
        that NH sellers trust.
      </p>

      <div style={{ padding: '3rem', border: '1px solid #f1f5f9', borderRadius: '24px', background: 'hsla(var(--nh-gold), 0.05)' }}>
        <h2 style={{ marginBottom: '1.5rem' }}>3. The ROI of "Local-First" Financing</h2>
        <p>
          By choosing a local NH-focused engine over a national "big-box" lender, you avoid the $1,200+ junk fees often hidden in 
          closing costs. Our data shows that NH homeowners using local specialized engines save an average of <strong>0.375%</strong> 
          on their APR over the life of the loan.
        </p>
      </div>

      <div style={{ marginTop: '4rem', textAlign: 'center' }}>
        <h3 className="display-font" style={{ fontSize: '1.5rem', marginBottom: '2rem' }}>Ready to calculate your actual NH ROI?</h3>
        <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none' }}>Launch Rate Engine</Link>
      </div>
    </main>
  );
}
