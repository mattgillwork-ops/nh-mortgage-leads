import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Top 10 Best Mortgage Lenders in NH (2026 Reviews) | NH Financial Review',
  description: 'Compare the top 10 mortgage lenders in New Hampshire for 2026. See our top picks for first-time buyers, refinancing, and fast local closings.',
};

const lenders = [
  {
    id: 'nextgen',
    name: 'NH Mortgage Journal (Powered by NextGen)',
    rating: 5.0,
    badge: 'Best Overall in NH',
    description: 'Our top recommendation. An independent, Nashua-based engine that compares rates across wholesale channels to find the absolute lowest APR for NH residents. Exceptional local knowledge and access to NHHFA Home Start programs.',
    pros: ['Direct access to wholesale rates', 'NHHFA approved', 'Sovereign pre-approval engine', 'Extremely fast local closing times'],
    cons: ['Limited to NH and surrounding New England states'],
    ctaText: 'Calculate Your NH Rate',
    ctaLink: 'https://nh-mortgage-leads.onrender.com/funnel',
    isPrimary: true,
  },
  {
    id: 'rocket',
    name: 'Rocket Mortgage',
    rating: 4.6,
    badge: 'Best Digital Experience',
    description: 'A national powerhouse known for its seamless online application process. Great for tech-savvy borrowers who want to handle everything from their smartphone.',
    pros: ['Excellent mobile app', 'Fast online pre-approval', 'Customizable loan terms'],
    cons: ['Can have higher fees', 'Lacks localized NH market expertise'],
    ctaText: 'Check Rocket Rates',
    ctaLink: 'https://www.rocketmortgage.com/?affiliate=nhfr-lead',
    isPrimary: false,
  },
  {
    id: 'better',
    name: 'Better.com',
    rating: 4.5,
    badge: 'Best for No Origination Fees',
    description: 'Better.com stands out by eliminating traditional lender fees and offering a fully digital process. They provide aggressive rate matching.',
    pros: ['No origination or lender fees', 'Fast underwriting', '24/7 customer support'],
    cons: ['Online only (no physical branches)', 'May not support complex financial situations'],
    ctaText: 'Check Better Rates',
    ctaLink: 'https://better.com/mortgage/?affiliate=nhfr-lead',
    isPrimary: false,
  },
  {
    id: 'cmg',
    name: 'CMG Home Loans',
    rating: 4.4,
    badge: 'Best for Unique Loan Products',
    description: 'Known for their "All In One Loan" and strong presence in New Hampshire. They are a solid choice for borrowers needing creative financing solutions.',
    pros: ['Innovative loan options', 'Good local presence', 'First-time buyer friendly'],
    cons: ['Rates can sometimes be higher than wholesale brokers'],
    ctaText: 'Check CMG Rates',
    ctaLink: 'https://www.cmghomeloans.com/?affiliate=nhfr-lead',
    isPrimary: false,
  },
  {
    id: 'navyfederal',
    name: 'Navy Federal Credit Union',
    rating: 4.8,
    badge: 'Best for Military & Veterans',
    description: 'The top choice for active military and veterans seeking VA loans. They offer exceptional rates and zero down payment options for eligible borrowers.',
    pros: ['Industry-leading VA loan rates', 'No PMI requirements', 'Excellent customer service'],
    cons: ['Requires military affiliation to join', 'Physical branches are scarce in NH'],
    ctaText: 'Check Navy Federal Rates',
    ctaLink: 'https://www.navyfederal.org/loans-cards/mortgage.html',
    isPrimary: false,
  },
  {
    id: 'sofi',
    name: 'SoFi',
    rating: 4.5,
    badge: 'Best for Jumbo Loans',
    description: 'Ideal for buyers looking at high-value properties in NH (like the Seacoast or Lakes Region). SoFi offers competitive rates on high-balance loans with quick pre-approvals.',
    pros: ['Low rates for jumbo loans', 'Flexible down payment options', 'Member discounts available'],
    cons: ['Strict credit requirements (typically 680+)', 'No physical branches'],
    ctaText: 'Check SoFi Rates',
    ctaLink: 'https://www.sofi.com/home-loans/?affiliate=nhfr-lead',
    isPrimary: false,
  },
  {
    id: 'chase',
    name: 'Chase Bank',
    rating: 4.3,
    badge: 'Best for Low Down Payments',
    description: 'With their DreaMaker mortgage requiring as little as 3% down, Chase is a strong contender for first-time buyers with limited cash on hand.',
    pros: ['Low down payment programs', 'Homebuyer grants available', 'Robust online dashboard'],
    cons: ['Slower underwriting times', 'Rates often higher than wholesale'],
    ctaText: 'Check Chase Rates',
    ctaLink: 'https://mortgage.chase.com/',
    isPrimary: false,
  },
  {
    id: 'fairway',
    name: 'Fairway Independent Mortgage',
    rating: 4.6,
    badge: 'Best FHA Local Expertise',
    description: 'Fairway operates several local branches in New Hampshire and specializes in government-backed loans (FHA, USDA, VA) for borrowers with less-than-perfect credit.',
    pros: ['Highly localized NH presence', 'Fast closing guarantees', 'Great for FHA/USDA loans'],
    cons: ['Higher origination fees', 'Servicing is often transferred'],
    ctaText: 'Check Fairway Rates',
    ctaLink: 'https://www.fairwayindependentmc.com/',
    isPrimary: false,
  },
  {
    id: 'stmarys',
    name: "St. Mary's Bank",
    rating: 4.7,
    badge: 'Best NH Credit Union',
    description: 'The nation’s first credit union, based right here in Manchester. They offer incredible localized service, portfolio loans, and community-focused lending.',
    pros: ['Incredible local customer service', 'Portfolio lending for unique properties', 'Low fees'],
    cons: ['Must become a member', 'Slower technology interface'],
    ctaText: "Check St. Mary's Rates",
    ctaLink: 'https://www.stmarysbank.com/Personal/Mortgages',
    isPrimary: false,
  },
  {
    id: 'boa',
    name: 'Bank of America',
    rating: 4.1,
    badge: 'Best for Existing Customers',
    description: 'For borrowers who already bank with BoA, their Preferred Rewards program can offer significant discounts on mortgage origination fees.',
    pros: ['Discounts for existing customers', 'Grants for low-income buyers', 'Massive branch network'],
    cons: ['Slowest closing times', 'Rigid underwriting standards'],
    ctaText: 'Check BoA Rates',
    ctaLink: 'https://www.bankofamerica.com/mortgage/',
    isPrimary: false,
  },
];

export default function Home() {
  return (
    <main style={{ minHeight: '100vh', background: '#f9fafb', color: '#111827', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <header style={{ background: '#ffffff', padding: '1rem 2rem', borderBottom: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', justifyContent: 'space-between', boxShadow: '0 1px 3px 0 rgba(0,0,0,0.05)' }}>
        <div style={{ fontSize: '1.2rem', fontWeight: 800, fontFamily: 'Georgia, serif', color: '#111827' }}>NH Financial Review</div>
        <div style={{ fontSize: '0.75rem', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>Independent Mortgage Analysis</div>
      </header>
      
      <div style={{ margin: '0 auto', padding: '2rem 1.5rem', maxWidth: '800px', lineHeight: '1.6' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem', fontFamily: 'Georgia, serif', fontWeight: 700, color: '#111827', lineHeight: 1.2 }}>
          Top 10 Best Mortgage Lenders in New Hampshire (2026)
        </h1>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem', borderBottom: '1px solid #e5e7eb', paddingBottom: '1rem' }}>
          <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: '#e5e7eb', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: '#4b5563', fontSize: '0.9rem' }}>
            NR
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '0.85rem', color: '#111827', fontWeight: 600 }}>By NHFR Review Team</span>
            <span style={{ fontSize: '0.75rem', color: '#6b7280' }}>Updated: May 18, 2026 • 7 min read</span>
          </div>
        </div>


        
        <div style={{ marginBottom: '2.5rem' }}>
          <p style={{ fontSize: '1.1rem', color: '#374151', margin: '0 0 1rem 0' }}>
            When you're buying a home in New Hampshire, securing the right mortgage is just as important as finding the perfect property. A lower interest rate can save you tens of thousands of dollars over the life of your loan, while a highly responsive lender can mean the difference between winning a bidding war in Manchester or missing out entirely.
          </p>
          <p style={{ fontSize: '1.1rem', color: '#374151', margin: 0 }}>
            To help you navigate the highly competitive 2026 Granite State housing market, our editorial team analyzed dozens of national and local lenders. We weighed current rates, access to NHHFA Home Start programs, closing speeds, and customer satisfaction to bring you our definitive top picks.
          </p>
        </div>

        <div style={{ background: '#f3f4f6', padding: '1.5rem', borderRadius: '8px', marginBottom: '3rem', border: '1px solid #e5e7eb' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', color: '#111827', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Jump to our top picks:
          </h3>
          <ul style={{ listStyleType: 'none', padding: 0, margin: 0, display: 'grid', gridTemplateColumns: '1fr', gap: '0.5rem' }}>
            {lenders.slice(0, 5).map(lender => (
              <li key={lender.id}>
                <a href={`#${lender.id}`} style={{ textDecoration: 'none', color: '#1d4ed8', fontWeight: 600, fontSize: '0.95rem' }}>
                  {lender.name} — <span style={{ color: '#4b5563', fontWeight: 400 }}>{lender.badge}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {lenders.map((lender, index) => (
            <div id={lender.id} key={index} style={{ 
              padding: '1.5rem', 
              border: lender.isPrimary ? '2px solid #1d4ed8' : '1px solid #e5e7eb',
              background: '#ffffff',
              borderRadius: '8px',
              boxShadow: lender.isPrimary ? '0 4px 6px -1px rgba(29, 78, 216, 0.1)' : '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
              position: 'relative',
              overflow: 'hidden'
            }}>
              {lender.isPrimary && (
                <div style={{
                  position: 'absolute',
                  top: '0.75rem',
                  right: '-2rem',
                  background: '#1d4ed8',
                  color: 'white',
                  padding: '0.25rem 2.5rem',
                  transform: 'rotate(45deg)',
                  fontWeight: 'bold',
                  fontSize: '0.65rem',
                  letterSpacing: '0.05em',
                  zIndex: 10,
                }}>
                  #1 RATED
                </div>
              )}
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <div>
                  <h2 style={{ fontSize: '1.5rem', margin: '0 0 0.25rem 0', fontFamily: 'Georgia, serif', color: '#111827', fontWeight: 700 }}>
                    {index + 1}. {lender.name}
                  </h2>
                  <span style={{ 
                    display: 'inline-block', 
                    padding: '0.15rem 0.5rem', 
                    background: lender.isPrimary ? '#eff6ff' : '#f3f4f6', 
                    borderRadius: '4px',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    color: lender.isPrimary ? '#1d4ed8' : '#4b5563',
                    textTransform: 'uppercase'
                  }}>
                    {lender.badge}
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  <span style={{ fontSize: '1rem', color: '#fbbf24' }}>★★★★★</span>
                  <span style={{ fontSize: '1rem', fontWeight: 700, color: '#111827' }}>{lender.rating}</span>
                </div>
              </div>

              <p style={{ fontSize: '1rem', margin: '0 0 1rem 0', color: '#4b5563', lineHeight: 1.6 }}>
                {lender.description}
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem', background: '#f9fafb', padding: '1rem', borderRadius: '6px' }}>
                <div>
                  <h3 style={{ color: '#16a34a', margin: '0 0 0.5rem 0', fontSize: '0.9rem', fontWeight: 700 }}>Pros</h3>
                  <ul style={{ listStyleType: 'none', padding: 0, margin: 0, color: '#374151', fontSize: '0.9rem' }}>
                    {lender.pros.map((pro, i) => (
                      <li key={i} style={{ marginBottom: '0.25rem', display: 'flex', gap: '0.35rem' }}>
                        <span style={{ color: '#16a34a' }}>✓</span> {pro}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 style={{ color: '#dc2626', margin: '0 0 0.5rem 0', fontSize: '0.9rem', fontWeight: 700 }}>Cons</h3>
                  <ul style={{ listStyleType: 'none', padding: 0, margin: 0, color: '#374151', fontSize: '0.9rem' }}>
                    {lender.cons.map((con, i) => (
                      <li key={i} style={{ marginBottom: '0.25rem', display: 'flex', gap: '0.35rem' }}>
                        <span style={{ color: '#dc2626' }}>✗</span> {con}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <a href={lender.ctaLink} style={{ 
                textDecoration: 'none', 
                display: 'block',
                padding: '0.75rem 1.5rem',
                background: lender.isPrimary ? '#1d4ed8' : '#ffffff',
                color: lender.isPrimary ? '#ffffff' : '#111827',
                borderRadius: '6px',
                fontWeight: 700,
                border: lender.isPrimary ? 'none' : '1px solid #d1d5db',
                textAlign: 'center',
                fontSize: '1rem',
                transition: 'all 0.2s ease-in-out'
              }}>
                {lender.ctaText}
              </a>
            </div>
          ))}
        </div>
        
        <div style={{ marginTop: '3rem', padding: '2rem 0', borderTop: '1px solid #e5e7eb', color: '#6b7280', fontSize: '0.75rem', lineHeight: 1.5, textAlign: 'center' }}>
          <p style={{ marginBottom: '1rem', opacity: 0.8 }}>
            <em><strong>Advertiser Disclosure:</strong> Many of the offers that appear on this site are from companies from which NH Financial Review receives compensation. This compensation may impact how and where products appear on this site (including, for example, the order in which they appear). However, this does not influence our evaluations. Our opinions are our own.</em>
          </p>
          <p>
            © 2026 NH Financial Review. All rights reserved.
          </p>
        </div>
      </div>
    </main>
  );
}
