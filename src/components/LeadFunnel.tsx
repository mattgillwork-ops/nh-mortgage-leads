'use client';

import React, { useState } from 'react';
import rateData from '../data/rates.json';

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
    const rate = rateData.rate / 100; 
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
      <div className="glass-panel animate-fade-in" style={{ padding: '4rem', textAlign: 'center', maxWidth: '800px', margin: '2rem auto' }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>💹</div>
        <h2 className="gold-gradient" style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>ROI Intelligence Report</h2>
        <p style={{ opacity: 0.7, marginBottom: '3rem' }}>Wealth Impact Analysis for <strong>{formData.location_nh || 'New Hampshire'}</strong></p>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '4rem' }}>
            <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <div style={{ fontSize: '0.7rem', opacity: 0.5, textTransform: 'uppercase' }}>Monthly Payment</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700 }}>${formData.est_payment}</div>
            </div>
            <div className="glass-panel" style={{ padding: '1.5rem', border: '1px solid hsla(var(--nh-gold), 0.3)' }}>
                <div style={{ fontSize: '0.7rem', opacity: 0.5, textTransform: 'uppercase', color: 'hsl(var(--nh-gold))' }}>Monthly Savings</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'hsl(var(--nh-gold))' }}>${formData.monthly_savings}</div>
            </div>
            <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <div style={{ fontSize: '0.7rem', opacity: 0.5, textTransform: 'uppercase' }}>Market Rate</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700 }}>{rateData.rate}%</div>
            </div>
        </div>

        <div className="glass-panel" style={{ padding: '2rem', marginBottom: '3rem', background: 'hsla(var(--nh-gold), 0.05)' }}>
            <div style={{ fontSize: '0.8rem', opacity: 0.7, marginBottom: '0.5rem' }}>30-Year Wealth Impact</div>
            <div style={{ fontSize: '3rem', fontWeight: 900 }} className="gold-gradient">{formData.lifetime_roi}</div>
            <p style={{ fontSize: '0.9rem', opacity: 0.5, marginTop: '1rem' }}>Projected savings and equity growth over the loan term.</p>
        </div>

        <div style={{ textAlign: 'left', background: 'rgba(255,255,255,0.02)', padding: '2rem', borderRadius: '16px' }}>
            <h3 style={{ marginBottom: '1rem', fontSize: '1.2rem' }}>Next Steps:</h3>
            <ul style={{ listStyle: 'none', display: 'grid', gap: '1rem' }}>
                <li>✅ <strong>Verify Credit</strong>: Your {formData.credit_score} profile is ready for audit.</li>
                <li>✅ <strong>Email Sent</strong>: A full PDF copy of this report has been sent to your inbox.</li>
                <li>📞 <strong>Local Support</strong>: A Manchester analyst will reach out to verify these numbers at {formData.phone}.</li>
            </ul>
        </div>

        <button 
            onClick={() => { setStep(1); setIsSubmitted(false); setFormData({}); }}
            className="btn-primary" 
            style={{ marginTop: '3rem', width: 'auto', padding: '1rem 3rem' }}
        >
            Start New Analysis
        </button>
      </div>
    );
  }

  const currentStepData = STEPS[step - 1];

  return (
    <div className="glass-panel animate-fade-in" style={{ padding: '3rem', maxWidth: '600px', margin: '2rem auto', position: 'relative' }}>
      <div style={{ marginBottom: '2rem' }}>
        <div className="badge">Step {step} of {STEPS.length}</div>
        <div style={{ height: '4px', background: 'rgba(255,255,255,0.05)', borderRadius: '2px', marginTop: '1rem' }}>
          <div style={{ height: '100%', background: 'hsl(var(--nh-gold))', width: `${(step / STEPS.length) * 100}%`, transition: 'width 0.5s ease', boxShadow: '0 0 10px hsl(var(--nh-gold))' }} />
        </div>
      </div>

      <h2 style={{ fontSize: '2rem', marginBottom: '2rem' }}>{currentStepData.title}</h2>

      {currentStepData.type === 'choice' ? (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {currentStepData.options?.map(opt => (
            <button 
              key={opt}
              onClick={() => handleChoice(currentStepData.field!, opt)}
              className="glass-panel"
              style={{ padding: '1.5rem', textAlign: 'left', cursor: 'pointer', fontWeight: 600, transition: 'all 0.2s', background: formData[currentStepData.field!] === opt ? 'hsl(var(--nh-gold))' : 'transparent', color: formData[currentStepData.field!] === opt ? 'black' : 'white' }}
            >
              {opt}
            </button>
          ))}
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '1.5rem' }}>
          {currentStepData.fields?.map(f => (
            <div key={f.name}>
              <label style={{ display: 'block', fontSize: '0.8rem', opacity: 0.5, marginBottom: '0.5rem', textTransform: 'uppercase' }}>{f.label}</label>
              <input 
                type={f.type} 
                name={f.name}
                placeholder={f.placeholder}
                onChange={handleInputChange}
                className="glass-panel"
                style={{ width: '100%', padding: '1rem', background: 'rgba(255,255,255,0.03)', color: 'white', border: '1px solid rgba(255,255,255,0.1)' }}
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
