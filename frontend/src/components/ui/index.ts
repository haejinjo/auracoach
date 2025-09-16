export { Button } from './Button';
export { Input } from './Input';

// src/components/LoginForm/LoginForm.types.ts
export interface LoginFormProps {
  onSubmit: (email: string) => Promise<void>;
  loading?: boolean;
  error?: string | null;
  className?: string;
}

export interface LoginFormState {
  email: string;
  isSubmitting: boolean;
}