import { useState, useCallback } from 'react';
import { Background } from './components/layout/Background';
import { Container } from './components/layout/Container';
import { LoginForm } from './components/LoginForm';
import { Button } from './components/ui';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backgroundBlurred, setBackgroundBlurred] = useState(false);

  const handleSubmit = useCallback(async (email: string) => {
    setLoading(true);
    setError(null);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log('Email submitted:', email);
      
      // You would replace this with actual authentication logic
      // const response = await loginUser(email);
      
    } catch (err) {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="min-h-screen bg-auracoach-bg text-auracoach-text-primary font-calibre relative overflow-hidden">

      <Background isBlurred={backgroundBlurred} />
      
      {/* Close Button */}
      <Button variant="close">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path 
            d="M6.75 6.75L17.25 17.25M17.25 6.75L6.75 17.25" 
            stroke="currentColor" 
            strokeWidth="1.5" 
            strokeLinecap="round" 
            strokeLinejoin="round"
          />
        </svg>
      </Button>

      <Container center>
        <LoginForm 
          onSubmit={handleSubmit}
          loading={loading}
          error={error}
          onFocusChange={setBackgroundBlurred}
        />
      </Container>
    </div>
  );
}

export default App;