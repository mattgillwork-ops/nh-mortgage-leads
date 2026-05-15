import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { supabase } from '@/utils/supabase';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: Request) {
  try {
    const data = await request.json();
    
    // Server-Side Validation
    if (!data.email || !data.phone || !data.first_name) {
        return NextResponse.json({ status: 'error', message: 'Missing required borrower intelligence' }, { status: 400 });
    }

    console.log("API: Processing Lead Intelligence:", data.email);

    // 1. PERSISTENCE (Supabase Integration)
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
            lifetime_roi: data.lifetime_roi,
            created_at: new Date().toISOString()
        }]);

    if (dbError) {
        console.error("Supabase Persistence Error:", dbError);
    }

    // 2. DISPATCH (Autonomous Email Notification)
    const ADMIN_EMAIL = process.env.ADMIN_EMAIL || "mgillnh@gmail.com";
    
    if (process.env.RESEND_API_KEY) {
        // Admin Alert
        await resend.emails.send({
            from: 'NH Mortgage Intelligence <onboarding@resend.dev>',
            to: [ADMIN_EMAIL],
            replyTo: data.email,
            subject: `[Lead Alert] ${data.first_name} ${data.last_name} - NH Intelligence Captured`,
            html: `
                <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b; background: #f8fafc; padding: 20px;">
                    <div style="background: #0f172a; padding: 40px; text-align: center; border-radius: 12px 12px 0 0;">
                        <h1 style="color: #fbbf24; margin: 0; font-size: 24px;">NH Mortgage Journal</h1>
                        <p style="color: #94a3b8; margin: 10px 0 0;">New High-Intent Lead Captured</p>
                    </div>
                    
                    <div style="padding: 40px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px; background: #ffffff;">
                        <h2 style="font-size: 18px; margin-top: 0; color: #0f172a; border-bottom: 2px solid #fbbf24; padding-bottom: 8px;">Borrower Profile</h2>
                        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                            <tr><td style="padding: 10px 0; color: #64748b;">Name:</td><td style="font-weight: 600; text-align: right;">${data.first_name} ${data.last_name}</td></tr>
                            <tr><td style="padding: 10px 0; color: #64748b;">Phone:</td><td style="font-weight: 600; text-align: right;">${data.phone}</td></tr>
                            <tr><td style="padding: 10px 0; color: #64748b;">Email:</td><td style="font-weight: 600; text-align: right;">${data.email}</td></tr>
                            <tr><td style="padding: 10px 0; color: #64748b;">Location:</td><td style="font-weight: 600; text-align: right;">${data.location_nh}</td></tr>
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
                            <div style="font-size: 28px; font-weight: 800; color: #fbbf24;">$${data.lifetime_roi.toLocaleString()}</div>
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
                    <h2>Hello ${data.first_name},</h2>
                    <p>Thank you for using the NH Mortgage Journal Intelligence Engine. We have processed your profile for <strong>${data.location_nh}</strong>.</p>
                    <div style="background: #f8fafc; padding: 30px; border-radius: 12px; border: 1px solid #fbbf24;">
                        <h3 style="margin-top: 0;">Report Summary:</h3>
                        <ul style="list-style: none; padding: 0;">
                            <li>💰 <strong>Total Monthly:</strong> $${data.total_monthly_payment}</li>
                            <li>📈 <strong>Projected Savings:</strong> $${data.monthly_savings}/mo</li>
                            <li>🏔️ <strong>30-Year Impact:</strong> $${data.lifetime_roi.toLocaleString()}</li>
                        </ul>
                    </div>
                    <p>A local mortgage analyst will reach out to you at ${data.phone} to verify these numbers and discuss next steps.</p>
                    <p>Best regards,<br/>The NH Mortgage Journal Team</p>
                </div>
            `
        });
    }

    return NextResponse.json({ 
        status: 'success', 
        message: 'Intelligence captured and reports dispatched.',
        timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error("API Error:", error);
    return NextResponse.json({ status: 'error', message: 'Internal Server Error' }, { status: 500 });
  }
}
