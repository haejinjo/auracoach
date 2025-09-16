import React from 'react';
import { cn } from '../../utils/cn';
import { ANIMATIONS } from '../../utils/constants';
import type { BaseComponentProps } from '../../types/common';

interface BackgroundProps extends BaseComponentProps {
  isBlurred?: boolean;
}

export const Background: React.FC<BackgroundProps> = ({ 
  isBlurred = false, 
  className 
}) => {
  return (
    <div 
      className={cn(
        'fixed inset-0 -z-10',
        ANIMATIONS.BLUR_TRANSITION,
        isBlurred && 'blur-sm opacity-30',
        className
      )}
    >
      <div 
        className="h-full w-full bg-gradient-to-br from-auracoach-bg/90 to-auracoach-bg/70"
        style={{
          backgroundImage: `url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><defs><pattern id='grain' width='100' height='100' patternUnits='userSpaceOnUse'><circle cx='25' cy='25' r='1' fill='%23ffffff' opacity='0.02'/><circle cx='75' cy='75' r='1' fill='%23ffffff' opacity='0.02'/><circle cx='50' cy='10' r='0.5' fill='%23ffffff' opacity='0.03'/><circle cx='90' cy='50' r='0.5' fill='%23ffffff' opacity='0.03'/></pattern></defs><rect width='100' height='100' fill='url(%23grain)'/></svg>")`
        }}
      />
    </div>
  );
};