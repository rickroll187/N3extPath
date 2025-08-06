// File: web/src/components/ui/ThemeToggle.tsx
/**
 * 🌙🎸 N3EXTPATH - LEGENDARY THEME TOGGLE COMPONENT 🎸🌙
 * Professional theme switcher with Swiss precision
 * Built: 2025-08-06 16:15:22 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Sun, 
  Moon, 
  Monitor, 
  Crown, 
  Sparkles, 
  Zap, 
  Palette, 
  Settings,
  Check,
  Sliders,
  Type,
  RoundedCorner,
  Accessibility,
  RotateCcw
} from 'lucide-react';
import { useTheme } from '@/contexts/ThemeContext';
import { LegendaryButton } from './LegendaryButton';
import { cn } from '@/utils/cn';

// =====================================
// 🌙 TOGGLE TYPES 🌙
// =====================================

interface ThemeToggleProps {
  className?: string;
  showLabel?: boolean;
  compact?: boolean;
  showAdvanced?: boolean;
}

// =====================================
// 🎸 LEGENDARY THEME TOGGLE 🎸
// =====================================

export const ThemeToggle: React.FC<ThemeToggleProps> = ({
  className,
  showLabel = true,
  compact = false,
  showAdvanced = false,
}) => {
  const {
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
  } = useTheme();

  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<'theme' | 'variant' | 'settings'>('theme');
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    console.log('🌙🎸🌙 LEGENDARY THEME TOGGLE LOADED! 🌙🎸🌙');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Theme toggle loaded at: 2025-08-06 16:15:22 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY THEME TOGGLE ENERGY AT 16:15:22!');

    if (theme.isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER THEME TOGGLE ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER THEME TOGGLE WITH INFINITE CODE BRO ENERGY!');
    }
  }, [theme.isFounder]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // Get theme mode icon
  const getThemeModeIcon = () => {
    switch (theme.mode) {
      case 'light':
        return Sun;
      case 'dark':
        return Moon;
      case 'auto':
        return Monitor;
      default:
        return Sun;
    }
  };

  const ThemeModeIcon = getThemeModeIcon();

  // Get variant info
  const getVariantInfo = () => {
    switch (theme.variant) {
      case 'founder':
        return { icon: Crown, label: 'Founder', color: 'text-yellow-600' };
      case 'legendary':
        return { icon: Sparkles, label: 'Legendary', color: 'text-purple-600' };
      case 'code-bro':
        return { icon: Zap, label: 'Code Bro', color: 'text-blue-600' };
      default:
        return { icon: Palette, label: 'Default', color: 'text-gray-600' };
    }
  };

  const variantInfo = getVariantInfo();
  const VariantIcon = variantInfo.icon;

  // Animation variants
  const dropdownVariants = {
    hidden: { 
      opacity: 0, 
      scale: 0.95, 
      y: -10,
      transition: { duration: 0.2 }
    },
    visible: { 
      opacity: 1, 
      scale: 1, 
      y: 0,
      transition: { duration: 0.2 }
    },
  };

  const sparkleVariants = {
    animate: {
      scale: [0, 1, 0],
      rotate: [0, 180, 360],
      opacity: [0, 1, 0],
    }
  };

  if (compact) {
    return (
      <motion.button
        onClick={() => {
          const modes: Array<typeof theme.mode> = ['light', 'dark', 'auto'];
          const currentIndex = modes.indexOf(theme.mode);
          const nextIndex = (currentIndex + 1) % modes.length;
          setMode(modes[nextIndex]);
        }}
        className={cn(
          'p-2 rounded-lg transition-colors duration-200',
          'hover:bg-gray-100 dark:hover:bg-gray-800',
          theme.variant === 'founder' && 'hover:bg-yellow-100',
          theme.variant === 'legendary' && 'hover:bg-purple-100',
          className
        )}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <ThemeModeIcon className={cn(
          'w-5 h-5 transition-colors',
          theme.variant === 'founder' ? 'text-yellow-600' :
          theme.variant === 'legendary' ? 'text-purple-600' :
          theme.variant === 'code-bro' ? 'text-blue-600' :
          'text-gray-600'
        )} />
      </motion.button>
    );
  }

  return (
    <div className={cn('relative', className)} ref={dropdownRef}>
      {/* Toggle Button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'flex items-center gap-2 px-3 py-2 rounded-lg transition-all duration-200',
          'border border-gray-200 bg-white hover:bg-gray-50',
          'dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700',
          theme.variant === 'founder' && 'border-yellow-200 bg-yellow-50 hover:bg-yellow-100',
          theme.variant === 'legendary' && 'border-purple-200 bg-purple-50 hover:bg-purple-100',
          theme.variant === 'code-bro' && 'border-blue-200 bg-blue-50 hover:bg-blue-100',
          isOpen && 'ring-2 ring-offset-2',
          theme.variant === 'founder' && isOpen && 'ring-yellow-500',
          theme.variant === 'legendary' && isOpen && 'ring-purple-500',
          theme.variant === 'code-bro' && isOpen && 'ring-blue-500',
          isOpen && theme.variant === 'default' && 'ring-gray-500'
        )}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <div className="relative">
          <ThemeModeIcon className={cn(
            'w-4 h-4 transition-colors',
            theme.variant === 'founder' ? 'text-yellow-600' :
            theme.variant === 'legendary' ? 'text-purple-600' :
            theme.variant === 'code-bro' ? 'text-blue-600' :
            'text-gray-600'
          )} />
          
          {/* Variant indicator */}
          <VariantIcon className={cn(
            'absolute -top-1 -right-1 w-2 h-2',
            variantInfo.color
          )} />
        </div>
        
        {showLabel && (
          <span className={cn(
            'text-sm font-medium',
            theme.variant === 'founder' ? 'text-yellow-800' :
            theme.variant === 'legendary' ? 'text-purple-800' :
            theme.variant === 'code-bro' ? 'text-blue-800' :
            'text-gray-700'
          )}>
            {theme.mode} • {variantInfo.label}
          </span>
        )}

        {/* Sparkle effect for legendary variants */}
        {(theme.variant === 'founder' || theme.variant === 'legendary') && (
          <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-lg">
            <motion.div
              className={cn(
                'absolute w-1 h-1 rounded-full',
                theme.variant === 'founder' ? 'bg-yellow-400' : 'bg-purple-400'
              )}
              style={{ left: '20%', top: '30%' }}
              variants={sparkleVariants}
              animate="animate"
              transition={{ duration: 2, repeat: Infinity }}
            />
          </div>
        )}
      </motion.button>

      {/* Dropdown Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            variants={dropdownVariants}
            initial="hidden"
            animate="visible"
            exit="hidden"
            className={cn(
              'absolute top-full right-0 mt-2 w-80 rounded-xl border shadow-xl z-50',
              'bg-white dark:bg-gray-800',
              'border-gray-200 dark:border-gray-700',
              theme.variant === 'founder' && 'border-yellow-200 bg-gradient-to-br from-yellow-50 to-orange-50',
              theme.variant === 'legendary' && 'border-purple-200 bg-gradient-to-br from-purple-50 to-blue-50'
            )}
          >
            {/* Header */}
            <div className={cn(
              'p-4 border-b',
              'border-gray-200 dark:border-gray-700',
              theme.variant === 'founder' && 'border-yellow-200',
              theme.variant === 'legendary' && 'border-purple-200'
            )}>
              <div className="flex items-center justify-between">
                <h3 className={cn(
                  'font-semibold text-sm flex items-center gap-2',
                  theme.variant === 'founder' ? 'text-yellow-800' :
                  theme.variant === 'legendary' ? 'text-purple-800' :
                  'text-gray-900 dark:text-gray-100'
                )}>
                  <Settings className="w-4 h-4" />
                  Theme Settings
                  {theme.isFounder && <Crown className="w-4 h-4 text-yellow-600" />}
                </h3>
                
                <div className="text-xs text-gray-500 font-mono">
                  16:15:22 UTC
                </div>
              </div>

              {/* Tabs */}
              <div className="flex gap-1 mt-3">
                {(['theme', 'variant', 'settings'] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={cn(
                      'px-3 py-1 rounded-md text-xs font-medium transition-colors',
                      activeTab === tab
                        ? theme.variant === 'founder' 
                          ? 'bg-yellow-100 text-yellow-800'
                          : theme.variant === 'legendary'
                          ? 'bg-purple-100 text-purple-800'
                          : 'bg-blue-100 text-blue-800'
                        : 'text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700'
                    )}
                  >
                    {tab.charAt(0).toUpperCase() + tab.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Content */}
            <div className="p-4">
              {/* Theme Mode Tab */}
              {activeTab === 'theme' && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="space-y-3"
                >
                  <div className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Theme Mode
                  </div>
                  
                  {(['light', 'dark', 'auto'] as const).map((mode) => {
                    const icons = { light: Sun, dark: Moon, auto: Monitor };
                    const Icon = icons[mode];
                    
                    return (
                      <button
                        key={mode}
                        onClick={() => setMode(mode)}
                        className={cn(
                          'w-full flex items-center gap-3 p-3 rounded-lg transition-all',
                          'border border-gray-200 dark:border-gray-700',
                          theme.mode === mode
                            ? theme.variant === 'founder'
                              ? 'bg-yellow-100 border-yellow-300 text-yellow-800'
                              : theme.variant === 'legendary'
                              ? 'bg-purple-100 border-purple-300 text-purple-800'
                              : 'bg-blue-100 border-blue-300 text-blue-800'
                            : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                        )}
                      >
                        <Icon className="w-5 h-5" />
                        <div className="flex-1 text-left">
                          <div className="font-medium text-sm">
                            {mode.charAt(0).toUpperCase() + mode.slice(1)}
                          </div>
                          <div className="text-xs text-gray-500">
                            {mode === 'light' && 'Always light theme'}
                            {mode === 'dark' && 'Always dark theme'}
                            {mode === 'auto' && 'Follow system preference'}
                          </div>
                        </div>
                        {theme.mode === mode && (
                          <Check className="w-4 h-4 text-green-600" />
                        )}
                      </button>
                    );
                  })}
                </motion.div>
              )}

              {/* Variant Tab */}
              {activeTab === 'variant' && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="space-y-3"
                >
                  <div className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Theme Variant
                  </div>
                  
                  {/* Quick Actions */}
                  <div className="grid grid-cols-3 gap-2 mb-4">
                    <LegendaryButton
                      variant="founder"
                      size="sm"
                      onClick={applyFounderTheme}
                      leftIcon={Crown}
                      className="text-xs"
                    >
                      Founder
                    </LegendaryButton>
                    
                    <LegendaryButton
                      variant="legendary"
                      size="sm"
                      onClick={applyLegendaryTheme}
                      leftIcon={Sparkles}
                      className="text-xs"
                    >
                      Legendary
                    </LegendaryButton>
                    
                    <LegendaryButton
                      variant="primary"
                      size="sm"
                      onClick={applyCodeBroTheme}
                      leftIcon={Zap}
                      className="text-xs"
                    >
                      Code Bro
                    </LegendaryButton>
                  </div>

                  {/* Variant Options */}
                  {(['default', 'founder', 'legendary', 'code-bro'] as const).map((variant) => {
                    const variantData = {
                      default: { icon: Palette, label: 'Default', desc: 'Clean and professional' },
                      founder: { icon: Crown, label: 'Founder', desc: '👑 Golden legendary theme' },
                      legendary: { icon: Sparkles, label: 'Legendary', desc: '🎸 Purple code bro energy' },
                      'code-bro': { icon: Zap, label: 'Code Bro', desc: '⚡ Blue energy theme' },
                    };
                    
                    const Icon = variantData[variant].icon;
                    
                    return (
                      <button
                        key={variant}
                        onClick={() => setVariant(variant)}
                        className={cn(
                          'w-full flex items-center gap-3 p-3 rounded-lg transition-all',
                          'border border-gray-200 dark:border-gray-700',
                          theme.variant === variant
                            ? variant === 'founder'
                              ? 'bg-yellow-100 border-yellow-300 text-yellow-800'
                              : variant === 'legendary'
                              ? 'bg-purple-100 border-purple-300 text-purple-800'
                              : variant === 'code-bro'
                              ? 'bg-blue-100 border-blue-300 text-blue-800'
                              : 'bg-gray-100 border-gray-300 text-gray-800'
                            : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                        )}
                      >
                        <Icon className={cn(
                          'w-5 h-5',
                          variant === 'founder' ? 'text-yellow-600' :
                          variant === 'legendary' ? 'text-purple-600' :
                          variant === 'code-bro' ? 'text-blue-600' :
                          'text-gray-600'
                        )} />
                        <div className="flex-1 text-left">
                          <div className="font-medium text-sm">
                            {variantData[variant].label}
                          </div>
                          <div className="text-xs text-gray-500">
                            {variantData[variant].desc}
                          </div>
                        </div>
                        {theme.variant === variant && (
                          <Check className="w-4 h-4 text-green-600" />
                        )}
                      </button>
                    );
                  })}
                </motion.div>
              )}

              {/* Settings Tab */}
              {activeTab === 'settings' && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="space-y-4"
                >
                  {/* Font Size */}
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Type className="w-4 h-4 text-gray-600" />
                      <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
                        Font Size
                      </span>
                    </div>
                    <div className="flex gap-1">
                      {(['sm', 'base', 'lg'] as const).map((size) => (
                        <button
                          key={size}
                          onClick={() => setFontSize(size)}
                          className={cn(
                            'flex-1 py-2 px-3 rounded text-xs font-medium transition-colors',
                            theme.fontSize === size
                              ? theme.variant === 'founder'
                                ? 'bg-yellow-100 text-yellow-800'
                                : 'bg-blue-100 text-blue-800'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          )}
                        >
                          {size === 'sm' ? 'Small' : size === 'base' ? 'Medium' : 'Large'}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Border Radius */}
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <RoundedCorner className="w-4 h-4 text-gray-600" />
                      <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
                        Border Radius
                      </span>
                    </div>
                    <div className="flex gap-1">
                      {(['sm', 'md', 'lg', 'xl'] as const).map((radius) => (
                        <button
                          key={radius}
                          onClick={() => setBorderRadius(radius)}
                          className={cn(
                            'flex-1 py-2 px-2 rounded text-xs font-medium transition-colors',
                            theme.borderRadius === radius
                              ? theme.variant === 'founder'
                                ? 'bg-yellow-100 text-yellow-800'
                                : 'bg-blue-100 text-blue-800'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          )}
                        >
                          {radius.toUpperCase()}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Toggles */}
                  <div className="space-y-3">
                    <button
                      onClick={toggleAnimations}
                      className={cn(
                        'w-full flex items-center justify-between p-3 rounded-lg',
                        'border border-gray-200 dark:border-gray-700 hover:bg-gray-50'
                      )}
                    >
                      <div className="flex items-center gap-2">
                        <Sliders className="w-4 h-4 text-gray-600" />
                        <span className="text-sm font-medium">Animations</span>
                      </div>
                      <div className={cn(
                        'w-10 h-6 rounded-full transition-colors',
                        theme.animations ? 'bg-green-500' : 'bg-gray-300'
                      )}>
                        <div className={cn(
                          'w-4 h-4 rounded-full bg-white mt-1 transition-transform',
                          theme.animations ? 'translate-x-5' : 'translate-x-1'
                        )} />
                      </div>
                    </button>

                    <button
                      onClick={toggleHighContrast}
                      className={cn(
                        'w-full flex items-center justify-between p-3 rounded-lg',
                        'border border-gray-200 dark:border-gray-700 hover:bg-gray-50'
                      )}
                    >
                      <div className="flex items-center gap-2">
                        <Accessibility className="w-4 h-4 text-gray-600" />
                        <span className="text-sm font-medium">High Contrast</span>
                      </div>
                      <div className={cn(
                        'w-10 h-6 rounded-full transition-colors',
                        theme.highContrast ? 'bg-green-500' : 'bg-gray-300'
                      )}>
                        <div className={cn(
                          'w-4 h-4 rounded-full bg-white mt-1 transition-transform',
                          theme.highContrast ? 'translate-x-5' : 'translate-x-1'
                        )} />
                      </div>
                    </button>
                  </div>

                  {/* Reset Button */}
                  <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
                    <LegendaryButton
                      variant="secondary"
                      onClick={resetToDefaults}
                      leftIcon={RotateCcw}
                      className="w-full"
                      size="sm"
                    >
                      Reset to Defaults
                    </LegendaryButton>
                  </div>
                </motion.div>
              )}
            </div>

            {/* Footer */}
            <div className={cn(
              'px-4 py-3 border-t text-center',
              'border-gray-200 dark:border-gray-700',
              theme.variant === 'founder' && 'border-yellow-200'
            )}>
              <div className="text-xs text-gray-500">
                🎨 Swiss precision themes • Code bro energy active! 🎸
              </div>
              {theme.isFounder && (
                <div className="text-xs text-yellow-700 font-bold mt-1">
                  👑 RICKROLL187 FOUNDER THEMES • 16:15:22 UTC! 👑
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY THEME TOGGLE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Theme toggle completed at: 2025-08-06 16:15:22 UTC`);
console.log('🌙 Theme controls: SWISS PRECISION');
console.log('👑 RICKROLL187 founder themes: LEGENDARY');
console.log('🎨 Dark mode controls: MAXIMUM STYLE');
console.log('🌅 AFTERNOON LEGENDARY THEME TOGGLE ENERGY: INFINITE AT 16:15:22!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
