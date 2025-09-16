import React from 'react';
import { cn } from '../../utils/cn';
import type { BaseComponentProps } from '../../types/common';

interface ContainerProps extends BaseComponentProps {
  center?: boolean;
}

export const Container: React.FC<ContainerProps> = ({ 
  children, 
  center = false, 
  className 
}) => {
  return (
    <div 
      className={cn(
        'min-h-screen',
        center && 'flex items-center justify-center',
        className
      )}
    >
      {children}
    </div>
  );
};
