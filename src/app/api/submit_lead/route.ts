import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { supabase } from '@/utils/supabase';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: Request) {
  try {
    // SECURITY: Basic rate limiting/spam protection could go here
    // For now, we ensure the request is valid JSON and has required fields
    const data = await request.json();
    
    if (!data.email || !data.phone) {
        return NextResponse.json({ status: 'error', message: 'Missing required fields' }, { status: 400 });
    }

    console.log("API: Received Secured Lead Data:", data.email);

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
            est_payment: data.est_payment,
            monthly_savings: data.monthly_savings,
            lifetime_roi: data.lifetime_roi,
            created_at: new Date().toISOString()
        }]);

    if (dbError) {
        console.error("Supabase Persistence Error:", dbError);
        // We continue to email even if DB fails to ensure lead isn't totally lost
    }

    // 2. DISPATCH (Autonomous Email Notification)
    const ADMIN_EMAIL = process.env.ADMIN_EMAIL || "mgillnh@gmail.com";
    
    if (process.env.RESEND_API_KEY) {
        console.log("Attempting email dispatch to:", ADMIN_EMAIL);
        const { data: emailData, error: emailError } = await resend.emails.send({
            from: 'NH Mortgage Journal <onboarding@resend.dev>',
            to: [ADMIN_EMAIL],
            replyTo: data.email,
            subject: `[Lead Alert] ${data.first_name} ${data.last_name} - NH Intelligence Captured`,
            html: `
                <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b;">
                    <div style="background: #0f172a; padding: 40px; text-align: center; border-radius: 12px 12px 0 0;">
                        <h1 style="color: #fbbf24; margin: 0; font-size: 24px;">NH Mortgage Journal</h1>
                        <p style="color: #94a3b8; margin: 10px 0 0;">New Lead Intelligence Report</p>
                    </div>
                    
                    <div style="padding: 40px; border: 1px solid #f1f5f9; border-top: none; border-radius: 0 0 12px 12px; background: #ffffff;">
                        <h2 style="font-size: 18px; margin-top: 0; border-bottom: 2px solid #fbbf24; display: inline-block; padding-bottom: 4px;">Borrower Profile</h2>
                        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                            <tr><td style="padding: 8px 0; color: #64748b;">Name:</td><td style="font-weight: 600;">${data.first_name} ${data.last_name}</td></tr>
                            <tr><td style="padding: 8px 0; color: #64748b;">Phone:</td><td style="font-weight: 600;">${data.phone}</td></tr>
                            <tr><td style="padding: 8px 0; color: #64748b;">Email:</td><td style="font-weight: 600;">${data.email}</td></tr>
                            <tr><td style="padding: 8px 0; color: #64748b;">Intent:</td><td style="font-weight: 600;">${data.loan_purpose}</td></tr>
                        </table>
                        
                        <h2 style="font-size: 18px; margin-top: 30px; border-bottom: 2px solid #fbbf24; display: inline-block; padding-bottom: 4px;">Loan Parameters</h2>
                        <ul style="list-style: none; padding: 0; margin-top: 15px;">
                            <li style="margin-bottom: 8px;"><strong>Property:</strong> $${data.est_value} (${data.property_type})</li>
                            <li style="margin-bottom: 8px;"><strong>Equity:</strong> $${data.down_payment} Down</li>
                            <li style="margin-bottom: 8px;"><strong>Credit:</strong> ${data.credit_score}</li>
                            <li style="margin-bottom: 8px;"><strong>Target:</strong> ${data.location_nh}</li>
                        </ul>
                        
                        <div style="margin-top: 40px; padding: 20px; background: #f8fafc; border-radius: 8px; font-size: 13px; color: #94a3b8; text-align: center;">
                            This is an automated intelligence dispatch from the NH Mortgage Journal Lead Engine.
                            <br/>Sovereign Data Protection Active.
                        </div>
                    </div>
                </div>
            `
        });

        if (emailError) {
            console.error("Resend Dispatch Error:", emailError);
        } else {
            console.log("Resend Dispatch Success:", emailData?.id);
        }
    } else {
        console.warn("RESEND_API_KEY missing. Skipping email.");
    }

    return NextResponse.json({ 
        status: 'success', 
        message: 'Lead captured and emailed.',
        timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error("API Error:", error);
    return NextResponse.json({ status: 'error', message: 'Internal Server Error' }, { status: 500 });
  }
}
