// File: mobile/src/theme/legendaryTheme.ts
/**
 * 🎨🎸 N3EXTPATH - LEGENDARY THEME SYSTEM 🎸🎨
 * Swiss precision design system with code bro energy
 * Built: 2025-08-06 01:24:40 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { DefaultTheme } from 'react-native-paper';
import { Platform, Dimensions } from 'react-native';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

// =====================================
// 🎸 LEGENDARY COLOR PALETTE 🎸
// =====================================

export const legendaryColors = {
  // Primary legendary colors
  legendary: '#FFD700',        // Legendary gold
  swissPrecision: '#DC143C',   // Swiss precision red
  codeBroEnergy: '#1E90FF',    // Code bro energy blue
  rickroll187: '#9932CC',      // RICKROLL187 purple
  
  // UI Colors with legendary precision
  primary: '#1a1a1a',          // Legendary dark
  primaryVariant: '#2d2d2d',   // Darker variant
  secondary: '#FFD700',        // Legendary gold
  secondaryVariant: '#FFA500', // Orange gold
  
  // Background colors
  background: '#ffffff',       // Clean white
  surface: '#f8f9fa',         // Light surface
  surfaceVariant: '#e9ecef',  // Variant surface
  
  // Dark theme colors
  backgroundDark: '#121212',   // Dark background
  surfaceDark: '#1e1e1e',     // Dark surface
  surfaceVariantDark: '#2d2d2d', // Dark surface variant
  
  // Text colors
  onPrimary: '#ffffff',        // White on primary
  onSecondary: '#000000',      // Black on secondary
  onBackground: '#212529',     // Dark text on light
  onBackgroundDark: '#ffffff', // Light text on dark
  onSurface: '#495057',        // Medium text
  onSurfaceVariant: '#6c757d', // Light text
  
  // Status colors
  success: '#28a745',          // Success green
  successBackground: '#d4edda', // Light success
  warning: '#ffc107',          // Warning amber
  warningBackground: '#fff3cd', // Light warning
  error: '#dc3545',            // Error red
  errorBackground: '#f8d7da',  // Light error
  info: '#17a2b8',            // Info cyan
  infoBackground: '#d1ecf1',   // Light info
  
  // Legendary status colors
  legendarySuccess: '#32CD32',  // Legendary lime green
  swissPrecisionBlue: '#4169E1', // Swiss precision blue
  codeBroOrange: '#FF8C00',     // Code bro orange
  founderPurple: '#8A2BE2',     // Founder blue violet
  
  // Interactive colors
  accent: '#007bff',           // Accent blue
  accentVariant: '#0056b3',    // Darker accent
  outline: '#dee2e6',          // Border color
  outlineVariant: '#adb5bd',   // Darker border
  
  // Overlay colors
  backdrop: 'rgba(0, 0, 0, 0.5)',     // Modal backdrop
  overlay: 'rgba(26, 26, 26, 0.8)',   // Dark overlay
  shimmer: 'rgba(255, 255, 255, 0.1)', // Shimmer effect
  
  // Legendary gradient colors
  gradientStart: '#FFD700',    // Gold start
  gradientMiddle: '#FFA500',   // Orange middle
  gradientEnd: '#FF6347',      // Tomato end
  
  // Swiss precision gradients
  swissGradientStart: '#DC143C', // Swiss red start
  swissGradientEnd: '#B22222',   // Fire brick end
  
  // Code bro energy gradients
  codeBroGradientStart: '#1E90FF', // Dodger blue start
  codeBroGradientEnd: '#0000FF',   // Blue end
};

// =====================================
// ⚙️ TYPOGRAPHY WITH SWISS PRECISION ⚙️
// =====================================

export const legendaryTypography = {
  // Font families
  fontFamily: {
    regular: Platform.OS === 'ios' ? 'System' : 'Roboto',
    medium: Platform.OS === 'ios' ? 'System' : 'Roboto-Medium',
    bold: Platform.OS === 'ios' ? 'System' : 'Roboto-Bold',
    legendary: 'Legendary-Regular',
    legendaryBold: 'Legendary-Bold',
    swissPrecision: 'SwissPrecision-Regular',
    swissPrecisionBold: 'SwissPrecision-Bold',
    codeBro: 'CodeBro-Regular',
    codeBroBold: 'CodeBro-Bold',
    monospace: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  
  // Font sizes with legendary scaling
  fontSize: {
    xs: 10,    // Extra small
    sm: 12,    // Small
    base: 14,  // Base size
    lg: 16,    // Large
    xl: 18,    // Extra large
    '2xl': 20, // 2X Large
    '3xl': 24, // 3X Large
    '4xl': 28, // 4X Large
    '5xl': 32, // 5X Large
    '6xl': 36, // 6X Large
    legendary: 40,    // Legendary size
    founder: 48,      // Founder size
  },
  
  // Line heights
  lineHeight: {
    tight: 1.2,
    normal: 1.4,
    relaxed: 1.6,
    loose: 1.8,
  },
  
  // Font weights
  fontWeight: {
    thin: '100',
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
    extrabold: '800',
    black: '900',
  },
  
  // Letter spacing
  letterSpacing: {
    tight: -0.5,
    normal: 0,
    wide: 0.5,
    wider: 1,
    widest: 2,
  },
};

// =====================================
// 📏 SPACING WITH LEGENDARY PRECISION 📏
// =====================================

export const legendarySpacing = {
  // Base spacing unit (8px)
  unit: 8,
  
  // Spacing scale
  xs: 4,     // 0.5 units
  sm: 8,     // 1 unit
  md: 16,    // 2 units
  lg: 24,    // 3 units
  xl: 32,    // 4 units
  '2xl': 48, // 6 units
  '3xl': 64, // 8 units
  '4xl': 96, // 12 units
  
  // Legendary spacing
  legendary: 128,  // 16 units
  swiss: 160,      // 20 units
  infinite: 256,   // 32 units
  
  // Component-specific spacing
  padding: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  
  margin: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  
  gap: {
    xs: 4,
    sm: 8,
    md: 12,
    lg: 16,
    xl: 20,
  },
};

// =====================================
// 🎨 BORDER RADIUS & SHADOWS 🎨
// =====================================

export const legendaryBorders = {
  radius: {
    none: 0,
    xs: 2,
    sm: 4,
    md: 8,
    lg: 12,
    xl: 16,
    '2xl': 24,
    '3xl': 32,
    full: 9999,
    legendary: 20,
    swiss: 16,
  },
  
  width: {
    none: 0,
    thin: 0.5,
    base: 1,
    thick: 2,
    legendary: 3,
  },
};

export const legendaryShadows = {
  // iOS-style shadows
  ios: {
    sm: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.18,
      shadowRadius: 1.0,
    },
    md: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.23,
      shadowRadius: 2.62,
    },
    lg: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.30,
      shadowRadius: 4.65,
    },
    legendary: {
      shadowColor: legendaryColors.legendary,
      shadowOffset: { width: 0, height: 8 },
      shadowOpacity: 0.4,
      shadowRadius: 12,
    },
  },
  
  // Android-style elevation
  android: {
    sm: { elevation: 2 },
    md: { elevation: 4 },
    lg: { elevation: 8 },
    legendary: { elevation: 16 },
  },
};

// =====================================
// 📱 RESPONSIVE BREAKPOINTS 📱
// =====================================

export const legendaryBreakpoints = {
  sm: 480,   // Small phones
  md: 768,   // Large phones / small tablets
  lg: 1024,  // Tablets
  xl: 1280,  // Large tablets / small laptops
  
  // Helper functions
  isSmall: screenWidth < 480,
  isMedium: screenWidth >= 480 && screenWidth < 768,
  isLarge: screenWidth >= 768 && screenWidth < 1024,
  isExtraLarge: screenWidth >= 1024,
};

// =====================================
// 🎸 LEGENDARY THEME CONFIGURATION 🎸
// =====================================

export const legendaryTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    ...legendaryColors,
    primary: legendaryColors.primary,
    primaryContainer: legendaryColors.primaryVariant,
    secondary: legendaryColors.secondary,
    secondaryContainer: legendaryColors.secondaryVariant,
    surface: legendaryColors.surface,
    surfaceVariant: legendaryColors.surfaceVariant,
    background: legendaryColors.background,
    error: legendaryColors.error,
    onPrimary: legendaryColors.onPrimary,
    onSecondary: legendaryColors.onSecondary,
    onSurface: legendaryColors.onSurface,
    onBackground: legendaryColors.onBackground,
    outline: legendaryColors.outline,
  },
  
  // Legendary theme extensions
  legendary: {
    colors: legendaryColors,
    typography: legendaryTypography,
    spacing: legendarySpacing,
    borders: legendaryBorders,
    shadows: legendaryShadows,
    breakpoints: legendaryBreakpoints,
    
    // Theme metadata
    name: 'Legendary Theme',
    version: '2.0.0',
    author: 'RICKROLL187',
    contact: 'letstalktech010@gmail.com',
    motto: 'WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!',
    
    // Feature flags
    features: {
      swissPrecision: true,
      codeBroEnergy: true,
      legendaryAnimations: true,
      founderzAccess: true,
    },
  },
};

// =====================================
// 🌙 DARK THEME CONFIGURATION 🌙
// =====================================

export const legendaryDarkTheme = {
  ...legendaryTheme,
  dark: true,
  colors: {
    ...legendaryTheme.colors,
    primary: legendaryColors.legendary,
    primaryContainer: legendaryColors.primaryVariant,
    surface: legendaryColors.surfaceDark,
    surfaceVariant: legendaryColors.surfaceVariantDark,
    background: legendaryColors.backgroundDark,
    onPrimary: legendaryColors.onPrimary,
    onSecondary: legendaryColors.onPrimary,
    onSurface: legendaryColors.onBackgroundDark,
    onBackground: legendaryColors.onBackgroundDark,
  },
};

// =====================================
// 🎸 THEME UTILITIES 🎸
// =====================================

export const getThemeColor = (colorName: keyof typeof legendaryColors, opacity?: number) => {
  const color = legendaryColors[colorName];
  if (opacity !== undefined) {
    // Convert hex to rgba with opacity
    const hex = color.replace('#', '');
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
  }
  return color;
};

export const getLegendarySpacing = (size: keyof typeof legendarySpacing) => {
  return legendarySpacing[size];
};

export const getLegendaryFontSize = (size: keyof typeof legendaryTypography.fontSize) => {
  return legendaryTypography.fontSize[size];
};

export const getLegendaryBorderRadius = (size: keyof typeof legendaryBorders.radius) => {
  return legendaryBorders.radius[size];
};

export const getLegendaryShadow = (size: 'sm' | 'md' | 'lg' | 'legendary') => {
  return Platform.OS === 'ios' 
    ? legendaryShadows.ios[size] 
    : legendaryShadows.android[size];
};

// =====================================
// 🎸 LEGENDARY THEME EXPORTS 🎸
// =====================================

export default legendaryTheme;

// Export type definitions
export type LegendaryTheme = typeof legendaryTheme;
export type LegendaryColors = typeof legendaryColors;
export type LegendarySpacing = typeof legendarySpacing;
export type LegendaryTypography = typeof legendaryTypography;

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY THEME SYSTEM LOADED! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log('🎨 Legendary colors: GOLD PRECISION');
console.log('⚙️ Swiss precision typography: MAXIMUM QUALITY');
console.log('💪 Code bro energy spacing: INFINITE HARMONY');
console.log('👑 RICKROLL187 theme: FOUNDER APPROVED');
