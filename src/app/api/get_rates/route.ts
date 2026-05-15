import { NextResponse } from 'next/server';
import { supabase } from '@/utils/supabase';

export async function GET() {
  try {
    const { data, error } = await supabase
      .from('market_rates')
      .select('*')
      .order('last_verified', { ascending: false })
      .limit(1)
      .single();

    if (error) {
      console.error('Error fetching rates:', error);
      return NextResponse.json({ rate: 5.25, lender: 'NH Mortgage Co.' }, { status: 200 }); // Fallback
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json({ rate: 5.25 }, { status: 500 });
  }
}
