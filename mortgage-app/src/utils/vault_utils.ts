import fs from 'fs';
import path from 'path';

/**
 * Vault Utilities for Sovereign Lead Persistence
 * Saves lead intelligence to the local Obsidian vault for private tracking.
 */

const VAULT_LEADS_PATH = path.join(process.cwd(), '..', 'tru', 'Leads');

export async function saveLeadToVault(data: any) {
    try {
        // Ensure Leads directory exists
        if (!fs.existsSync(VAULT_LEADS_PATH)) {
            fs.mkdirSync(VAULT_LEADS_PATH, { recursive: true });
        }

        const filename = `${new Date().toISOString().split('T')[0]}_${data.first_name.toLowerCase()}_${data.last_name.toLowerCase()}.md`;
        const filePath = path.join(VAULT_LEADS_PATH, filename);

        const content = `---
type: lead
status: captured
grade: ${data.grade || 'U'}
loan_purpose: ${data.loan_purpose}
property_type: ${data.property_type}
location: ${data.location_nh}
credit_score: ${data.credit_score}
est_value: ${data.est_value}
down_payment: ${data.down_payment}
monthly_savings: ${data.monthly_savings}
equity_30y: ${data.equity_30y}
utm_source: ${data.utm_source || ''}
utm_medium: ${data.utm_medium || ''}
utm_campaign: ${data.utm_campaign || ''}
captured_at: ${new Date().toISOString()}
---

# Lead Intelligence: ${data.first_name} ${data.last_name}

## 📞 Contact Information
- **Email**: ${data.email}
- **Phone**: ${data.phone}
- **NH Location**: ${data.location_nh}

## 💰 Financial Intelligence
- **Objective**: ${data.loan_purpose} (${data.property_type})
- **Credit Profile**: ${data.credit_score}
- **Loan Amount**: $${(data.est_value - data.down_payment).toLocaleString()}
- **Monthly Savings**: $${data.monthly_savings}
- **30-Year Wealth Projection**: $${data.equity_30y.toLocaleString()}

## 📊 Marketing Attribution
- **UTM Source**: ${data.utm_source || 'direct'}
- **UTM Medium**: ${data.utm_medium || 'none'}
- **UTM Campaign**: ${data.utm_campaign || 'none'}

## 🛠️ Strategy Notes
- **Grade**: ${data.grade}
- **Next Step**: Automated report dispatched. Manchester analyst review required.
`;

        fs.writeFileSync(filePath, content);
        console.log(`[VAULT] Lead saved successfully: ${filename}`);
        return true;
    } catch (error) {
        console.error("[VAULT] Persistence Error:", error);
        return false;
    }
}
