// File: web/src/components/layout/LegendarySidebar.tsx
/**
 * 📋🎸 N3EXTPATH - LEGENDARY SIDEBAR COMPONENT 🎸📋
 * Professional sidebar navigation with Swiss precision
 * Built: 2025-08-06 14:13:16 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard,
  User,
  BarChart3,
  Target,
  Users,
  Bell,
  Settings,
  Crown,
  Zap,
  Gauge,
  Award,
  TrendingUp,
  Calendar,
  MessageCircle,
  FileText,
  Shield,
  Database,
  X,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { cn } from '@/utils/cn';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { User as UserType } from '@/hooks/useAuth';

// =====================================
// 📋 SIDEBAR TYPES 📋
// =====================================

interface NavigationItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string; size?: number }>;
  badge?: string | number;
  isNew?: boolean;
  foundersOnly?: boolean;
  legendaryOnly?: boolean;
  comingSoon?: boolean;
}

interface LegendarySidebarProps {
  isOpen: boolean;
  onClose: () => void;
  isFounder?: boolean;
  isLegendary?: boolean;
  user: UserType | null;
}

// =====================================
// 🎸 NAVIGATION ITEMS 🎸
// =====================================

const mainNavigation: NavigationItem[] = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'Profile',
    href: '/profile',
    icon: User,
  },
  {
    name: 'Performance',
    href: '/performance',
    icon: BarChart3,
    badge: 'Updated',
  },
  {
    name: 'OKRs',
    href: '/okrs',
    icon: Target,
    badge: 3,
  },
  {
    name: 'Teams',
    href: '/teams',
    icon: Users,
    isNew: true,
  },
  {
    name: 'Notifications',
    href: '/notifications',
    icon: Bell,
    badge: 8,
  },
];

const founderNavigation: NavigationItem[] = [
  {
    name: 'Founder Console',
    href: '/founder',
    icon: Crown,
    foundersOnly: true,
    badge: 'NEW',
  },
  {
    name: 'Platform Analytics',
    href: '/analytics',
    icon: TrendingUp,
    foundersOnly: true,
  },
  {
    name: 'User Management',
    href: '/admin/users',
    icon: Shield,
    foundersOnly: true,
  },
  {
    name: 'System Health',
    href: '/admin/system',
    icon: Database,
    foundersOnly: true,
  },
];

const legendaryFeatures: NavigationItem[] = [
  {
    name: 'Legendary Achievements',
    href: '/achievements',
    icon: Award,
    legendaryOnly: true,
  },
  {
    name: 'Energy Tracker',
    href: '/energy',
    icon: Zap,
    legendaryOnly: true,
  },
  {
    name: 'Precision Metrics',
    href: '/metrics',
    icon: Gauge,
    legendaryOnly: true,
  },
];

const additionalFeatures: NavigationItem[] = [
  {
    name: 'Calendar',
    href: '/calendar',
    icon: Calendar,
    comingSoon: true,
  },
  {
    name: 'Messages',
    href: '/messages',
    icon: MessageCircle,
    comingSoon: true,
  },
  {
    name: 'Reports',
    href: '/reports',
    icon: FileText,
    comingSoon: true,
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
  },
];

// =====================================
// 🎸 LEGENDARY SIDEBAR COMPONENT 🎸
// =====================================

export function LegendarySidebar({ 
  isOpen, 
  onClose, 
  isFounder = false, 
  isLegendary = false, 
  user 
}: LegendarySidebarProps) {
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);

  useEffect(() => {
    console.log('📋🎸📋 LEGENDARY SIDEBAR LOADED! 📋🎸📋');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Sidebar loaded at: 2025-08-06 14:13:16 UTC`);
    
    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER SIDEBAR ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY NAVIGATION WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION SIDEBAR SYSTEM!');
      console.log('🌅 AFTERNOON FOUNDER POWER AT 14:13:16!');
    }

    // Close sidebar on route change (mobile)
    const handleRouteChange = () => {
      if (window.innerWidth < 1024) {
        onClose();
      }
    };

    // Listen for route changes
    handleRouteChange();
  }, [location.pathname, isFounder, onClose]);

  // =====================================
  // 🎸 LEGENDARY HANDLERS 🎸
  // =====================================

  const handleLinkClick = (href: string) => {
    console.log(`🔗 Navigating to: ${href}`);
    if (window.innerWidth < 1024) {
      onClose();
    }
  };

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
    console.log(`📋 Sidebar ${isCollapsed ? 'expanded' : 'collapsed'}`);
  };

  // =====================================
  // 🎸 RENDER NAVIGATION ITEMS 🎸
  // =====================================

  const renderNavigationItem = (item: NavigationItem) => {
    const isActive = location.pathname === item.href || 
                     (item.href !== '/' && location.pathname.startsWith(item.href));
    
    const isAccessible = !item.foundersOnly || isFounder;
    const isLegendaryAccessible = !item.legendaryOnly || (isLegendary || isFounder);
    
    if (!isAccessible || !isLegendaryAccessible) {
      return null;
    }

    return (
      <motion.div
        key={item.name}
        onHoverStart={() => setHoveredItem(item.name)}
        onHoverEnd={() => setHoveredItem(null)}
        whileHover={{ x: 2 }}
        transition={{ duration: 0.2 }}
      >
        <Link
          to={item.comingSoon ? '#' : item.href}
          onClick={() => !item.comingSoon && handleLinkClick(item.href)}
          className={cn(
            'group flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 relative',
            isActive && !item.comingSoon ? [
              'bg-gradient-to-r text-white shadow-md',
              isFounder ? 'from-yellow-500 to-orange-500' :
              isLegendary ? 'from-blue-500 to-purple-500' :
              'from-blue-600 to-blue-700',
            ] : [
              'text-gray-700 hover:bg-gray-100',
              item.comingSoon && 'opacity-50 cursor-not-allowed',
              isFounder && 'hover:bg-yellow-50 hover:text-yellow-800',
              isLegendary && !isFounder && 'hover:bg-blue-50 hover:text-blue-800',
            ]
          )}
        >
          {/* Icon */}
          <item.icon 
            className={cn(
              'flex-shrink-0 w-5 h-5 transition-colors duration-200',
              isCollapsed ? 'mr-0' : 'mr-3',
              isActive && !item.comingSoon ? 'text-white' : [
                'text-gray-500 group-hover:text-gray-700',
                isFounder && 'group-hover:text-yellow-600',
                isLegendary && !isFounder && 'group-hover:text-blue-600',
              ]
            )}
          />
          
          {/* Label */}
          <AnimatePresence>
            {!isCollapsed && (
              <motion.div
                className="flex-1 flex items-center justify-between min-w-0"
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: 'auto' }}
                exit={{ opacity: 0, width: 0 }}
                transition={{ duration: 0.2 }}
              >
                <span className="truncate">{item.name}</span>
                
                {/* Badges */}
                <div className="flex items-center gap-1 ml-2">
                  {item.isNew && (
                    <span className="px-1.5 py-0.5 text-xs font-medium bg-green-100 text-green-800 rounded">
                      NEW
                    </span>
                  )}
                  
                  {item.badge && (
                    <span className={cn(
                      'px-1.5 py-0.5 text-xs font-medium rounded',
                      typeof item.badge === 'number' ? [
                        'bg-red-100 text-red-800',
                        isFounder && 'bg-orange-100 text-orange-800',
                      ] : 'bg-blue-100 text-blue-800'
                    )}>
                      {item.badge}
                    </span>
                  )}
                  
                  {item.comingSoon && (
                    <span className="px-1.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-600 rounded">
                      SOON
                    </span>
                  )}
                  
                  {item.foundersOnly && (
                    <Crown className="w-3 h-3 text-yellow-500" />
                  )}
                  
                  {item.legendaryOnly && (
                    <Zap className="w-3 h-3 text-purple-500" />
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          
          {/* Active Indicator */}
          {isActive && !item.comingSoon && (
            <motion.div
              className={cn(
                'absolute left-0 top-0 bottom-0 w-1 rounded-r-full',
                isFounder ? 'bg-yellow-300' :
                isLegendary ? 'bg-blue-300' :
                'bg-white'
              )}
              layoutId="activeIndicator"
              transition={{ duration: 0.3 }}
            />
          )}
          
          {/* Hover Effect */}
          {hoveredItem === item.name && !isActive && !item.comingSoon && (
            <motion.div
              className={cn(
                'absolute inset-0 rounded-lg opacity-10',
                isFounder ? 'bg-yellow-500' :
                isLegendary ? 'bg-blue-500' :
                'bg-gray-500'
              )}
              layoutId="hoverEffect"
              transition={{ duration: 0.2 }}
            />
          )}
        </Link>
      </motion.div>
    );
  };

  // =====================================
  // 🎸 RENDER LEGENDARY SIDEBAR 🎸
  // =====================================

  return (
    <>
      {/* Mobile Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <AnimatePresence>
        <motion.aside
          className={cn(
            'fixed top-0 left-0 z-50 h-full bg-white border-r border-gray-200 shadow-xl',
            'lg:sticky lg:top-16 lg:h-[calc(100vh-4rem)] lg:shadow-lg',
            isCollapsed ? 'w-16' : 'w-72',
            'transition-all duration-300 ease-in-out',
            isFounder && 'bg-gradient-to-b from-yellow-50/50 via-white to-orange-50/50 border-yellow-200',
            isLegendary && !isFounder && 'bg-gradient-to-b from-blue-50/50 via-white to-purple-50/50 border-blue-200'
          )}
          initial={{ x: -300 }}
          animate={{ 
            x: isOpen || window.innerWidth >= 1024 ? 0 : -300,
            width: isCollapsed ? 64 : 288
          }}
          exit={{ x: -300 }}
          transition={{ duration: 0.3, ease: 'easeInOut' }}
        >
          {/* Sidebar Header */}
          <div className={cn(
            'flex items-center justify-between p-4 border-b border-gray-200',
            isFounder && 'border-yellow-200',
            isLegendary && !isFounder && 'border-blue-200'
          )}>
            {!isCollapsed && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-center gap-3"
              >
                <div className={cn(
                  'w-8 h-8 rounded-lg flex items-center justify-center text-white text-sm font-bold',
                  'bg-gradient-to-br',
                  isFounder ? 'from-yellow-500 to-orange-600' :
                  isLegendary ? 'from-blue-500 to-purple-600' :
                  'from-gray-600 to-gray-700'
                )}>
                  {isFounder ? <Crown className="w-5 h-5" /> :
                   isLegendary ? <Zap className="w-5 h-5" /> :
                   <Gauge className="w-5 h-5" />}
                </div>
                <div>
                  <h2 className={cn(
                    'text-sm font-bold text-gray-900',
                    isFounder && 'text-yellow-800',
                    isLegendary && !isFounder && 'text-blue-800'
                  )}>
                    {isFounder ? '👑 Founder Menu' : isLegendary ? '🎸 Legendary Menu' : 'Navigation'}
                  </h2>
                  <p className="text-xs text-gray-500">
                    {isFounder ? 'Infinite Power' : isLegendary ? 'Code Bro Energy' : 'Swiss Precision'}
                  </p>
                </div>
              </motion.div>
            )}

            <div className="flex items-center gap-1">
              {/* Collapse Toggle */}
              <LegendaryButton
                variant="ghost"
                size="sm"
                iconOnly
                leftIcon={isCollapsed ? ChevronRight : ChevronLeft}
                onClick={toggleCollapse}
                className="hidden lg:flex"
                aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
              />

              {/* Mobile Close Button */}
              <LegendaryButton
                variant="ghost"
                size="sm"
                iconOnly
                leftIcon={X}
                onClick={onClose}
                className="lg:hidden"
                aria-label="Close sidebar"
              />
            </div>
          </div>

          {/* Navigation Content */}
          <div className="flex-1 overflow-y-auto py-4 space-y-6">
            {/* Main Navigation */}
            <nav className="px-3">
              <div className="space-y-1">
                {mainNavigation.map(renderNavigationItem)}
              </div>
            </nav>

            {/* Founder Only Features */}
            {isFounder && (
              <div className="px-3">
                {!isCollapsed && (
                  <h3 className="px-3 mb-2 text-xs font-semibold text-yellow-600 uppercase tracking-wider">
                    👑 Founder Tools
                  </h3>
                )}
                <div className="space-y-1">
                  {founderNavigation.map(renderNavigationItem)}
                </div>
              </div>
            )}

            {/* Legendary Features */}
            {(isLegendary || isFounder) && (
              <div className="px-3">
                {!isCollapsed && (
                  <h3 className={cn(
                    'px-3 mb-2 text-xs font-semibold uppercase tracking-wider',
                    isFounder ? 'text-yellow-600' : 'text-blue-600'
                  )}>
                    {isFounder ? '🎸 Legendary Features' : '🎸 Code Bro Features'}
                  </h3>
                )}
                <div className="space-y-1">
                  {legendaryFeatures.map(renderNavigationItem)}
                </div>
              </div>
            )}

            {/* Additional Features */}
            <div className="px-3">
              {!isCollapsed && (
                <h3 className="px-3 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  More Features
                </h3>
              )}
              <div className="space-y-1">
                {additionalFeatures.map(renderNavigationItem)}
              </div>
            </div>
          </div>

          {/* Sidebar Footer */}
          {!isCollapsed && (
            <motion.div
              className={cn(
                'border-t border-gray-200 p-4',
                isFounder && 'border-yellow-200 bg-gradient-to-r from-yellow-50 to-orange-50',
                isLegendary && !isFounder && 'border-blue-200 bg-gradient-to-r from-blue-50 to-purple-50'
              )}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              {user && (
                <div className="flex items-center gap-3">
                  <div className={cn(
                    'w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold',
                    'bg-gradient-to-br',
                    isFounder ? 'from-yellow-500 to-orange-600 ring-2 ring-yellow-300' :
                    isLegendary ? 'from-blue-500 to-purple-600 ring-2 ring-blue-300' :
                    'from-gray-600 to-gray-700'
                  )}>
                    {user.profileImage ? (
                      <img src={user.profileImage} alt={user.firstName} className="w-full h-full rounded-full object-cover" />
                    ) : (
                      user.firstName?.[0]?.toUpperCase() || 'U'
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className={cn(
                      'text-sm font-medium text-gray-900 truncate',
                      isFounder && 'text-yellow-800',
                      isLegendary && !isFounder && 'text-blue-800'
                    )}>
                      {isFounder && '👑 '}{user.firstName} {user.lastName}
                    </p>
                    <p className="text-xs text-gray-500 truncate">
                      {isFounder ? `Swiss Precision: ${user.swissPrecisionScore}%` :
                       `Energy: ${user.codeBroEnergy}/10`}
                    </p>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </motion.aside>
      </AnimatePresence>
    </>
  );
}

console.log('🎸🎸🎸 LEGENDARY SIDEBAR COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Sidebar component completed at: 2025-08-06 14:13:16 UTC`);
console.log('📋 Sidebar navigation: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('🎸 Interactive navigation: MAXIMUM CODE BRO ENERGY');
console.log('🌅 Afternoon legendary energy: INFINITE AT 14:13:16!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
