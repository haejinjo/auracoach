import { supabase } from './supabase';

// Minimal auth callback output
export interface User {
  id: string; // uuid matching auth user id
  timezone?: string;
  created_at: string;
}

// Represents DB table "user_profiles"
export interface UserProfile {
  id: string; // uuid matching auth user id
  created_at: string;
  updated_at: string | null;
  display_name: string;
  onboarding_step: number;
  user_timezone: string | null;
}

// Get timezone
export function getUserTimezone(): string {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
  } catch {
    return 'UTC';
  }
}

// Check if user profile exists
export async function checkUserProfileExists(userId: string): Promise<boolean> {
  try {
    const { data, error } = await supabase
      .from('user_profiles')
      .select('id')
      .eq('id', userId)
      .single();

    return !error && !!data;
  } catch {
    return false;
  }
}

// export async function createUserProfile(userId: string, email: string): Promise<{ success: boolean; error?: string }> {
//   try {
//     const { error } = await supabase
//       .from('user_profiles')
//       .insert({
//         id: userId,
//         display_name: email,
//         user_timezone: getUserTimezone(),
//         onboarding_step: 0
//       });

//     return error ? { success: false, error: error.message } : { success: true };
//   } catch (error) {
//     return { success: false, error: 'Failed to create user profile' };
//   }
// }

export async function updateUserTimezone(userId: string): Promise<{ success: boolean; error?: string }> {
  try {
    const userTimezone = getUserTimezone();
    if (!userTimezone) { return { success: false, error: 'Client failed to derive user timezone' }; }

    // Always update user timezone even if it is the same
    const { error } = await supabase
      .from('user_profiles')
      .update({
        user_timezone: userTimezone,
      })
      .eq('id', userId);

    return error ? { success: false, error: error.message } : { success: true };
  } catch (error) {
    return { success: false, error: 'Failed to update user timezone' };
  }
}

export async function sendMagicLink(email: string): Promise<{ success: boolean; error?: string }> {
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: { emailRedirectTo: 'auracoach://auth/callback' }
  });

  return error ? { success: false, error: error.message } : { success: true };
}

export async function handleAuthCallback(url: string): Promise<{ success: boolean; user?: any;}> {
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

    // Check if user profile exists, create if new user
    const profileExists = await checkUserProfileExists(sessionData.user.id);
    if (!profileExists) {
      throw new Error('Backend failed to auto-create user profile on new signup');
      // const profileResult = await createUserProfile(sessionData.user.id, sessionData.user.email);
      // if (!profileResult.success) {
      //   console.error('Failed to create user profile:', profileResult.error);
      // }
    } else {
      // Update timezone for existing user
      const timezoneResult = await updateUserTimezone(sessionData.user.id);
      if (!timezoneResult.success) {
        console.error('Failed to update user timezone:', timezoneResult.error);
      }
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