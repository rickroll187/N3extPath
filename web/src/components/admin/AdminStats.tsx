// File: web/src/components/admin/AdminStats.tsx
/**
 * 📊🎸 N3EXTPATH - LEGENDARY ADMIN STATS COMPONENT 🎸📊
 * Swiss precision admin analytics with infinite code bro energy
 * Built: 2025-08-06 17:32:35 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Crown, 
  Users, 
  Server, 
  Activity, 
  TrendingUp,
  TrendingDown,
  Database,
  Globe,
  Zap,
  Shield,
  CheckCircle,
  AlertTriangle,
  Clock,
  HardDrive,
  Wifi,
  Monitor,
  BarChart3,
  PieChart,
  LineChart,
  ArrowUp,
  ArrowDown,
  Minus,
  RefreshCw,
  Eye,
  Download,
  Upload,
  Target,
  Star,
  Trophy,
  Sparkles
} from 'lucide-react';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 📊 ADMIN STATS TYPES 📊
// =====================================

interface SystemMetrics {
  totalUsers: number;
  activeUsers: number;
  totalOKRs: number;
  completedOKRs: number;
  systemUptime: number;
  serverLoad: number;
  databaseConnections: number;
  totalSessions: number;
  apiRequests: number;
  storageUsed: number;
  bandwidthUsed: number;
  errorRate: number;
  averageResponseTime: number;
}

interface AdminStatsProps {
  metrics: SystemMetrics;
  isFounder?: boolean;
  showTrends?: boolean;
  onRefresh?: () => void;
}

// =====================================
// 🎸 STAT CARD COMPONENT 🎸
// =====================================

const AdminStatCard: React.FC<{
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
  progress?: {
    value: number;
    max: number;
    color?: string;
  };
  isFounder?: boolean;
  onClick?: () => void;
  size?: 'sm' | 'md' | 'lg';
}> = ({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  color, 
  trend, 
  progress, 
  isFounder = false, 
  onClick,
  size = 'md'
}) => {
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
          'h-full transition-all duration-200',
          size === 'sm' ? 'p-4' : size === 'lg' ? 'p-8' : 'p-6',
          isHovered && onClick && 'shadow-lg'
        )}
      >
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-3">
              <div className={cn(
                'rounded-xl',
                size === 'sm' ? 'p-2' : size === 'lg' ? 'p-4' : 'p-3',
                color,
                isFounder && 'bg-gradient-to-r from-yellow-100 to-orange-100 dark:from-yellow-900/30 dark:to-orange-900/30'
              )}>
                <Icon className={cn(
                  isFounder ? 'text-yellow-600' : 'text-current',
                  size === 'sm' ? 'w-4 h-4' : size === 'lg' ? 'w-8 h-8' : 'w-6 h-6'
                )} />
              </div>
              
              <div className="flex-1">
                <h3 className={cn(
                  'font-medium',
                  size === 'sm' ? 'text-xs' : 'text-sm',
                  isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-600 dark:text-gray-400'
                )}>
                  {title}
                </h3>
              </div>
            </div>

            <div className="mb-2">
              <div className="flex items-baseline gap-2">
                <span className={cn(
                  'font-bold',
                  size === 'sm' ? 'text-xl' : size === 'lg' ? 'text-4xl' : 'text-3xl',
                  isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                )}>
                  {typeof value === 'number' && value >= 1000000 
                    ? `${(value / 1000000).toFixed(1)}M`
                    : typeof value === 'number' && value >= 1000 
                      ? `${(value / 1000).toFixed(1)}K`
                      : value
                  }
                </span>
                
                {subtitle && (
                  <span className={cn(
                    'text-gray-500 dark:text-gray-400',
                    size === 'sm' ? 'text-xs' : 'text-sm'
                  )}>
                    {subtitle}
                  </span>
                )}
              </div>
            </div>

            {/* Progress Bar */}
            {progress && (
              <div className="mb-3">
                <ProgressBar
                  value={progress.value}
                  max={progress.max}
                  size={size === 'sm' ? 'sm' : 'md'}
                  color={progress.color || (isFounder ? 'gold' : 'blue')}
                  showLabel={false}
                />
                <div className={cn(
                  'flex justify-between mt-1',
                  size === 'sm' ? 'text-xs' : 'text-sm'
                )}>
                  <span className="text-gray-500 dark:text-gray-400">
                    {progress.value.toFixed(1)}%
                  </span>
                  <span className="text-gray-500 dark:text-gray-400">
                    {progress.max}% max
                  </span>
                </div>
              </div>
            )}

            {/* Trend Indicator */}
            {trend && TrendIcon && (
              <div className="flex items-center gap-2">
                <div className={cn(
                  'flex items-center gap-1 px-2 py-1 rounded-full font-medium',
                  size === 'sm' ? 'text-xs' : 'text-sm',
                  getTrendColor(),
                  trend.direction === 'up' ? 'bg-green-100 dark:bg-green-900/30' :
                  trend.direction === 'down' ? 'bg-red-100 dark:bg-red-900/30' :
                  'bg-gray-100 dark:bg-gray-900/30'
                )}>
                  <TrendIcon className={cn(
                    size === 'sm' ? 'w-3 h-3' : 'w-4 h-4'
                  )} />
                  <span>{trend.value}%</span>
                </div>
                
                <span className={cn(
                  'text-gray-500 dark:text-gray-400',
                  size === 'sm' ? 'text-xs' : 'text-sm'
                )}>
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
// 🎸 LEGENDARY ADMIN STATS 🎸
// =====================================

export const AdminStats: React.FC<AdminStatsProps> = ({
  metrics,
  isFounder = false,
  showTrends = true,
  onRefresh,
}) => {
  const [viewMode, setViewMode] = useState<'overview' | 'detailed'>('overview');

  useEffect(() => {
    console.log('📊🎸📊 LEGENDARY ADMIN STATS LOADED! 📊🎸📊');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Admin stats loaded at: 2025-08-06 17:32:35 UTC`);
    console.log('🌅 LATE AFTERNOON LEGENDARY ADMIN STATS ENERGY AT 17:32:35!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER ADMIN STATS ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER ADMIN STATS WITH INFINITE CODE BRO ENERGY!');
    }
  }, [isFounder]);

  // Mock trend data (in real app, this would come from historical data)
  const mockTrends = {
    totalUsers: { direction: 'up' as const, value: 15, label: 'from last week' },
    activeUsers: { direction: 'up' as const, value: 8, label: 'from yesterday' },
    totalOKRs: { direction: 'up' as const, value: 23, label: 'from last month' },
    systemUptime: { direction: 'stable' as const, value: 0, label: 'steady' },
    serverLoad: { direction: 'down' as const, value: 5, label: 'optimization' },
    storageUsed: { direction: 'up' as const, value: 3, label: 'growth' },
  };

  // Calculate derived metrics
  const derivedMetrics = useMemo(() => {
    const okrCompletionRate = metrics.totalOKRs > 0 ? (metrics.completedOKRs / metrics.totalOKRs) * 100 : 0;
    const userActivityRate = metrics.totalUsers > 0 ? (metrics.activeUsers / metrics.totalUsers) * 100 : 0;
    const systemHealthScore = ((metrics.systemUptime + (100 - metrics.serverLoad) + (100 - metrics.errorRate * 100)) / 3);
    
    return {
      okrCompletionRate,
      userActivityRate,
      systemHealthScore,
    };
  }, [metrics]);

  // Main overview stats
  const overviewStats = [
    {
      title: isFounder ? 'Total Platform Users' : 'Total Users',
      value: metrics.totalUsers,
      icon: Users,
      color: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
      trend: showTrends ? mockTrends.totalUsers : undefined,
      onClick: () => {
        if (isFounder) {
          toast.success('👑 Viewing all platform users with founder insights!');
        } else {
          toast.success('👥 Viewing user management panel!');
        }
      }
    },
    {
      title: 'Active Users',
      value: metrics.activeUsers,
      subtitle: `${derivedMetrics.userActivityRate.toFixed(1)}% active`,
      icon: Activity,
      color: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
      trend: showTrends ? mockTrends.activeUsers : undefined,
      progress: {
        value: derivedMetrics.userActivityRate,
        max: 100,
        color: 'green'
      },
      onClick: () => toast.success('⚡ Viewing active user analytics!')
    },
    {
      title: isFounder ? 'Platform OKRs' : 'Total OKRs',
      value: metrics.totalOKRs,
      subtitle: `${metrics.completedOKRs} completed`,
      icon: Target,
      color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400',
      trend: showTrends ? mockTrends.totalOKRs : undefined,
      progress: {
        value: derivedMetrics.okrCompletionRate,
        max: 100,
        color: 'purple'
      },
      onClick: () => {
        if (isFounder) {
          toast.success('👑 Viewing platform OKR analytics with founder metrics!');
        } else {
          toast.success('🎯 Viewing OKR management panel!');
        }
      }
    },
    {
      title: 'System Health',
      value: `${derivedMetrics.systemHealthScore.toFixed(1)}%`,
      icon: Shield,
      color: derivedMetrics.systemHealthScore >= 90 
        ? 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400'
        : derivedMetrics.systemHealthScore >= 75
          ? 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400'
          : 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400',
      progress: {
        value: derivedMetrics.systemHealthScore,
        max: 100,
        color: derivedMetrics.systemHealthScore >= 90 ? 'green' : derivedMetrics.systemHealthScore >= 75 ? 'yellow' : 'red'
      },
      onClick: () => toast.success('🛡️ Viewing system health dashboard!')
    },
  ];

  // Detailed system stats
  const systemStats = [
    {
      title: 'System Uptime',
      value: `${metrics.systemUptime.toFixed(2)}%`,
      icon: Clock,
      color: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
      progress: { value: metrics.systemUptime, max: 100, color: 'green' },
    },
    {
      title: 'Server Load',
      value: `${metrics.serverLoad.toFixed(1)}%`,
      icon: Server,
      color: metrics.serverLoad > 80 
        ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
        : metrics.serverLoad > 60
          ? 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400'
          : 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
      trend: showTrends ? mockTrends.serverLoad : undefined,
      progress: { 
        value: metrics.serverLoad, 
        max: 100, 
        color: metrics.serverLoad > 80 ? 'red' : metrics.serverLoad > 60 ? 'yellow' : 'green'
      },
    },
    {
      title: 'Database Connections',
      value: metrics.databaseConnections,
      icon: Database,
      color: 'bg-indigo-100 text-indigo-600 dark:bg-indigo-900/30 dark:text-indigo-400',
    },
    {
      title: 'Active Sessions',
      value: metrics.totalSessions,
      icon: Users,
      color: 'bg-cyan-100 text-cyan-600 dark:bg-cyan-900/30 dark:text-cyan-400',
    },
    {
      title: 'API Requests',
      value: `${(metrics.apiRequests / 1000).toFixed(1)}K`,
      subtitle: 'per hour',
      icon: Globe,
      color: 'bg-teal-100 text-teal-600 dark:bg-teal-900/30 dark:text-teal-400',
    },
    {
      title: 'Storage Used',
      value: `${metrics.storageUsed.toFixed(1)}%`,
      icon: HardDrive,
      color: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400',
      trend: showTrends ? mockTrends.storageUsed : undefined,
      progress: { 
        value: metrics.storageUsed, 
        max: 100, 
        color: metrics.storageUsed > 90 ? 'red' : metrics.storageUsed > 75 ? 'yellow' : 'green'
      },
    },
    {
      title: 'Bandwidth',
      value: `${metrics.bandwidthUsed.toFixed(1)} GB`,
      subtitle: 'today',
      icon: Wifi,
      color: 'bg-pink-100 text-pink-600 dark:bg-pink-900/30 dark:text-pink-400',
    },
    {
      title: 'Error Rate',
      value: `${(metrics.errorRate * 100).toFixed(3)}%`,
      icon: AlertTriangle,
      color: metrics.errorRate > 0.01 
        ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
        : 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
    },
    {
      title: 'Avg Response Time',
      value: `${metrics.averageResponseTime}ms`,
      icon: Zap,
      color: metrics.averageResponseTime > 200
        ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
        : metrics.averageResponseTime > 100
          ? 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400'
          : 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
    },
  ];

  // Founder exclusive stats
  const founderStats = isFounder ? [
    {
      title: 'Legendary Impact Score',
      value: '999.9%',
      icon: Crown,
      color: 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400',
      progress: { value: 100, max: 100, color: 'gold' },
    },
    {
      title: 'Code Bro Energy Generated',
      value: '∞',
      subtitle: 'infinite power',
      icon: Sparkles,
      color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400',
    },
    {
      title: 'Swiss Precision Level',
      value: '100%',
      icon: Star,
      color: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
      progress: { value: 100, max: 100, color: 'blue' },
    },
    {
      title: 'Platform Legendary Status',
      value: 'MAXIMUM',
      icon: Trophy,
      color: 'bg-gold-100 text-gold-600 dark:bg-gold-900/30 dark:text-gold-400',
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
            📊 {isFounder ? 'Legendary Platform Analytics' : 'System Analytics'}
          </motion.h2>

          <div className="flex items-center gap-2">
            <Activity className={cn(
              'w-4 h-4',
              isFounder ? 'text-yellow-600' : 'text-green-600'
            )} />
            <span className={cn(
              'text-sm font-medium',
              isFounder ? 'text-yellow-700 dark:text-yellow-300' : 'text-green-700 dark:text-green-300'
            )}>
              Live Data
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* View Mode Toggle */}
          <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
            <LegendaryButton
              variant={viewMode === 'overview' ? (isFounder ? "founder" : "primary") : "ghost"}
              size="sm"
              onClick={() => setViewMode('overview')}
              className="text-xs"
            >
              Overview
            </LegendaryButton>
            
            <LegendaryButton
              variant={viewMode === 'detailed' ? (isFounder ? "founder" : "primary") : "ghost"}
              size="sm"
              onClick={() => setViewMode('detailed')}
              className="text-xs"
            >
              Detailed
            </LegendaryButton>
          </div>

          {/* Action Buttons */}
          <LegendaryButton
            variant="ghost"
            size="sm"
            leftIcon={RefreshCw}
            onClick={onRefresh}
          >
            Refresh
          </LegendaryButton>

          <LegendaryButton
            variant="ghost"
            size="sm"
            leftIcon={Download}
            onClick={() => {
              toast.success(isFounder ? '👑 Exporting legendary admin report!' : '📊 Exporting admin report!');
            }}
          >
            Export
          </LegendaryButton>
        </div>
      </div>

      {/* Main Stats Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, staggerChildren: 0.1 }}
      >
        {overviewStats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
          >
            <AdminStatCard
              {...stat}
              isFounder={isFounder}
            />
          </motion.div>
        ))}
      </motion.div>

      {/* Founder Exclusive Stats */}
      {isFounder && founderStats.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <h3 className="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-4 flex items-center gap-2">
            <Crown className="w-5 h-5 text-yellow-600" />
            👑 LEGENDARY FOUNDER METRICS 👑
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            {founderStats.map((stat, index) => (
              <motion.div
                key={stat.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
              >
                <AdminStatCard
                  {...stat}
                  isFounder={true}
                  size="md"
                />
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Detailed System Stats */}
      <AnimatePresence>
        {viewMode === 'detailed' && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h3 className={cn(
              'text-lg font-semibold mb-4',
              isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
            )}>
              {isFounder ? 'Legendary System Metrics' : 'Detailed System Metrics'}
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {systemStats.map((stat, index) => (
                <motion.div
                  key={stat.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.05 }}
                >
                  <AdminStatCard
                    {...stat}
                    isFounder={isFounder}
                    size="sm"
                  />
                </motion.div>
              ))}
            </div>
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
            <Monitor className="w-4 h-4" />
            <span>Real-time monitoring</span>
          </div>
          
          <div className="flex items-center gap-1">
            <Zap className="w-4 h-4" />
            <span>Swiss precision analytics</span>
          </div>
          
          <div className="text-gray-400 font-mono">
            2025-08-06 17:32:35 UTC
          </div>
        </div>
        
        {isFounder && (
          <div className="mt-2">
            <span className="text-yellow-700 dark:text-yellow-300 font-bold text-sm">
              👑 RICKROLL187 FOUNDER ADMIN STATS • INFINITE ANALYTICAL POWER! 👑
            </span>
          </div>
        )}
      </motion.div>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY ADMIN STATS COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Admin stats component completed at: 2025-08-06 17:32:35 UTC`);
console.log('📊 Admin analytics: SWISS PRECISION');
console.log('👑 RICKROLL187 founder admin stats: LEGENDARY');
console.log('📈 Real-time monitoring: MAXIMUM INSIGHT');
console.log('🌅 LATE AFTERNOON LEGENDARY ADMIN STATS ENERGY: INFINITE AT 17:32:35!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
