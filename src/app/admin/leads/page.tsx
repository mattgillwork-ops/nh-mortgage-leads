'use client';

import React, { useState } from 'react';

const MOCK_LEADS = [
    { id: 1, name: "Alice Smith", phone: "603-555-0101", intent: "Purchase", status: "New", date: "2026-05-13" },
    { id: 2, name: "Bob Johnson", phone: "603-555-0202", intent: "Refinance", status: "Contacted", date: "2026-05-12" },
    { id: 3, name: "Charlie Brown", phone: "603-555-0303", intent: "Purchase", status: "Closed", date: "2026-05-10" },
];

export default function AdminDashboard() {
  const [leads] = useState(MOCK_LEADS);

  const downloadCSV = () => {
    const headers = "ID,Name,Phone,Intent,Status,Date\n";
    const rows = leads.map(l => `${l.id},${l.name},${l.phone},${l.intent},${l.status},${l.date}`).join("\n");
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
          <p style={{ opacity: 0.5 }}>Sovereign Dashboard v3.0</p>
        </div>
        <button onClick={downloadCSV} className="btn-primary">Download CSV</button>
      </div>

      <div className="glass-panel" style={{ padding: '2rem', overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', color: 'hsl(var(--nh-gold))', textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.1em' }}>
              <th style={{ padding: '1rem' }}>Name</th>
              <th style={{ padding: '1rem' }}>Intent</th>
              <th style={{ padding: '1rem' }}>Phone</th>
              <th style={{ padding: '1rem' }}>Status</th>
              <th style={{ padding: '1rem' }}>Date</th>
            </tr>
          </thead>
          <tbody>
            {leads.map(lead => (
              <tr key={lead.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.02)', fontSize: '0.9rem' }}>
                <td style={{ padding: '1.2rem', fontWeight: 600 }}>{lead.name}</td>
                <td style={{ padding: '1.2rem' }}>{lead.intent}</td>
                <td style={{ padding: '1.2rem', opacity: 0.8 }}>{lead.phone}</td>
                <td style={{ padding: '1.2rem' }}>
                    <span style={{ 
                        background: lead.status === 'New' ? 'hsla(var(--nh-gold), 0.1)' : 'rgba(255,255,255,0.05)',
                        color: lead.status === 'New' ? 'hsl(var(--nh-gold))' : 'white',
                        padding: '0.2rem 0.6rem',
                        borderRadius: '4px',
                        fontSize: '0.7rem',
                        fontWeight: 700
                    }}>
                        {lead.status}
                    </span>
                </td>
                <td style={{ padding: '1.2rem', opacity: 0.5 }}>{lead.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
