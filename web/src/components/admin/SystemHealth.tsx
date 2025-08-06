// File: web/src/components/admin/SystemHealth.tsx
/**
 * 🖥️🎸 N3EXTPATH - LEGENDARY SYSTEM HEALTH COMPONENT 🎸🖥️
 * Swiss precision system monitoring with infinite code bro energy
 * Built: 2025-08-06 17:43:16 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Crown, 
  Server, 
  Database, 
  Monitor, 
  Activity, 
  Cpu,
  HardDrive,
  MemoryStick,
  Wifi,
  Globe,
  Zap,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Clock,
  TrendingUp,
  TrendingDown,
  BarChart3,
  PieChart,
  LineChart,
  RefreshCw,
  Play,
  Pause,
  Stop,
  Settings,
  Download,
  Upload,
  Terminal,
  Code,
  Bug,
  Shield,
  Lock,
  Eye,
  AlertCircle,
  Info,
  Thermometer,
  Radio,
  NetworkIcon as Network
} from 'lucide-react';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 🖥️ SYSTEM HEALTH TYPES 🖥️
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

interface SystemService {
  id: string;
  name: string;
  status: 'running' | 'stopped' | 'error' | 'warning';
  uptime: number;
  memory: number;
  cpu: number;
  lastRestart: Date;
  version: string;
  description: string;
}

interface SystemHealthProps {
  metrics: SystemMetrics | null;
  isFounder?: boolean;
  onRefresh?: () => void;
}

// =====================================
// 🎸 SERVICE STATUS COMPONENT 🎸
// =====================================

const ServiceStatus: React.FC<{
  service: SystemService;
  onAction: (serviceId: string, action: 'start' | 'stop' | 'restart') => void;
  isFounder: boolean;
}> = ({ service, onAction, isFounder }) => {
  const [isActioning, setIsActioning] = useState(false);

  // Get status info
  const getStatusInfo = () => {
    switch (service.status) {
      case 'running':
        return { 
          color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
          icon: CheckCircle,
          label: 'Running'
        };
      case 'stopped':
        return { 
          color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
          icon: Stop,
          label: 'Stopped'
        };
      case 'error':
        return { 
          color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
          icon: XCircle,
          label: 'Error'
        };
      default:
        return { 
          color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
          icon: AlertTriangle,
          label: 'Warning'
        };
    }
  };

  const statusInfo = getStatusInfo();
  const StatusIcon = statusInfo.icon;

  // Handle service action
  const handleAction = async (action: 'start' | 'stop' | 'restart') => {
    setIsActioning(true);
    
    try {
      // Simulate action delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      onAction(service.id, action);
      
      if (isFounder) {
        toast.success(`👑 FOUNDER ACTION: Service ${service.name} ${action}ed with infinite power!`, {
          duration: 3000,
          style: {
            background: 'linear-gradient(135deg, #FFD700, #FFA500)',
            color: '#000000',
            fontWeight: '700',
          },
        });
      } else {
        toast.success(`✅ Service ${service.name} ${action}ed successfully!`);
      }
      
    } catch (error) {
      toast.error(`❌ Failed to ${action} service ${service.name}`);
    } finally {
      setIsActioning(false);
    }
  };

  // Format uptime
  const formatUptime = (minutes: number) => {
    const days = Math.floor(minutes / (24 * 60));
    const hours = Math.floor((minutes % (24 * 60)) / 60);
    const mins = minutes % 60;
    
    if (days > 0) return `${days}d ${hours}h ${mins}m`;
    if (hours > 0) return `${hours}h ${mins}m`;
    return `${mins}m`;
  };

  return (
    <motion.div
      className={cn(
        'p-4 border rounded-lg',
        service.status === 'running' ? 'border-green-200 bg-green-50/30 dark:border-green-700 dark:bg-green-900/10' :
        service.status === 'error' ? 'border-red-200 bg-red-50/30 dark:border-red-700 dark:bg-red-900/10' :
        service.status === 'warning' ? 'border-yellow-200 bg-yellow-50/30 dark:border-yellow-700 dark:bg-yellow-900/10' :
        'border-gray-200 bg-gray-50/30 dark:border-gray-700 dark:bg-gray-800/30'
      )}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Service Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className={cn(
            'flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium',
            statusInfo.color
          )}>
            <StatusIcon className="w-3 h-3" />
            <span>{statusInfo.label}</span>
          </div>
          
          <div>
            <h4 className={cn(
              'font-semibold',
              isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
            )}>
              {service.name}
            </h4>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              v{service.version}
            </p>
          </div>
        </div>

        {/* Service Actions */}
        <div className="flex items-center gap-1">
          {service.status === 'stopped' && (
            <LegendaryButton
              variant={isFounder ? "founder" : "primary"}
              size="sm"
              onClick={() => handleAction('start')}
              disabled={isActioning}
              leftIcon={Play}
              className="text-xs"
            >
              Start
            </LegendaryButton>
          )}
          
          {service.status === 'running' && (
            <>
              <LegendaryButton
                variant="secondary"
                size="sm"
                onClick={() => handleAction('restart')}
                disabled={isActioning}
                leftIcon={RefreshCw}
                className="text-xs"
              >
                Restart
              </LegendaryButton>
              
              <LegendaryButton
                variant="ghost"
                size="sm"
                onClick={() => handleAction('stop')}
                disabled={isActioning}
                leftIcon={Pause}
                className="text-xs text-red-600"
              >
                Stop
              </LegendaryButton>
            </>
          )}

          {service.status === 'error' && (
            <LegendaryButton
              variant={isFounder ? "founder" : "primary"}
              size="sm"
              onClick={() => handleAction('restart')}
              disabled={isActioning}
              leftIcon={RefreshCw}
              className="text-xs"
            >
              Fix
            </LegendaryButton>
          )}
        </div>
      </div>

      {/* Service Description */}
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
        {service.description}
      </p>

      {/* Service Metrics */}
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div>
          <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Uptime</div>
          <div className="font-semibold text-gray-900 dark:text-white">
            {formatUptime(service.uptime)}
          </div>
        </div>
        
        <div>
          <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Memory</div>
          <div className="space-y-1">
            <div className="font-semibold text-gray-900 dark:text-white">
              {service.memory.toFixed(1)} MB
            </div>
            <ProgressBar
              value={(service.memory / 1024) * 100}
              max={100}
              size="sm"
              color={service.memory > 800 ? 'red' : service.memory > 500 ? 'yellow' : 'green'}
            />
          </div>
        </div>
        
        <div>
          <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">CPU</div>
          <div className="space-y-1">
            <div className="font-semibold text-gray-900 dark:text-white">
              {service.cpu.toFixed(1)}%
            </div>
            <ProgressBar
              value={service.cpu}
              max={100}
              size="sm"
              color={service.cpu > 80 ? 'red' : service.cpu > 60 ? 'yellow' : 'green'}
            />
          </div>
        </div>
      </div>

      {/* Last Restart */}
      <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
        <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
          <Clock className="w-3 h-3" />
          <span>Last restart: {service.lastRestart.toLocaleString()}</span>
        </div>
      </div>

      {/* Loading Overlay */}
      {isActioning && (
        <motion.div
          className="absolute inset-0 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-lg flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
            <span className="text-sm font-medium">Processing...</span>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

// =====================================
// 🎸 LEGENDARY SYSTEM HEALTH 🎸
// =====================================

export const SystemHealth: React.FC<SystemHealthProps> = ({
  metrics,
  isFounder = false,
  onRefresh,
}) => {
  const [services, setServices] = useState<SystemService[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedTab, setSelectedTab] = useState<'overview' | 'services' | 'performance'>('overview');

  useEffect(() => {
    console.log('🖥️🎸🖥️ LEGENDARY SYSTEM HEALTH LOADED! 🖥️🎸🖥️');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`System health loaded at: 2025-08-06 17:43:16 UTC`);
    console.log('🌅 LATE AFTERNOON LEGENDARY SYSTEM HEALTH ENERGY AT 17:43:16!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER SYSTEM HEALTH ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER SYSTEM HEALTH WITH INFINITE CODE BRO ENERGY!');
    }

    loadServices();
    
    // Auto refresh every 30 seconds
    const interval = autoRefresh ? setInterval(() => {
      if (onRefresh) onRefresh();
      loadServices();
    }, 30000) : null;

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isFounder, autoRefresh, onRefresh]);

  // Load services
  const loadServices = useCallback(async () => {
    try {
      // Generate mock services data
      const mockServices: SystemService[] = [
        {
          id: 'web-server',
          name: 'Web Server',
          status: 'running',
          uptime: 8640, // 6 days
          memory: 256.8,
          cpu: 12.5,
          lastRestart: new Date('2025-07-31T10:00:00.000Z'),
          version: '2.4.1',
          description: 'Main web application server handling HTTP requests'
        },
        {
          id: 'database',
          name: 'Database Server',
          status: 'running',
          uptime: 10080, // 7 days
          memory: 512.3,
          cpu: 8.7,
          lastRestart: new Date('2025-07-30T08:00:00.000Z'),
          version: '14.2',
          description: 'PostgreSQL database server for application data'
        },
        {
          id: 'redis-cache',
          name: 'Redis Cache',
          status: 'running',
          uptime: 7200, // 5 days
          memory: 128.6,
          cpu: 3.2,
          lastRestart: new Date('2025-08-01T14:30:00.000Z'),
          version: '7.0.8',
          description: 'Redis in-memory cache for session and data caching'
        },
        {
          id: 'background-jobs',
          name: 'Background Workers',
          status: 'warning',
          uptime: 4320, // 3 days
          memory: 89.4,
          cpu: 15.8,
          lastRestart: new Date('2025-08-03T16:00:00.000Z'),
          version: '1.8.2',
          description: 'Background job processing for async tasks'
        },
        {
          id: 'file-storage',
          name: 'File Storage',
          status: 'running',
          uptime: 12960, // 9 days
          memory: 45.2,
          cpu: 2.1,
          lastRestart: new Date('2025-07-28T12:00:00.000Z'),
          version: '3.1.4',
          description: 'File upload and storage service'
        },
        {
          id: 'monitoring',
          name: 'System Monitor',
          status: 'error',
          uptime: 0,
          memory: 0,
          cpu: 0,
          lastRestart: new Date('2025-08-06T17:40:00.000Z'),
          version: '2.7.1',
          description: 'System monitoring and alerting service'
        }
      ];

      setServices(mockServices);
    } catch (error) {
      console.error('🚨 Error loading services:', error);
      toast.error('Failed to load system services');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Handle service action
  const handleServiceAction = useCallback((serviceId: string, action: 'start' | 'stop' | 'restart') => {
    setServices(prev => prev.map(service => {
      if (service.id === serviceId) {
        const newStatus = action === 'start' ? 'running' : action === 'stop' ? 'stopped' : 'running';
        return {
          ...service,
          status: newStatus as SystemService['status'],
          lastRestart: new Date(),
          uptime: action === 'restart' ? 0 : service.uptime
        };
      }
      return service;
    }));
  }, []);

  // Calculate system health score
  const systemHealthScore = useMemo(() => {
    if (!metrics) return 0;
    
    const uptimeScore = metrics.systemUptime;
    const loadScore = Math.max(0, 100 - metrics.serverLoad);
    const errorScore = Math.max(0, 100 - (metrics.errorRate * 10000));
    const responseScore = Math.max(0, 100 - Math.min(100, metrics.averageResponseTime / 10));
    
    return (uptimeScore + loadScore + errorScore + responseScore) / 4;
  }, [metrics]);

  // Service health summary
  const serviceHealth = useMemo(() => {
    const running = services.filter(s => s.status === 'running').length;
    const warning = services.filter(s => s.status === 'warning').length;
    const error = services.filter(s => s.status === 'error').length;
    const stopped = services.filter(s => s.status === 'stopped').length;
    
    return { running, warning, error, stopped, total: services.length };
  }, [services]);

  if (isLoading || !metrics) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="flex flex-col items-center gap-4">
          <div className="flex gap-2">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className={cn(
                  'w-4 h-4 rounded-full',
                  isFounder ? 'bg-yellow-500' : 'bg-blue-500'
                )}
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.7, 1, 0.7],
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: i * 0.2,
                }}
              />
            ))}
          </div>
          <p className={cn(
            'text-lg font-medium',
            isFounder ? 'text-yellow-700' : 'text-gray-700'
          )}>
            {isFounder 
              ? 'Loading legendary system health data...'
              : 'Loading system health dashboard...'
            }
          </p>
        </div>
      </div>
    );
  }

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
            🖥️ {isFounder ? 'Legendary System Control Center' : 'System Health Monitor'}
          </motion.h2>

          <div className="flex items-center gap-2">
            <div className={cn(
              'w-2 h-2 rounded-full',
              systemHealthScore >= 95 ? 'bg-green-500' :
              systemHealthScore >= 80 ? 'bg-yellow-500' : 'bg-red-500'
            )} />
            <span className={cn(
              'text-sm font-medium',
              systemHealthScore >= 95 ? 'text-green-600' :
              systemHealthScore >= 80 ? 'text-yellow-600' : 'text-red-600'
            )}>
              {systemHealthScore >= 95 ? 'Excellent' :
               systemHealthScore >= 80 ? 'Good' : 'Needs Attention'}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Auto Refresh Toggle */}
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="sr-only"
            />
            <div className={cn(
              'w-10 h-5 rounded-full transition-colors',
              autoRefresh 
                ? isFounder ? 'bg-yellow-500' : 'bg-blue-500'
                : 'bg-gray-300 dark:bg-gray-600'
            )}>
              <div className={cn(
                'w-4 h-4 bg-white rounded-full transform transition-transform',
                autoRefresh ? 'translate-x-5' : 'translate-x-0.5',
                'mt-0.5'
              )} />
            </div>
            <span className="text-sm text-gray-600 dark:text-gray-400">Auto Refresh</span>
          </label>

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
              toast.success(isFounder ? '👑 Exporting legendary system report!' : '📊 Exporting system report!');
            }}
          >
            Export
          </LegendaryButton>

          <LegendaryButton
            variant={isFounder ? "founder" : "primary"}
            leftIcon={Terminal}
            onClick={() => {
              toast.success(isFounder ? '👑 Opening legendary system console!' : '💻 Opening system console!');
            }}
          >
            Console
          </LegendaryButton>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'overview', label: 'System Overview', icon: Monitor },
            { id: 'services', label: 'Services', icon: Server },
            { id: 'performance', label: 'Performance', icon: BarChart3 },
          ].map((tab) => {
            const TabIcon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setSelectedTab(tab.id as typeof selectedTab)}
                className={cn(
                  'group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap',
                  'transition-colors duration-200',
                  selectedTab === tab.id
                    ? isFounder
                      ? 'border-yellow-500 text-yellow-600 dark:text-yellow-400'
                      : 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 hover:border-gray-300'
                )}
              >
                <TabIcon className={cn(
                  'w-5 h-5 mr-2',
                  selectedTab === tab.id
                    ? isFounder ? 'text-yellow-600' : 'text-blue-600'
                    : 'text-gray-400 group-hover:text-gray-500'
                )} />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={selectedTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.4 }}
        >
          {selectedTab === 'overview' && (
            <div className="space-y-6">
              {/* System Health Score */}
              <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className={cn(
                    'text-lg font-semibold',
                    isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                  )}>
                    Overall System Health
                  </h3>
                  
                  <div className="text-right">
                    <div className={cn(
                      'text-3xl font-bold',
                      systemHealthScore >= 95 ? 'text-green-600' :
                      systemHealthScore >= 80 ? 'text-yellow-600' : 'text-red-600'
                    )}>
                      {systemHealthScore.toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Health Score</div>
                  </div>
                </div>

                <ProgressBar
                  value={systemHealthScore}
                  max={100}
                  size="lg"
                  color={systemHealthScore >= 95 ? 'green' : systemHealthScore >= 80 ? 'yellow' : 'red'}
                  showLabel={false}
                />

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                  <div className="text-center">
                    <div className="text-lg font-semibold text-green-600">
                      {metrics.systemUptime.toFixed(2)}%
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Uptime</div>
                  </div>
                  
                  <div className="text-center">
                    <div className={cn(
                      'text-lg font-semibold',
                      metrics.serverLoad > 80 ? 'text-red-600' : 
                      metrics.serverLoad > 60 ? 'text-yellow-600' : 'text-green-600'
                    )}>
                      {metrics.serverLoad.toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Server Load</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-lg font-semibold text-blue-600">
                      {metrics.averageResponseTime}ms
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Response Time</div>
                  </div>
                  
                  <div className="text-center">
                    <div className={cn(
                      'text-lg font-semibold',
                      metrics.errorRate > 0.01 ? 'text-red-600' : 'text-green-600'
                    )}>
                      {(metrics.errorRate * 100).toFixed(3)}%
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Error Rate</div>
                  </div>
                </div>
              </LegendaryCard>

              {/* Quick Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
                {[
                  {
                    title: 'Active Sessions',
                    value: metrics.totalSessions,
                    icon: Users,
                    color: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400'
                  },
                  {
                    title: 'API Requests/hr',
                    value: `${(metrics.apiRequests / 1000).toFixed(1)}K`,
                    icon: Globe,
                    color: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400'
                  },
                  {
                    title: 'Storage Used',
                    value: `${metrics.storageUsed.toFixed(1)}%`,
                    icon: HardDrive,
                    color: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400',
                    progress: { value: metrics.storageUsed, max: 100 }
                  },
                  {
                    title: 'Bandwidth Today',
                    value: `${metrics.bandwidthUsed.toFixed(1)} GB`,
                    icon: Wifi,
                    color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400'
                  },
                ].map((stat, index) => (
                  <motion.div
                    key={stat.title}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                  >
                    <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-6">
                      <div className="flex items-center gap-3 mb-3">
                        <div className={cn('p-2 rounded-lg', stat.color)}>
                          <stat.icon className="w-5 h-5" />
                        </div>
                        <div>
                          <h4 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                            {stat.title}
                          </h4>
                          <div className={cn(
                            'text-2xl font-bold',
                            isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                          )}>
                            {stat.value}
                          </div>
                        </div>
                      </div>

                      {stat.progress && (
                        <ProgressBar
                          value={stat.progress.value}
                          max={stat.progress.max}
                          size="sm"
                          color={stat.progress.value > 90 ? 'red' : stat.progress.value > 75 ? 'yellow' : 'green'}
                        />
                      )}
                    </LegendaryCard>
                  </motion.div>
                ))}
              </div>

              {/* Service Status Summary */}
              <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-6">
                <h3 className={cn(
                  'text-lg font-semibold mb-4',
                  isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                )}>
                  Service Status Summary
                </h3>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600 mb-1">
                      {serviceHealth.running}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Running</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-600 mb-1">
                      {serviceHealth.warning}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Warning</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600 mb-1">
                      {serviceHealth.error}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Error</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-600 mb-1">
                      {serviceHealth.stopped}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Stopped</div>
                  </div>
                </div>
              </LegendaryCard>
            </div>
          )}

          {selectedTab === 'services' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <p className="text-gray-600 dark:text-gray-400">
                  {serviceHealth.total} total services • {serviceHealth.running} running • {serviceHealth.error + serviceHealth.warning} need attention
                </p>
                
                <LegendaryButton
                  variant={isFounder ? "founder" : "primary"}
                  leftIcon={Plus}
                  onClick={() => toast.success(isFounder ? '👑 Adding new legendary service!' : '➕ Adding new service!')}
                >
                  Add Service
                </LegendaryButton>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {services.map((service, index) => (
                  <motion.div
                    key={service.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                  >
                    <ServiceStatus
                      service={service}
                      onAction={handleServiceAction}
                      isFounder={isFounder}
                    />
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {selectedTab === 'performance' && (
            <div className="space-y-6">
              <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-6 text-center">
                <BarChart3 className={cn(
                  'w-16 h-16 mx-auto mb-4',
                  isFounder ? 'text-yellow-600' : 'text-blue-600'
                )} />
                <h3 className={cn(
                  'text-xl font-bold mb-2',
                  isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                )}>
                  {isFounder ? 'Legendary Performance Charts' : 'Performance Analytics'}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  {isFounder 
                    ? '👑 Advanced performance monitoring with infinite analytical power coming soon!'
                    : 'Advanced performance monitoring and analytics charts coming soon!'
                  }
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600 mb-1">
                      {metrics.systemUptime.toFixed(2)}%
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Average Uptime</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600 mb-1">
                      {metrics.averageResponseTime}ms
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Response Time</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600 mb-1">
                      {(metrics.apiRequests / 1000).toFixed(1)}K
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Requests/Hour</div>
                  </div>
                </div>
              </LegendaryCard>
            </div>
          )}
        </motion.div>
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
            <Activity className="w-4 h-4" />
            <span>Real-time monitoring</span>
          </div>
          
          <div className="flex items-center gap-1">
            <Zap className="w-4 h-4" />
            <span>Swiss precision system health</span>
          </div>
          
          <div className="text-gray-400 font-mono">
            2025-08-06 17:43:16 UTC
          </div>
        </div>
        
        {isFounder && (
          <div className="mt-2">
            <span className="text-yellow-700 dark:text-yellow-300 font-bold text-sm">
              👑 RICKROLL187 FOUNDER SYSTEM HEALTH • INFINITE MONITORING POWER! 👑
            </span>
          </div>
        )}
      </motion.div>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY SYSTEM HEALTH COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`System health component completed at: 2025-08-06 17:43:16 UTC`);
console.log('🖥️ System monitoring: SWISS PRECISION');
console.log('👑 RICKROLL187 founder system health: LEGENDARY');
console.log('📊 Performance tracking: MAXIMUM INSIGHT');
console.log('🌅 LATE AFTERNOON LEGENDARY SYSTEM HEALTH ENERGY: INFINITE AT 17:43:16!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
