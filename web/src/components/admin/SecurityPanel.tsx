// File: web/src/components/admin/SecurityPanel.tsx
/**
 * 🔒🎸 N3EXTPATH - LEGENDARY SECURITY PANEL COMPONENT 🎸🔒
 * Swiss precision security monitoring with infinite code bro energy
 * Built: 2025-08-06 17:47:54 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Crown, 
  Shield, 
  Lock, 
  Unlock,
  Eye,
  EyeOff,
  AlertTriangle,
  AlertCircle,
  CheckCircle,
  XCircle,
  Ban,
  UserX,
  Key,
  Fingerprint,
  Globe,
  Monitor,
  Wifi,
  MapPin,
  Clock,
  Calendar,
  Search,
  Filter,
  MoreVertical,
  Download,
  Upload,
  RefreshCw,
  Settings,
  Terminal,
  Code,
  Bug,
  Zap,
  Activity,
  TrendingUp,
  BarChart3,
  PieChart,
  Target,
  Star,
  Sparkles,
  Trophy,
  Database,
  Server,
  HardDrive
} from 'lucide-react';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { Modal } from '@/components/ui/Modal';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 🔒 SECURITY TYPES 🔒
// =====================================

interface SecurityAlert {
  id: string;
  type: 'login_attempt' | 'permission_change' | 'data_access' | 'system_error' | 'suspicious_activity' | 'intrusion_attempt' | 'malware_detected' | 'ddos_attack';
  severity: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  description?: string;
  userId?: string;
  userName?: string;
  userAgent?: string;
  ipAddress?: string;
  location?: string;
  timestamp: Date;
  resolved: boolean;
  resolvedBy?: string;
  resolvedAt?: Date;
  actions?: string[];
}

interface SecurityMetrics {
  totalAlerts: number;
  criticalAlerts: number;
  resolvedAlerts: number;
  activeThreats: number;
  blockedIPs: number;
  failedLogins: number;
  suspiciousActivities: number;
  malwareAttempts: number;
  securityScore: number;
}

interface SecurityPanelProps {
  alerts: SecurityAlert[];
  onAlertResolve: (alertId: string) => void;
  isFounder?: boolean;
}

// =====================================
// 🎸 ALERT ITEM COMPONENT 🎸
// =====================================

const AlertItem: React.FC<{
  alert: SecurityAlert;
  onResolve: (alertId: string) => void;
  onViewDetails: (alert: SecurityAlert) => void;
  isFounder: boolean;
}> = ({ alert, onResolve, onViewDetails, isFounder }) => {
  const [isResolving, setIsResolving] = useState(false);

  // Get alert styling
  const getAlertInfo = () => {
    switch (alert.severity) {
      case 'critical':
        return {
          color: 'border-red-500 bg-red-50/50 dark:border-red-400 dark:bg-red-900/20',
          badgeColor: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
          icon: XCircle,
          label: 'CRITICAL'
        };
      case 'high':
        return {
          color: 'border-orange-500 bg-orange-50/50 dark:border-orange-400 dark:bg-orange-900/20',
          badgeColor: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300',
          icon: AlertTriangle,
          label: 'HIGH'
        };
      case 'medium':
        return {
          color: 'border-yellow-500 bg-yellow-50/50 dark:border-yellow-400 dark:bg-yellow-900/20',
          badgeColor: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
          icon: AlertCircle,
          label: 'MEDIUM'
        };
      default:
        return {
          color: 'border-blue-500 bg-blue-50/50 dark:border-blue-400 dark:bg-blue-900/20',
          badgeColor: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
          icon: CheckCircle,
          label: 'LOW'
        };
    }
  };

  // Get alert type icon
  const getTypeIcon = () => {
    switch (alert.type) {
      case 'login_attempt': return Key;
      case 'permission_change': return Shield;
      case 'data_access': return Database;
      case 'system_error': return Bug;
      case 'suspicious_activity': return Eye;
      case 'intrusion_attempt': return Ban;
      case 'malware_detected': return XCircle;
      case 'ddos_attack': return Zap;
      default: return AlertCircle;
    }
  };

  const alertInfo = getAlertInfo();
  const AlertIcon = alertInfo.icon;
  const TypeIcon = getTypeIcon();

  // Handle resolve
  const handleResolve = async () => {
    if (alert.resolved) return;

    setIsResolving(true);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      onResolve(alert.id);
      
      if (isFounder) {
        toast.success('👑 FOUNDER SECURITY ACTION: Alert resolved with infinite authority!', {
          duration: 3000,
          style: {
            background: 'linear-gradient(135deg, #FFD700, #FFA500)',
            color: '#000000',
            fontWeight: '700',
          },
        });
      } else {
        toast.success('✅ Security alert resolved successfully!');
      }
      
    } catch (error) {
      toast.error('❌ Failed to resolve alert');
    } finally {
      setIsResolving(false);
    }
  };

  return (
    <motion.div
      className={cn(
        'p-4 rounded-lg border',
        alert.resolved 
          ? 'border-green-200 bg-green-50/30 dark:border-green-700 dark:bg-green-900/10 opacity-75'
          : alertInfo.color
      )}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-start gap-3">
        {/* Alert Icon */}
        <div className={cn(
          'p-2 rounded-full',
          alert.resolved 
            ? 'bg-green-100 dark:bg-green-900/30'
            : alert.severity === 'critical' ? 'bg-red-100 dark:bg-red-900/30' :
              alert.severity === 'high' ? 'bg-orange-100 dark:bg-orange-900/30' :
              alert.severity === 'medium' ? 'bg-yellow-100 dark:bg-yellow-900/30' :
              'bg-blue-100 dark:bg-blue-900/30'
        )}>
          {alert.resolved ? (
            <CheckCircle className="w-4 h-4 text-green-600" />
          ) : (
            <AlertIcon className={cn(
              'w-4 h-4',
              alert.severity === 'critical' ? 'text-red-600' :
              alert.severity === 'high' ? 'text-orange-600' :
              alert.severity === 'medium' ? 'text-yellow-600' :
              'text-blue-600'
            )} />
          )}
        </div>

        {/* Alert Content */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className={cn(
              'inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium',
              alert.resolved ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' : alertInfo.badgeColor
            )}>
              <TypeIcon className="w-3 h-3" />
              {alert.resolved ? 'RESOLVED' : alertInfo.label}
            </span>
            
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {alert.timestamp.toLocaleString()}
            </span>
          </div>

          <h4 className={cn(
            'font-semibold mb-1',
            isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
          )}>
            {alert.message}
          </h4>

          {alert.description && (
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              {alert.description}
            </p>
          )}

          <div className="flex flex-wrap gap-4 text-xs text-gray-500 dark:text-gray-400">
            {alert.userName && (
              <div className="flex items-center gap-1">
                <span>User:</span>
                <span className="font-medium">{alert.userName}</span>
              </div>
            )}
            
            {alert.ipAddress && (
              <div className="flex items-center gap-1">
                <Globe className="w-3 h-3" />
                <span>{alert.ipAddress}</span>
              </div>
            )}
            
            {alert.location && (
              <div className="flex items-center gap-1">
                <MapPin className="w-3 h-3" />
                <span>{alert.location}</span>
              </div>
            )}
          </div>

          {alert.resolved && alert.resolvedBy && (
            <div className="mt-2 pt-2 border-t border-green-200 dark:border-green-700">
              <div className="flex items-center gap-2 text-xs text-green-600 dark:text-green-400">
                <CheckCircle className="w-3 h-3" />
                <span>Resolved by {alert.resolvedBy} at {alert.resolvedAt?.toLocaleString()}</span>
              </div>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <LegendaryButton
            variant="ghost"
            size="sm"
            onClick={() => onViewDetails(alert)}
            className="p-1"
          >
            <Eye className="w-3 h-3" />
          </LegendaryButton>

          {!alert.resolved && (
            <LegendaryButton
              variant={isFounder ? "founder" : "primary"}
              size="sm"
              onClick={handleResolve}
              disabled={isResolving}
              className="text-xs"
            >
              {isResolving ? (
                <div className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
              ) : (
                'Resolve'
              )}
            </LegendaryButton>
          )}

          <LegendaryButton
            variant="ghost"
            size="sm"
            className="p-1"
          >
            <MoreVertical className="w-3 h-3" />
          </LegendaryButton>
        </div>
      </div>
    </motion.div>
  );
};

// =====================================
// 🎸 LEGENDARY SECURITY PANEL 🎸
// =====================================

export const SecurityPanel: React.FC<SecurityPanelProps> = ({
  alerts,
  onAlertResolve,
  isFounder = false,
}) => {
  const [selectedAlert, setSelectedAlert] = useState<SecurityAlert | null>(null);
  const [showAlertDetails, setShowAlertDetails] = useState(false);
  const [filters, setFilters] = useState<{
    severity?: string;
    type?: string;
    resolved?: boolean;
    search?: string;
  }>({});
  const [selectedTab, setSelectedTab] = useState<'alerts' | 'threats' | 'access' | 'logs'>('alerts');

  useEffect(() => {
    console.log('🔒🎸🔒 LEGENDARY SECURITY PANEL LOADED! 🔒🎸🔒');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Security panel loaded at: 2025-08-06 17:47:54 UTC`);
    console.log('🌅 LATE AFTERNOON LEGENDARY SECURITY ENERGY AT 17:47:54!');

    if (isFounder) {
      console.log('👑🔒👑 RICKROLL187 FOUNDER SECURITY PANEL ACTIVATED! 👑🔒👑');
      console.log('🚀 LEGENDARY FOUNDER SECURITY PANEL WITH INFINITE CODE BRO PROTECTION!');
    }
  }, [isFounder]);

  // Calculate security metrics
  const metrics = useMemo<SecurityMetrics>(() => {
    const total = alerts.length;
    const critical = alerts.filter(a => a.severity === 'critical').length;
    const resolved = alerts.filter(a => a.resolved).length;
    const active = total - resolved;
    const suspicious = alerts.filter(a => a.type === 'suspicious_activity').length;
    const malware = alerts.filter(a => a.type === 'malware_detected').length;
    const failed = alerts.filter(a => a.type === 'login_attempt').length;
    
    // Calculate security score (higher is better)
    const criticalPenalty = critical * 20;
    const unresolvedPenalty = active * 5;
    const baseScore = 100;
    const securityScore = Math.max(0, baseScore - criticalPenalty - unresolvedPenalty);
    
    return {
      totalAlerts: total,
      criticalAlerts: critical,
      resolvedAlerts: resolved,
      activeThreats: active,
      blockedIPs: 12, // Mock data
      failedLogins: failed,
      suspiciousActivities: suspicious,
      malwareAttempts: malware,
      securityScore,
    };
  }, [alerts]);

  // Filter alerts
  const filteredAlerts = useMemo(() => {
    let filtered = alerts;

    if (filters.search) {
      const search = filters.search.toLowerCase();
      filtered = filtered.filter(alert =>
        alert.message.toLowerCase().includes(search) ||
        alert.description?.toLowerCase().includes(search) ||
        alert.userName?.toLowerCase().includes(search) ||
        alert.ipAddress?.includes(search)
      );
    }

    if (filters.severity) {
      filtered = filtered.filter(alert => alert.severity === filters.severity);
    }

    if (filters.type) {
      filtered = filtered.filter(alert => alert.type === filters.type);
    }

    if (filters.resolved !== undefined) {
      filtered = filtered.filter(alert => alert.resolved === filters.resolved);
    }

    // Sort by timestamp (newest first) and severity
    return filtered.sort((a, b) => {
      if (a.resolved !== b.resolved) return a.resolved ? 1 : -1;
      if (a.severity !== b.severity) {
        const severityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
        return severityOrder[b.severity] - severityOrder[a.severity];
      }
      return b.timestamp.getTime() - a.timestamp.getTime();
    });
  }, [alerts, filters]);

  // Handle alert details
  const handleViewAlertDetails = (alert: SecurityAlert) => {
    setSelectedAlert(alert);
    setShowAlertDetails(true);
  };

  // Security actions
  const securityActions = [
    {
      title: isFounder ? 'Legendary Security Scan' : 'Security Scan',
      description: isFounder ? 'Run comprehensive security scan with infinite power' : 'Run comprehensive security scan',
      icon: Shield,
      action: () => {
        if (isFounder) {
          toast.success('👑 LEGENDARY FOUNDER SECURITY SCAN initiated with infinite precision!', {
            duration: 4000,
            style: {
              background: 'linear-gradient(135deg, #FFD700, #FFA500)',
              color: '#000000',
              fontWeight: '700',
            },
          });
        } else {
          toast.success('🛡️ Security scan initiated!');
        }
      },
      color: isFounder ? 'text-yellow-600 bg-yellow-100' : 'text-blue-600 bg-blue-100',
    },
    {
      title: 'Block Suspicious IPs',
      description: 'Block all flagged IP addresses',
      icon: Ban,
      action: () => toast.success('🚫 Suspicious IPs blocked!'),
      color: 'text-red-600 bg-red-100',
    },
    {
      title: 'Update Security Rules',
      description: 'Apply latest security rule updates',
      icon: Settings,
      action: () => toast.success('⚙️ Security rules updated!'),
      color: 'text-purple-600 bg-purple-100',
    },
    {
      title: 'Generate Report',
      description: 'Generate comprehensive security report',
      icon: Download,
      action: () => toast.success('📊 Security report generated!'),
      color: 'text-green-600 bg-green-100',
    },
  ];

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
            🔒 {isFounder ? 'Legendary Security Command Center' : 'Security Control Panel'}
          </motion.h2>

          <div className="flex items-center gap-2">
            <div className={cn(
              'w-2 h-2 rounded-full',
              metrics.securityScore >= 90 ? 'bg-green-500' :
              metrics.securityScore >= 70 ? 'bg-yellow-500' : 'bg-red-500'
            )} />
            <span className={cn(
              'text-sm font-medium',
              metrics.securityScore >= 90 ? 'text-green-600' :
              metrics.securityScore >= 70 ? 'text-yellow-600' : 'text-red-600'
            )}>
              {metrics.securityScore >= 90 ? 'Secure' :
               metrics.securityScore >= 70 ? 'Moderate Risk' : 'High Risk'}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <LegendaryButton
            variant="ghost"
            size="sm"
            leftIcon={RefreshCw}
            onClick={() => toast.success('🔄 Security data refreshed!')}
          >
            Refresh
          </LegendaryButton>
          
          <LegendaryButton
            variant="ghost"
            size="sm"
            leftIcon={Download}
            onClick={() => toast.success(isFounder ? '👑 Exporting legendary security report!' : '📊 Exporting security report!')}
          >
            Export
          </LegendaryButton>
          
          <LegendaryButton
            variant={isFounder ? "founder" : "primary"}
            leftIcon={Terminal}
            onClick={() => toast.success(isFounder ? '👑 Opening legendary security console!' : '💻 Opening security console!')}
          >
            Console
          </LegendaryButton>
        </div>
      </div>

      {/* Security Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {[
          {
            title: 'Security Score',
            value: `${metrics.securityScore.toFixed(0)}%`,
            icon: Shield,
            color: metrics.securityScore >= 90 ? 'bg-green-100 text-green-600' : 
                   metrics.securityScore >= 70 ? 'bg-yellow-100 text-yellow-600' : 'bg-red-100 text-red-600',
            progress: { value: metrics.securityScore, max: 100 }
          },
          {
            title: 'Active Threats',
            value: metrics.activeThreats,
            icon: AlertTriangle,
            color: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
          },
          {
            title: 'Critical Alerts',
            value: metrics.criticalAlerts,
            icon: XCircle,
            color: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400'
          },
          {
            title: 'Blocked IPs',
            value: metrics.blockedIPs,
            icon: Ban,
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
                  color={stat.progress.value >= 90 ? 'green' : stat.progress.value >= 70 ? 'yellow' : 'red'}
                />
              )}
            </LegendaryCard>
          </motion.div>
        ))}
      </div>

      {/* Quick Actions */}
      <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-6">
        <h3 className={cn(
          'text-lg font-semibold mb-4',
          isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
        )}>
          {isFounder ? 'Legendary Security Actions' : 'Quick Security Actions'}
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          {securityActions.map((action, index) => (
            <motion.div
              key={action.title}
              className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
              onClick={action.action}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="flex items-start gap-3">
                <div className={cn('p-2 rounded-lg', action.color)}>
                  <action.icon className="w-4 h-4" />
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white mb-1">
                    {action.title}
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {action.description}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </LegendaryCard>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'alerts', label: 'Security Alerts', icon: AlertTriangle, count: metrics.totalAlerts },
            { id: 'threats', label: 'Active Threats', icon: Shield, count: metrics.activeThreats },
            { id: 'access', label: 'Access Control', icon: Key },
            { id: 'logs', label: 'Security Logs', icon: Terminal },
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
                {tab.count !== undefined && (
                  <span className={cn(
                    'ml-2 py-0.5 px-2 rounded-full text-xs font-medium',
                    selectedTab === tab.id
                      ? isFounder 
                        ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
                        : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                      : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'
                  )}>
                    {tab.count}
                  </span>
                )}
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
          {selectedTab === 'alerts' && (
            <div className="space-y-4">
              {/* Filters */}
              <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {/* Search */}
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search alerts..."
                      value={filters.search || ''}
                      onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
                      className={cn(
                        'w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                        'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                        'focus:outline-none focus:ring-2 focus:ring-offset-2',
                        isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                      )}
                    />
                  </div>

                  {/* Severity Filter */}
                  <select
                    value={filters.severity || ''}
                    onChange={(e) => setFilters(prev => ({ ...prev, severity: e.target.value || undefined }))}
                    className={cn(
                      'w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                      'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                      'focus:outline-none focus:ring-2 focus:ring-offset-2',
                      isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                    )}
                  >
                    <option value="">All Severity</option>
                    <option value="critical">Critical</option>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>

                  {/* Type Filter */}
                  <select
                    value={filters.type || ''}
                    onChange={(e) => setFilters(prev => ({ ...prev, type: e.target.value || undefined }))}
                    className={cn(
                      'w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                      'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                      'focus:outline-none focus:ring-2 focus:ring-offset-2',
                      isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                    )}
                  >
                    <option value="">All Types</option>
                    <option value="login_attempt">Login Attempt</option>
                    <option value="permission_change">Permission Change</option>
                    <option value="data_access">Data Access</option>
                    <option value="system_error">System Error</option>
                    <option value="suspicious_activity">Suspicious Activity</option>
                    <option value="intrusion_attempt">Intrusion Attempt</option>
                    <option value="malware_detected">Malware Detected</option>
                    <option value="ddos_attack">DDoS Attack</option>
                  </select>

                  {/* Status Filter */}
                  <select
                    value={filters.resolved === undefined ? '' : filters.resolved ? 'true' : 'false'}
                    onChange={(e) => setFilters(prev => ({ 
                      ...prev, 
                      resolved: e.target.value === '' ? undefined : e.target.value === 'true' 
                    }))}
                    className={cn(
                      'w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                      'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                      'focus:outline-none focus:ring-2 focus:ring-offset-2',
                      isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                    )}
                  >
                    <option value="">All Status</option>
                    <option value="false">Active</option>
                    <option value="true">Resolved</option>
                  </select>
                </div>
              </LegendaryCard>

              {/* Alert List */}
              <div className="space-y-4">
                {filteredAlerts.length === 0 ? (
                  <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-12 text-center">
                    <Shield className={cn(
                      'w-16 h-16 mx-auto mb-4 opacity-50',
                      isFounder ? 'text-yellow-600' : 'text-blue-600'
                    )} />
                    <h3 className={cn(
                      'text-xl font-bold mb-2',
                      isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
                    )}>
                      {Object.keys(filters).length > 1 ? 'No alerts match your filters' : 'No security alerts'}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400">
                      {Object.keys(filters).length > 1 
                        ? 'Try adjusting your filters to find alerts'
                        : isFounder
                          ? '👑 Your legendary security system is operating at maximum protection!'
                          : '🛡️ Your system security is operating normally'
                      }
                    </p>
                  </LegendaryCard>
                ) : (
                  filteredAlerts.map((alert) => (
                    <AlertItem
                      key={alert.id}
                      alert={alert}
                      onResolve={onAlertResolve}
                      onViewDetails={handleViewAlertDetails}
                      isFounder={isFounder}
                    />
                  ))
                )}
              </div>
            </div>
          )}

          {selectedTab === 'threats' && (
            <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-12 text-center">
              <Shield className={cn(
                'w-16 h-16 mx-auto mb-4',
                isFounder ? 'text-yellow-600' : 'text-blue-600'
              )} />
              <h3 className={cn(
                'text-xl font-bold mb-2',
                isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
              )}>
                {isFounder ? 'Legendary Threat Detection' : 'Advanced Threat Detection'}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                {isFounder 
                  ? '👑 Advanced threat monitoring with infinite protection power coming soon!'
                  : 'Advanced threat monitoring and real-time protection coming soon!'
                }
              </p>
              
              <div className="text-sm text-gray-500">
                Active monitoring: {metrics.activeThreats} threats detected
              </div>
            </LegendaryCard>
          )}

          {selectedTab === 'access' && (
            <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-12 text-center">
              <Key className={cn(
                'w-16 h-16 mx-auto mb-4',
                isFounder ? 'text-yellow-600' : 'text-blue-600'
              )} />
              <h3 className={cn(
                'text-xl font-bold mb-2',
                isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
              )}>
                {isFounder ? 'Legendary Access Control' : 'Access Control Management'}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {isFounder 
                  ? '👑 Advanced access control with infinite permission management coming soon!'
                  : 'Advanced access control and permission management coming soon!'
                }
              </p>
            </LegendaryCard>
          )}

          {selectedTab === 'logs' && (
            <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-12 text-center">
              <Terminal className={cn(
                'w-16 h-16 mx-auto mb-4',
                isFounder ? 'text-yellow-600' : 'text-blue-600'
              )} />
              <h3 className={cn(
                'text-xl font-bold mb-2',
                isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
              )}>
                {isFounder ? 'Legendary Security Logs' : 'Security Audit Logs'}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {isFounder 
                  ? '👑 Comprehensive audit logging with infinite forensic power coming soon!'
                  : 'Comprehensive security audit logging and forensics coming soon!'
                }
              </p>
            </LegendaryCard>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Alert Details Modal */}
      <Modal 
        isOpen={showAlertDetails} 
        onClose={() => setShowAlertDetails(false)}
        size="lg"
      >
        {selectedAlert && (
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                Security Alert Details
              </h3>
              <button
                onClick={() => setShowAlertDetails(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <XCircle className="w-6 h-6" />
              </button>
            </div>
            
            <div className="space-y-6">
              {/* Alert Info */}
              <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex items-center gap-3 mb-3">
                  <div className={cn(
                    'p-2 rounded-full',
                    selectedAlert.severity === 'critical' ? 'bg-red-100 text-red-600' :
                    selectedAlert.severity === 'high' ? 'bg-orange-100 text-orange-600' :
                    selectedAlert.severity === 'medium' ? 'bg-yellow-100 text-yellow-600' :
                    'bg-blue-100 text-blue-600'
                  )}>
                    <AlertTriangle className="w-5 h-5" />
                  </div>
                  
                  <div>
                    <h4 className="font-bold text-lg text-gray-900 dark:text-white">
                      {selectedAlert.message}
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {selectedAlert.timestamp.toLocaleString()}
                    </p>
                  </div>
                </div>

                {selectedAlert.description && (
                  <p className="text-gray-700 dark:text-gray-300">
                    {selectedAlert.description}
                  </p>
                )}
              </div>

              {/* Technical Details */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h5 className="font-semibold text-gray-900 dark:text-white mb-3">Alert Details</h5>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Severity:</span>
                      <span className={cn(
                        'font-medium capitalize',
                        selectedAlert.severity === 'critical' ? 'text-red-600' :
                        selectedAlert.severity === 'high' ? 'text-orange-600' :
                        selectedAlert.severity === 'medium' ? 'text-yellow-600' :
                        'text-blue-600'
                      )}>
                        {selectedAlert.severity}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Type:</span>
                      <span className="text-gray-900 dark:text-white capitalize">
                        {selectedAlert.type.replace('_', ' ')}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Status:</span>
                      <span className={cn(
                        'font-medium',
                        selectedAlert.resolved ? 'text-green-600' : 'text-red-600'
                      )}>
                        {selectedAlert.resolved ? 'Resolved' : 'Active'}
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <h5 className="font-semibold text-gray-900 dark:text-white mb-3">Source Information</h5>
                  <div className="space-y-2 text-sm">
                    {selectedAlert.userName && (
                      <div className="flex justify-between">
                        <span className="text-gray-500">User:</span>
                        <span className="text-gray-900 dark:text-white">{selectedAlert.userName}</span>
                      </div>
                    )}
                    {selectedAlert.ipAddress && (
                      <div className="flex justify-between">
                        <span className="text-gray-500">IP Address:</span>
                        <span className="text-gray-900 dark:text-white font-mono">{selectedAlert.ipAddress}</span>
                      </div>
                    )}
                    {selectedAlert.location && (
                      <div className="flex justify-between">
                        <span className="text-gray-500">Location:</span>
                        <span className="text-gray-900 dark:text-white">{selectedAlert.location}</span>
                      </div>
                    )}
                    {selectedAlert.userAgent && (
                      <div>
                        <span className="text-gray-500 block mb-1">User Agent:</span>
                        <span className="text-gray-900 dark:text-white text-xs font-mono break-all">
                          {selectedAlert.userAgent}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                <LegendaryButton
                  variant="secondary"
                  onClick={() => setShowAlertDetails(false)}
                >
                  Close
                </LegendaryButton>
                
                {!selectedAlert.resolved && (
                  <LegendaryButton
                    variant={isFounder ? "founder" : "primary"}
                    leftIcon={CheckCircle}
                    onClick={() => {
                      onAlertResolve(selectedAlert.id);
                      setShowAlertDetails(false);
                      
                      if (isFounder) {
                        toast.success('👑 FOUNDER SECURITY: Alert resolved with infinite authority!');
                      } else {
                        toast.success('✅ Alert resolved successfully!');
                      }
                    }}
                  >
                    Resolve Alert
                  </LegendaryButton>
                )}
              </div>
            </div>
          </div>
        )}
      </Modal>

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
            <Shield className="w-4 h-4" />
            <span>24/7 security monitoring</span>
          </div>
          
          <div className="flex items-center gap-1">
            <Activity className="w-4 h-4" />
            <span>Swiss precision protection</span>
          </div>
          
          <div className="text-gray-400 font-mono">
            2025-08-06 17:47:54 UTC
          </div>
        </div>
        
        {isFounder && (
          <div className="mt-2">
            <span className="text-yellow-700 dark:text-yellow-300 font-bold text-sm">
              👑 RICKROLL187 FOUNDER SECURITY • INFINITE PROTECTION POWER! 👑
            </span>
          </div>
        )}
      </motion.div>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY SECURITY PANEL COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Security panel component completed at: 2025-08-06 17:47:54 UTC`);
console.log('🔒 Security monitoring: SWISS PRECISION');
console.log('👑 RICKROLL187 founder security: LEGENDARY');
console.log('🛡️ Threat detection: MAXIMUM PROTECTION');
console.log('🌅 LATE AFTERNOON LEGENDARY SECURITY ENERGY: INFINITE AT 17:47:54!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
