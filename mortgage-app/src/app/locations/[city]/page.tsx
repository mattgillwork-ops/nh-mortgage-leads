import React from 'react';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import locationsData from '@/data/locations.json';
import { Metadata } from 'next';

type Props = {
  params: Promise<{ city: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { city } = await params;
  const location = locationsData.find((loc) => loc.slug === city);
  
  if (!location) {
    return { title: 'Location Not Found' };
  }

  return {
    title: `${location.name} NH Mortgage Rates & Home Loans 2026 | NH Mortgage Journal`,
    description: `Current mortgage rates, home loan options, and housing market trends for ${location.name}, NH. Median home prices and local first-time buyer programs.`,
  };
}

export default async function LocationPage({ params }: Props) {
  const { city } = await params;
  const location = locationsData.find((loc) => loc.slug === city);

  if (!location) {
    notFound();
  }

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
          Mortgage Rates & Home Loans in <span className="gold-gradient">{location.name}, {location.state}</span>
        </h1>
        
        <div className="glass-panel" style={{ padding: '3rem', marginBottom: '4rem' }}>
          <h2 style={{ color: 'hsl(var(--nh-gold))', marginBottom: '1.5rem' }}>Local Market Intel: 2026</h2>
          <p style={{ opacity: 0.85, fontSize: '1.2rem', marginBottom: '1.5rem' }}>
            {location.description}
          </p>
          <div style={{ display: 'flex', gap: '2rem', marginTop: '2rem' }}>
            <div style={{ flex: 1, padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
              <h3 style={{ fontSize: '1rem', color: 'gray', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Median Home Price</h3>
              <p className="display-font" style={{ fontSize: '2rem', margin: '0.5rem 0 0 0', color: 'white' }}>{location.medianHomePrice}</p>
            </div>
            <div style={{ flex: 1, padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
              <h3 style={{ fontSize: '1rem', color: 'gray', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Market Pace</h3>
              <p className="display-font" style={{ fontSize: '2rem', margin: '0.5rem 0 0 0', color: 'white' }}>{location.marketPace}</p>
            </div>
          </div>
        </div>

        <h2 className="display-font" style={{ fontSize: '2.5rem', marginBottom: '1.5rem', color: 'white' }}>Top Loan Programs in {location.name}</h2>
        <ul style={{ listStyleType: 'none', padding: 0, marginBottom: '4rem' }}>
          {location.programs.map((program, index) => (
            <li key={index} style={{ marginBottom: '1rem', opacity: 0.85, fontSize: '1.2rem', display: 'flex', alignItems: 'center' }}>
              <span style={{ color: 'hsl(var(--nh-gold))', marginRight: '1rem' }}>✓</span> {program}
            </li>
          ))}
        </ul>

        <div className="glass-panel" style={{ padding: '3rem', background: 'rgba(212,175,55,0.05)', border: '1px solid rgba(212,175,55,0.15)', textAlign: 'center' }}>
          <h2 style={{ marginBottom: '1.5rem', color: 'hsl(var(--nh-gold))' }}>Get Your Custom Rate for {location.name}</h2>
          <p style={{ opacity: 0.85, marginBottom: '2rem' }}>
            Our engine builds a sovereign pre-approval and calculates your 30-year wealth trajectory using actual NH data.
          </p>
          <Link href="/funnel" className="btn-primary" style={{ textDecoration: 'none', display: 'inline-block' }}>Launch Rate Engine</Link>
        </div>
      </div>
    </main>
  );
}

export async function generateStaticParams() {
  return locationsData.map((location) => ({
    city: location.slug,
  }));
}
