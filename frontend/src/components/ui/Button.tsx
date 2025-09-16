import React from 'react';
import { cn } from '../../utils/cn';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'submit' | 'close';
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  variant = 'default', 
  loading = false, 
  className, 
  disabled,
  ...props 
}) => {
  const baseClasses = 'transition-all duration-200 ease-out focus:outline-none';
  
  const variants = {
    default: 'bg-white/[0.06] border border-white/[0.08] backdrop-blur-sm rounded-lg px-4 py-3 text-white/90 hover:bg-white/[0.08] hover:border-white/[0.12]',
    submit: 'absolute right-2.5 top-1/2 -translate-y-1/2 w-6 h-6 bg-transparent border-0 cursor-pointer flex items-center justify-center',
    close: 'absolute top-5 right-5 bg-transparent border-0 text-white/90 cursor-pointer p-2 rounded hover:bg-white/[0.06] transition-colors duration-200',
  };

  return (
    <button
      className={cn(
        baseClasses,
        variants[variant],
        (disabled || loading) && 'opacity-50 cursor-not-allowed',
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <div className="animate-spin w-4 h-4 border-2 border-white/20 border-t-white/80 rounded-full" />
      ) : (
        children
      )}
    </button>
  );
};