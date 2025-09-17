import { useState, useCallback, useEffect } from 'react';
import { Background } from './components/layout/Background';
import { Container } from './components/layout/Container';
import { LoginForm } from './components/LoginForm';
import { Button } from './components/ui';
import { type User, sendMagicLink, handleAuthCallback } from './lib/auth';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backgroundBlurred, setBackgroundBlurred] = useState(false);
  const [magicLinkSent, setMagicLinkSent] = useState(false);

  const handleSubmit = useCallback(async (email: string) => {
    setLoading(true);
    setError(null);

    try {
      const result = await sendMagicLink(email);

      if (result.success) {
        setMagicLinkSent(true);
      } else {
        setError(result.error || 'Failed to send magic link');
      }
    } catch (err) {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  // Handle Electron auth callbacks
  useEffect(() => {
    if (window.electronAPI) {
      const handleCallback = async (url: string) => {
        setLoading(true);
        const result = await handleAuthCallback(url);

        if (result.success && result.user) {
          setUser(result.user);
          setMagicLinkSent(false);
          console.log('Timezone:', result.user.timezone);
        } else {
          setError('Authentication failed');
        }
        setLoading(false);
      };

      window.electronAPI.onAuthCallback(handleCallback);
      return () => window.electronAPI?.removeAuthCallback();
    }
  }, []);

  // Logged in state
  if (user) {
    return (
      <div className="min-h-screen bg-auracoach-bg text-auracoach-text-primary font-calibre relative overflow-hidden">
        <Background isBlurred={false} />
        <Container center>
          <div className="text-center space-y-4">
            <h1 className="text-2xl font-semibold">Welcome to AuraCoach!</h1>
            <div className="space-y-2">
              <p>✅ Authentication successful</p>
              <p>🌍 Timezone: {user.timezone}</p>
              <p>📅 Joined: {new Date(user.created_at).toLocaleDateString()}</p>
              {window.electronAPI && <p>🖥️ Running in Electron</p>}
            </div>
            <Button onClick={() => { setUser(null); setMagicLinkSent(false); setError(null); }}>
              Sign Out
            </Button>
          </div>
        </Container>
      </div>
    );
  }

  // Magic link sent
  if (magicLinkSent) {
    return (
      <div className="min-h-screen bg-auracoach-bg text-auracoach-text-primary font-calibre relative overflow-hidden">
        <Background isBlurred={backgroundBlurred} />
        <Container center>
          <div className="text-center space-y-4">
            <h1 className="text-xl font-semibold">Check Your Email</h1>
            <p>Click the magic link to sign in!</p>
            <p className="text-sm opacity-70">
              {window.electronAPI ? 'Link will open AuraCoach automatically' : 'Return here after clicking'}
            </p>
            <Button onClick={() => { setMagicLinkSent(false); setError(null); }}>
              Back to Login
            </Button>
          </div>
        </Container>
      </div>
    );
  }

  // Login form (existing)
  return (
    <div className="min-h-screen bg-auracoach-bg text-auracoach-text-primary font-calibre relative overflow-hidden">
      <Background isBlurred={backgroundBlurred} />
      <Button variant="close">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M6.75 6.75L17.25 17.25M17.25 6.75L6.75 17.25" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </Button>
      <Container center>
        <LoginForm onSubmit={handleSubmit} loading={loading} error={error} onFocusChange={setBackgroundBlurred} />
      </Container>
    </div>
  );
}

export default App;