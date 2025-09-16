import React from 'react';
import { cn } from '../../utils/cn';
import type { InputProps } from './Input.types';

export const Input: React.FC<InputProps> = ({ 
  error, 
  label, 
  className, 
  ...props 
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-white/70 mb-2">
          {label}
        </label>
      )}
      <input
        className={cn(
          'w-full bg-transparent border-0 text-white caret-[rgb(71,159,250)] text-sm',
          'placeholder:text-white/50 focus:outline-none',
          'leading-[19px] px-2 py-1',
          error && 'text-red-400',
          className
        )}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-400" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};