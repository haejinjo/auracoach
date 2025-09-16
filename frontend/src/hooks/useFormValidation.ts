import { useState, useCallback } from 'react';

interface UseFormValidationProps {
  initialValues: Record<string, string>;
  validate?: (values: Record<string, string>) => Record<string, string>;
}

interface UseFormValidationReturn {
  values: Record<string, string>;
  errors: Record<string, string>;
  handleChange: (name: string, value: string) => void;
  handleSubmit: (onSubmit: (values: Record<string, string>) => void) => (e: React.FormEvent) => void;
  isValid: boolean;
}

export const useFormValidation = ({ 
  initialValues, 
  validate 
}: UseFormValidationProps): UseFormValidationReturn => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = useCallback((name: string, value: string) => {
    setValues(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  }, [errors]);

  const handleSubmit = useCallback((onSubmit: (values: Record<string, string>) => void) => {
    return (e: React.FormEvent) => {
      e.preventDefault();
      
      if (validate) {
        const newErrors = validate(values);
        setErrors(newErrors);
        
        if (Object.keys(newErrors).length === 0) {
          onSubmit(values);
        }
      } else {
        onSubmit(values);
      }
    };
  }, [values, validate]);

  const isValid = Object.keys(errors).length === 0 && 
    Object.values(values).every(value => value.trim() !== '');

  return {
    values,
    errors,
    handleChange,
    handleSubmit,
    isValid,
  };
};
