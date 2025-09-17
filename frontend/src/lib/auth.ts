import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAPIKey = import.meta.env.VITE_SUPABASE_DEFAULT_KEY;

if (!supabaseUrl || !supabaseAPIKey) {
  throw new Error('Missing Supabase environment variables');
}
const supabase = createClient(
  supabaseUrl,
  supabaseAPIKey
);

// Types (minimal)
export interface User {
  id: string;
  timezone?: string;
  created_at: string;
}

// Get timezone
export function getUserTimezone(): string {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
  } catch {
    return 'UTC';
  }
}

// Send magic link
export async function sendMagicLink(email: string): Promise<{ success: boolean; error?: string }> {
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: { emailRedirectTo: 'auracoach://auth/callback' }
  });

  return error ? { success: false, error: error.message } : { success: true };
}

// Handle auth callback
export async function handleAuthCallback(url: string): Promise<{ success: boolean; user?: User;}> {
  try {
    const fragment = url.split('#')[1] || url.split('?')[1] || '';
    const params = new URLSearchParams(fragment);
    const accessToken = params.get('access_token');
    const refreshToken = params.get('refresh_token');

    if (!accessToken) {
      throw new Error('No access token');
    }

    const { data: sessionData, error: sessionError } = await supabase.auth.setSession({
      access_token: accessToken,
      refresh_token: refreshToken || ''
    });

    if (sessionError || !sessionData.user?.email) {
      throw new Error('Failed to establish session');
    }

    // Return user info on success
    return {
      success: true,
      user: {
        id: sessionData.user.id,
        timezone: getUserTimezone(),
        created_at: sessionData.user.created_at
      }
    };
  } catch (error) {
    console.error('Auth callback error:', error);
    return { success: false };
  }
}