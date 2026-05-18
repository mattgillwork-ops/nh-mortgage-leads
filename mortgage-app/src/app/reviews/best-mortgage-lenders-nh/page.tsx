import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Top 5 Best Mortgage Lenders in NH (2026 Reviews) | NH Mortgage Journal',
  description: 'Compare the best mortgage lenders in New Hampshire for 2026. See our top picks for first-time buyers, refinancing, and fast local closings.',
};

const lenders = [
  {
    name: 'NH Mortgage Journal (Powered by NextGen)',
    rating: 5.0,
    badge: 'Best Local Pick for 2026',
    description: 'Our top recommendation. An independent, Nashua-based engine that compares rates across wholesale channels to find the absolute lowest APR for NH residents. Exceptional local knowledge and access to NHHFA Home Start programs.',
    pros: ['Direct access to wholesale rates', 'NHHFA approved', 'Sovereign pre-approval engine', 'Extremely fast local closing times'],
    cons: ['Limited to NH and surrounding New England states'],
    ctaText: 'Calculate Your NH Rate',
    ctaLink: '/funnel',
    isPrimary: true,
  },
  {
    name: 'Rocket Mortgage',
    rating: 4.6,
    badge: 'Best Digital Experience',
    description: 'A national powerhouse known for its seamless online application process. Great for tech-savvy borrowers who want to handle everything from their smartphone.',
    pros: ['Excellent mobile app', 'Fast online pre-approval', 'Customizable loan terms'],
    cons: ['Can have higher fees', 'Lacks localized NH market expertise', 'Strict credit requirements'],
    ctaText: 'Check Rocket Rates (Affiliate)',
    ctaLink: '#rocket',
    isPrimary: false,
  },
  {
    name: 'Better.com',
    rating: 4.5,
    badge: 'Best for No Origination Fees',
    description: 'Better.com stands out by eliminating traditional lender fees and offering a fully digital process. They provide aggressive rate matching.',
    pros: ['No origination or lender fees', '24/7 customer support', 'Fast underwriting'],
    cons: ['Online only (no physical branches)', 'May not support complex financial situations'],
    ctaText: 'Check Better Rates (Affiliate)',
    ctaLink: '#better',
    isPrimary: false,
  },
  {
    name: 'CMG Home Loans',
    rating: 4.4,
    badge: 'Best for Unique Loan Products',
    description: 'Known for their "All In One Loan" and strong presence in New Hampshire. They are a solid choice for borrowers needing creative financing solutions.',
    pros: ['Innovative loan options', 'Good local presence', 'First-time buyer friendly'],
    cons: ['Rates can sometimes be higher than wholesale brokers'],
    ctaText: 'Check CMG Rates (Affiliate)',
    ctaLink: '#cmg',
    isPrimary: false,
  },
  {
    name: 'Bank of America',
    rating: 4.2,
    badge: 'Best for Existing Customers',
    description: 'For borrowers who already bank with BoA, their Preferred Rewards program can offer significant discounts on mortgage origination fees.',
    pros: ['Discounts for existing customers', 'Grants for low-income buyers', 'Massive branch network'],
    cons: ['Slowest closing times', 'Rigid underwriting standards'],
    ctaText: 'Check BoA Rates (Affiliate)',
    ctaLink: '#boa',
    isPrimary: false,
  },
];

export default function BestLendersNH() {
  return (
    <main style={{ minHeight: '100vh', background: 'hsl(var(--background))' }}>
      <div className="nh-blue-box gliding-box" style={{ 
        margin: '0 auto', 
        minHeight: '100vh', 
        padding: '8rem 4rem',
        maxWidth: '1200px',
        lineHeight: '1.8'
      }}>
        <h1 className="display-font" style={{ fontSize: '3.5rem', marginBottom: '2rem', letterSpacing: '-0.04em' }}>
          Best Mortgage Lenders in <span className="gold-gradient">New Hampshire (2026)</span>
        </h1>
        <p style={{ opacity: 0.85, fontSize: '1.2rem', marginBottom: '4rem' }}>
          Finding the right mortgage lender in NH's competitive housing market is critical. 
          We've reviewed the top options based on interest rates, local expertise, closing speed, and customer service.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
          {lenders.map((lender, index) => (
            <div key={index} className="glass-panel" style={{ 
              padding: '3rem', 
              border: lender.isPrimary ? '2px solid hsl(var(--nh-gold))' : '1px solid rgba(255,255,255,0.1)',
              background: lender.isPrimary ? 'rgba(212,175,55,0.05)' : 'rgba(255,255,255,0.03)',
              position: 'relative',
              overflow: 'hidden'
            }}>
              {lender.isPrimary && (
                <div style={{
                  position: 'absolute',
                  top: '1rem',
                  right: '-3rem',
                  background: 'hsl(var(--nh-gold))',
                  color: 'black',
                  padding: '0.5rem 4rem',
                  transform: 'rotate(45deg)',
                  fontWeight: 'bold',
                  fontSize: '0.8rem',
                  letterSpacing: '0.1em'
                }}>
                  #1 RATED
                </div>
              )}
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem' }}>
                <div>
                  <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem', color: lender.isPrimary ? 'hsl(var(--nh-gold))' : 'white' }}>
                    {index + 1}. {lender.name}
                  </h2>
                  <span style={{ 
                    display: 'inline-block', 
                    padding: '0.25rem 0.75rem', 
                    background: 'rgba(255,255,255,0.1)', 
                    borderRadius: '4px',
                    fontSize: '0.9rem',
                    color: '#ddd'
                  }}>
                    {lender.badge}
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '1.5rem', color: 'hsl(var(--nh-gold))' }}>★★★★★</span>
                  <span style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{lender.rating}/5.0</span>
                </div>
              </div>

              <p style={{ opacity: 0.85, fontSize: '1.1rem', marginBottom: '2rem' }}>
                {lender.description}
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
                <div>
                  <h3 style={{ color: '#4ade80', marginBottom: '1rem', fontSize: '1.1rem' }}>✓ Pros</h3>
                  <ul style={{ listStyleType: 'none', padding: 0, margin: 0, opacity: 0.85 }}>
                    {lender.pros.map((pro, i) => (
                      <li key={i} style={{ marginBottom: '0.5rem' }}>• {pro}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 style={{ color: '#f87171', marginBottom: '1rem', fontSize: '1.1rem' }}>✗ Cons</h3>
                  <ul style={{ listStyleType: 'none', padding: 0, margin: 0, opacity: 0.85 }}>
                    {lender.cons.map((con, i) => (
                      <li key={i} style={{ marginBottom: '0.5rem' }}>• {con}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <Link href={lender.ctaLink} className={lender.isPrimary ? "btn-primary" : ""} style={{ 
                textDecoration: 'none', 
                display: 'inline-block',
                padding: lender.isPrimary ? undefined : '1rem 2rem',
                background: lender.isPrimary ? undefined : 'rgba(255,255,255,0.1)',
                color: 'white',
                borderRadius: '8px',
                fontWeight: 600,
                border: lender.isPrimary ? undefined : '1px solid rgba(255,255,255,0.2)'
              }}>
                {lender.ctaText}
              </Link>
            </div>
          ))}
        </div>
        
        <div style={{ marginTop: '4rem', padding: '2rem', borderTop: '1px solid rgba(255,255,255,0.1)', opacity: 0.6, fontSize: '0.9rem' }}>
          <p>
            <strong>Advertising Disclosure:</strong> NH Mortgage Journal is an independent, advertising-supported comparison service. 
            The offers that appear on this site are from companies from which we may receive compensation. 
            This compensation may impact how and where products appear on this site (including, for example, the order in which they appear).
          </p>
        </div>
      </div>
    </main>
  );
}
