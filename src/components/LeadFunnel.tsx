'use client';

import React, { useState, useEffect } from 'react';
import { supabase } from '@/utils/supabase';

const STEPS = [
  { id: 1, title: "Objective", type: 'choice', field: 'loan_purpose', options: ['Purchase', 'Refinance'] },
  { id: 2, title: "Property", type: 'choice', field: 'property_type', options: ['Primary Residence', 'Secondary/Vacation', 'Investment'] },
  { id: 3, title: "Financials", type: 'input', fields: [
      { name: 'est_value', label: 'Target Purchase Price ($)', type: 'number', placeholder: '450,000' },
      { name: 'down_payment', label: 'Planned Down Payment ($)', type: 'number', placeholder: '20,000' },
      { name: 'current_payment', label: 'Current Monthly Rent/Mortgage ($)', type: 'number', placeholder: '2,500' }
  ]},
  { id: 4, title: "Credit", type: 'choice', field: 'credit_score', options: ['Excellent (740+)', 'Good (680-739)', 'Fair (620-679)', 'Poor (<620)'] },
  { id: 5, title: "Location", type: 'input', fields: [
      { name: 'location_nh', label: 'City or County in New Hampshire', type: 'text', placeholder: 'e.g. Manchester, Rockingham' }
  ]},
  { id: 6, title: "Contact", type: 'input', fields: [
      { name: 'first_name', label: 'First Name', type: 'text', placeholder: 'John' },
      { name: 'last_name', label: 'Last Name', type: 'text', placeholder: 'Doe' },
      { name: 'email', label: 'Email Address', type: 'email', placeholder: 'john@example.com' },
      { name: 'phone', label: 'Phone Number', type: 'tel', placeholder: '603-XXX-XXXX' }
  ]}
];

export default function LeadFunnel() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<any>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [marketRate, setMarketRate] = useState<any>({ rate: 6.875, last_verified: 'Loading...' });

  useEffect(() => {
    async function fetchRate() {
        const { data, error } = await supabase
            .from('market_rates')
            .select('rate, last_verified')
            .eq('rate_type', '30Y_FIXED')
            .single();
        
        if (data && !error) {
            setMarketRate(data);
        }
    }
    fetchRate();
  }, []);

  const handleChoice = (field: string, value: string) => {
    const updatedData = { ...formData, [field]: value };
    setFormData(updatedData);
    if (step < STEPS.length) setStep(step + 1);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    console.log("Submitting Lead:", formData);
    
    // Dynamic ROI calculation logic
    const principal = (formData.est_value || 450000) - (formData.down_payment || 20000);
    const rate = marketRate.rate / 100; 
    const monthlyRate = rate / 12;
    const n = 360; 
    const monthlyPayment = principal * (monthlyRate * Math.pow(1+monthlyRate, n)) / (Math.pow(1+monthlyRate, n) - 1);
    
    const monthlySavings = (formData.current_payment || 2500) - monthlyPayment;
    const lifetimeROI = monthlySavings * 12 * 30; // 30-year impact
    
    setFormData({ 
        ...formData, 
        est_payment: monthlyPayment.toFixed(2),
        monthly_savings: monthlySavings.toFixed(2),
        lifetime_roi: lifetimeROI.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
    });
    
    // Send lead to API (which sends email via Resend)
    try {
        await fetch('/api/submit_lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
    } catch (e) { console.error("Lead delivery failed", e); }
    
    setIsSubmitted(true);
  };

  if (isSubmitted) {
    return (
      <div className="journal-card animate-fade-in" style={{ textAlign: 'center', maxWidth: '800px', margin: '2rem auto' }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>💹</div>
        <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>ROI Intelligence Report</h2>
        <p style={{ opacity: 0.7, marginBottom: '3rem' }}>Wealth Impact Analysis for <strong>{formData.location_nh || 'New Hampshire'}</strong></p>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '4rem' }}>
            <div className="journal-card" style={{ padding: '1.5rem' }}>
                <div style={{ fontSize: '0.7rem', opacity: 0.5, textTransform: 'uppercase' }}>Monthly Payment</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700 }}>${formData.est_payment}</div>
            </div>
            <div className="journal-card" style={{ padding: '1.5rem', border: '1px solid hsla(var(--nh-gold), 0.3)' }}>
                <div style={{ fontSize: '0.7rem', opacity: 0.6, textTransform: 'uppercase', color: 'hsl(var(--nh-gold))' }}>Monthly Savings</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'hsl(var(--nh-gold))' }}>${formData.monthly_savings}</div>
            </div>
            <div className="journal-card" style={{ padding: '1.5rem' }}>
                <div style={{ fontSize: '0.7rem', opacity: 0.5, textTransform: 'uppercase' }}>Market Rate</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700 }}>{marketRate.rate}%</div>
                <div style={{ fontSize: '0.6rem', opacity: 0.4, marginTop: '0.5rem', textTransform: 'uppercase' }}>
                    Verified: {new Date(marketRate.last_verified).toLocaleDateString()}
                </div>
            </div>
        </div>

        <div className="journal-card" style={{ padding: '2rem', marginBottom: '3rem', background: 'hsla(var(--nh-gold), 0.03)', border: '1px solid hsla(var(--nh-gold), 0.1)' }}>
            <div style={{ fontSize: '0.8rem', opacity: 0.7, marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.1em' }}>30-Year Wealth Impact</div>
            <div style={{ fontSize: '3.5rem', fontWeight: 900, color: 'hsl(var(--nh-gold))' }}>{formData.lifetime_roi}</div>
            <p style={{ fontSize: '0.9rem', opacity: 0.6, marginTop: '1rem' }}>Projected savings and equity growth over the loan term.</p>
        </div>

        <div style={{ textAlign: 'left', background: '#f8fafc', padding: '2.5rem', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
            <h3 style={{ marginBottom: '1.5rem', fontSize: '1.2rem' }}>Status & Next Steps:</h3>
            <ul className="journal-list" style={{ margin: 0 }}>
                <li><strong>Lead Verified</strong>: Your market profile has been successfully ingested into our local engine.</li>
                <li><strong>Analyst Assigned</strong>: A NH-based lead analyst will review your ROI numbers for accuracy.</li>
                <li><strong>Direct Outreach</strong>: We will verify these projections with you at {formData.phone} shortly.</li>
            </ul>
        </div>

        <button 
            onClick={() => { setStep(1); setIsSubmitted(false); setFormData({}); }}
            className="btn-primary" 
            style={{ marginTop: '3rem' }}
        >
            Start New Analysis
        </button>
      </div>
    );
  }

  const currentStepData = STEPS[step - 1];

  return (
    <div className="journal-card animate-fade-in" style={{ maxWidth: '600px', margin: '4rem auto', position: 'relative' }}>
      <div style={{ marginBottom: '3rem' }}>
        <div className="badge">Step {step} of {STEPS.length}</div>
        <div style={{ height: '2px', background: '#f1f5f9', marginTop: '1.5rem' }}>
          <div style={{ height: '100%', background: 'hsl(var(--nh-gold))', width: `${(step / STEPS.length) * 100}%`, transition: 'width 0.4s ease' }} />
        </div>
      </div>

      <h2 style={{ fontSize: '2.5rem', marginBottom: '2.5rem', letterSpacing: '-0.02em' }}>{currentStepData.title}</h2>

      {currentStepData.type === 'choice' ? (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {currentStepData.options?.map(opt => (
            <button 
              key={opt}
              onClick={() => handleChoice(currentStepData.field!, opt)}
              style={{ 
                  padding: '1.5rem', 
                  textAlign: 'left', 
                  cursor: 'pointer', 
                  fontWeight: 600, 
                  transition: 'all 0.2s', 
                  background: formData[currentStepData.field!] === opt ? 'hsl(var(--nh-slate))' : 'white', 
                  color: formData[currentStepData.field!] === opt ? 'white' : 'hsl(var(--nh-slate))',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                  fontSize: '1rem'
              }}
            >
              {opt}
            </button>
          ))}
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '2rem' }}>
          {currentStepData.fields?.map(f => (
            <div key={f.name}>
              <label style={{ display: 'block', fontSize: '0.7rem', opacity: 0.6, marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 700 }}>{f.label}</label>
              <input 
                type={f.type} 
                name={f.name}
                placeholder={f.placeholder}
                onChange={handleInputChange}
                style={{ 
                    width: '100%', 
                    padding: '1.2rem', 
                    background: 'white', 
                    color: 'hsl(var(--nh-slate))', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    fontSize: '1.1rem'
                }}
              />
            </div>
          ))}
          <button 
            onClick={step === STEPS.length ? handleSubmit : () => setStep(step + 1)}
            className="btn-primary" 
            style={{ marginTop: '1rem' }}
          >
            {step === STEPS.length ? 'Generate Analysis' : 'Continue'}
          </button>
        </div>
      )}
    </div>
  );
}
