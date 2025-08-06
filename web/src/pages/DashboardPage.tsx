// File: web/src/pages/DashboardPage.tsx
/**
 * 📊🎸 N3EXTPATH - LEGENDARY DASHBOARD PAGE 🎸📊
 * Professional dashboard with Swiss precision
 * Built: 2025-08-06 14:30:15 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Helmet } from 'react-helmet-async';
import { 
  Crown,
  Zap,
  TrendingUp,
  Target,
  Users,
  Award,
  Calendar,
  Clock,
  BarChart3,
  Activity,
  Sparkles,
  Coffee,
  Gauge,
  Star,
  ChevronRight,
  Plus,
  Bell,
  CheckCircle,
  AlertCircle,
  Info
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 📊 DASHBOARD TYPES 📊
// =====================================

interface MetricCard {
  id: string;
  title: string;
  value: string | number;
  change: string;
  changeType: 'positive' | 'negative' | 'neutral';
  icon: React.ComponentType<{ className?: string; size?: number }>;
  color: 'blue' | 'green' | 'yellow' | 'purple' | 'red';
  isNew?: boolean;
}

interface ActivityItem {
  id: string;
  type: 'achievement' | 'review' | 'okr' | 'team' | 'system';
  title: string;
  description: string;
  timestamp: Date;
  icon: React.ComponentType<{ className?: string; size?: number }>;
  color: string;
}

interface QuickAction {
  id: string;
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string; size?: number }>;
  color: string;
  onClick: () => void;
}

// =====================================
// 📊 DASHBOARD PAGE COMPONENT 📊
// =====================================

export function DashboardPage() {
  const { user, getUserDisplayName, getGreeting, isFounder, isLegendary } = useAuth();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    console.log('📊🎸📊 LEGENDARY DASHBOARD PAGE LOADED! 📊🎸📊');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Dashboard page loaded at: 2025-08-06 14:30:15 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY ENERGY AT 14:30:15!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER DASHBOARD ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER DASHBOARD WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER DASHBOARD SYSTEM!');
      console.log('🌅 AFTERNOON FOUNDER POWER AT 14:30:15!');
      
      toast.success('👑 Welcome to your LEGENDARY FOUNDER DASHBOARD! Infinite code bro energy activated!', {
        duration: 5000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    } else if (isLegendary) {
      console.log('🎸 LEGENDARY USER DASHBOARD ACTIVATED!');
      toast.success('🎸 Welcome back, legendary code bro! Your dashboard is loaded with Swiss precision!', {
        duration: 4000,
      });
    }

    setIsLoaded(true);

    // Update time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, [isFounder, isLegendary]);

  // =====================================
  // 🎸 LEGENDARY DASHBOARD DATA 🎸
  // =====================================

  const metrics: MetricCard[] = [
    {
      id: 'performance-score',
      title: isFounder ? 'Legendary Founder Score' : 'Swiss Precision Score',
      value: isFounder ? '100%' : `${user?.swissPrecisionScore || 85}%`,
      change: isFounder ? 'Maximum Level' : '+12%',
      changeType: 'positive',
      icon: isFounder ? Crown : Gauge,
      color: isFounder ? 'yellow' : 'blue',
      isNew: !isFounder,
    },
    {
      id: 'code-bro-energy',
      title: 'Code Bro Energy',
      value: `${user?.codeBroEnergy || 8}/10`,
      change: isFounder ? 'Infinite' : '+2',
      changeType: 'positive',
      icon: Zap,
      color: 'purple',
    },
    {
      id: 'achievements',
      title: 'Achievements Unlocked',
      value: isFounder ? '∞' : user?.achievements?.length || 5,
      change: isFounder ? 'All Unlocked' : '+3 this week',
      changeType: 'positive',
      icon: Award,
      color: 'green',
    },
    {
      id: 'active-okrs',
      title: 'Active OKRs',
      value: isFounder ? '12' : '4',
      change: isFounder ? 'Platform Goals' : '2 completed',
      changeType: 'positive',
      icon: Target,
      color: 'red',
    },
  ];

  const recentActivity: ActivityItem[] = [
    {
      id: '1',
      type: isFounder ? 'system' : 'achievement',
      title: isFounder ? 'Platform Milestone Reached' : 'Swiss Precision Master Achieved',
      description: isFounder ? '10,000+ users joined the legendary platform!' : 'Congratulations on achieving 90%+ performance score!',
      timestamp: new Date(Date.now() - 2 * 60 * 1000), // 2 minutes ago
      icon: isFounder ? Crown : Award,
      color: isFounder ? 'text-yellow-600' : 'text-green-600',
    },
    {
      id: '2',
      type: 'review',
      title: isFounder ? 'Founder Review Complete' : 'Performance Review Ready',
      description: isFounder ? 'Legendary founder quarterly review completed with infinite energy!' : 'Your Q3 performance review is available for viewing.',
      timestamp: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
      icon: BarChart3,
      color: 'text-blue-600',
    },
    {
      id: '3',
      type: 'okr',
      title: isFounder ? 'Platform OKR Updated' : 'OKR Progress Updated',
      description: isFounder ? 'User growth objective exceeded expectations!' : 'Project delivery objective is 75% complete.',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      icon: Target,
      color: 'text-orange-600',
    },
    {
      id: '4',
      type: 'team',
      title: isFounder ? 'New Team Formed' : 'Team Collaboration',
      description: isFounder ? 'Frontend Legends team created with 12 legendary members!' : 'You were added to the Mobile Development team.',
      timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
      icon: Users,
      color: 'text-purple-600',
    },
  ];

  const quickActions: QuickAction[] = [
    {
      id: 'new-okr',
      title: isFounder ? 'Create Platform Goal' : 'Create New OKR',
      description: isFounder ? 'Set legendary platform objectives' : 'Define your next performance objective',
      icon: Target,
      color: 'bg-blue-500 hover:bg-blue-600',
      onClick: () => toast.success('🎯 OKR creation coming soon with legendary precision!'),
    },
    {
      id: 'schedule-review',
      title: isFounder ? 'Founder Review' : 'Schedule Review',
      description: isFounder ? 'Legendary founder performance analysis' : 'Book your next performance review',
      icon: Calendar,
      color: 'bg-green-500 hover:bg-green-600',
      onClick: () => toast.success('📅 Review scheduling coming soon with Swiss precision!'),
    },
    {
      id: 'view-analytics',
      title: isFounder ? 'Platform Analytics' : 'View Analytics',
      description: isFounder ? 'Deep platform insights and metrics' : 'Check your performance analytics',
      icon: BarChart3,
      color: 'bg-purple-500 hover:bg-purple-600',
      onClick: () => toast.success('📊 Analytics dashboard coming soon with legendary insights!'),
    },
    {
      id: 'team-management',
      title: isFounder ? 'Manage Platform' : 'Join Team',
      description: isFounder ? 'Manage users and legendary features' : 'Connect with your team members',
      icon: isFounder ? Crown : Users,
      color: isFounder ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-indigo-500 hover:bg-indigo-600',
      onClick: () => toast.success(isFounder ? '👑 Platform management coming soon!' : '👥 Team features coming soon!'),
    },
  ];

  // =====================================
  // 🎸 LEGENDARY HANDLERS 🎸
  // =====================================

  const getTimeOfDay = () => {
    const hour = currentTime.getHours();
    if (hour < 12) return '🌅 Morning';
    if (hour < 17) return '🌞 Afternoon';
    if (hour < 21) return '🌆 Evening';
    return '🌙 Night';
  };

  const formatTimeAgo = (timestamp: Date) => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  };

  // =====================================
  // 🎸 RENDER LEGENDARY DASHBOARD 🎸
  // =====================================

  return (
    <>
      <Helmet>
        <title>
          {isFounder ? '👑 Legendary Founder Dashboard | N3EXTPATH' : 'Dashboard | N3EXTPATH Legendary Platform'}
        </title>
        <meta 
          name="description" 
          content={isFounder 
            ? "RICKROLL187 founder dashboard with infinite code bro energy and Swiss precision platform management" 
            : "Your legendary performance dashboard with Swiss precision metrics and code bro energy tracking"
          } 
        />
      </Helmet>

      <div className={cn(
        'min-h-screen bg-gradient-to-br',
        isFounder ? 'from-yellow-50 via-white to-orange-50' : 'from-blue-50 via-white to-purple-50'
      )}>
        
        {/* Header Section */}
        <motion.div 
          className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-40"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: isLoaded ? 1 : 0, y: isLoaded ? 0 : -20 }}
          transition={{ duration: 0.6 }}
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
              
              {/* Welcome Message */}
              <div>
                <motion.h1 
                  className={cn(
                    'text-2xl sm:text-3xl font-bold flex items-center gap-3',
                    isFounder ? 'text-yellow-800' : 'text-gray-900'
                  )}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  {isFounder && <Crown className="w-8 h-8 text-yellow-600" />}
                  {getGreeting()}
                </motion.h1>
                
                <motion.div 
                  className="flex items-center gap-4 mt-2"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: 0.3 }}
                >
                  <p className="text-gray-600">
                    {getTimeOfDay()} legendary energy • {currentTime.toLocaleString('en-US', { 
                      weekday: 'long', 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}
                  </p>
                  <div className={cn(
                    'text-sm font-mono font-bold px-3 py-1 rounded-full',
                    isFounder ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'
                  )}>
                    {currentTime.toISOString().replace('T', ' ').slice(11, 19)} UTC
                  </div>
                </div>
              </div>

              {/* Quick Stats */}
              <motion.div 
                className="flex items-center gap-6"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                {isFounder && (
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-600">∞</div>
                    <div className="text-xs text-gray-500">Founder Power</div>
                  </div>
                )}
                
                <div className="text-center">
                  <div className={cn(
                    'text-2xl font-bold',
                    isFounder ? 'text-yellow-600' : 'text-blue-600'
                  )}>
                    {user?.swissPrecisionScore || 100}%
                  </div>
                  <div className="text-xs text-gray-500">Swiss Precision</div>
                </div>
                
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {isFounder ? '∞' : user?.codeBroEnergy || 10}/10
                  </div>
                  <div className="text-xs text-gray-500">Code Bro Energy</div>
                </div>
              </motion.div>
            </div>
          </div>
        </motion.div>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          
          {/* Metrics Grid */}
          <motion.div 
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            {metrics.map((metric, index) => (
              <motion.div
                key={metric.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 + (index * 0.1) }}
              >
                <LegendaryCard 
                  variant={isFounder && metric.color === 'yellow' ? 'founder' : 'elevated'}
                  hover
                  interactive
                  className="h-full relative group"
                >
                  {metric.isNew && (
                    <div className="absolute top-3 right-3">
                      <span className="px-2 py-1 text-xs font-bold bg-green-100 text-green-800 rounded-full">
                        NEW
                      </span>
                    </div>
                  )}
                  
                  <div className="flex items-center justify-between mb-4">
                    <div className={cn(
                      'w-12 h-12 rounded-xl flex items-center justify-center',
                      'group-hover:scale-110 transition-transform duration-300',
                      metric.color === 'blue' && 'bg-blue-100 text-blue-600',
                      metric.color === 'green' && 'bg-green-100 text-green-600',
                      metric.color === 'yellow' && 'bg-yellow-100 text-yellow-600',
                      metric.color === 'purple' && 'bg-purple-100 text-purple-600',
                      metric.color === 'red' && 'bg-red-100 text-red-600',
                      isFounder && metric.color === 'yellow' && 'bg-gradient-to-br from-yellow-200 to-orange-200'
                    )}>
                      <metric.icon className="w-6 h-6" />
                    </div>
                    
                    <div className={cn(
                      'text-sm font-medium px-2 py-1 rounded-full',
                      metric.changeType === 'positive' && 'bg-green-100 text-green-700',
                      metric.changeType === 'negative' && 'bg-red-100 text-red-700',
                      metric.changeType === 'neutral' && 'bg-gray-100 text-gray-700'
                    )}>
                      {metric.change}
                    </div>
                  </div>
                  
                  <h3 className="text-sm font-medium text-gray-600 mb-2">
                    {metric.title}
                  </h3>
                  
                  <div className={cn(
                    'text-3xl font-bold',
                    isFounder && metric.color === 'yellow' ? 'text-yellow-700' : 'text-gray-900'
                  )}>
                    {metric.value}
                  </div>
                </LegendaryCard>
              </motion.div>
            ))}
          </motion.div>

          {/* Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Quick Actions */}
            <motion.div 
              className="lg:col-span-1"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 1.0 }}
            >
              <LegendaryCard 
                variant={isFounder ? 'founder' : 'elevated'}
                header={
                  <div className="flex items-center justify-between">
                    <h2 className={cn(
                      'text-lg font-semibold',
                      isFounder ? 'text-yellow-800' : 'text-gray-900'
                    )}>
                      {isFounder ? '👑 Founder Actions' : '🚀 Quick Actions'}
                    </h2>
                    <Sparkles className={cn(
                      'w-5 h-5',
                      isFounder ? 'text-yellow-600' : 'text-blue-600'
                    )} />
                  </div>
                }
              >
                <div className="space-y-3">
                  {quickActions.map((action, index) => (
                    <motion.button
                      key={action.id}
                      onClick={action.onClick}
                      className="w-full p-4 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-md transition-all duration-200 text-left group"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 1.1 + (index * 0.1) }}
                    >
                      <div className="flex items-center gap-3">
                        <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center text-white', action.color)}>
                          <action.icon className="w-5 h-5" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-medium text-gray-900 group-hover:text-gray-700">
                            {action.title}
                          </h3>
                          <p className="text-sm text-gray-600">
                            {action.description}
                          </p>
                        </div>
                        <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-gray-600" />
                      </div>
                    </motion.button>
                  ))}
                </div>
              </LegendaryCard>
            </motion.div>

            {/* Recent Activity */}
            <motion.div 
              className="lg:col-span-2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 1.2 }}
            >
              <LegendaryCard 
                variant={isFounder ? 'founder' : 'elevated'}
                header={
                  <div className="flex items-center justify-between">
                    <h2 className={cn(
                      'text-lg font-semibold',
                      isFounder ? 'text-yellow-800' : 'text-gray-900'
                    )}>
                      {isFounder ? '👑 Legendary Activity' : '📊 Recent Activity'}
                    </h2>
                    <Activity className={cn(
                      'w-5 h-5',
                      isFounder ? 'text-yellow-600' : 'text-blue-600'
                    )} />
                  </div>
                }
              >
                <div className="space-y-4">
                  {recentActivity.map((activity, index) => (
                    <motion.div
                      key={activity.id}
                      className="flex items-start gap-4 p-4 rounded-lg hover:bg-gray-50 transition-colors duration-200"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 1.3 + (index * 0.1) }}
                    >
                      <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center bg-gray-100', activity.color)}>
                        <activity.icon className="w-5 h-5" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-gray-900 truncate">
                          {activity.title}
                        </h3>
                        <p className="text-sm text-gray-600 mt-1">
                          {activity.description}
                        </p>
                        <p className="text-xs text-gray-500 mt-2 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {formatTimeAgo(activity.timestamp)}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </LegendaryCard>
            </motion.div>
          </div>

          {/* Bottom Message */}
          <motion.div
            className="mt-12 text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.8 }}
          >
            <div className={cn(
              'inline-flex items-center gap-2 px-6 py-3 rounded-full text-sm font-medium',
              'bg-gradient-to-r border-2',
              isFounder 
                ? 'from-yellow-100 via-orange-100 to-yellow-100 border-yellow-300 text-yellow-800'
                : 'from-blue-100 via-purple-100 to-blue-100 border-blue-300 text-blue-800'
            )}>
              <Coffee className="w-4 h-4" />
              <span>
                🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸
              </span>
              {isFounder && <Crown className="w-4 h-4" />}
            </div>
            
            {isFounder && (
              <motion.p 
                className="text-sm text-yellow-700 mt-3 font-bold"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.6, delay: 2.0 }}
              >
                👑 RICKROLL187 FOUNDER DASHBOARD • AFTERNOON LEGENDARY ENERGY AT 14:30:15 UTC! 👑
              </motion.p>
            )}
          </motion.div>
        </div>
      </div>
    </>
  );
}

console.log('🎸🎸🎸 LEGENDARY DASHBOARD PAGE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Dashboard page completed at: 2025-08-06 14:30:15 UTC`);
console.log('📊 Dashboard UI: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('🎸 Code bro dashboard experience: MAXIMUM ENERGY');
console.log('🌅 Afternoon legendary energy: INFINITE AT 14:30:15!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
