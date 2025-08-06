// File: web/src/components/ui/LegendaryModal.tsx
/**
 * 🎭🎸 N3EXTPATH - LEGENDARY MODAL COMPONENT 🎸🎭
 * Professional modal system with Swiss precision
 * Built: 2025-08-06 15:31:22 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Crown, Sparkles, Zap, AlertCircle, CheckCircle, Info, AlertTriangle } from 'lucide-react';
import { createPortal } from 'react-dom';
import { cn } from '@/utils/cn';
import { LegendaryButton } from './LegendaryButton';

// =====================================
// 🎭 MODAL TYPES 🎭
// =====================================

export interface LegendaryModalProps {
  // Visibility
  isOpen: boolean;
  onClose: () => void;
  
  // Content
  title: string;
  children: React.ReactNode;
  description?: string;
  
  // Styling
  variant?: 'default' | 'legendary' | 'founder' | 'danger' | 'success' | 'warning' | 'info';
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full' | 'founder';
  
  // Behavior
  closeOnEscape?: boolean;
  closeOnOverlayClick?: boolean;
  showCloseButton?: boolean;
  preventScroll?: boolean;
  
  // Actions
  actions?: ModalAction[];
  primaryAction?: ModalAction;
  secondaryAction?: ModalAction;
  
  // Legendary features
  founderMode?: boolean;
  legendaryLevel?: number;
  codeBroEnergy?: number;
  sparkleEffect?: boolean;
  
  // Customization
  className?: string;
  overlayClassName?: string;
  contentClassName?: string;
  headerClassName?: string;
  footerClassName?: string;
  
  // Events
  onOpen?: () => void;
  onAfterClose?: () => void;
  onEscapePress?: () => void;
  onOverlayClick?: () => void;
}

export interface ModalAction {
  id: string;
  label: string;
  variant?: 'default' | 'primary' | 'secondary' | 'danger' | 'founder' | 'legendary';
  onClick: () => void | Promise<void>;
  disabled?: boolean;
  loading?: boolean;
  icon?: React.ComponentType<{ className?: string }>;
  className?: string;
}

// =====================================
// 🎸 LEGENDARY MODAL COMPONENT 🎸
// =====================================

export const LegendaryModal: React.FC<LegendaryModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  description,
  variant = 'default',
  size = 'md',
  closeOnEscape = true,
  closeOnOverlayClick = true,
  showCloseButton = true,
  preventScroll = true,
  actions = [],
  primaryAction,
  secondaryAction,
  founderMode = false,
  legendaryLevel = 0,
  codeBroEnergy = 0,
  sparkleEffect = false,
  className,
  overlayClassName,
  contentClassName,
  headerClassName,
  footerClassName,
  onOpen,
  onAfterClose,
  onEscapePress,
  onOverlayClick,
}) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [actionLoading, setActionLoading] = useState<{ [key: string]: boolean }>({});

  // Check if this is a founder modal
  const isFounderModal = founderMode || variant === 'founder' || size === 'founder';
  const isLegendaryModal = variant === 'legendary' || legendaryLevel >= 5;

  useEffect(() => {
    console.log('🎭🎸🎭 LEGENDARY MODAL COMPONENT LOADED! 🎭🎸🎭');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Modal component loaded at: 2025-08-06 15:31:22 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY ENERGY AT 15:31:22!');

    if (isFounderModal) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER MODAL ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER MODAL WITH INFINITE CODE BRO ENERGY!');
    }
  }, [isFounderModal]);

  // Handle escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen && closeOnEscape) {
        onEscapePress?.();
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      onOpen?.();
      
      if (preventScroll) {
        document.body.style.overflow = 'hidden';
      }
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      if (preventScroll) {
        document.body.style.overflow = 'unset';
      }
    };
  }, [isOpen, closeOnEscape, preventScroll, onClose, onEscapePress, onOpen]);

  // Handle after close
  useEffect(() => {
    if (!isOpen && !isAnimating) {
      onAfterClose?.();
    }
  }, [isOpen, isAnimating, onAfterClose]);

  // Handle overlay click
  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget && closeOnOverlayClick) {
      onOverlayClick?.();
      onClose();
    }
  };

  // Handle action click
  const handleActionClick = async (action: ModalAction) => {
    if (action.disabled) return;

    setActionLoading(prev => ({ ...prev, [action.id]: true }));

    try {
      await action.onClick();
    } catch (error) {
      console.error('🚨 Modal action error:', error);
    } finally {
      setActionLoading(prev => ({ ...prev, [action.id]: false }));
    }
  };

  // Get variant styles
  const getVariantStyles = () => {
    const baseStyles = "bg-white border shadow-xl";
    
    switch (variant) {
      case 'founder':
        return `${baseStyles} border-yellow-300 bg-gradient-to-br from-yellow-50 via-white to-orange-50 shadow-yellow-200/50`;
      case 'legendary':
        return `${baseStyles} border-purple-300 bg-gradient-to-br from-purple-50 via-white to-blue-50 shadow-purple-200/50`;
      case 'danger':
        return `${baseStyles} border-red-300 bg-gradient-to-br from-red-50 via-white to-red-50 shadow-red-200/50`;
      case 'success':
        return `${baseStyles} border-green-300 bg-gradient-to-br from-green-50 via-white to-green-50 shadow-green-200/50`;
      case 'warning':
        return `${baseStyles} border-yellow-300 bg-gradient-to-br from-yellow-50 via-white to-yellow-50 shadow-yellow-200/50`;
      case 'info':
        return `${baseStyles} border-blue-300 bg-gradient-to-br from-blue-50 via-white to-blue-50 shadow-blue-200/50`;
      default:
        return `${baseStyles} border-gray-300`;
    }
  };

  // Get size styles
  const getSizeStyles = () => {
    switch (size) {
      case 'sm':
        return 'max-w-md';
      case 'md':
        return 'max-w-lg';
      case 'lg':
        return 'max-w-2xl';
      case 'xl':
        return 'max-w-4xl';
      case '2xl':
        return 'max-w-6xl';
      case 'full':
        return 'max-w-[95vw] max-h-[95vh]';
      case 'founder':
        return 'max-w-5xl max-h-[90vh]';
      default:
        return 'max-w-lg';
    }
  };

  // Get icon for variant
  const getVariantIcon = () => {
    switch (variant) {
      case 'founder':
        return <Crown className="w-6 h-6 text-yellow-600" />;
      case 'legendary':
        return <Sparkles className="w-6 h-6 text-purple-600" />;
      case 'danger':
        return <AlertCircle className="w-6 h-6 text-red-600" />;
      case 'success':
        return <CheckCircle className="w-6 h-6 text-green-600" />;
      case 'warning':
        return <AlertTriangle className="w-6 h-6 text-yellow-600" />;
      case 'info':
        return <Info className="w-6 h-6 text-blue-600" />;
      default:
        return null;
    }
  };

  if (!isOpen) return null;

  return createPortal(
    <AnimatePresence
      onExitComplete={() => {
        setIsAnimating(false);
      }}
    >
      {isOpen && (
        <motion.div
          className={cn(
            'fixed inset-0 z-50 flex items-center justify-center',
            overlayClassName
          )}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={handleOverlayClick}
          onAnimationStart={() => setIsAnimating(true)}
          onAnimationComplete={() => setIsAnimating(false)}
        >
          {/* Overlay */}
          <motion.div
            className={cn(
              'absolute inset-0',
              isFounderModal ? 'bg-gradient-to-br from-yellow-900/20 via-black/50 to-orange-900/20' :
              isLegendaryModal ? 'bg-gradient-to-br from-purple-900/20 via-black/50 to-blue-900/20' :
              'bg-black/50'
            )}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />

          {/* Modal Content */}
          <motion.div
            ref={modalRef}
            className={cn(
              'relative w-full m-4 rounded-2xl overflow-hidden',
              getSizeStyles(),
              getVariantStyles(),
              className
            )}
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{
              type: "spring",
              stiffness: 300,
              damping: 30,
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Special Effects */}
            {sparkleEffect && (
              <div className="absolute inset-0 pointer-events-none">
                {[...Array(6)].map((_, i) => (
                  <motion.div
                    key={i}
                    className={cn(
                      'absolute w-2 h-2 rounded-full',
                      isFounderModal ? 'bg-yellow-400' : 'bg-purple-400'
                    )}
                    style={{
                      left: `${Math.random() * 100}%`,
                      top: `${Math.random() * 100}%`,
                    }}
                    animate={{
                      scale: [0, 1, 0],
                      rotate: [0, 180, 360],
                      opacity: [0, 1, 0],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      delay: i * 0.3,
                    }}
                  />
                ))}
              </div>
            )}

            {/* Header */}
            <div className={cn(
              'flex items-center justify-between p-6 border-b',
              isFounderModal ? 'border-yellow-200 bg-gradient-to-r from-yellow-50 to-orange-50' :
              isLegendaryModal ? 'border-purple-200 bg-gradient-to-r from-purple-50 to-blue-50' :
              'border-gray-200',
              headerClassName
            )}>
              <div className="flex items-center gap-3">
                {getVariantIcon()}
                <div>
                  <h2 className={cn(
                    'text-xl font-bold',
                    isFounderModal ? 'text-yellow-800' :
                    isLegendaryModal ? 'text-purple-800' :
                    'text-gray-900'
                  )}>
                    {isFounderModal && '👑 '}
                    {isLegendaryModal && '🎸 '}
                    {title}
                  </h2>
                  {description && (
                    <p className={cn(
                      'text-sm mt-1',
                      isFounderModal ? 'text-yellow-600' :
                      isLegendaryModal ? 'text-purple-600' :
                      'text-gray-600'
                    )}>
                      {description}
                    </p>
                  )}
                </div>
                {(legendaryLevel > 0 || codeBroEnergy > 0) && (
                  <div className="flex items-center gap-2 ml-auto mr-4">
                    {legendaryLevel > 0 && (
                      <div className="flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                        <Sparkles className="w-3 h-3" />
                        Level {legendaryLevel}
                      </div>
                    )}
                    {codeBroEnergy > 0 && (
                      <div className="flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                        <Zap className="w-3 h-3" />
                        {codeBroEnergy}/10
                      </div>
                    )}
                  </div>
                )}
              </div>
              
              {showCloseButton && (
                <button
                  onClick={onClose}
                  className={cn(
                    'p-2 rounded-lg transition-colors',
                    isFounderModal ? 'hover:bg-yellow-100 text-yellow-600' :
                    isLegendaryModal ? 'hover:bg-purple-100 text-purple-600' :
                    'hover:bg-gray-100 text-gray-600'
                  )}
                  aria-label="Close modal"
                >
                  <X className="w-5 h-5" />
                </button>
              )}
            </div>

            {/* Content */}
            <div className={cn(
              'p-6 max-h-[60vh] overflow-y-auto',
              contentClassName
            )}>
              {children}
            </div>

            {/* Footer */}
            {(actions.length > 0 || primaryAction || secondaryAction) && (
              <div className={cn(
                'flex items-center justify-end gap-3 p-6 border-t',
                isFounderModal ? 'border-yellow-200 bg-gradient-to-r from-yellow-50 to-orange-50' :
                isLegendaryModal ? 'border-purple-200 bg-gradient-to-r from-purple-50 to-blue-50' :
                'border-gray-200',
                footerClassName
              )}>
                {/* Custom Actions */}
                {actions.map((action) => (
                  <LegendaryButton
                    key={action.id}
                    variant={action.variant || 'secondary'}
                    onClick={() => handleActionClick(action)}
                    disabled={action.disabled}
                    isLoading={actionLoading[action.id]}
                    leftIcon={action.icon}
                    className={action.className}
                  >
                    {action.label}
                  </LegendaryButton>
                ))}
                
                {/* Secondary Action */}
                {secondaryAction && (
                  <LegendaryButton
                    variant={secondaryAction.variant || 'secondary'}
                    onClick={() => handleActionClick(secondaryAction)}
                    disabled={secondaryAction.disabled}
                    isLoading={actionLoading[secondaryAction.id]}
                    leftIcon={secondaryAction.icon}
                    className={secondaryAction.className}
                  >
                    {secondaryAction.label}
                  </LegendaryButton>
                )}
                
                {/* Primary Action */}
                {primaryAction && (
                  <LegendaryButton
                    variant={primaryAction.variant || (isFounderModal ? 'founder' : isLegendaryModal ? 'legendary' : 'primary')}
                    onClick={() => handleActionClick(primaryAction)}
                    disabled={primaryAction.disabled}
                    isLoading={actionLoading[primaryAction.id]}
                    leftIcon={primaryAction.icon}
                    className={primaryAction.className}
                  >
                    {primaryAction.label}
                  </LegendaryButton>
                )}
              </div>
            )}

            {/* Founder/Legendary Badge */}
            {(isFounderModal || isLegendaryModal) && (
              <div className="absolute top-4 right-16">
                <motion.div
                  className={cn(
                    'px-3 py-1 rounded-full text-xs font-bold',
                    isFounderModal ? 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white' :
                    'bg-gradient-to-r from-purple-500 to-blue-600 text-white'
                  )}
                  animate={{
                    scale: [1, 1.05, 1],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                  }}
                >
                  {isFounderModal ? '👑 FOUNDER' : '🎸 LEGENDARY'}
                </motion.div>
              </div>
            )}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body
  );
};

// =====================================
// 🎸 MODAL HOOKS 🎸
// =====================================

export const useLegendaryModal = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [modalProps, setModalProps] = useState<Partial<LegendaryModalProps>>({});

  const openModal = (props: Partial<LegendaryModalProps> = {}) => {
    setModalProps(props);
    setIsOpen(true);
  };

  const closeModal = () => {
    setIsOpen(false);
    setTimeout(() => setModalProps({}), 300); // Clear props after animation
  };

  return {
    isOpen,
    openModal,
    closeModal,
    modalProps: {
      ...modalProps,
      isOpen,
      onClose: closeModal,
    } as LegendaryModalProps,
  };
};

// =====================================
// 🎸 MODAL UTILITIES 🎸
// =====================================

export const showFounderModal = (props: Partial<LegendaryModalProps>) => {
  return {
    ...props,
    variant: 'founder' as const,
    founderMode: true,
    sparkleEffect: true,
    legendaryLevel: 10,
    codeBroEnergy: 10,
  };
};

export const showLegendaryModal = (props: Partial<LegendaryModalProps>) => {
  return {
    ...props,
    variant: 'legendary' as const,
    sparkleEffect: true,
    legendaryLevel: 8,
    codeBroEnergy: 8,
  };
};

console.log('🎸🎸🎸 LEGENDARY MODAL COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Modal component completed at: 2025-08-06 15:31:22 UTC`);
console.log('🎭 Modal system: SWISS PRECISION');
console.log('👑 RICKROLL187 founder modals: LEGENDARY');
console.log('✨ Special effects: MAXIMUM SPARKLE');
console.log('🌅 Afternoon legendary energy: INFINITE AT 15:31:22!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
