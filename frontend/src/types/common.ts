export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
}

export interface FormState {
  email: string;
  loading: boolean;
  error: string | null;
}

export interface FocusState {
  isFocused: boolean;
}
