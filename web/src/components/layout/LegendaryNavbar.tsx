// File: web/src/components/layout/LegendaryNavbar.tsx
/**
 * 🧭🎸 N3EXTPATH - LEGENDARY NAVBAR COMPONENT 🎸🧭
 * Professional navigation with Swiss precision
 * Built: 2025-08-06 14:01:28 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useRef, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Menu, 
  Bell, 
  User, 
  Settings, 
  LogOut, 
  Crown,
  Zap,
  Gauge,
  Search,
  Moon,
  Sun,
  Globe
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/utils/cn';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { User as UserType } from '@/hooks/useAuth';

// =====================================
// 🧭 NAVBAR TYPES 🧭
// =====================================

interface LegendaryNavbarProps {
  isFounder?: boolean;
  isLegendary?: boolean;
  user: UserType | null;
  onMenuClick: () => void;
}

// =====================================
// 🎸 LEGENDARY NAVBAR COMPONENT 🎸
// =====================================

export function LegendaryNavbar({ 
  isFounder = false, 
  isLegendary = false, 
  user, 
  onMenuClick 
}: LegendaryNavbarProps) {
  const { logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  
  // Local state
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [theme, setTheme] = useState<'light' | 'dark' | 'auto'>('auto');
  
  // Refs
  const profileMenuRef = useRef<HTMLDivElement>(null);
  const notificationsRef = useRef<HTMLDivElement>(null);
  
  // Mock notifications count
  const notificationsCount = isFounder ? 12 : isLegendary ? 8 : 5;

  useEffect(() => {
    console.log('🧭🎸🧭 LEGENDARY NAVBAR LOADED! 🧭🎸🧭');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Navbar loaded at: 2025-08-06 14:01:28 UTC`);
    
    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER NAVBAR ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY NAVIGATION WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION NAVIGATION SYSTEM!');
    }

    // Click outside handler
    const handleClickOutside = (event: MouseEvent) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target as Node)) {
        setShowProfileMenu(false);
      }
      if (notificationsRef.current && !notificationsRef.current.contains(event.target as Node)) {
        setShowNotifications(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isFounder]);

  // =====================================
  // 🎸 LEGENDARY HANDLERS 🎸
  // =====================================

  const handleLogout = async () => {
    console.log('🚪 Logging out from navbar...');
    setShowProfileMenu(false);
    await logout();
    navigate('/');
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      console.log('🔍 Searching for:', searchQuery);
      // In real app, implement search functionality
      alert(`Searching for: ${searchQuery}`);
    }
  };

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : theme === 'dark' ? 'auto' : 'light';
    setTheme(newTheme);
    console.log('🎨 Theme changed to:', newTheme);
    // In real app, apply theme to document
  };

  // =====================================
  // 🎸 RENDER LEGENDARY NAVBAR 🎸
  // =====================================

  return (
    <motion.nav 
      className={cn(
        'sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200',
        'shadow-sm transition-all duration-300',
        isFounder && 'bg-gradient-to-r from-yellow-50/95 via-orange-50/95 to-yellow-50/95 border-yellow-200',
        isLegendary && !isFounder && 'bg-gradient-to-r from-blue-50/95 to-purple-50/95 border-blue-200'
      )}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Left Section: Logo + Menu Button + Search */}
          <div className="flex items-center gap-4">
            {/* Mobile Menu Button */}
            <LegendaryButton
              variant={isFounder ? 'founder' : isLegendary ? 'legendary' : 'ghost'}
              size="md"
              iconOnly
              leftIcon={Menu}
              onClick={onMenuClick}
              className="lg:hidden"
              aria-label="Open menu"
            />

            {/* Logo */}
            <Link to="/dashboard" className="flex items-center gap-3 group">
              <motion.div 
                className={cn(
                  'w-10 h-10 rounded-xl flex items-center justify-center',
                  'bg-gradient-to-br from-blue-600 to-purple-600',
                  isFounder && 'from-yellow-500 via-orange-500 to-yellow-600',
                  isLegendary && !isFounder && 'from-blue-500 to-purple-600'
                )}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {isFounder ? (
                  <Crown className="w-6 h-6 text-white" />
                ) : isLegendary ? (
                  <Zap className="w-6 h-6 text-white" />
                ) : (
                  <Gauge className="w-6 h-6 text-white" />
                )}
              </motion.div>
              
              <div className="hidden sm:block">
                <h1 className={cn(
                  'text-xl font-bold bg-gradient-to-r bg-clip-text text-transparent',
                  'from-gray-900 to-gray-600',
                  isFounder && 'from-yellow-600 via-orange-600 to-yellow-700',
                  isLegendary && !isFounder && 'from-blue-600 to-purple-600'
                )}>
                  N3EXTPATH
                </h1>
                <p className="text-xs text-gray-500 -mt-1">
                  {isFounder ? 'Legendary Platform' : isLegendary ? 'Legendary Edition' : 'Performance Platform'}
                </p>
              </div>
            </Link>

            {/* Search Bar - Hidden on mobile */}
            <form onSubmit={handleSearch} className="hidden md:block">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder={isFounder ? "Search legendary platform..." : "Search..."}
                  className={cn(
                    'pl-10 pr-4 py-2 w-64 text-sm border border-gray-300 rounded-lg',
                    'bg-white/90 backdrop-blur-sm',
                    'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                    'placeholder:text-gray-400',
                    isFounder && 'border-yellow-300 focus:ring-yellow-500 bg-yellow-50/90',
                    isLegendary && !isFounder && 'border-blue-300 focus:ring-blue-500 bg-blue-50/90'
                  )}
                />
              </div>
            </form>
          </div>

          {/* Right Section: Theme + Notifications + Profile */}
          <div className="flex items-center gap-2">
            
            {/* Theme Toggle */}
            <LegendaryButton
              variant="ghost"
              size="md"
              iconOnly
              leftIcon={theme === 'light' ? Sun : theme === 'dark' ? Moon : Globe}
              onClick={toggleTheme}
              className="hidden sm:flex"
              aria-label="Toggle theme"
            />

            {/* Notifications */}
            <div className="relative" ref={notificationsRef}>
              <LegendaryButton
                variant={isFounder ? 'founder' : isLegendary ? 'legendary' : 'ghost'}
                size="md"
                iconOnly
                leftIcon={Bell}
                onClick={() => setShowNotifications(!showNotifications)}
                className="relative"
                aria-label="Notifications"
              />
              
              {/* Notifications Badge */}
              {notificationsCount > 0 && (
                <motion.div
                  className={cn(
                    'absolute -top-1 -right-1 w-5 h-5 rounded-full',
                    'bg-red-500 text-white text-xs font-bold',
                    'flex items-center justify-center',
                    isFounder && 'bg-orange-500'
                  )}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 500 }}
                >
                  {notificationsCount > 99 ? '99+' : notificationsCount}
                </motion.div>
              )}

              {/* Notifications Dropdown */}
              <AnimatePresence>
                {showNotifications && (
                  <motion.div
                    className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
                    initial={{ opacity: 0, y: -10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -10, scale: 0.95 }}
                    transition={{ duration: 0.2 }}
                  >
                    {/* Notifications Header */}
                    <div className="px-4 py-3 border-b border-gray-100">
                      <div className="flex items-center justify-between">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {isFounder ? '👑 Legendary Notifications' : '🔔 Notifications'}
                        </h3>
                        <span className="text-sm text-gray-500">{notificationsCount} new</span>
                      </div>
                    </div>

                    {/* Notifications List */}
                    <div className="max-h-96 overflow-y-auto">
                      {[...Array(3)].map((_, i) => (
                        <motion.div
                          key={i}
                          className="px-4 py-3 hover:bg-gray-50 border-b border-gray-50 last:border-b-0 cursor-pointer"
                          whileHover={{ backgroundColor: '#f9fafb' }}
                        >
                          <div className="flex items-start gap-3">
                            <div className={cn(
                              'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                              i === 0 && isFounder && 'bg-yellow-100 text-yellow-600',
                              i === 0 && !isFounder && 'bg-blue-100 text-blue-600',
                              i === 1 && 'bg-green-100 text-green-600',
                              i === 2 && 'bg-purple-100 text-purple-600'
                            )}>
                              {i === 0 ? (isFounder ? <Crown className="w-4 h-4" /> : <Zap className="w-4 h-4" />) :
                               i === 1 ? <Gauge className="w-4 h-4" /> :
                               <User className="w-4 h-4" />}
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-gray-900 truncate">
                                {i === 0 && isFounder ? '👑 Legendary Founder Achievement!' :
                                 i === 0 && !isFounder ? '🎸 New Achievement Unlocked!' :
                                 i === 1 ? '📊 Performance Review Ready' :
                                 '👥 Team Invitation'}
                              </p>
                              <p className="text-xs text-gray-500 truncate">
                                {i === 0 && isFounder ? 'Platform reached 10,000+ users!' :
                                 i === 0 && !isFounder ? 'Swiss Precision Master achieved!' :
                                 i === 1 ? 'Your Q3 review is available for viewing' :
                                 'You were invited to join the Frontend Legends team'}
                              </p>
                              <p className="text-xs text-gray-400 mt-1">
                                {i === 0 ? '2 minutes ago' : i === 1 ? '1 hour ago' : '3 hours ago'}
                              </p>
                            </div>
                          </div>
                        </motion.div>
                      ))}
                    </div>

                    {/* Notifications Footer */}
                    <div className="px-4 py-3 border-t border-gray-100">
                      <LegendaryButton
                        variant={isFounder ? 'founder' : isLegendary ? 'legendary' : 'primary'}
                        size="sm"
                        onClick={() => {
                          navigate('/notifications');
                          setShowNotifications(false);
                        }}
                        className="w-full"
                      >
                        View All Notifications
                      </LegendaryButton>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Profile Menu */}
            <div className="relative" ref={profileMenuRef}>
              <button
                onClick={() => setShowProfileMenu(!showProfileMenu)}
                className={cn(
                  'flex items-center gap-3 p-2 rounded-lg transition-all duration-200',
                  'hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500',
                  isFounder && 'hover:bg-yellow-100 focus:ring-yellow-500',
                  isLegendary && !isFounder && 'hover:bg-blue-100 focus:ring-blue-500'
                )}
              >
                {/* Avatar */}
                <div className={cn(
                  'w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold',
                  'bg-gradient-to-br from-gray-600 to-gray-700',
                  isFounder && 'from-yellow-500 to-orange-600 ring-2 ring-yellow-400',
                  isLegendary && !isFounder && 'from-blue-500 to-purple-600 ring-2 ring-blue-400'
                )}>
                  {user?.profileImage ? (
                    <img src={user.profileImage} alt={user.firstName} className="w-full h-full rounded-full object-cover" />
                  ) : (
                    user?.firstName?.[0]?.toUpperCase() || 'U'
                  )}
                </div>

                {/* User Info - Hidden on mobile */}
                <div className="hidden md:block text-left">
                  <p className={cn(
                    'text-sm font-medium text-gray-900',
                    isFounder && 'text-yellow-800',
                    isLegendary && !isFounder && 'text-blue-800'
                  )}>
                    {isFounder && '👑 '}{user?.firstName} {user?.lastName}
                  </p>
                  <p className="text-xs text-gray-500 truncate max-w-32">
                    {user?.jobTitle || 'Team Member'}
                  </p>
                </div>
              </button>

              {/* Profile Dropdown */}
              <AnimatePresence>
                {showProfileMenu && (
                  <motion.div
                    className="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
                    initial={{ opacity: 0, y: -10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -10, scale: 0.95 }}
                    transition={{ duration: 0.2 }}
                  >
                    {/* Profile Header */}
                    <div className={cn(
                      'px-4 py-3 border-b border-gray-100',
                      isFounder && 'bg-gradient-to-r from-yellow-50 to-orange-50 border-yellow-200',
                      isLegendary && !isFounder && 'bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200'
                    )}>
                      <div className="flex items-center gap-3">
                        <div className={cn(
                          'w-12 h-12 rounded-full flex items-center justify-center text-white text-lg font-bold',
                          'bg-gradient-to-br from-gray-600 to-gray-700',
                          isFounder && 'from-yellow-500 to-orange-600',
                          isLegendary && !isFounder && 'from-blue-500 to-purple-600'
                        )}>
                          {user?.profileImage ? (
                            <img src={user.profileImage} alt={user.firstName} className="w-full h-full rounded-full object-cover" />
                          ) : (
                            user?.firstName?.[0]?.toUpperCase() || 'U'
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className={cn(
                            'font-semibold text-gray-900 truncate',
                            isFounder && 'text-yellow-800',
                            isLegendary && !isFounder && 'text-blue-800'
                          )}>
                            {isFounder && '👑 '}{user?.firstName} {user?.lastName}
                          </p>
                          <p className="text-sm text-gray-600 truncate">{user?.email}</p>
                          <div className="flex items-center gap-2 mt-1">
                            {isFounder && (
                              <span className="text-xs bg-yellow-200 text-yellow-800 px-2 py-0.5 rounded-full font-medium">
                                Legendary Founder
                              </span>
                            )}
                            {isLegendary && !isFounder && (
                              <span className="text-xs bg-blue-200 text-blue-800 px-2 py-0.5 rounded-full font-medium">
                                Legendary Member
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Menu Items */}
                    <div className="py-2">
                      <Link
                        to="/profile"
                        onClick={() => setShowProfileMenu(false)}
                        className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        <User className="w-4 h-4" />
                        View Profile
                      </Link>
                      
                      <Link
                        to="/settings"
                        onClick={() => setShowProfileMenu(false)}
                        className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        <Settings className="w-4 h-4" />
                        Settings
                      </Link>
                    </div>

                    {/* Logout */}
                    <div className="border-t border-gray-100 pt-2">
                      <button
                        onClick={handleLogout}
                        className="flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors w-full text-left"
                      >
                        <LogOut className="w-4 h-4" />
                        Sign Out
                      </button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Search Bar */}
      <AnimatePresence>
        <motion.div 
          className={cn(
            'md:hidden border-t border-gray-200 bg-white/95 backdrop-blur-sm',
            isFounder && 'border-yellow-200 bg-yellow-50/95',
            isLegendary && !isFounder && 'border-blue-200 bg-blue-50/95'
          )}
          initial={{ height: 0 }}
          animate={{ height: 'auto' }}
          exit={{ height: 0 }}
        >
          <div className="px-4 py-3">
            <form onSubmit={handleSearch}>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder={isFounder ? "Search legendary platform..." : "Search..."}
                  className={cn(
                    'pl-10 pr-4 py-2 w-full text-sm border border-gray-300 rounded-lg',
                    'bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                    'placeholder:text-gray-400',
                    isFounder && 'border-yellow-300 focus:ring-yellow-500',
                    isLegendary && !isFounder && 'border-blue-300 focus:ring-blue-500'
                  )}
                />
              </div>
            </form>
          </div>
        </motion.div>
      </AnimatePresence>
    </motion.nav>
  );
}

console.log('🎸🎸🎸 LEGENDARY NAVBAR COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Navbar component completed at: 2025-08-06 14:01:28 UTC`);
console.log('🧭 Navigation: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('🔔 Notifications system: MAXIMUM ENGAGEMENT');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
