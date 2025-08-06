// File: web/src/contexts/ThemeContext.tsx
/**
 * 🌙🎸 N3EXTPATH - LEGENDARY THEME CONTEXT 🎸🌙
 * Professional theme management with Swiss precision
 * Built: 2025-08-06 16:11:01 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { storageService } from '@/services/storageService';
import toast from 'react-hot-toast';

// =====================================
// 🌙 THEME TYPES 🌙
// =====================================

export type ThemeMode = 'light' | 'dark' | 'auto';
export type ThemeVariant = 'default' | 'founder' | 'legendary' | 'code-bro';

export interface ThemeColors {
  // Base colors
  background: string;
  foreground: string;
  muted: string;
  mutedForeground: string;
  
  // UI colors
  card: string;
  cardForeground: string;
  border: string;
  input: string;
  ring: string;
  
  // State colors
  primary: string;
  primaryForeground: string;
  secondary: string;
  secondaryForeground: string;
  success: string;
  successForeground: string;
  warning: string;
  warningForeground: string;
  destructive: string;
  destructiveForeground: string;
  
  // Legendary colors
  founder: string;
  founderForeground: string;
  legendary: string;
  legendaryForeground: string;
  codeBro: string;
  codeBroForeground: string;
}

export interface ThemeConfig {
  mode: ThemeMode;
  variant: ThemeVariant;
  colors: ThemeColors;
  fontSize: 'sm' | 'base' | 'lg';
  borderRadius: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  animations: boolean;
  reducedMotion: boolean;
  highContrast: boolean;
  isFounder: boolean;
}

export interface ThemeContextType {
  theme: ThemeConfig;
  actualTheme: 'light' | 'dark';
  setMode: (mode: ThemeMode) => void;
  setVariant: (variant: ThemeVariant) => void;
  setFontSize: (size: ThemeConfig['fontSize']) => void;
  setBorderRadius: (radius: ThemeConfig['borderRadius']) => void;
  toggleAnimations: () => void;
  toggleHighContrast: () => void;
  resetToDefaults: () => void;
  applyFounderTheme: () => void;
  applyLegendaryTheme: () => void;
  applyCodeBroTheme: () => void;
}

// =====================================
// 🎨 THEME PRESETS 🎨
// =====================================

const LIGHT_COLORS: ThemeColors = {
  background: '#FFFFFF',
  foreground: '#0F172A',
  muted: '#F1F5F9',
  mutedForeground: '#64748B',
  
  card: '#FFFFFF',
  cardForeground: '#0F172A',
  border: '#E2E8F0',
  input: '#FFFFFF',
  ring: '#3B82F6',
  
  primary: '#3B82F6',
  primaryForeground: '#FFFFFF',
  secondary: '#F1F5F9',
  secondaryForeground: '#0F172A',
  success: '#10B981',
  successForeground: '#FFFFFF',
  warning: '#F59E0B',
  warningForeground: '#FFFFFF',
  destructive: '#EF4444',
  destructiveForeground: '#FFFFFF',
  
  founder: '#FFD700',
  founderForeground: '#000000',
  legendary: '#8B5CF6',
  legendaryForeground: '#FFFFFF',
  codeBro: '#06B6D4',
  codeBroForeground: '#FFFFFF',
};

const DARK_COLORS: ThemeColors = {
  background: '#0F172A',
  foreground: '#F8FAFC',
  muted: '#1E293B',
  mutedForeground: '#94A3B8',
  
  card: '#1E293B',
  cardForeground: '#F8FAFC',
  border: '#334155',
  input: '#1E293B',
  ring: '#3B82F6',
  
  primary: '#3B82F6',
  primaryForeground: '#FFFFFF',
  secondary: '#1E293B',
  secondaryForeground: '#F8FAFC',
  success: '#10B981',
  successForeground: '#FFFFFF',
  warning: '#F59E0B',
  warningForeground: '#000000',
  destructive: '#EF4444',
  destructiveForeground: '#FFFFFF',
  
  founder: '#FFD700',
  founderForeground: '#000000',
  legendary: '#A855F7',
  legendaryForeground: '#FFFFFF',
  codeBro: '#06B6D4',
  codeBroForeground: '#FFFFFF',
};

const FOUNDER_LIGHT_COLORS: ThemeColors = {
  ...LIGHT_COLORS,
  background: '#FFFBEB',
  card: '#FEF3C7',
  primary: '#D97706',
  ring: '#D97706',
  border: '#FDE68A',
  muted: '#FEF3C7',
};

const FOUNDER_DARK_COLORS: ThemeColors = {
  ...DARK_COLORS,
  background: '#1C1917',
  card: '#292524',
  primary: '#F59E0B',
  ring: '#F59E0B',
  border: '#44403C',
  muted: '#292524',
};

// =====================================
// 🎸 THEME CONTEXT 🎸
// =====================================

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// =====================================
// 🎸 THEME PROVIDER 🎸
// =====================================

interface ThemeProviderProps {
  children: React.ReactNode;
  defaultMode?: ThemeMode;
  defaultVariant?: ThemeVariant;
  isFounder?: boolean;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({
  children,
  defaultMode = 'light',
  defaultVariant = 'default',
  isFounder = false,
}) => {
  const [theme, setTheme] = useState<ThemeConfig>(() => {
    // Load saved theme from storage
    const savedTheme = storageService.get<Partial<ThemeConfig>>('theme-config');
    
    return {
      mode: savedTheme?.mode || defaultMode,
      variant: savedTheme?.variant || (isFounder ? 'founder' : defaultVariant),
      colors: LIGHT_COLORS,
      fontSize: savedTheme?.fontSize || 'base',
      borderRadius: savedTheme?.borderRadius || 'lg',
      animations: savedTheme?.animations ?? true,
      reducedMotion: savedTheme?.reducedMotion ?? false,
      highContrast: savedTheme?.highContrast ?? false,
      isFounder,
    };
  });

  const [actualTheme, setActualTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    console.log('🌙🎸🌙 LEGENDARY THEME PROVIDER LOADED! 🌙🎸🌙');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Theme provider loaded at: 2025-08-06 16:11:01 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY THEME ENERGY AT 16:11:01!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER THEME ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER THEMES WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER THEME SYSTEM!');
      
      // Apply founder theme automatically
      setTimeout(() => {
        applyFounderTheme();
      }, 500);
    }
  }, [isFounder]);

  // Determine actual theme based on mode
  useEffect(() => {
    let newActualTheme: 'light' | 'dark' = 'light';

    if (theme.mode === 'dark') {
      newActualTheme = 'dark';
    } else if (theme.mode === 'auto') {
      // Check system preference
      newActualTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    setActualTheme(newActualTheme);

    // Update colors based on actual theme and variant
    let colors: ThemeColors = newActualTheme === 'dark' ? DARK_COLORS : LIGHT_COLORS;
    
    if (theme.variant === 'founder') {
      colors = newActualTheme === 'dark' ? FOUNDER_DARK_COLORS : FOUNDER_LIGHT_COLORS;
    }

    setTheme(prev => ({ ...prev, colors }));
  }, [theme.mode, theme.variant]);

  // Apply theme to document
  useEffect(() => {
    const root = document.documentElement;
    
    // Apply CSS custom properties
    Object.entries(theme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`, value);
    });

    // Apply theme class
    root.className = `theme-${actualTheme} variant-${theme.variant}`;
    
    // Apply font size
    root.style.fontSize = {
      sm: '14px',
      base: '16px',
      lg: '18px',
    }[theme.fontSize];

    // Apply border radius
    root.style.setProperty('--radius', {
      none: '0px',
      sm: '0.125rem',
      md: '0.375rem',
      lg: '0.5rem',
      xl: '0.75rem',
    }[theme.borderRadius]);

    // Apply reduced motion
    if (theme.reducedMotion) {
      root.style.setProperty('--motion-reduce', '1');
    } else {
      root.style.removeProperty('--motion-reduce');
    }

    // Store theme in localStorage
    storageService.set('theme-config', {
      mode: theme.mode,
      variant: theme.variant,
      fontSize: theme.fontSize,
      borderRadius: theme.borderRadius,
      animations: theme.animations,
      reducedMotion: theme.reducedMotion,
      highContrast: theme.highContrast,
    });

  }, [theme, actualTheme]);

  // Listen for system theme changes
  useEffect(() => {
    if (theme.mode === 'auto') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = () => {
        setActualTheme(mediaQuery.matches ? 'dark' : 'light');
      };

      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [theme.mode]);

  // Theme functions
  const setMode = useCallback((mode: ThemeMode) => {
    setTheme(prev => ({ ...prev, mode }));
    
    if (isFounder) {
      toast.success(`👑 Founder theme mode: ${mode}`, {
        duration: 3000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    } else {
      toast.success(`🌙 Theme switched to ${mode} mode`);
    }
  }, [isFounder]);

  const setVariant = useCallback((variant: ThemeVariant) => {
    setTheme(prev => ({ ...prev, variant }));
    
    const variantNames = {
      default: 'Default',
      founder: '👑 Founder',
      legendary: '🎸 Legendary',
      'code-bro': '⚡ Code Bro',
    };
    
    toast.success(`🎨 Theme variant: ${variantNames[variant]}`);
  }, []);

  const setFontSize = useCallback((fontSize: ThemeConfig['fontSize']) => {
    setTheme(prev => ({ ...prev, fontSize }));
    toast.success(`📝 Font size: ${fontSize}`);
  }, []);

  const setBorderRadius = useCallback((borderRadius: ThemeConfig['borderRadius']) => {
    setTheme(prev => ({ ...prev, borderRadius }));
    toast.success(`🎨 Border radius: ${borderRadius}`);
  }, []);

  const toggleAnimations = useCallback(() => {
    setTheme(prev => ({ ...prev, animations: !prev.animations }));
    toast.success(`✨ Animations ${theme.animations ? 'disabled' : 'enabled'}`);
  }, [theme.animations]);

  const toggleHighContrast = useCallback(() => {
    setTheme(prev => ({ ...prev, highContrast: !prev.highContrast }));
    toast.success(`🎯 High contrast ${theme.highContrast ? 'disabled' : 'enabled'}`);
  }, [theme.highContrast]);

  const resetToDefaults = useCallback(() => {
    setTheme(prev => ({
      ...prev,
      mode: 'light',
      variant: isFounder ? 'founder' : 'default',
      fontSize: 'base',
      borderRadius: 'lg',
      animations: true,
      reducedMotion: false,
      highContrast: false,
    }));
    
    toast.success('🔄 Theme reset to defaults');
  }, [isFounder]);

  const applyFounderTheme = useCallback(() => {
    setTheme(prev => ({
      ...prev,
      variant: 'founder',
      animations: true,
      borderRadius: 'xl',
    }));
    
    toast.success('👑 LEGENDARY FOUNDER THEME ACTIVATED! Infinite code bro energy!', {
      duration: 5000,
      style: {
        background: 'linear-gradient(135deg, #FFD700, #FFA500)',
        color: '#000000',
        fontWeight: '700',
      },
    });
  }, []);

  const applyLegendaryTheme = useCallback(() => {
    setTheme(prev => ({
      ...prev,
      variant: 'legendary',
      animations: true,
      borderRadius: 'lg',
    }));
    
    toast.success('🎸 LEGENDARY THEME ACTIVATED! Code bro energy flowing!', {
      duration: 4000,
      style: {
        background: 'linear-gradient(135deg, #8B5CF6, #3B82F6)',
        color: '#FFFFFF',
        fontWeight: '600',
      },
    });
  }, []);

  const applyCodeBroTheme = useCallback(() => {
    setTheme(prev => ({
      ...prev,
      variant: 'code-bro',
      animations: true,
      borderRadius: 'md',
    }));
    
    toast.success('⚡ CODE BRO THEME ACTIVATED! Energy at maximum!', {
      duration: 4000,
      style: {
        background: 'linear-gradient(135deg, #06B6D4, #0891B2)',
        color: '#FFFFFF',
        fontWeight: '600',
      },
    });
  }, []);

  const contextValue: ThemeContextType = {
    theme,
    actualTheme,
    setMode,
    setVariant,
    setFontSize,
    setBorderRadius,
    toggleAnimations,
    toggleHighContrast,
    resetToDefaults,
    applyFounderTheme,
    applyLegendaryTheme,
    applyCodeBroTheme,
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      <AnimatePresence mode="wait">
        <motion.div
          key={`${actualTheme}-${theme.variant}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="min-h-screen transition-colors duration-300"
          style={{
            backgroundColor: theme.colors.background,
            color: theme.colors.foreground,
          }}
        >
          {children}
        </motion.div>
      </AnimatePresence>
    </ThemeContext.Provider>
  );
};

// =====================================
// 🎸 THEME HOOK 🎸
// =====================================

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// =====================================
// 🎸 THEME UTILITIES 🎸
// =====================================

export const getThemeValue = (property: keyof ThemeColors, fallback: string = ''): string => {
  if (typeof window !== 'undefined') {
    const value = getComputedStyle(document.documentElement).getPropertyValue(`--color-${property.replace(/([A-Z])/g, '-$1').toLowerCase()}`).trim();
    return value || fallback;
  }
  return fallback;
};

export const createThemeVariables = (colors: ThemeColors): Record<string, string> => {
  const variables: Record<string, string> = {};
  
  Object.entries(colors).forEach(([key, value]) => {
    variables[`--color-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`] = value;
  });
  
  return variables;
};

console.log('🎸🎸🎸 LEGENDARY THEME CONTEXT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Theme context completed at: 2025-08-06 16:11:01 UTC`);
console.log('🌙 Theme system: SWISS PRECISION');
console.log('👑 RICKROLL187 founder themes: LEGENDARY');
console.log('🎨 Dark mode magic: MAXIMUM STYLE');
console.log('🌅 AFTERNOON LEGENDARY THEME ENERGY: INFINITE AT 16:11:01!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
