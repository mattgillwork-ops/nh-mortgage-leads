import React from 'react';
import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: "NH First-Time Buyer Guide | NH Mortgage Journal",
  description: "State-level advantages and ROI audits for NH home buyers.",
};

export default function FirstTimeBuyerGuide() {
  return (
    <main className="container-journal animate-fade-in" style={{ padding: '8rem 0' }}>
      <Link href="/guides" style={{ color: 'hsl(var(--nh-gold))', textDecoration: 'none', marginBottom: '3rem', display: 'inline-block', fontWeight: 600, fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        ← Back to Resources
      </Link>
      
      <h1 style={{ fontSize: '4rem', marginBottom: '3rem', lineHeight: '1.1' }}>
        The <span style={{ color: 'hsl(var(--nh-gold))' }}>Sovereign</span> NH First-Time Buyer Guide
      </h1>
      
      <section className="journal-card" style={{ marginBottom: '3rem' }}>
        <h2 style={{ color: 'hsl(var(--nh-gold))', marginBottom: '1.5rem', fontSize: '1.8rem' }}>1. The NH Housing "Home Start" Advantage</h2>
        <p style={{ fontSize: '1.15rem', color: '#334155' }}>
          New Hampshire offers unique state-level advantages that retail banks often overlook. The <strong>Home Start</strong> program 
          provides below-market interest rates for low-to-moderate income households in cities like <strong>Manchester</strong> and <strong>Nashua</strong>. 
          Unlike standard FHA loans, NH Housing programs often allow for lower mortgage insurance premiums (PMI), which can save you up to <strong>$150/month</strong> 
          on a standard $400,000 home.
        </p>
      </section>

      <section style={{ padding: '2rem 0', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2.2rem', marginBottom: '1.5rem' }}>2. Navigating the Seacoast Market</h2>
        <p style={{ fontSize: '1.15rem', color: '#334155' }}>
          Inventory in Rockingham County is currently at a 10-year low. To win in this environment, your "Lead Intelligence" must be 
          fully verified before you make an offer. Our engine doesn't just give you a rate; it prepares a <strong>Sovereign Pre-Approval</strong> 
          that NH sellers trust.
        </p>
      </section>

      <section className="journal-card" style={{ background: 'hsla(var(--nh-gold), 0.02)', borderColor: 'hsla(var(--nh-gold), 0.1)' }}>
        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.8rem' }}>3. The ROI of "Local-First" Financing</h2>
        <p style={{ fontSize: '1.15rem', color: '#334155' }}>
          By choosing a local NH-focused engine over a national "big-box" lender, you avoid the $1,200+ junk fees often hidden in 
          closing costs. Our data shows that NH homeowners using local specialized engines save an average of <strong>0.375%</strong> 
          on their APR over the life of the loan.
        </p>
      </section>

      <div style={{ marginTop: '6rem', textAlign: 'center', padding: '4rem', background: '#f8fafc', borderRadius: '24px' }}>
        <h3 style={{ fontSize: '2rem', marginBottom: '2rem' }}>Ready to calculate your actual NH ROI?</h3>
        <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none' }}>Launch Rate Engine</Link>
      </div>
    </main>
  );
}
