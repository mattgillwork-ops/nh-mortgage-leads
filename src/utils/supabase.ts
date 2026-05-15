import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL || 'https://placeholder.supabase.co';
const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY || 'placeholder-key';

if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SERVICE_ROLE_KEY) {
  if (process.env.NODE_ENV === 'production' && typeof window === 'undefined') {
    console.warn('Supabase credentials missing in production environment.');
  }
}

export const supabase = createClient(supabaseUrl, supabaseServiceRoleKey);
