// File: web/src/components/ui/LegendaryButton.tsx
/**
 * 🔘🎸 N3EXTPATH - LEGENDARY BUTTON COMPONENT 🎸🔘
 * Professional UI button with Swiss precision
 * Built: 2025-08-06 13:34:22 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { forwardRef, ButtonHTMLAttributes, ReactNode } from 'react';
import { motion, MotionProps } from 'framer-motion';
import { LucideIcon } from 'lucide-react';
import { cn } from '@/utils/cn';

// =====================================
// 🔘 LEGENDARY BUTTON TYPES 🔘
// =====================================

export interface LegendaryButtonProps extends 
  Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'size'>,
  Omit<MotionProps, 'children'> {
  
  // Visual variants
  variant?: 
    | 'primary' 
    | 'secondary' 
    | 'outline' 
    | 'ghost' 
    | 'legendary' 
    | 'founder' 
    | 'swiss-precision' 
    | 'code-bro-energy'
    | 'success' 
    | 'warning' 
    | 'error' 
    | 'info';
  
  // Size variants
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'legendary';
  
  // Loading state
  isLoading?: boolean;
  loadingText?: string;
  
  // Icon support
  leftIcon?: LucideIcon;
  rightIcon?: LucideIcon;
  iconOnly?: boolean;
  
  // Special features
  pulse?: boolean;
  bounce?: boolean;
  glow?: boolean;
  gradient?: boolean;
  
  // Content
  children?: ReactNode;
  
  // Accessibility
  'aria-label'?: string;
}

// =====================================
// 🎸 LEGENDARY BUTTON COMPONENT 🎸
// =====================================

export const LegendaryButton = forwardRef<HTMLButtonElement, LegendaryButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      loadingText = 'Loading...',
      leftIcon: LeftIcon,
      rightIcon: RightIcon,
      iconOnly = false,
      pulse = false,
      bounce = false,
      glow = false,
      gradient = false,
      children,
      disabled,
      className,
      onClick,
      ...props
    },
    ref
  ) => {
    
    // =====================================
    // 🎨 LEGENDARY STYLING 🎨
    // =====================================
    
    const baseStyles = [
      // Base button styles
      'relative inline-flex items-center justify-center',
      'font-medium transition-all duration-200 ease-in-out',
      'focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
      'disabled:pointer-events-none disabled:opacity-50',
      'select-none whitespace-nowrap',
    ];
    
    // Size styles
    const sizeStyles = {
      xs: 'px-2 py-1 text-xs h-6 min-w-[1.5rem] gap-1',
      sm: 'px-3 py-1.5 text-sm h-8 min-w-[2rem] gap-1.5',
      md: 'px-4 py-2 text-sm h-10 min-w-[2.5rem] gap-2',
      lg: 'px-6 py-2.5 text-base h-12 min-w-[3rem] gap-2.5',
      xl: 'px-8 py-3 text-lg h-14 min-w-[3.5rem] gap-3',
      legendary: 'px-12 py-4 text-xl h-16 min-w-[4rem] gap-4 font-bold',
    };
    
    // Variant styles
    const variantStyles = {
      primary: [
        'bg-blue-600 text-white border border-blue-600',
        'hover:bg-blue-700 hover:border-blue-700',
        'focus-visible:ring-blue-500',
        'shadow-sm hover:shadow-md',
      ],
      secondary: [
        'bg-gray-100 text-gray-900 border border-gray-300',
        'hover:bg-gray-200 hover:border-gray-400',
        'focus-visible:ring-gray-500',
        'shadow-sm hover:shadow-md',
      ],
      outline: [
        'bg-transparent text-gray-700 border border-gray-300',
        'hover:bg-gray-50 hover:border-gray-400',
        'focus-visible:ring-gray-500',
      ],
      ghost: [
        'bg-transparent text-gray-700 border border-transparent',
        'hover:bg-gray-100 hover:text-gray-900',
        'focus-visible:ring-gray-500',
      ],
      legendary: [
        'bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600',
        'text-gray-900 border border-yellow-500',
        'hover:from-yellow-500 hover:via-yellow-600 hover:to-yellow-700',
        'focus-visible:ring-yellow-500',
        'shadow-lg hover:shadow-xl',
        'font-bold',
        gradient && 'animate-gradient-x bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600 bg-[length:200%_100%]',
      ],
      founder: [
        'bg-gradient-to-r from-yellow-400 via-orange-500 to-yellow-600',
        'text-gray-900 border-2 border-yellow-500',
        'hover:from-yellow-500 hover:via-orange-600 hover:to-yellow-700',
        'focus-visible:ring-yellow-500 focus-visible:ring-offset-2',
        'shadow-xl hover:shadow-2xl',
        'font-black text-shadow',
        'transform hover:scale-105 active:scale-95',
      ],
      'swiss-precision': [
        'bg-gradient-to-r from-red-600 via-red-700 to-red-800',
        'text-white border border-red-600',
        'hover:from-red-700 hover:via-red-800 hover:to-red-900',
        'focus-visible:ring-red-500',
        'shadow-lg hover:shadow-xl',
        'font-semibold',
      ],
      'code-bro-energy': [
        'bg-gradient-to-r from-purple-600 via-purple-700 to-purple-800',
        'text-white border border-purple-600',
        'hover:from-purple-700 hover:via-purple-800 hover:to-purple-900',
        'focus-visible:ring-purple-500',
        'shadow-lg hover:shadow-xl',
        'font-semibold',
      ],
      success: [
        'bg-green-600 text-white border border-green-600',
        'hover:bg-green-700 hover:border-green-700',
        'focus-visible:ring-green-500',
        'shadow-sm hover:shadow-md',
      ],
      warning: [
        'bg-orange-600 text-white border border-orange-600',
        'hover:bg-orange-700 hover:border-orange-700',
        'focus-visible:ring-orange-500',
        'shadow-sm hover:shadow-md',
      ],
      error: [
        'bg-red-600 text-white border border-red-600',
        'hover:bg-red-700 hover:border-red-700',
        'focus-visible:ring-red-500',
        'shadow-sm hover:shadow-md',
      ],
      info: [
        'bg-blue-600 text-white border border-blue-600',
        'hover:bg-blue-700 hover:border-blue-700',
        'focus-visible:ring-blue-500',
        'shadow-sm hover:shadow-md',
      ],
    };
    
    // Radius styles
    const radiusStyles = {
      xs: 'rounded',
      sm: 'rounded-md',
      md: 'rounded-lg',
      lg: 'rounded-xl',
      xl: 'rounded-2xl',
      legendary: 'rounded-3xl',
    };
    
    // Animation classes
    const animationClasses = [
      pulse && 'animate-pulse',
      bounce && 'animate-bounce',
      glow && `shadow-${variant === 'legendary' || variant === 'founder' ? 'yellow' : variant === 'swiss-precision' ? 'red' : variant === 'code-bro-energy' ? 'purple' : 'blue'}-500/50 shadow-2xl`,
    ].filter(Boolean);
    
    // Icon size mapping
    const iconSizes = {
      xs: 12,
      sm: 14,
      md: 16,
      lg: 18,
      xl: 20,
      legendary: 24,
    };
    
    // =====================================
    // 🎸 LEGENDARY CLICK HANDLER 🎸
    // =====================================
    
    const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
      if (isLoading || disabled) return;
      
      // Add legendary click effects for special variants
      if (variant === 'founder') {
        console.log('👑 RICKROLL187 FOUNDER BUTTON CLICKED! WE ARE CODE BROS!');
      } else if (variant === 'legendary') {
        console.log('🎸 LEGENDARY BUTTON ACTIVATED WITH CODE BRO ENERGY!');
      }
      
      onClick?.(e);
    };
    
    // =====================================
    // 🎸 RENDER LEGENDARY BUTTON 🎸
    // =====================================
    
    return (
      <motion.button
        ref={ref}
        className={cn(
          baseStyles,
          sizeStyles[size],
          variantStyles[variant],
          radiusStyles[size],
          animationClasses,
          className
        )}
        disabled={disabled || isLoading}
        onClick={handleClick}
        whileHover={!disabled && !isLoading ? { scale: 1.02 } : undefined}
        whileTap={!disabled && !isLoading ? { scale: 0.98 } : undefined}
        {...props}
      >
        {/* Loading Spinner */}
        {isLoading && (
          <motion.div
            className={cn(
              'absolute inset-0 flex items-center justify-center',
              'bg-current opacity-10 rounded-inherit'
            )}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div
              className={cn(
                'border-2 border-current border-t-transparent rounded-full animate-spin',
                size === 'xs' ? 'w-3 h-3' :
                size === 'sm' ? 'w-4 h-4' :
                size === 'md' ? 'w-5 h-5' :
                size === 'lg' ? 'w-6 h-6' :
                size === 'xl' ? 'w-7 h-7' :
                'w-8 h-8'
              )}
            />
          </motion.div>
        )}
        
        {/* Left Icon */}
        {LeftIcon && !isLoading && (
          <LeftIcon 
            size={iconSizes[size]} 
            className={cn(
              'flex-shrink-0',
              iconOnly && 'mx-0',
              children && 'mr-1'
            )}
          />
        )}
        
        {/* Button Content */}
        {!iconOnly && (
          <span className={cn(
            'flex-1 truncate',
            isLoading && 'opacity-0'
          )}>
            {isLoading ? loadingText : children}
          </span>
        )}
        
        {/* Right Icon */}
        {RightIcon && !isLoading && (
          <RightIcon 
            size={iconSizes[size]} 
            className={cn(
              'flex-shrink-0',
              iconOnly && 'mx-0',
              children && 'ml-1'
            )}
          />
        )}
        
        {/* Legendary Glow Effect */}
        {(variant === 'founder' || variant === 'legendary') && (
          <div className="absolute inset-0 rounded-inherit opacity-0 hover:opacity-20 transition-opacity duration-300 bg-gradient-to-r from-yellow-400 via-orange-500 to-yellow-600 pointer-events-none" />
        )}
        
        {/* Swiss Precision Effect */}
        {variant === 'swiss-precision' && (
          <div className="absolute inset-0 rounded-inherit opacity-0 hover:opacity-20 transition-opacity duration-300 bg-gradient-to-r from-red-500 to-red-700 pointer-events-none" />
        )}
        
        {/* Code Bro Energy Effect */}
        {variant === 'code-bro-energy' && (
          <div className="absolute inset-0 rounded-inherit opacity-0 hover:opacity-20 transition-opacity duration-300 bg-gradient-to-r from-purple-500 to-purple-700 pointer-events-none" />
        )}
      </motion.button>
    );
  }
);

LegendaryButton.displayName = 'LegendaryButton';

console.log('🎸🎸🎸 LEGENDARY BUTTON COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Button component completed at: 2025-08-06 13:34:22 UTC`);
console.log('🔘 Button UI: SWISS PRECISION');
console.log('👑 RICKROLL187 founder variant: LEGENDARY');
console.log('🎸 Code bro energy effects: MAXIMUM POWER');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
