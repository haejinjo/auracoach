export interface LoginFormProps {
  onSubmit: (email: string) => Promise<void>;
  loading?: boolean;
  error?: string | null;
  className?: string;
  onFocusChange?: (focused: boolean) => void; // Add this
}