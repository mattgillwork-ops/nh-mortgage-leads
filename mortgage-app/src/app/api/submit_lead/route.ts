import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { supabase } from '@/utils/supabase';
import { saveLeadToVault } from '@/utils/vault_utils';

const resend = new Resend(process.env.RESEND_API_KEY);

function scoreLead(data: any): string {
    const credit = data.credit_score || '';
    const ltv = (data.est_value - data.down_payment) / data.est_value;
    
    const isExcellentCredit = credit.includes('740+');
    const isGoodCredit = credit.includes('680-739');
    
    if (isExcellentCredit && ltv <= 0.8) return 'A';
    if ((isExcellentCredit || isGoodCredit) && ltv <= 0.95) return 'B';
    return 'C';
}

export async function POST(request: Request) {
  try {
    const data = await request.json();
    
    // Server-Side Validation
    if (!data.email || !data.phone || !data.first_name) {
        return NextResponse.json({ status: 'error', message: 'Missing required borrower intelligence' }, { status: 400 });
    }

    // 1. LEAD SCORING
    const grade = scoreLead(data);
    data.grade = grade;

    console.log(`API: Processing Lead Intelligence [Grade ${grade}]:`, data.email);

    // 2. SOVEREIGN PERSISTENCE (Local Vault)
    // We attempt this first as it's the primary sovereign requirement
    const vaultSaved = await saveLeadToVault(data);

    // 3. CLOUD PERSISTENCE (Supabase Integration)
    const { error: dbError } = await supabase
        .from('leads')
        .insert([{
            first_name: data.first_name,
            last_name: data.last_name,
            email: data.email,
            phone: data.phone,
            loan_purpose: data.loan_purpose,
            property_type: data.property_type,
            est_value: data.est_value,
            down_payment: data.down_payment,
            credit_score: data.credit_score,
            location_nh: data.location_nh,
            est_payment: data.total_monthly_payment,
            monthly_savings: data.monthly_savings,
            lifetime_roi: data.equity_30y, // Using equity_30y as lifetime_roi
            grade: grade,
            vault_sync: vaultSaved,
            created_at: new Date().toISOString()
        }]);

    if (dbError) {
        console.error("Supabase Persistence Error:", dbError);
    }

    // 4. DISPATCH (Autonomous Email Notification)
    const ADMIN_EMAIL = process.env.ADMIN_EMAIL || "mgillnh@gmail.com";
    
    if (process.env.RESEND_API_KEY) {
        // Admin Alert
        await resend.emails.send({
            from: 'NH Mortgage Intelligence <onboarding@resend.dev>',
            to: [ADMIN_EMAIL],
            replyTo: data.email,
            subject: `[Lead Alert - Grade ${grade}] ${data.first_name} ${data.last_name} - NH Intelligence Captured`,
            html: `
                <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b; background: #f8fafc; padding: 20px;">
                    <div style="background: #0f172a; padding: 40px; text-align: center; border-radius: 12px 12px 0 0;">
                        <h1 style="color: #fbbf24; margin: 0; font-size: 24px;">NH Mortgage Journal</h1>
                        <p style="color: #94a3b8; margin: 10px 0 0;">New High-Intent Lead [Grade ${grade}]</p>
                    </div>
                    
                    <div style="padding: 40px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px; background: #ffffff;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                            <h2 style="font-size: 18px; margin: 0; color: #0f172a; border-bottom: 2px solid #fbbf24; padding-bottom: 8px;">Borrower Profile</h2>
                            <div style="background: #fbbf24; color: #0f172a; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 14px;">GRADE ${grade}</div>
                        </div>
                        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                            <tr><td style="padding: 10px 0; color: #64748b;">Name:</td><td style="font-weight: 600; text-align: right;">${data.first_name} ${data.last_name}</td></tr>
                            <tr><td style="padding: 10px 0; color: #64748b;">Phone:</td><td style="font-weight: 600; text-align: right;">${data.phone}</td></tr>
                            <tr><td style="padding: 10px 0; color: #64748b;">Email:</td><td style="font-weight: 600; text-align: right;">${data.email}</td></tr>
                            <tr><td style="padding: 10px 0; color: #64748b;">Location:</td><td style="font-weight: 600; text-align: right;">${data.location_nh}</td></tr>
                            <tr><td style="padding: 10px 0; color: #64748b;">Credit:</td><td style="font-weight: 600; text-align: right;">${data.credit_score}</td></tr>
                        </table>
                        
                        <h2 style="font-size: 18px; margin-top: 30px; color: #0f172a; border-bottom: 2px solid #fbbf24; padding-bottom: 8px;">Financial Breakdown</h2>
                        <div style="background: #f1f5f9; padding: 20px; border-radius: 8px; margin-top: 15px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <span style="color: #64748b;">P&I Payment:</span>
                                <strong style="float: right;">$${data.monthly_pi}</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px; clear: both;">
                                <span style="color: #64748b;">Est. NH Taxes:</span>
                                <strong style="float: right;">$${data.monthly_taxes}</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px; clear: both;">
                                <span style="color: #64748b;">Insurance:</span>
                                <strong style="float: right;">$${data.monthly_insurance}</strong>
                            </div>
                            <div style="border-top: 1px solid #cbd5e1; margin-top: 10px; padding-top: 10px; font-size: 16px; clear: both;">
                                <span>Total Payment:</span>
                                <strong style="float: right; color: #0f172a;">$${data.total_monthly_payment}</strong>
                            </div>
                        </div>

                        <div style="margin-top: 30px; text-align: center;">
                            <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">30-Year Wealth Impact</div>
                            <div style="font-size: 28px; font-weight: 800; color: #fbbf24;">$${data.equity_30y.toLocaleString()}</div>
                        </div>
                    </div>
                </div>
            `
        });

        // User Confirmation
        await resend.emails.send({
            from: 'NH Mortgage Intelligence <onboarding@resend.dev>',
            to: [data.email],
            subject: `Your NH Mortgage Intelligence Report is Ready`,
            html: `
                <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b;">
                    <h2 style="color: #0f172a;">Hello ${data.first_name},</h2>
                    <p>Thank you for using the NH Mortgage Journal Intelligence Engine. We have processed your profile for <strong>${data.location_nh}</strong>.</p>
                    <div style="background: #f8fafc; padding: 30px; border-radius: 12px; border: 1px solid #fbbf24;">
                        <h3 style="margin-top: 0; color: #0f172a;">Wealth Intelligence Summary:</h3>
                        <ul style="list-style: none; padding: 0;">
                            <li style="margin-bottom: 10px;">💰 <strong>Total Monthly:</strong> $${data.total_monthly_payment}</li>
                            <li style="margin-bottom: 10px;">📈 <strong>Projected Savings:</strong> $${data.monthly_savings}/mo</li>
                            <li style="margin-bottom: 10px;">🏔️ <strong>30-Year Wealth Impact:</strong> $${data.equity_30y.toLocaleString()}</li>
                        </ul>
                    </div>
                    <p>A senior Manchester analyst has been assigned to your profile. They will reach out to you at ${data.phone} within 24 hours to review your asset growth plan.</p>
                    <p>Best regards,<br/>The NH Mortgage Journal Team</p>
                </div>
            `
        });
    }

    return NextResponse.json({ 
        status: 'success', 
        message: 'Intelligence captured and reports dispatched.',
        grade: grade,
        timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error("API Error:", error);
    return NextResponse.json({ status: 'error', message: 'Internal Server Error' }, { status: 500 });
  }
}
