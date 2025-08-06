// File: web/src/components/ui/LegendaryInput.tsx
/**
 * 📝🎸 N3EXTPATH - LEGENDARY INPUT COMPONENT 🎸📝
 * Professional form input with Swiss precision
 * Built: 2025-08-06 13:34:22 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { forwardRef, InputHTMLAttributes, ReactNode, useState } from 'react';
import { motion } from 'framer-motion';
import { LucideIcon, Eye, EyeOff, AlertCircle, CheckCircle } from 'lucide-react';
import { cn } from '@/utils/cn';

// =====================================
// 📝 LEGENDARY INPUT TYPES 📝
// =====================================

export interface LegendaryInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  // Visual variants
  variant?: 'default' | 'legendary' | 'founder' | 'swiss-precision' | 'code-bro-energy' | 'success' | 'warning' | 'error';
  
  // Size variants
  size?: 'sm' | 'md' | 'lg' | 'xl';
  
  // Label and description
  label?: string;
  description?: string;
  helperText?: string;
  
  // Icons
  leftIcon?: LucideIcon;
  rightIcon?: LucideIcon;
  
  // States
  isLoading?: boolean;
  error?: string;
  success?: boolean;
  
  // Features
  showPassword?: boolean;
  clearable?: boolean;
  onClear?: () => void;
  
  // Container props
  containerClassName?: string;
  labelClassName?: string;
}

// =====================================
// 🎸 LEGENDARY INPUT COMPONENT 🎸
// =====================================

export const LegendaryInput = forwardRef<HTMLInputElement, LegendaryInputProps>(
  (
    {
      variant = 'default',
      size = 'md',
      label,
      description,
      helperText,
      leftIcon: LeftIcon,
      rightIcon: RightIcon,
      isLoading = false,
      error,
      success = false,
      showPassword = false,
      clearable = false,
      onClear,
      containerClassName,
      labelClassName,
      className,
      type = 'text',
      disabled,
      value,
      ...props
    },
    ref
  ) => {
    
    const [showPasswordVisible, setShowPasswordVisible] = useState(false);
    const [isFocused, setIsFocused] = useState(false);
    
    // Determine if this is a password input
    const isPasswordType = type === 'password';
    const actualType = isPasswordType && showPasswordVisible ? 'text' : type;
    
    // Determine state
    const hasError = !!error;
    const hasValue = !!value;
    const isDisabled = disabled || isLoading;
    
    // =====================================
    // 🎨 LEGENDARY STYLING 🎨
    // =====================================
    
    const baseInputStyles = [
      'w-full transition-all duration-200 ease-in-out',
      'border rounded-lg',
      'focus:outline-none focus:ring-2 focus:ring-offset-1',
      'disabled:pointer-events-none disabled:opacity-50',
      'placeholder:text-gray-400',
    ];
    
    // Size styles
    const sizeStyles = {
      sm: 'px-3 py-2 text-sm h-9',
      md: 'px-4 py-2.5 text-sm h-10',
      lg: 'px-4 py-3 text-base h-12',
      xl: 'px-6 py-4 text-lg h-14',
    };
    
    // Icon sizes
    const iconSizes = {
      sm: 16,
      md: 18,
      lg: 20,
      xl: 22,
    };
    
    // Variant styles
    const variantStyles = {
      default: [
        'bg-white border-gray-300 text-gray-900',
        'hover:border-gray-400',
        'focus:border-blue-500 focus:ring-blue-500',
      ],
      legendary: [
        'bg-yellow-50 border-yellow-300 text-gray-900',
        'hover:border-yellow-400 hover:bg-yellow-100',
        'focus:border-yellow-500 focus:ring-yellow-500',
      ],
      founder: [
        'bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-400 text-gray-900',
        'hover:border-yellow-500 hover:from-yellow-100 hover:to-orange-100',
        'focus:border-yellow-600 focus:ring-yellow-500 focus:ring-2',
        'font-medium',
      ],
      'swiss-precision': [
        'bg-red-50 border-red-300 text-gray-900',
        'hover:border-red-400 hover:bg-red-100',
        'focus:border-red-500 focus:ring-red-500',
      ],
      'code-bro-energy': [
        'bg-purple-50 border-purple-300 text-gray-900',
        'hover:border-purple-400 hover:bg-purple-100',
        'focus:border-purple-500 focus:ring-purple-500',
      ],
      success: [
        'bg-green-50 border-green-300 text-gray-900',
        'hover:border-green-400',
        'focus:border-green-500 focus:ring-green-500',
      ],
      warning: [
        'bg-orange-50 border-orange-300 text-gray-900',
        'hover:border-orange-400',
        'focus:border-orange-500 focus:ring-orange-500',
      ],
      error: [
        'bg-red-50 border-red-300 text-gray-900',
        'hover:border-red-400',
        'focus:border-red-500 focus:ring-red-500',
      ],
    };
    
    // Apply error/success overrides
    const finalVariant = hasError ? 'error' : success ? 'success' : variant;
    
    // =====================================
    // 🎸 LEGENDARY HANDLERS 🎸
    // =====================================
    
    const handlePasswordToggle = () => {
      setShowPasswordVisible(!showPasswordVisible);
      
      if (variant === 'founder') {
        console.log('👑 RICKROLL187 FOUNDER PASSWORD TOGGLE! LEGENDARY SECURITY!');
      }
    };
    
    const handleClear = () => {
      onClear?.();
      
      if (variant === 'founder' || variant === 'legendary') {
        console.log('🎸 LEGENDARY INPUT CLEARED WITH CODE BRO ENERGY!');
      }
    };
    
    // =====================================
    // 🎸 RENDER LEGENDARY INPUT 🎸
    // =====================================
    
    return (
      <div className={cn('w-full', containerClassName)}>
        {/* Label */}
        {label && (
          <label className={cn(
            'block text-sm font-medium text-gray-700 mb-1.5',
            variant === 'founder' && 'text-yellow-800 font-bold',
            variant === 'legendary' && 'text-yellow-700 font-semibold',
            variant === 'swiss-precision' && 'text-red-700 font-semibold',
            variant === 'code-bro-energy' && 'text-purple-700 font-semibold',
            labelClassName
          )}>
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        
        {/* Description */}
        {description && (
          <p className="text-sm text-gray-600 mb-2">{description}</p>
        )}
        
        {/* Input Container */}
        <div className="relative">
          {/* Left Icon */}
          {LeftIcon && (
            <div className={cn(
              'absolute left-0 top-0 h-full flex items-center justify-center pointer-events-none',
              size === 'sm' ? 'w-9' : 
              size === 'md' ? 'w-10' : 
              size === 'lg' ? 'w-12' : 
              'w-14'
            )}>
              <LeftIcon 
                size={iconSizes[size]} 
                className={cn(
                  'text-gray-400',
                  isFocused && 'text-gray-600',
                  variant === 'founder' && 'text-yellow-600',
                  variant === 'legendary' && 'text-yellow-500',
                  variant === 'swiss-precision' && 'text-red-500',
                  variant === 'code-bro-energy' && 'text-purple-500'
                )}
              />
            </div>
          )}
          
          {/* Main Input */}
          <motion.input
            ref={ref}
            type={actualType}
            className={cn(
              baseInputStyles,
              sizeStyles[size],
              variantStyles[finalVariant],
              LeftIcon && (size === 'sm' ? 'pl-9' : size === 'md' ? 'pl-10' : size === 'lg' ? 'pl-12' : 'pl-14'),
              (RightIcon || isPasswordType || clearable || isLoading) && (size === 'sm' ? 'pr-9' : size === 'md' ? 'pr-10' : size === 'lg' ? 'pr-12' : 'pr-14'),
              className
            )}
            disabled={isDisabled}
            value={value}
            onFocus={(e) => {
              setIsFocused(true);
              props.onFocus?.(e);
            }}
            onBlur={(e) => {
              setIsFocused(false);
              props.onBlur?.(e);
            }}
            whileFocus={{ scale: variant === 'founder' ? 1.01 : 1 }}
            {...props}
          />
          
          {/* Right Icons Container */}
          <div className={cn(
            'absolute right-0 top-0 h-full flex items-center justify-center gap-1',
            size === 'sm' ? 'w-9 pr-2' : 
            size === 'md' ? 'w-10 pr-3' : 
            size === 'lg' ? 'w-12 pr-3' : 
            'w-14 pr-4'
          )}>
            {/* Loading Spinner */}
            {isLoading && (
              <div
                className={cn(
                  'border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin',
                  size === 'sm' ? 'w-4 h-4' : 'w-5 h-5'
                )}
              />
            )}
            
            {/* Clear Button */}
            {clearable && hasValue && !isLoading && (
              <button
                type="button"
                onClick={handleClear}
                className="text-gray-400 hover:text-gray-600 transition-colors p-0.5"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            )}
            
            {/* Password Toggle */}
            {isPasswordType && showPassword && !isLoading && (
              <button
                type="button"
                onClick={handlePasswordToggle}
                className="text-gray-400 hover:text-gray-600 transition-colors p-0.5"
              >
                {showPasswordVisible ? (
                  <EyeOff size={iconSizes[size]} />
                ) : (
                  <Eye size={iconSizes[size]} />
                )}
              </button>
            )}
            
            {/* Status Icons */}
            {!isLoading && hasError && (
              <AlertCircle size={iconSizes[size]} className="text-red-500" />
            )}
            
            {!isLoading && success && !hasError && (
              <CheckCircle size={iconSizes[size]} className="text-green-500" />
            )}
            
            {/* Custom Right Icon */}
            {RightIcon && !isLoading && !hasError && !success && (
              <RightIcon 
                size={iconSizes[size]} 
                className={cn(
                  'text-gray-400',
                  isFocused && 'text-gray-600',
                  variant === 'founder' && 'text-yellow-600',
                  variant === 'legendary' && 'text-yellow-500',
                  variant === 'swiss-precision' && 'text-red-500',
                  variant === 'code-bro-energy' && 'text-purple-500'
                )}
              />
            )}
          </div>
        </div>
        
        {/* Helper Text / Error Message */}
        {(helperText || error) && (
          <motion.p 
            className={cn(
              'text-sm mt-1.5',
              hasError ? 'text-red-600' : 'text-gray-500',
              variant === 'founder' && !hasError && 'text-yellow-700',
              variant === 'legendary' && !hasError && 'text-yellow-600'
            )}
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {error || helperText}
          </motion.p>
        )}
      </div>
    );
  }
);

LegendaryInput.displayName = 'LegendaryInput';

console.log('🎸🎸🎸 LEGENDARY INPUT COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Input component completed at: 2025-08-06 13:34:22 UTC`);
console.log('📝 Form input: SWISS PRECISION');
console.log('👑 RICKROLL187 founder variant: LEGENDARY');
console.log('🎸 Interactive features: MAXIMUM USABILITY');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
