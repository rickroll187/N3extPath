// File: web/src/components/ui/LegendaryCard.tsx
/**
 * 🎴🎸 N3EXTPATH - LEGENDARY CARD COMPONENT 🎸🎴
 * Professional UI card with Swiss precision
 * Built: 2025-08-06 13:34:22 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { forwardRef, HTMLAttributes, ReactNode } from 'react';
import { motion, MotionProps } from 'framer-motion';
import { cn } from '@/utils/cn';

// =====================================
// 🎴 LEGENDARY CARD TYPES 🎴
// =====================================

export interface LegendaryCardProps extends 
  Omit<HTMLAttributes<HTMLDivElement>, 'children'>,
  Omit<MotionProps, 'children'> {
  
  // Visual variants
  variant?: 
    | 'default' 
    | 'elevated' 
    | 'bordered' 
    | 'glass' 
    | 'legendary' 
    | 'founder' 
    | 'swiss-precision' 
    | 'code-bro-energy';
  
  // Size variants
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  
  // Padding variants
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  
  // Special features
  hover?: boolean;
  glow?: boolean;
  gradient?: boolean;
  interactive?: boolean;
  loading?: boolean;
  
  // Header and footer
  header?: ReactNode;
  footer?: ReactNode;
  
  // Content
  children?: ReactNode;
}

// =====================================
// 🎸 LEGENDARY CARD COMPONENT 🎸
// =====================================

export const LegendaryCard = forwardRef<HTMLDivElement, LegendaryCardProps>(
  (
    {
      variant = 'default',
      size = 'md',
      padding = 'md',
      hover = false,
      glow = false,
      gradient = false,
      interactive = false,
      loading = false,
      header,
      footer,
      children,
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
      'relative overflow-hidden',
      'transition-all duration-300 ease-in-out',
      interactive && 'cursor-pointer select-none',
    ];
    
    // Size styles
    const sizeStyles = {
      sm: 'max-w-sm',
      md: 'max-w-md',
      lg: 'max-w-lg',
      xl: 'max-w-xl',
      full: 'w-full',
    };
    
    // Padding styles
    const paddingStyles = {
      none: 'p-0',
      sm: 'p-3',
      md: 'p-4',
      lg: 'p-6',
      xl: 'p-8',
    };
    
    // Variant styles
    const variantStyles = {
      default: [
        'bg-white border border-gray-200',
        'shadow-sm',
        hover && 'hover:shadow-md hover:border-gray-300',
      ],
      elevated: [
        'bg-white border border-gray-200',
        'shadow-lg',
        hover && 'hover:shadow-xl hover:border-gray-300',
      ],
      bordered: [
        'bg-white border-2 border-gray-300',
        hover && 'hover:border-gray-400 hover:shadow-sm',
      ],
      glass: [
        'bg-white/80 backdrop-blur-sm border border-white/20',
        'shadow-lg',
        hover && 'hover:bg-white/90 hover:shadow-xl',
      ],
      legendary: [
        'bg-gradient-to-br from-yellow-50 to-orange-50',
        'border-2 border-yellow-300',
        'shadow-lg shadow-yellow-500/20',
        hover && 'hover:shadow-xl hover:shadow-yellow-500/30 hover:border-yellow-400',
        glow && 'shadow-2xl shadow-yellow-500/40',
      ],
      founder: [
        'bg-gradient-to-br from-yellow-100 via-orange-50 to-yellow-100',
        'border-3 border-yellow-400',
        'shadow-2xl shadow-yellow-500/30',
        'ring-1 ring-yellow-300',
        hover && 'hover:shadow-3xl hover:shadow-yellow-500/50 hover:ring-2 hover:ring-yellow-400',
        'transform transition-transform',
        interactive && 'hover:scale-[1.02] active:scale-[0.98]',
      ],
      'swiss-precision': [
        'bg-gradient-to-br from-red-50 to-pink-50',
        'border-2 border-red-300',
        'shadow-lg shadow-red-500/20',
        hover && 'hover:shadow-xl hover:shadow-red-500/30 hover:border-red-400',
        glow && 'shadow-2xl shadow-red-500/40',
      ],
      'code-bro-energy': [
        'bg-gradient-to-br from-purple-50 to-indigo-50',
        'border-2 border-purple-300',
        'shadow-lg shadow-purple-500/20',
        hover && 'hover:shadow-xl hover:shadow-purple-500/30 hover:border-purple-400',
        glow && 'shadow-2xl shadow-purple-500/40',
      ],
    };
    
    // Radius styles
    const radiusStyles = {
      sm: 'rounded-lg',
      md: 'rounded-xl',
      lg: 'rounded-2xl',
      xl: 'rounded-3xl',
      full: 'rounded-3xl',
    };
    
    // =====================================
    // 🎸 LEGENDARY CLICK HANDLER 🎸
    // =====================================
    
    const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
      if (!interactive || loading) return;
      
      // Add legendary click effects
      if (variant === 'founder') {
        console.log('👑 RICKROLL187 FOUNDER CARD CLICKED! LEGENDARY INTERACTION!');
      } else if (variant === 'legendary') {
        console.log('🎸 LEGENDARY CARD ACTIVATED WITH CODE BRO ENERGY!');
      }
      
      onClick?.(e);
    };
    
    // =====================================
    // 🎸 RENDER LEGENDARY CARD 🎸
    // =====================================
    
    return (
      <motion.div
        ref={ref}
        className={cn(
          baseStyles,
          sizeStyles[size],
          variantStyles[variant],
          radiusStyles[size],
          !header && !footer && paddingStyles[padding],
          className
        )}
        onClick={handleClick}
        whileHover={interactive && !loading ? { y: -2 } : undefined}
        whileTap={interactive && !loading ? { scale: 0.98 } : undefined}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        {...props}
      >
        {/* Loading Overlay */}
        {loading && (
          <motion.div
            className="absolute inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-10 rounded-inherit"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
              <span className="text-sm font-medium text-gray-600">Loading...</span>
            </div>
          </motion.div>
        )}
        
        {/* Header */}
        {header && (
          <div className={cn(
            'border-b border-gray-200 bg-gray-50/50',
            padding === 'none' ? 'p-4' : 
            padding === 'sm' ? 'p-3' : 
            padding === 'md' ? 'p-4' : 
            padding === 'lg' ? 'px-6 py-4' : 
            'px-8 py-5',
            variant === 'legendary' && 'bg-yellow-50/50 border-yellow-200',
            variant === 'founder' && 'bg-gradient-to-r from-yellow-100 to-orange-100 border-yellow-300',
            variant === 'swiss-precision' && 'bg-red-50/50 border-red-200',
            variant === 'code-bro-energy' && 'bg-purple-50/50 border-purple-200'
          )}>
            {header}
          </div>
        )}
        
        {/* Main Content */}
        <div className={cn(
          'relative',
          (header || footer) && paddingStyles[padding]
        )}>
          {children}
        </div>
        
        {/* Footer */}
        {footer && (
          <div className={cn(
            'border-t border-gray-200 bg-gray-50/50',
            padding === 'none' ? 'p-4' : 
            padding === 'sm' ? 'p-3' : 
            padding === 'md' ? 'p-4' : 
            padding === 'lg' ? 'px-6 py-4' : 
            'px-8 py-5',
            variant === 'legendary' && 'bg-yellow-50/50 border-yellow-200',
            variant === 'founder' && 'bg-gradient-to-r from-yellow-100 to-orange-100 border-yellow-300',
            variant === 'swiss-precision' && 'bg-red-50/50 border-red-200',
            variant === 'code-bro-energy' && 'bg-purple-50/50 border-purple-200'
          )}>
            {footer}
          </div>
        )}
        
        {/* Legendary Glow Effect */}
        {variant === 'founder' && (
          <div className="absolute inset-0 rounded-inherit opacity-0 hover:opacity-10 transition-opacity duration-500 bg-gradient-to-br from-yellow-400 via-orange-500 to-yellow-600 pointer-events-none" />
        )}
        
        {/* Interactive Ripple Effect */}
        {interactive && variant === 'founder' && (
          <div className="absolute inset-0 rounded-inherit overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-yellow-400/0 via-yellow-400/20 to-yellow-400/0 transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-out" />
          </div>
        )}
        
        {/* Gradient Overlay for Special Variants */}
        {gradient && (variant === 'legendary' || variant === 'founder') && (
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-yellow-400 to-transparent opacity-60" />
        )}
        
        {gradient && variant === 'swiss-precision' && (
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-red-500 to-transparent opacity-60" />
        )}
        
        {gradient && variant === 'code-bro-energy' && (
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-purple-500 to-transparent opacity-60" />
        )}
      </motion.div>
    );
  }
);

LegendaryCard.displayName = 'LegendaryCard';

console.log('🎸🎸🎸 LEGENDARY CARD COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Card component completed at: 2025-08-06 13:34:22 UTC`);
console.log('🎴 Card UI: SWISS PRECISION');
console.log('👑 RICKROLL187 founder variant: LEGENDARY');
console.log('🎸 Interactive effects: MAXIMUM ENGAGEMENT');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
