'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { calculateMortgageReport, MortgageReport } from '../utils/mortgage_utils';

const STEPS = [
  { id: 1, title: "Your Objective", type: 'choice', field: 'loan_purpose', options: ['Purchase', 'Refinance'] },
  { id: 2, title: "Property Type", type: 'choice', field: 'property_type', options: ['Primary Residence', 'Secondary/Vacation', 'Investment'] },
  { id: 3, title: "Financial Overview", type: 'input', fields: [
      { name: 'est_value', label: 'Estimated Value / Purchase Price ($)', type: 'number', placeholder: '450,000', required: true },
      { name: 'down_payment', label: 'Down Payment ($)', type: 'number', placeholder: '20,000', required: true },
      { name: 'current_payment', label: 'Current Monthly Rent/Mortgage ($)', type: 'number', placeholder: '2,500', required: true }
  ]},
  { id: 4, title: "Credit Health", type: 'choice', field: 'credit_score', options: ['Excellent (740+)', 'Good (680-739)', 'Fair (620-679)', 'Poor (<620)'] },
  { id: 5, title: "NH Location", type: 'input', fields: [
      { name: 'location_nh', label: 'City or County in New Hampshire', type: 'text', placeholder: 'e.g. Manchester, Rockingham', required: true }
  ]},
  { id: 6, title: "Intelligence Dispatch", type: 'input', fields: [
      { name: 'first_name', label: 'First Name', type: 'text', placeholder: 'John', required: true },
      { name: 'last_name', label: 'Last Name', type: 'text', placeholder: 'Doe', required: true },
      { name: 'email', label: 'Email Address', type: 'email', placeholder: 'john@example.com', required: true },
      { name: 'phone', label: 'Phone Number', type: 'tel', placeholder: '603-XXX-XXXX', required: true }
  ]}
];

export default function LeadFunnel() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<any>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [report, setReport] = useState<MortgageReport | null>(null);
  const [marketRate, setMarketRate] = useState<any>({ rate: 5.25 });
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetch('/api/get_rates')
      .then(res => res.json())
      .then(data => setMarketRate(data))
      .catch(() => console.warn('Using fallback market rates'));

    // Capture UTM parameters from URL search query on mount
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const utmSource = params.get('utm_source');
      const utmMedium = params.get('utm_medium');
      const utmCampaign = params.get('utm_campaign');

      if (utmSource || utmMedium || utmCampaign) {
        setFormData((prev: any) => ({
          ...prev,
          ...(utmSource ? { utm_source: utmSource } : {}),
          ...(utmMedium ? { utm_medium: utmMedium } : {}),
          ...(utmCampaign ? { utm_campaign: utmCampaign } : {}),
        }));
      }
    }
  }, []);

  const validateStep = () => {
    const currentStep = STEPS[step - 1];
    if (currentStep.type === 'choice') {
      if (!formData[currentStep.field!]) {
        setError('Please select an option to continue.');
        return false;
      }
    } else {
      for (const field of currentStep.fields!) {
        if (field.required && !formData[field.name]) {
          setError(`Please fill out the ${field.label.toLowerCase()} field.`);
          return false;
        }
        if (field.type === 'email' && formData[field.name]) {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(formData[field.name])) {
            setError('Please enter a valid email address.');
            return false;
          }
        }
      }
    }
    setError(null);
    return true;
  };

  const handleNext = () => {
    if (validateStep()) {
      if (step < STEPS.length) {
        setStep(step + 1);
      } else {
        handleSubmit();
      }
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
      setError(null);
    }
  };

  const handleChoice = (field: string, value: string) => {
    setFormData({ ...formData, [field]: value });
    setError(null);
    setTimeout(() => {
        if (step < STEPS.length) setStep(step + 1);
    }, 300);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    
    // Calculate Report
    const calculationReport = calculateMortgageReport({
        est_value: parseFloat(formData.est_value),
        down_payment: parseFloat(formData.down_payment),
        current_payment: parseFloat(formData.current_payment),
        annual_rate: marketRate.rate,
    });
    
    setReport(calculationReport);
    
    const submissionData = { ...formData, ...calculationReport };
    
    try {
        const response = await fetch('/api/submit_lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(submissionData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Submission failed');
        }

        setIsSubmitted(true);
    } catch (e: any) { 
        console.error("Lead delivery failed", e);
        setError(e.message || "Something went wrong during submission. Please try again.");
    } finally {
        setIsSubmitting(false);
    }
  };

  if (isSubmitted && report) {
    const isPositiveSavings = report.monthly_savings > 0;
    
    return (
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel" 
        style={{ padding: '4rem', textAlign: 'center', maxWidth: '900px', margin: '4rem auto' }}
      >
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🏔️</div>
        <h2 className="gold-gradient" style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>NH Wealth Intelligence Report</h2>
        <p style={{ opacity: 0.7, marginBottom: '3rem' }}>Strategy for <strong>{formData.location_nh}</strong> at <strong>{marketRate.rate}%</strong> Locked Market Rate</p>
        
        {/* Primary Insight: Positive Pivot Logic */}
        {!isPositiveSavings ? (
            <div className="glass-panel" style={{ padding: '2.5rem', marginBottom: '3rem', background: 'hsla(var(--nh-gold), 0.1)', border: '1px solid hsla(var(--nh-gold), 0.5)', position: 'relative', overflow: 'hidden' }}>
                <div style={{ position: 'absolute', top: '-10%', right: '-10%', fontSize: '8rem', opacity: 0.05 }}>🏔️</div>
                <div style={{ fontSize: '0.9rem', color: 'hsl(var(--nh-gold))', fontWeight: 600, textTransform: 'uppercase', marginBottom: '0.5rem' }}>Primary Opportunity Found</div>
                <div style={{ fontSize: '1.2rem', marginBottom: '1.5rem', fontWeight: 500 }}>While your current payment is lower than market rates, your <strong>30-Year Wealth Trajectory</strong> remains the primary asset driver in NH.</div>
                <div style={{ fontSize: '4rem', fontWeight: 900 }} className="gold-gradient">${report.equity_30y.toLocaleString()}</div>
                <div style={{ fontSize: '0.9rem', opacity: 0.7, marginTop: '1rem' }}>Projected Home Equity & Asset Appreciation Value</div>
            </div>
        ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '4rem' }}>
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <div style={{ fontSize: '0.7rem', opacity: 0.5, textTransform: 'uppercase' }}>Monthly P&I</div>
                    <div style={{ fontSize: '1.8rem', fontWeight: 700 }}>${report.monthly_pi}</div>
                </div>
                
                <div className="glass-panel" style={{ padding: '1.5rem', border: '1px solid hsla(var(--nh-gold), 0.3)' }}>
                    <div style={{ fontSize: '0.7rem', opacity: 0.5, textTransform: 'uppercase', color: 'hsl(var(--nh-gold))' }}>Monthly Savings</div>
                    <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'hsl(var(--nh-gold))' }}>${report.monthly_savings}</div>
                </div>

                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <div style={{ fontSize: '0.7rem', opacity: 0.5, textTransform: 'uppercase' }}>Locked Market Rate</div>
                    <div style={{ fontSize: '1.8rem', fontWeight: 700 }}>{marketRate.rate}%</div>
                </div>
            </div>
        )}

        {isPositiveSavings && (
            <div className="glass-panel" style={{ padding: '2.5rem', marginBottom: '3rem', background: 'hsla(var(--nh-gold), 0.05)', position: 'relative', overflow: 'hidden' }}>
                <div style={{ position: 'absolute', top: '-10%', right: '-10%', fontSize: '8rem', opacity: 0.03 }}>💰</div>
                <div style={{ fontSize: '0.9rem', opacity: 0.7, marginBottom: '0.5rem' }}>30-Year Wealth Projection (Equity + Asset Growth)</div>
                <div style={{ fontSize: '4rem', fontWeight: 900 }} className="gold-gradient">${report.equity_30y.toLocaleString()}</div>
                <p style={{ fontSize: '0.9rem', opacity: 0.5, marginTop: '1rem' }}>Total projected asset value based on NH historical appreciation and principal payoff.</p>
            </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', textAlign: 'left', marginBottom: '3rem' }}>
            <div className="glass-panel" style={{ padding: '2rem' }}>
                <h3 style={{ marginBottom: '1.5rem', fontSize: '1.1rem', color: 'hsl(var(--nh-gold))' }}>Payment Breakdown</h3>
                <ul style={{ listStyle: 'none', display: 'grid', gap: '0.8rem', fontSize: '0.9rem' }}>
                    <li style={{ display: 'flex', justifyContent: 'space-between' }}><span>Principal & Interest</span> <strong>${report.monthly_pi}</strong></li>
                    <li style={{ display: 'flex', justifyContent: 'space-between' }}><span>Est. NH Property Taxes</span> <strong>${report.monthly_taxes}</strong></li>
                    <li style={{ display: 'flex', justifyContent: 'space-between' }}><span>Homeowners Insurance</span> <strong>${report.monthly_insurance}</strong></li>
                    {report.monthly_pmi > 0 && <li style={{ display: 'flex', justifyContent: 'space-between' }}><span>PMI (Low Down Payment)</span> <strong>${report.monthly_pmi}</strong></li>}
                    <li style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1rem', fontWeight: 700 }}><span>Total Monthly Payment</span> <span>${report.total_monthly_payment}</span></li>
                </ul>
            </div>
            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '2rem', borderRadius: '24px', border: '1px solid rgba(255,255,255,0.05)' }}>
                <h3 style={{ marginBottom: '1.5rem', fontSize: '1.1rem' }}>Concierge Next Steps:</h3>
                <ul style={{ listStyle: 'none', display: 'grid', gap: '1.2rem' }}>
                    <li style={{ display: 'flex', gap: '1rem' }}><span style={{ color: 'hsl(var(--nh-gold))' }}>⚜️</span> <div><strong>Priority Onboarding</strong>: Your {formData.credit_score} profile has been flagged for immediate asset verification.</div></li>
                    <li style={{ display: 'flex', gap: '1rem' }}><span style={{ color: 'hsl(var(--nh-gold))' }}>📞</span> <div><strong>Strategy Call</strong>: A Manchester senior analyst will call {formData.phone} within 24 hours to review your asset growth plan.</div></li>
                </ul>
            </div>
        </div>

        {/* Affiliate Integrations */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', textAlign: 'left', marginBottom: '2rem' }}>
            {(formData.credit_score.includes('<620') || formData.credit_score.includes('Fair')) && (
                <div className="glass-panel" style={{ padding: '2rem', border: '1px solid #ef4444', background: 'rgba(239, 68, 68, 0.05)', textAlign: 'center' }}>
                    <h3 style={{ color: '#ef4444', fontSize: '1.2rem', marginBottom: '0.5rem' }}>⚠️ Action Required: Optimize Your Credit Score</h3>
                    <p style={{ opacity: 0.8, fontSize: '0.95rem', marginBottom: '1.5rem', lineHeight: 1.5 }}>
                        Your current score ({formData.credit_score}) will result in significantly higher interest rates or denial from wholesale lenders. 
                        We highly recommend enrolling in a rapid credit repair program before your strategy call to secure the lowest possible rate.
                    </p>
                    <a href="https://www.lexingtonlaw.com/?affiliate=nhfr-lead" target="_blank" rel="noopener noreferrer" className="btn-primary" style={{ display: 'inline-block', background: '#ef4444', textDecoration: 'none' }}>
                        Start Credit Repair (Lexington Law)
                    </a>
                </div>
            )}

            <div className="glass-panel" style={{ padding: '2rem', border: '1px solid #3b82f6', background: 'rgba(59, 130, 246, 0.05)', textAlign: 'center' }}>
                <h3 style={{ color: '#60a5fa', fontSize: '1.2rem', marginBottom: '0.5rem' }}>Secure Your Investment</h3>
                <p style={{ opacity: 0.8, fontSize: '0.95rem', marginBottom: '1.5rem', lineHeight: 1.5 }}>
                    Lenders require proof of Homeowners Insurance before clearing you to close. 
                    Get an instant, digital quote right now to avoid delays in your closing timeline.
                </p>
                <a href="https://www.lemonade.com/homeowners?affiliate=nhfr-lead" target="_blank" rel="noopener noreferrer" className="btn-primary" style={{ display: 'inline-block', background: '#3b82f6', textDecoration: 'none' }}>
                    Get Instant Insurance Quote (Lemonade)
                </a>
            </div>
        </div>

        <button 
            onClick={() => { setStep(1); setIsSubmitted(false); setFormData({}); setReport(null); }}
            className="btn-primary" 
            style={{ marginTop: '4rem', width: 'auto', padding: '1.2rem 4rem' }}
        >
            Start New Strategy
        </button>
      </motion.div>
    );
  }

  const currentStepData = STEPS[step - 1];

  return (
    <div className="glass-panel animate-fade-in" style={{ padding: '3.5rem', maxWidth: '650px', margin: '4rem auto', position: 'relative', overflow: 'hidden' }}>
      <div style={{ marginBottom: '2.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div className="badge">Step {step} of {STEPS.length}</div>
            <div style={{ fontSize: '0.8rem', opacity: 0.4 }}>NH Intelligence Engine v3.2</div>
        </div>
        <div style={{ height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px', marginTop: '1.5rem', overflow: 'hidden' }}>
          <motion.div 
            initial={{ width: 0 }}
            animate={{ width: `${(step / STEPS.length) * 100}%` }}
            transition={{ duration: 0.8, ease: "circOut" }}
            style={{ height: '100%', background: 'hsl(var(--nh-gold))', boxShadow: '0 0 15px hsla(var(--nh-gold), 0.5)' }} 
          />
        </div>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.3 }}
        >
          <h2 style={{ fontSize: '2.2rem', marginBottom: '2rem' }} className="display-font">{currentStepData.title}</h2>

          {currentStepData.type === 'choice' ? (
            <div style={{ display: 'grid', gap: '1.2rem' }}>
              {currentStepData.options?.map(opt => (
                <button 
                  key={opt}
                  onClick={() => handleChoice(currentStepData.field!, opt)}
                  className="glass-panel"
                  style={{ 
                    padding: '1.8rem', 
                    textAlign: 'left', 
                    cursor: 'pointer', 
                    fontWeight: 600, 
                    transition: 'all 0.3s ease', 
                    background: formData[currentStepData.field!] === opt ? 'hsl(var(--nh-gold))' : 'rgba(255,255,255,0.02)', 
                    color: formData[currentStepData.field!] === opt ? 'hsl(var(--nh-slate))' : 'hsl(var(--nh-blue-foreground))',
                    border: formData[currentStepData.field!] === opt ? '1px solid hsl(var(--nh-gold))' : '1px solid rgba(255,255,255,0.1)'
                  }}
                >
                  {opt}
                </button>
              ))}
            </div>
          ) : (
            <div style={{ display: 'grid', gap: '1.8rem' }}>
              {currentStepData.fields?.map(f => (
                <div key={f.name}>
                  <label style={{ display: 'block', fontSize: '0.75rem', opacity: 0.5, marginBottom: '0.6rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{f.label}</label>
                  <input 
                    type={f.type} 
                    name={f.name}
                    value={formData[f.name] || ''}
                    placeholder={f.placeholder}
                    onChange={handleInputChange}
                    className="glass-panel"
                    style={{ 
                        width: '100%', 
                        padding: '1.2rem', 
                        background: 'rgba(255,255,255,0.05)', 
                        color: 'hsl(var(--nh-blue-foreground))', 
                        border: '1px solid rgba(255,255,255,0.1)',
                        fontSize: '1rem'
                    }}
                  />

                </div>
              ))}
            </div>
          )}
        </motion.div>
      </AnimatePresence>

      {error && (
        <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            style={{ marginTop: '1.5rem', color: '#f87171', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
            <span>⚠️</span> {error}
        </motion.div>
      )}

      <div style={{ display: 'flex', gap: '1rem', marginTop: '3rem' }}>
        {step > 1 && (
            <button onClick={handleBack} className="glass-panel" style={{ flex: 1, padding: '1rem', cursor: 'pointer', fontWeight: 600 }}>Back</button>
        )}
        {(currentStepData.type === 'input' || step === STEPS.length) && (
            <button 
                onClick={handleNext}
                className="btn-primary" 
                style={{ flex: 2, position: 'relative' }}
                disabled={isSubmitting}
            >
                {isSubmitting ? 'Processing Intelligence...' : (step === STEPS.length ? 'Generate Report' : 'Continue')}
            </button>
        )}
      </div>
    </div>
  );
}
