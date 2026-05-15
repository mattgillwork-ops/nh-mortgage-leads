'use client';

import React, { useState, useEffect } from 'react';

export default function AdminDashboard() {
  const [leads, setLeads] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchLeads = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/get_leads');
      const data = await res.json();
      setLeads(data);
    } catch (err) {
      console.error('Failed to fetch leads', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  const downloadCSV = () => {
    const headers = "ID,Name,Phone,Email,Intent,Status,Date,MonthlySavings,ROI\n";
    const rows = leads.map(l => `${l.id},${l.first_name} ${l.last_name},${l.phone},${l.email},${l.loan_purpose},New,${l.created_at},${l.monthly_savings},${l.lifetime_roi}`).join("\n");
    const blob = new Blob([headers + rows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nh_mortgage_leads_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  return (
    <main style={{ padding: '4rem 8%', minHeight: '100vh', background: 'hsl(var(--nh-slate))' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
        <div>
          <h1 className="display-font" style={{ fontSize: '2.5rem' }}>Lead <span className="gold-gradient">Intelligence</span></h1>
          <p style={{ opacity: 0.5 }}>Sovereign Dashboard v3.5 - Connected to Live Data</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button onClick={fetchLeads} className="glass-panel" style={{ padding: '0.8rem 1.5rem', cursor: 'pointer' }}>Refresh</button>
          <button onClick={downloadCSV} className="btn-primary">Download CSV</button>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '2rem', overflowX: 'auto', minHeight: '400px' }}>
        {loading ? (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px', opacity: 0.5 }}>
                📡 Accessing Intelligence Vault...
            </div>
        ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
                <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', color: 'hsl(var(--nh-gold))', textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.1em' }}>
                <th style={{ padding: '1rem' }}>Borrower</th>
                <th style={{ padding: '1rem' }}>Intent</th>
                <th style={{ padding: '1rem' }}>Phone</th>
                <th style={{ padding: '1rem' }}>Savings/mo</th>
                <th style={{ padding: '1rem' }}>ROI Impact</th>
                <th style={{ padding: '1rem' }}>Status</th>
                <th style={{ padding: '1rem' }}>Captured</th>
                </tr>
            </thead>
            <tbody>
                {leads.map(lead => (
                <tr key={lead.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.02)', fontSize: '0.9rem' }}>
                    <td style={{ padding: '1.2rem' }}>
                        <div style={{ fontWeight: 600 }}>{lead.first_name} {lead.last_name}</div>
                        <div style={{ fontSize: '0.7rem', opacity: 0.5 }}>{lead.email}</div>
                    </td>
                    <td style={{ padding: '1.2rem' }}>{lead.loan_purpose}</td>
                    <td style={{ padding: '1.2rem', opacity: 0.8 }}>{lead.phone}</td>
                    <td style={{ padding: '1.2rem', color: 'hsl(var(--nh-gold))', fontWeight: 700 }}>${lead.monthly_savings}</td>
                    <td style={{ padding: '1.2rem' }}>{lead.lifetime_roi}</td>
                    <td style={{ padding: '1.2rem' }}>
                        <span style={{ 
                            background: 'hsla(var(--nh-gold), 0.1)',
                            color: 'hsl(var(--nh-gold))',
                            padding: '0.2rem 0.6rem',
                            borderRadius: '4px',
                            fontSize: '0.7rem',
                            fontWeight: 700
                        }}>
                            New
                        </span>
                    </td>
                    <td style={{ padding: '1.2rem', opacity: 0.5 }}>{new Date(lead.created_at).toLocaleDateString()}</td>
                </tr>
                ))}
                {leads.length === 0 && (
                    <tr>
                        <td colSpan={7} style={{ padding: '4rem', textAlign: 'center', opacity: 0.3 }}>No leads captured yet.</td>
                    </tr>
                )}
            </tbody>
            </table>
        )}
      </div>
    </main>
  );
}
