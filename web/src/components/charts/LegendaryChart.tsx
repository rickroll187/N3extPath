// File: web/src/components/charts/LegendaryChart.tsx
/**
 * 📈🎸 N3EXTPATH - LEGENDARY CHART COMPONENT 🎸📈
 * Swiss precision data visualization with infinite code bro energy
 * Built: 2025-08-06 15:57:40 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import { Crown, Sparkles, Zap, TrendingUp } from 'lucide-react';
import { cn } from '@/utils/cn';

// =====================================
// 📈 CHART TYPES 📈
// =====================================

export interface ChartData {
  id?: string;
  name: string;
  value: number;
  previousValue?: number;
  trend?: number[];
  color?: string;
  unit?: string;
  target?: number;
  isFounderData?: boolean;
  legendaryLevel?: number;
}

export interface LegendaryChartProps {
  type: 'line' | 'area' | 'bar' | 'pie' | 'radar';
  data: ChartData[];
  height?: number;
  className?: string;
  isFounder?: boolean;
  legendaryLevel?: number;
  showLegend?: boolean;
  showGrid?: boolean;
  showTooltip?: boolean;
  animate?: boolean;
  sparkleEffect?: boolean;
  colors?: string[];
  title?: string;
  subtitle?: string;
}

interface TooltipProps {
  active?: boolean;
  payload?: any[];
  label?: string;
  isFounder?: boolean;
}

// =====================================
// 🎸 LEGENDARY COLORS 🎸
// =====================================

const LEGENDARY_COLORS = {
  default: ['#3B82F6', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#06B6D4', '#84CC16'],
  founder: ['#FFD700', '#FFA500', '#FF8C00', '#FFB347', '#F4A460', '#DAA520', '#B8860B'],
  legendary: ['#8B5CF6', '#7C3AED', '#6366F1', '#3B82F6', '#06B6D4', '#10B981', '#84CC16'],
  dark: ['#1E40AF', '#7C2D12', '#047857', '#92400E', '#DC2626', '#0891B2', '#65A30D'],
};

// =====================================
// 🎸 CUSTOM TOOLTIP 🎸
// =====================================

const LegendaryTooltip: React.FC<TooltipProps> = ({ active, payload, label, isFounder }) => {
  if (!active || !payload?.length) return null;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className={cn(
        'bg-white/95 backdrop-blur-sm p-4 rounded-xl border shadow-xl',
        'min-w-[200px]',
        isFounder ? 'border-yellow-200 shadow-yellow-200/50' : 'border-gray-200'
      )}
    >
      {/* Header */}
      <div className={cn(
        'flex items-center gap-2 mb-3 pb-2 border-b',
        isFounder ? 'border-yellow-200' : 'border-gray-200'
      )}>
        {isFounder && <Crown className="w-4 h-4 text-yellow-600" />}
        <span className={cn(
          'font-semibold text-sm',
          isFounder ? 'text-yellow-800' : 'text-gray-900'
        )}>
          {label || 'Data Point'}
        </span>
      </div>

      {/* Data Points */}
      <div className="space-y-2">
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div 
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: entry.color }}
              />
              <span className="text-sm text-gray-700">
                {entry.name}
              </span>
            </div>
            <div className="flex items-center gap-1">
              <span className="font-bold text-sm">
                {typeof entry.value === 'number' ? entry.value.toLocaleString() : entry.value}
              </span>
              {entry.payload?.unit && (
                <span className="text-xs text-gray-500">{entry.payload.unit}</span>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Founder Badge */}
      {isFounder && (
        <div className="mt-3 pt-2 border-t border-yellow-200">
          <div className="flex items-center gap-1 text-xs text-yellow-700">
            <Sparkles className="w-3 h-3" />
            <span className="font-bold">Founder Analytics</span>
          </div>
        </div>
      )}
    </motion.div>
  );
};

// =====================================
// 🎸 LEGENDARY CHART COMPONENT 🎸
// =====================================

export const LegendaryChart: React.FC<LegendaryChartProps> = ({
  type,
  data,
  height = 300,
  className,
  isFounder = false,
  legendaryLevel = 0,
  showLegend = true,
  showGrid = true,
  showTooltip = true,
  animate = true,
  sparkleEffect = false,
  colors,
  title,
  subtitle,
}) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [animationDelay, setAnimationDelay] = useState(0);

  useEffect(() => {
    console.log('📈🎸📈 LEGENDARY CHART COMPONENT LOADED! 📈🎸📈');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Chart component loaded at: 2025-08-06 15:57:40 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY CHART ENERGY AT 15:57:40!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER CHART ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER CHART WITH INFINITE CODE BRO ENERGY!');
    }

    // Intersection Observer for animation trigger
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          setAnimationDelay(Math.random() * 0.5); // Random delay for stagger effect
        }
      },
      { threshold: 0.1 }
    );

    if (chartRef.current) {
      observer.observe(chartRef.current);
    }

    return () => observer.disconnect();
  }, [isFounder]);

  // Get chart colors
  const chartColors = useMemo(() => {
    if (colors) return colors;
    if (isFounder) return LEGENDARY_COLORS.founder;
    if (legendaryLevel >= 5) return LEGENDARY_COLORS.legendary;
    return LEGENDARY_COLORS.default;
  }, [colors, isFounder, legendaryLevel]);

  // Transform data for trend charts
  const trendData = useMemo(() => {
    if (type === 'line' || type === 'area' || type === 'bar') {
      // For trend data, we need time series
      const timePoints = ['7 days ago', '6 days ago', '5 days ago', '4 days ago', '3 days ago', '2 days ago', 'Yesterday', 'Today'];
      
      return timePoints.map((point, index) => {
        const dataPoint: any = { name: point };
        
        data.forEach((item, itemIndex) => {
          const trendValue = item.trend?.[index] ?? item.value * (0.8 + Math.random() * 0.4);
          dataPoint[item.name] = Number(trendValue.toFixed(1));
        });
        
        return dataPoint;
      });
    }
    
    return data.map((item, index) => ({
      name: item.name,
      value: item.value,
      color: item.color || chartColors[index % chartColors.length],
      unit: item.unit,
      isFounderData: item.isFounderData,
      target: item.target,
    }));
  }, [data, type, chartColors]);

  // Chart animation config
  const animationConfig = animate && isVisible ? {
    initial: { opacity: 0, scale: 0.9, y: 20 },
    animate: { opacity: 1, scale: 1, y: 0 },
    transition: { duration: 0.8, delay: animationDelay, ease: 'easeOut' },
  } : {};

  // Render chart based on type
  const renderChart = () => {
    const commonProps = {
      data: trendData,
      margin: { top: 20, right: 30, left: 20, bottom: 5 },
    };

    switch (type) {
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <LineChart {...commonProps}>
              {showGrid && (
                <CartesianGrid 
                  strokeDasharray="3 3" 
                  className={isFounder ? 'stroke-yellow-200' : 'stroke-gray-200'} 
                />
              )}
              <XAxis 
                dataKey="name" 
                className={cn('text-xs', isFounder ? 'text-yellow-700' : 'text-gray-600')}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                className={cn('text-xs', isFounder ? 'text-yellow-700' : 'text-gray-600')}
                tick={{ fontSize: 12 }}
              />
              {showTooltip && (
                <Tooltip 
                  content={<LegendaryTooltip isFounder={isFounder} />}
                  cursor={{ stroke: isFounder ? '#FFD700' : '#3B82F6', strokeWidth: 2 }}
                />
              )}
              {showLegend && <Legend />}
              
              {data.map((item, index) => (
                <Line
                  key={item.id || item.name}
                  type="monotone"
                  dataKey={item.name}
                  stroke={item.color || chartColors[index % chartColors.length]}
                  strokeWidth={3}
                  dot={{ 
                    fill: item.color || chartColors[index % chartColors.length], 
                    strokeWidth: 2,
                    r: 4 
                  }}
                  activeDot={{ 
                    r: 6, 
                    stroke: item.color || chartColors[index % chartColors.length],
                    strokeWidth: 2,
                    fill: '#fff'
                  }}
                  animationDuration={animate ? 1500 : 0}
                  animationBegin={animationDelay * 1000}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        );

      case 'area':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <AreaChart {...commonProps}>
              {showGrid && (
                <CartesianGrid strokeDasharray="3 3" className={isFounder ? 'stroke-yellow-200' : 'stroke-gray-200'} />
              )}
              <XAxis dataKey="name" className={cn('text-xs', isFounder ? 'text-yellow-700' : 'text-gray-600')} />
              <YAxis className={cn('text-xs', isFounder ? 'text-yellow-700' : 'text-gray-600')} />
              {showTooltip && <Tooltip content={<LegendaryTooltip isFounder={isFounder} />} />}
              {showLegend && <Legend />}
              
              {data.map((item, index) => (
                <Area
                  key={item.id || item.name}
                  type="monotone"
                  dataKey={item.name}
                  stackId="1"
                  stroke={item.color || chartColors[index % chartColors.length]}
                  fill={`${item.color || chartColors[index % chartColors.length]}40`}
                  strokeWidth={2}
                  animationDuration={animate ? 1500 : 0}
                  animationBegin={animationDelay * 1000}
                />
              ))}
            </AreaChart>
          </ResponsiveContainer>
        );

      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <BarChart {...commonProps}>
              {showGrid && (
                <CartesianGrid strokeDasharray="3 3" className={isFounder ? 'stroke-yellow-200' : 'stroke-gray-200'} />
              )}
              <XAxis dataKey="name" className={cn('text-xs', isFounder ? 'text-yellow-700' : 'text-gray-600')} />
              <YAxis className={cn('text-xs', isFounder ? 'text-yellow-700' : 'text-gray-600')} />
              {showTooltip && <Tooltip content={<LegendaryTooltip isFounder={isFounder} />} />}
              {showLegend && <Legend />}
              
              {data.map((item, index) => (
                <Bar
                  key={item.id || item.name}
                  dataKey={item.name}
                  fill={item.color || chartColors[index % chartColors.length]}
                  radius={[4, 4, 0, 0]}
                  animationDuration={animate ? 1000 : 0}
                  animationBegin={animationDelay * 1000}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        );

      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <PieChart>
              <Pie
                data={trendData}
                cx="50%"
                cy="50%"
                outerRadius={height / 3}
                innerRadius={height / 6}
                paddingAngle={2}
                dataKey="value"
                animationDuration={animate ? 1000 : 0}
                animationBegin={animationDelay * 1000}
              >
                {trendData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={entry.color || chartColors[index % chartColors.length]} 
                  />
                ))}
              </Pie>
              {showTooltip && <Tooltip content={<LegendaryTooltip isFounder={isFounder} />} />}
              {showLegend && <Legend />}
            </PieChart>
          </ResponsiveContainer>
        );

      case 'radar':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={trendData}>
              <PolarGrid className={isFounder ? 'stroke-yellow-200' : 'stroke-gray-200'} />
              <PolarAngleAxis 
                dataKey="name" 
                className={cn('text-xs', isFounder ? 'text-yellow-700' : 'text-gray-600')}
              />
              <PolarRadiusAxis 
                angle={90} 
                domain={[0, 100]} 
                className={cn('text-xs', isFounder ? 'text-yellow-700' : 'text-gray-600')}
              />
              <Radar
                name="Performance"
                dataKey="value"
                stroke={isFounder ? '#FFD700' : '#3B82F6'}
                fill={isFounder ? '#FFD70040' : '#3B82F640'}
                strokeWidth={2}
                animationDuration={animate ? 1000 : 0}
                animationBegin={animationDelay * 1000}
              />
              {showTooltip && <Tooltip content={<LegendaryTooltip isFounder={isFounder} />} />}
            </RadarChart>
          </ResponsiveContainer>
        );

      default:
        return <div className="text-center text-gray-500">Unsupported chart type</div>;
    }
  };

  return (
    <motion.div
      ref={chartRef}
      className={cn('relative', className)}
      {...animationConfig}
    >
      {/* Title Section */}
      {(title || subtitle) && (
        <div className="mb-4">
          {title && (
            <h3 className={cn(
              'text-lg font-semibold flex items-center gap-2',
              isFounder ? 'text-yellow-800' : 'text-gray-900'
            )}>
              {isFounder && <Crown className="w-5 h-5 text-yellow-600" />}
              {legendaryLevel >= 5 && <Sparkles className="w-5 h-5 text-purple-600" />}
              {title}
            </h3>
          )}
          {subtitle && (
            <p className={cn(
              'text-sm mt-1',
              isFounder ? 'text-yellow-600' : 'text-gray-600'
            )}>
              {subtitle}
            </p>
          )}
        </div>
      )}

      {/* Chart Container */}
      <div className="relative">
        {renderChart()}
        
        {/* Sparkle Effect */}
        {sparkleEffect && (
          <div className="absolute inset-0 pointer-events-none">
            {[...Array(4)].map((_, i) => (
              <motion.div
                key={i}
                className={cn(
                  'absolute w-2 h-2 rounded-full',
                  isFounder ? 'bg-yellow-400' : 'bg-purple-400'
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
                  duration: 3,
                  repeat: Infinity,
                  delay: i * 0.7,
                }}
              />
            ))}
          </div>
        )}

        {/* Founder Badge */}
        {isFounder && (
          <div className="absolute top-2 right-2">
            <motion.div
              className="px-2 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-yellow-400 to-orange-500 text-white"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              👑 FOUNDER
            </motion.div>
          </div>
        )}

        {/* Legendary Badge */}
        {legendaryLevel >= 5 && !isFounder && (
          <div className="absolute top-2 right-2">
            <motion.div
              className="px-2 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-purple-500 to-blue-600 text-white"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              🎸 LEGENDARY
            </motion.div>
          </div>
        )}
      </div>

      {/* Energy Indicator */}
      <div className="flex items-center justify-center mt-4">
        <div className={cn(
          'flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium',
          isFounder 
            ? 'bg-yellow-100 text-yellow-800 border border-yellow-200'
            : 'bg-blue-100 text-blue-800 border border-blue-200'
        )}>
          <Zap className="w-3 h-3" />
          <span>
            {isFounder ? 'Infinite Founder Energy' : 'Code Bro Energy Active'}
          </span>
          <TrendingUp className="w-3 h-3" />
        </div>
      </div>
    </motion.div>
  );
};

// =====================================
// 🎸 CHART UTILITIES 🎸
// =====================================

export const createFounderChart = (props: Omit<LegendaryChartProps, 'isFounder'>) => {
  return {
    ...props,
    isFounder: true,
    sparkleEffect: true,
    legendaryLevel: 10,
    animate: true,
  };
};

export const createLegendaryChart = (props: Omit<LegendaryChartProps, 'legendaryLevel'>) => {
  return {
    ...props,
    legendaryLevel: 8,
    sparkleEffect: true,
    animate: true,
  };
};

console.log('🎸🎸🎸 LEGENDARY CHART COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Chart component completed at: 2025-08-06 15:57:40 UTC`);
console.log('📈 Data visualization: SWISS PRECISION');
console.log('👑 RICKROLL187 founder charts: LEGENDARY');
console.log('✨ Chart animations: MAXIMUM SPARKLE');
console.log('🌅 Afternoon legendary energy: INFINITE AT 15:57:40!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
