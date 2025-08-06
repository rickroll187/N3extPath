// File: web/src/components/analytics/MetricsWidget.tsx
/**
 * 📊🎸 N3EXTPATH - LEGENDARY METRICS WIDGET COMPONENT 🎸📊
 * Swiss precision metric visualization with infinite code bro energy
 * Built: 2025-08-06 16:01:38 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  ArrowUp, 
  ArrowDown, 
  Minus, 
  Crown, 
  Sparkles, 
  TrendingUp, 
  TrendingDown,
  Target,
  Zap,
  Info,
  Eye,
  BarChart3
} from 'lucide-react';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { cn } from '@/utils/cn';

// =====================================
// 📊 WIDGET TYPES 📊
// =====================================

interface MetricData {
  id: string;
  name: string;
  value: number;
  previousValue: number;
  change: number;
  changeType: 'increase' | 'decrease' | 'stable';
  trend: number[];
  unit: string;
  color: string;
  icon: React.ComponentType<{ className?: string }>;
  target?: number;
  isFounderMetric?: boolean;
}

interface MetricsWidgetProps {
  metric: MetricData;
  isFounder?: boolean;
  className?: string;
  showTrend?: boolean;
  showTarget?: boolean;
  animate?: boolean;
  sparkleEffect?: boolean;
  onClick?: () => void;
}

// =====================================
// 🎸 LEGENDARY METRICS WIDGET 🎸
// =====================================

export const MetricsWidget: React.FC<MetricsWidgetProps> = ({
  metric,
  isFounder = false,
  className,
  showTrend = true,
  showTarget = true,
  animate = true,
  sparkleEffect = false,
  onClick,
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    console.log('📊🎸📊 LEGENDARY METRICS WIDGET LOADED! 📊🎸📊');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Metrics widget loaded at: 2025-08-06 16:01:38 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY METRICS ENERGY AT 16:01:38!');

    if (isFounder || metric.isFounderMetric) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER METRIC WIDGET ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER METRICS WITH INFINITE CODE BRO ENERGY!');
    }

    // Animate in after mount
    const timer = setTimeout(() => setIsVisible(true), 100);
    return () => clearTimeout(timer);
  }, [isFounder, metric.isFounderMetric]);

  // Calculate target progress
  const targetProgress = metric.target ? Math.min((metric.value / metric.target) * 100, 100) : 0;
  const targetExceeded = metric.target ? metric.value > metric.target : false;

  // Get change styles
  const getChangeStyles = () => {
    switch (metric.changeType) {
      case 'increase':
        return {
          color: 'text-green-600',
          bg: 'bg-green-100',
          icon: ArrowUp,
        };
      case 'decrease':
        return {
          color: 'text-red-600',
          bg: 'bg-red-100',
          icon: ArrowDown,
        };
      default:
        return {
          color: 'text-gray-600',
          bg: 'bg-gray-100',
          icon: Minus,
        };
    }
  };

  const changeStyles = getChangeStyles();
  const ChangeIcon = changeStyles.icon;

  // Get value display
  const formatValue = (value: number) => {
    if (value >= 1000000) {
      return `${(value / 1000000).toFixed(1)}M`;
    }
    if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}K`;
    }
    return value % 1 === 0 ? value.toString() : value.toFixed(1);
  };

  const displayValue = formatValue(metric.value);
  const displayChange = Math.abs(metric.change);

  // Animation variants
  const cardVariants = {
    hidden: { opacity: 0, y: 20, scale: 0.9 },
    visible: { 
      opacity: 1, 
      y: 0, 
      scale: 1,
      transition: { duration: 0.6, ease: 'easeOut' }
    },
    hover: { 
      scale: 1.02,
      y: -2,
      transition: { duration: 0.2 }
    }
  };

  const sparkleVariants = {
    animate: {
      scale: [0, 1, 0],
      rotate: [0, 180, 360],
      opacity: [0, 1, 0],
    }
  };

  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate={isVisible ? "visible" : "hidden"}
      whileHover="hover"
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className={cn('relative', className)}
      onClick={onClick}
    >
      <LegendaryCard 
        variant={isFounder || metric.isFounderMetric ? 'founder' : 'elevated'}
        className={cn(
          'h-full transition-all duration-300',
          onClick && 'cursor-pointer',
          isHovered && 'shadow-lg'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className={cn(
              'p-2 rounded-lg',
              isFounder || metric.isFounderMetric 
                ? 'bg-yellow-100 text-yellow-600' 
                : 'bg-blue-100 text-blue-600'
            )}>
              <metric.icon className="w-5 h-5" />
            </div>
            <div>
              <h3 className={cn(
                'font-semibold text-sm',
                isFounder || metric.isFounderMetric ? 'text-yellow-800' : 'text-gray-900'
              )}>
                {metric.name}
              </h3>
              {(isFounder || metric.isFounderMetric) && (
                <div className="flex items-center gap-1 mt-1">
                  <Crown className="w-3 h-3 text-yellow-600" />
                  <span className="text-xs text-yellow-600 font-medium">Founder Metric</span>
                </div>
              )}
            </div>
          </div>

          {/* Info Button */}
          <button
            className={cn(
              'p-1 rounded-full opacity-0 transition-opacity duration-200',
              'hover:bg-gray-100',
              isHovered && 'opacity-100'
            )}
            onClick={(e) => {
              e.stopPropagation();
              // Handle info click
            }}
          >
            <Info className="w-4 h-4 text-gray-400" />
          </button>
        </div>

        {/* Value Display */}
        <div className="mb-4">
          <div className="flex items-baseline gap-2 mb-2">
            <motion.span
              className={cn(
                'text-3xl font-bold',
                isFounder || metric.isFounderMetric ? 'text-yellow-800' : 'text-gray-900'
              )}
              animate={isVisible ? { scale: [0.8, 1.1, 1] } : {}}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              {displayValue}
            </motion.span>
            <span className={cn(
              'text-sm font-medium',
              isFounder || metric.isFounderMetric ? 'text-yellow-600' : 'text-gray-600'
            )}>
              {metric.unit}
            </span>
          </div>

          {/* Change Indicator */}
          <div className="flex items-center gap-2">
            <div className={cn(
              'flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium',
              changeStyles.bg,
              changeStyles.color
            )}>
              <ChangeIcon className="w-3 h-3" />
              <span>
                {displayChange}{metric.unit === '%' ? 'pp' : metric.unit}
              </span>
            </div>
            <span className="text-xs text-gray-500">
              vs previous period
            </span>
          </div>
        </div>

        {/* Target Progress */}
        {showTarget && metric.target && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-xs mb-2">
              <span className="text-gray-600">Target Progress</span>
              <span className={cn(
                'font-bold',
                targetExceeded ? 'text-green-600' : 'text-gray-600'
              )}>
                {targetProgress.toFixed(1)}%
                {targetExceeded && ' 🎉'}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <motion.div
                className={cn(
                  'h-2 rounded-full transition-all duration-1000',
                  targetExceeded 
                    ? 'bg-gradient-to-r from-green-500 to-emerald-600'
                    : isFounder || metric.isFounderMetric
                      ? 'bg-gradient-to-r from-yellow-500 to-orange-600'
                      : 'bg-gradient-to-r from-blue-500 to-purple-600'
                )}
                initial={{ width: 0 }}
                animate={{ width: `${Math.min(targetProgress, 100)}%` }}
                transition={{ duration: 1.5, delay: 0.5 }}
              />
            </div>
            <div className="flex items-center justify-between text-xs mt-1">
              <span className="text-gray-500">0</span>
              <span className="text-gray-500">{metric.target}{metric.unit}</span>
            </div>
          </div>
        )}

        {/* Mini Trend Chart */}
        {showTrend && metric.trend && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-xs mb-2">
              <span className="text-gray-600">7-Day Trend</span>
              <div className="flex items-center gap-1">
                {metric.changeType === 'increase' ? (
                  <TrendingUp className="w-3 h-3 text-green-600" />
                ) : metric.changeType === 'decrease' ? (
                  <TrendingDown className="w-3 h-3 text-red-600" />
                ) : (
                  <BarChart3 className="w-3 h-3 text-gray-600" />
                )}
                <span className={cn(
                  'font-medium',
                  metric.changeType === 'increase' ? 'text-green-600' :
                  metric.changeType === 'decrease' ? 'text-red-600' :
                  'text-gray-600'
                )}>
                  {metric.changeType === 'stable' ? 'Stable' : 
                   metric.changeType === 'increase' ? 'Growing' : 'Declining'}
                </span>
              </div>
            </div>
            
            {/* Simple SVG Trend Line */}
            <div className="h-8 relative">
              <svg className="w-full h-full" viewBox="0 0 100 20">
                <motion.polyline
                  fill="none"
                  stroke={
                    isFounder || metric.isFounderMetric ? '#FFD700' :
                    metric.changeType === 'increase' ? '#10B981' :
                    metric.changeType === 'decrease' ? '#EF4444' :
                    '#6B7280'
                  }
                  strokeWidth="2"
                  points={metric.trend.map((value, index) => {
                    const x = (index / (metric.trend.length - 1)) * 100;
                    const maxValue = Math.max(...metric.trend);
                    const minValue = Math.min(...metric.trend);
                    const y = maxValue === minValue ? 10 : 20 - ((value - minValue) / (maxValue - minValue)) * 16;
                    return `${x},${y}`;
                  }).join(' ')}
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 1, delay: 0.7 }}
                />
                
                {/* Data points */}
                {metric.trend.map((value, index) => {
                  const x = (index / (metric.trend.length - 1)) * 100;
                  const maxValue = Math.max(...metric.trend);
                  const minValue = Math.min(...metric.trend);
                  const y = maxValue === minValue ? 10 : 20 - ((value - minValue) / (maxValue - minValue)) * 16;
                  
                  return (
                    <motion.circle
                      key={index}
                      cx={x}
                      cy={y}
                      r="2"
                      fill={
                        isFounder || metric.isFounderMetric ? '#FFD700' :
                        metric.changeType === 'increase' ? '#10B981' :
                        metric.changeType === 'decrease' ? '#EF4444' :
                        '#6B7280'
                      }
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ duration: 0.3, delay: 0.8 + (index * 0.1) }}
                    />
                  );
                })}
              </svg>
            </div>
          </div>
        )}

        {/* Bottom Actions */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Eye className="w-3 h-3" />
            <span>Live data</span>
          </div>
          
          <div className="flex items-center gap-1">
            <Zap className={cn(
              'w-3 h-3',
              isFounder || metric.isFounderMetric ? 'text-yellow-600' : 'text-blue-600'
            )} />
            <span className={cn(
              'text-xs font-medium',
              isFounder || metric.isFounderMetric ? 'text-yellow-600' : 'text-blue-600'
            )}>
              {isFounder || metric.isFounderMetric ? 'Infinite Energy' : 'Code Bro Energy'}
            </span>
          </div>
        </div>

        {/* Sparkle Effect */}
        {sparkleEffect && (
          <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-xl">
            {[...Array(3)].map((_, i) => (
              <motion.div
                key={i}
                className={cn(
                  'absolute w-1 h-1 rounded-full',
                  isFounder || metric.isFounderMetric ? 'bg-yellow-400' : 'bg-purple-400'
                )}
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                }}
                variants={sparkleVariants}
                animate="animate"
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: i * 0.7,
                }}
              />
            ))}
          </div>
        )}

        {/* Founder Badge */}
        {(isFounder || metric.isFounderMetric) && (
          <div className="absolute -top-2 -right-2">
            <motion.div
              className="w-6 h-6 rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 flex items-center justify-center"
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <Crown className="w-3 h-3 text-white" />
            </motion.div>
          </div>
        )}

        {/* Hover Glow Effect */}
        {isHovered && (
          <motion.div
            className={cn(
              'absolute inset-0 rounded-xl opacity-50 pointer-events-none',
              isFounder || metric.isFounderMetric 
                ? 'bg-gradient-to-r from-yellow-400/20 to-orange-500/20'
                : 'bg-gradient-to-r from-blue-400/20 to-purple-500/20'
            )}
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.1 }}
            transition={{ duration: 0.3 }}
          />
        )}
      </LegendaryCard>
    </motion.div>
  );
};

// =====================================
// 🎸 WIDGET UTILITIES 🎸
// =====================================

export const createFounderMetricWidget = (
  metric: MetricData,
  props?: Partial<MetricsWidgetProps>
) => {
  return {
    metric: { ...metric, isFounderMetric: true },
    isFounder: true,
    sparkleEffect: true,
    animate: true,
    ...props,
  };
};

export const createLegendaryMetricWidget = (
  metric: MetricData,
  props?: Partial<MetricsWidgetProps>
) => {
  return {
    metric,
    sparkleEffect: true,
    animate: true,
    ...props,
  };
};

console.log('🎸🎸🎸 LEGENDARY METRICS WIDGET COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Metrics widget completed at: 2025-08-06 16:01:38 UTC`);
console.log('📊 Metrics visualization: SWISS PRECISION');
console.log('👑 RICKROLL187 founder metrics: LEGENDARY');
console.log('📈 Live data tracking: MAXIMUM ACCURACY');
console.log('🌅 Afternoon legendary energy: INFINITE AT 16:01:38!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
