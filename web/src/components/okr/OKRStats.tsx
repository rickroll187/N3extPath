// File: web/src/components/okr/OKRStats.tsx
/**
 * 📊🎸 N3EXTPATH - LEGENDARY OKR STATS COMPONENT 🎸📊
 * Swiss precision OKR analytics with infinite code bro energy
 * Built: 2025-08-06 17:12:03 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Crown, 
  Target, 
  TrendingUp, 
  TrendingDown,
  Award, 
  Activity, 
  Users,
  Calendar,
  BarChart3,
  PieChart,
  CheckCircle,
  Clock,
  Zap,
  Sparkles,
  Flame,
  Trophy,
  Star,
  ArrowUp,
  ArrowDown,
  Minus,
  ChevronDown,
  RefreshCw,
  Download,
  Filter
} from 'lucide-react';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 📊 OKR STATS TYPES 📊
// =====================================

interface OKRStatsData {
  total: number;
  completed: number;
  active: number;
  legendary: number;
  founderPriority: number;
  avgProgress: number;
  avgConfidence: number;
  completionRate: number;
}

interface OKRStatsProps {
  stats: OKRStatsData;
  isFounder?: boolean;
  period: string;
  onPeriodChange?: (period: string) => void;
  showTrends?: boolean;
  showDetails?: boolean;
}

// =====================================
// 🎸 STAT CARD COMPONENT 🎸
// =====================================

const StatCard: React.FC<{
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ElementType;
  color: string;
  trend?: {
    direction: 'up' | 'down' | 'stable';
    value: number;
    label: string;
  };
  isFounder?: boolean;
  onClick?: () => void;
}> = ({ title, value, subtitle, icon: Icon, color, trend, isFounder = false, onClick }) => {
  const [isHovered, setIsHovered] = useState(false);

  const getTrendIcon = () => {
    if (!trend) return null;
    switch (trend.direction) {
      case 'up': return ArrowUp;
      case 'down': return ArrowDown;
      default: return Minus;
    }
  };

  const getTrendColor = () => {
    if (!trend) return '';
    switch (trend.direction) {
      case 'up': return 'text-green-600';
      case 'down': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const TrendIcon = getTrendIcon();

  return (
    <motion.div
      className={cn(
        'cursor-pointer transition-all duration-200',
        onClick && 'hover:scale-105'
      )}
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      whileHover={onClick ? { y: -2 } : undefined}
      whileTap={onClick ? { scale: 0.98 } : undefined}
    >
      <LegendaryCard
        variant={isFounder ? 'founder' : 'elevated'}
        className={cn(
          'p-6 h-full transition-all duration-200',
          isHovered && onClick && 'shadow-lg'
        )}
      >
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <div className={cn(
                'p-3 rounded-xl',
                color,
                isFounder && 'bg-gradient-to-r from-yellow-100 to-orange-100 dark:from-yellow-900/30 dark:to-orange-900/30'
              )}>
                <Icon className={cn(
                  'w-6 h-6',
                  isFounder ? 'text-yellow-600' : 'text-current'
                )} />
              </div>
              
              <div className="flex-1">
                <h3 className={cn(
                  'text-sm font-medium',
                  isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-600 dark:text-gray-400'
                )}>
                  {title}
                </h3>
                
                <div className="flex items-baseline gap-2">
                  <span className={cn(
                    'text-3xl font-bold',
                    isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                  )}>
                    {value}
                  </span>
                  
                  {subtitle && (
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {subtitle}
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Trend Indicator */}
            {trend && TrendIcon && (
              <div className="flex items-center gap-1 mt-2">
                <div className={cn(
                  'flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium',
                  getTrendColor(),
                  trend.direction === 'up' ? 'bg-green-100 dark:bg-green-900/30' :
                  trend.direction === 'down' ? 'bg-red-100 dark:bg-red-900/30' :
                  'bg-gray-100 dark:bg-gray-900/30'
                )}>
                  <TrendIcon className="w-3 h-3" />
                  <span>{trend.value}%</span>
                </div>
                
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {trend.label}
                </span>
              </div>
            )}
          </div>
        </div>
      </LegendaryCard>
    </motion.div>
  );
};

// =====================================
// 🎸 LEGENDARY OKR STATS 🎸
// =====================================

export const OKRStats: React.FC<OKRStatsProps> = ({
  stats,
  isFounder = false,
  period,
  onPeriodChange,
  showTrends = true,
  showDetails = true,
}) => {
  const [showDetailedView, setShowDetailedView] = useState(false);
  const [selectedPeriod, setSelectedPeriod] = useState(period);

  useEffect(() => {
    console.log('📊🎸📊 LEGENDARY OKR STATS LOADED! 📊🎸📊');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`OKR stats loaded at: 2025-08-06 17:12:03 UTC`);
    console.log('🌅 LATE AFTERNOON LEGENDARY OKR STATS ENERGY AT 17:12:03!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER OKR STATS ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER OKR STATS WITH INFINITE CODE BRO ENERGY!');
    }
  }, [isFounder]);

  // Available periods
  const periods = [
    'Q3 2025',
    'Q2 2025', 
    'Q1 2025',
    '2025',
    'All Time'
  ];

  // Handle period change
  const handlePeriodChange = (newPeriod: string) => {
    setSelectedPeriod(newPeriod);
    onPeriodChange?.(newPeriod);
    
    if (isFounder) {
      toast.success(`👑 Founder view switched to ${newPeriod} with infinite analytics!`, {
        duration: 2000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '600',
        },
      });
    }
  };

  // Calculate derived stats
  const derivedStats = useMemo(() => {
    const onTrackRate = stats.total > 0 ? (stats.active / stats.total) * 100 : 0;
    const legendaryRate = stats.total > 0 ? (stats.legendary / stats.total) * 100 : 0;
    const founderRate = stats.total > 0 ? (stats.founderPriority / stats.total) * 100 : 0;
    
    return {
      onTrackRate,
      legendaryRate,
      founderRate,
      performanceScore: (stats.avgProgress + stats.avgConfidence) / 2,
    };
  }, [stats]);

  // Mock trend data (in real app, this would come from historical data)
  const mockTrends = {
    total: { direction: 'up' as const, value: 12, label: 'from last month' },
    completed: { direction: 'up' as const, value: 18, label: 'from last month' },
    active: { direction: 'stable' as const, value: 2, label: 'from last month' },
    avgProgress: { direction: 'up' as const, value: 8, label: 'from last week' },
  };

  // Main stat cards data
  const mainStats = [
    {
      title: isFounder ? 'Total Founder OKRs' : 'Total OKRs',
      value: stats.total,
      icon: Target,
      color: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
      trend: showTrends ? mockTrends.total : undefined,
      onClick: () => {
        if (isFounder) {
          toast.success('👑 Viewing all founder OKRs with infinite power!');
        } else {
          toast.success('🎯 Viewing all OKRs with Swiss precision!');
        }
      }
    },
    {
      title: 'Completed OKRs',
      value: stats.completed,
      subtitle: `${stats.completionRate.toFixed(1)}%`,
      icon: CheckCircle,
      color: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
      trend: showTrends ? mockTrends.completed : undefined,
      onClick: () => toast.success('✅ Viewing completed OKRs!')
    },
    {
      title: 'Active OKRs',
      value: stats.active,
      icon: Activity,
      color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400',
      trend: showTrends ? mockTrends.active : undefined,
      onClick: () => toast.success('⚡ Viewing active OKRs!')
    },
    {
      title: 'Average Progress',
      value: `${stats.avgProgress.toFixed(1)}%`,
      icon: BarChart3,
      color: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400',
      trend: showTrends ? mockTrends.avgProgress : undefined,
      onClick: () => toast.success('📊 Viewing progress analytics!')
    },
  ];

  // Additional stats for founder
  const founderStats = isFounder ? [
    {
      title: 'Legendary OKRs',
      value: stats.legendary,
      subtitle: `${derivedStats.legendaryRate.toFixed(1)}%`,
      icon: Sparkles,
      color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400',
      onClick: () => toast.success('✨ Viewing legendary OKRs!')
    },
    {
      title: 'Founder Priority',
      value: stats.founderPriority,
      subtitle: `${derivedStats.founderRate.toFixed(1)}%`,
      icon: Crown,
      color: 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400',
      onClick: () => toast.success('👑 Viewing founder priority OKRs!')
    },
    {
      title: 'Performance Score',
      value: `${derivedStats.performanceScore.toFixed(1)}%`,
      icon: Trophy,
      color: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400',
      onClick: () => toast.success('🏆 Viewing performance metrics!')
    },
    {
      title: 'Confidence Level',
      value: `${stats.avgConfidence.toFixed(1)}%`,
      icon: Star,
      color: 'bg-indigo-100 text-indigo-600 dark:bg-indigo-900/30 dark:text-indigo-400',
      onClick: () => toast.success('⭐ Viewing confidence analytics!')
    },
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
        <div className="flex items-center gap-4">
          <motion.h2 
            className={cn(
              'text-xl font-bold',
              isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
            )}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4 }}
          >
            {isFounder && <Crown className="inline w-5 h-5 mr-2 text-yellow-600" />}
            📊 {isFounder ? 'Founder Analytics' : 'OKR Analytics'}
          </motion.h2>

          <div className="flex items-center gap-2">
            <Activity className={cn(
              'w-4 h-4',
              isFounder ? 'text-yellow-600' : 'text-blue-600'
            )} />
            <span className={cn(
              'text-sm font-medium',
              isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-700 dark:text-gray-300'
            )}>
              Live Data
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Period Selector */}
          <div className="relative">
            <select
              value={selectedPeriod}
              onChange={(e) => handlePeriodChange(e.target.value)}
              className={cn(
                'pl-3 pr-8 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm',
                'focus:outline-none focus:ring-2 focus:ring-offset-2',
                'appearance-none cursor-pointer',
                isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
              )}
            >
              {periods.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>

          {/* Action Buttons */}
          <LegendaryButton
            variant="ghost"
            size="sm"
            leftIcon={RefreshCw}
            onClick={() => {
              toast.success(isFounder ? '👑 Refreshing founder analytics!' : '🔄 Refreshing analytics!');
            }}
          >
            Refresh
          </LegendaryButton>

          <LegendaryButton
            variant="ghost"
            size="sm"
            leftIcon={Download}
            onClick={() => {
              toast.success(isFounder ? '👑 Exporting founder report!' : '📊 Exporting report!');
            }}
          >
            Export
          </LegendaryButton>

          {showDetails && (
            <LegendaryButton
              variant={isFounder ? "founder" : "primary"}
              size="sm"
              leftIcon={showDetailedView ? PieChart : BarChart3}
              onClick={() => setShowDetailedView(!showDetailedView)}
            >
              {showDetailedView ? 'Simple' : 'Detailed'}
            </LegendaryButton>
          )}
        </div>
      </div>

      {/* Main Stats Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, staggerChildren: 0.1 }}
      >
        {mainStats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
          >
            <StatCard
              {...stat}
              isFounder={isFounder}
            />
          </motion.div>
        ))}
      </motion.div>

      {/* Founder Additional Stats */}
      {isFounder && founderStats.length > 0 && (
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4, staggerChildren: 0.1 }}
        >
          {founderStats.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
            >
              <StatCard
                {...stat}
                isFounder={isFounder}
              />
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Detailed View */}
      <AnimatePresence>
        {showDetailedView && (
          <motion.div
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.6 }}
          >
            {/* Progress Distribution */}
            <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className={cn(
                  'p-2 rounded-lg',
                  isFounder 
                    ? 'bg-yellow-100 dark:bg-yellow-900/30' 
                    : 'bg-blue-100 dark:bg-blue-900/30'
                )}>
                  <BarChart3 className={cn(
                    'w-5 h-5',
                    isFounder ? 'text-yellow-600' : 'text-blue-600'
                  )} />
                </div>
                
                <h3 className={cn(
                  'font-semibold',
                  isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                )}>
                  Progress Distribution
                </h3>
              </div>

              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600 dark:text-gray-400">Completion Rate</span>
                    <span className={cn(
                      'font-semibold',
                      isFounder ? 'text-yellow-700' : 'text-gray-900'
                    )}>
                      {stats.completionRate.toFixed(1)}%
                    </span>
                  </div>
                  <ProgressBar
                    value={stats.completionRate}
                    max={100}
                    color={isFounder ? 'gold' : 'green'}
                    size="lg"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600 dark:text-gray-400">Average Progress</span>
                    <span className={cn(
                      'font-semibold',
                      isFounder ? 'text-yellow-700' : 'text-gray-900'
                    )}>
                      {stats.avgProgress.toFixed(1)}%
                    </span>
                  </div>
                  <ProgressBar
                    value={stats.avgProgress}
                    max={100}
                    color={isFounder ? 'gold' : 'blue'}
                    size="lg"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600 dark:text-gray-400">Confidence Level</span>
                    <span className={cn(
                      'font-semibold',
                      isFounder ? 'text-yellow-700' : 'text-gray-900'
                    )}>
                      {stats.avgConfidence.toFixed(1)}%
                    </span>
                  </div>
                  <ProgressBar
                    value={stats.avgConfidence}
                    max={100}
                    color={isFounder ? 'gold' : 'purple'}
                    size="lg"
                  />
                </div>
              </div>
            </LegendaryCard>

            {/* Status Breakdown */}
            <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className={cn(
                  'p-2 rounded-lg',
                  isFounder 
                    ? 'bg-yellow-100 dark:bg-yellow-900/30' 
                    : 'bg-green-100 dark:bg-green-900/30'
                )}>
                  <PieChart className={cn(
                    'w-5 h-5',
                    isFounder ? 'text-yellow-600' : 'text-green-600'
                  )} />
                </div>
                
                <h3 className={cn(
                  'font-semibold',
                  isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                )}>
                  OKR Status Breakdown
                </h3>
              </div>

              <div className="space-y-3">
                {[
                  { label: 'Active', value: stats.active, color: 'bg-blue-500', total: stats.total },
                  { label: 'Completed', value: stats.completed, color: 'bg-green-500', total: stats.total },
                  ...(isFounder ? [
                    { label: 'Legendary', value: stats.legendary, color: 'bg-purple-500', total: stats.total },
                    { label: 'Founder Priority', value: stats.founderPriority, color: 'bg-yellow-500', total: stats.total },
                  ] : []),
                ].map((item) => (
                  <div key={item.label} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className={cn('w-3 h-3 rounded-full', item.color)} />
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {item.label}
                      </span>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-semibold text-gray-900 dark:text-white">
                        {item.value}
                      </span>
                      <span className="text-xs text-gray-500">
                        ({item.total > 0 ? ((item.value / item.total) * 100).toFixed(0) : 0}%)
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </LegendaryCard>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Bottom Status */}
      <motion.div
        className={cn(
          'text-center py-4 rounded-lg',
          'bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700',
          isFounder && 'bg-gradient-to-r from-yellow-50/50 to-orange-50/50 dark:from-yellow-900/10 dark:to-orange-900/10'
        )}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 1.0 }}
      >
        <div className="flex items-center justify-center gap-4 text-sm text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-1">
            <Zap className="w-4 h-4" />
            <span>Swiss precision analytics</span>
          </div>
          
          <div className="flex items-center gap-1">
            <Activity className="w-4 h-4" />
            <span>Real-time tracking</span>
          </div>
          
          <div className="text-gray-400 font-mono">
            2025-08-06 17:12:03 UTC
          </div>
        </div>
        
        {isFounder && (
          <div className="mt-2">
            <span className="text-yellow-700 dark:text-yellow-300 font-bold text-sm">
              👑 RICKROLL187 FOUNDER ANALYTICS • INFINITE STATISTICAL POWER! 👑
            </span>
          </div>
        )}
      </motion.div>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY OKR STATS COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`OKR stats component completed at: 2025-08-06 17:12:03 UTC`);
console.log('📊 OKR analytics: SWISS PRECISION');
console.log('👑 RICKROLL187 founder stats: LEGENDARY');
console.log('📈 Statistical tracking: MAXIMUM INSIGHT');
console.log('🌅 LATE AFTERNOON LEGENDARY OKR STATS ENERGY: INFINITE AT 17:12:03!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
