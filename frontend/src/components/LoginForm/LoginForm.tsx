import React, { useEffect, useCallback } from 'react';
import { cn } from '../../utils/cn';
import { ANIMATIONS } from '../../utils/constants';
import { useFocusBlur } from '../../hooks/useFocusBlur';
import { useFormValidation } from '../../hooks/useFormValidation';
import { Button, Input } from '../ui';
import type { LoginFormProps } from './LoginForm.types';

const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const LoginForm: React.FC<LoginFormProps> = ({ 
  onSubmit, 
  onFocusChange,
  loading = false, 
  error, 
  className 
}) => {
  const { isFocused, focusProps } = useFocusBlur();
  
  const { values, errors, handleChange, handleSubmit } = useFormValidation({
    initialValues: { email: '' },
    validate: (vals) => {
      const errors: Record<string, string> = {};
      if (!vals.email) {
        errors.email = 'Email is required';
      } else if (!validateEmail(vals.email)) {
        errors.email = 'Please enter a valid email';
      }
      return errors;
    },
  });

  const handleFormSubmit = useCallback(async (formValues: Record<string, string>) => {
    await onSubmit(formValues.email);
  }, [onSubmit]);


    useEffect(() => {
      onFocusChange?.(isFocused);
    }, [isFocused, onFocusChange]);

  return (
    <div className={cn('flex flex-col items-center text-center', className)}>
      {/* Logo */}
      <img
        src="/aura-coach.png"
        alt="AuraCoach Logo"
        className={cn(
          'mb-2 w-60 h-60 ',
          ANIMATIONS.BLUR_TRANSITION,
          isFocused && 'opacity-30 transform scale-95'
        )}
      />

    {/* Main Heading */}
    <h1 
      className={cn(
        'gradient-text', // Use your custom class
        'text-3xl font-semibold mb-2 leading-tight',
        ANIMATIONS.BLUR_TRANSITION,
        isFocused && 'opacity-30 transform -translate-y-1'
      )}
    >
      Lock in with AuraCoach
    </h1>
      {/* Description */}
      <p 
        className={cn(
          'text-white/70 text-sm leading-relaxed mb-8 max-w-md',
          ANIMATIONS.BLUR_TRANSITION,
          isFocused && 'opacity-30 transform -translate-y-1'
        )}
      >
        Here's to you. Commit to your fitness another day.<br />Enter your email to sign up or log in.
      </p>

        <form 
          onSubmit={handleSubmit(handleFormSubmit)}
          className={cn(
            'glassmorphic', // Use your custom class
            'relative w-80 h-11 mb-7 rounded-full',
            'flex items-center px-5 cursor-text',
            ANIMATIONS.FOCUS_TRANSITION,
            isFocused && 'border-auracoach-accent/30 bg-white/[0.08]'
          )}
        >
        <Input
          type="email"
          name="email"
          placeholder="account email"
          value={values.email}
          onChange={(e) => handleChange('email', e.target.value)}
          error={errors.email}
          className="flex-1"
          {...focusProps}
        />
        
        <Button
          type="submit"
          variant="submit"
          loading={loading}
          disabled={!values.email || !!errors.email}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <circle 
              cx="12" 
              cy="12" 
              r="11.25" 
              fill="none" 
              stroke="rgba(255, 255, 255, 0.2)" 
              strokeWidth="0.5"
            />
            <path 
              d="M7.75 12H16.25M16.25 12L13 15.25M16.25 12L13 8.75" 
              stroke="#868F97" 
              strokeWidth="1.5" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            />
          </svg>
        </Button>
      </form>

      {/* Error Display */}
      {error && (
        <div className="text-red-400 text-sm mb-4" role="alert">
          {error}
        </div>
      )}
    </div>
  );
};
