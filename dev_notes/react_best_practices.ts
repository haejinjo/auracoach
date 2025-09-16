// Use functional components with proper TypeScript interfaces
interface ComponentProps {
  // Explicit prop types
  onSubmit: (email: string) => void;
  loading?: boolean;
}

// Use React.FC pattern with proper typing
const LoginForm: React.FC<ComponentProps> = ({ onSubmit, loading = false }) => {
  // Component implementation
};

// Use React.memo for pure components like LoginForm
// Implement useCallback for event handlers like handleSubmit
// Use useMemo for expensive computations