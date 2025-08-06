// File: web/src/pages/AdminDashboard.tsx
/**
 * 👑🎸 N3EXTPATH - LEGENDARY ADMIN DASHBOARD PAGE 🎸👑
 * Swiss precision admin management with infinite code bro energy
 * Built: 2025-08-06 17:25:12 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Helmet } from 'react-helmet-async';
import { 
  Shield, 
  Crown, 
  Users, 
  Server, 
  Activity, 
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Settings,
  Database,
  Globe,
  Zap,
  Sparkles,
  Trophy,
  Star,
  BarChart3,
  PieChart,
  LineChart,
  Monitor,
  UserCheck,
  UserX,
  Ban,
  UnlockKeyhole,
  Eye,
  EyeOff,
  RefreshCw,
  Download,
  Upload,
  Calendar,
  Clock,
  Bell,
  MessageSquare,
  Mail,
  Phone,
  MapPin,
  ExternalLink,
  Search,
  Filter,
  MoreVertical
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { AdminStats } from '@/components/admin/AdminStats';
import { UserManagement } from '@/components/admin/UserManagement';
import { SystemHealth } from '@/components/admin/SystemHealth';
import { SecurityPanel } from '@/components/admin/SecurityPanel';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 👑 ADMIN TYPES 👑
// =====================================

interface AdminUser {
  id: string;
  username: string;
  displayName: string;
  email: string;
  avatar?: string;
  role: 'founder' | 'admin' | 'moderator' | 'user';
  status: 'active' | 'suspended' | 'banned' | 'pending';
  isLegendary: boolean;
  codeBroEnergy: number;
  joinedAt: Date;
  lastLogin: Date;
  totalOKRs: number;
  completionRate: number;
  location?: string;
  timezone?: string;
  verified: boolean;
}

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

interface SecurityAlert {
  id: string;
  type: 'login_attempt' | 'permission_change' | 'data_access' | 'system_error' | 'suspicious_activity';
  severity: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  userId?: string;
  userAgent?: string;
  ipAddress?: string;
  timestamp: Date;
  resolved: boolean;
}

// =====================================
// 🎸 LEGENDARY ADMIN DASHBOARD 🎸
// =====================================

export const AdminDashboard: React.FC = () => {
  const { user, isFounder, isAdmin } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [alerts, setAlerts] = useState<SecurityAlert[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    console.log('👑🎸👑 LEGENDARY ADMIN DASHBOARD LOADED! 👑🎸👑');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Admin dashboard loaded at: 2025-08-06 17:25:12 UTC`);
    console.log('🌅 LATE AFTERNOON LEGENDARY ADMIN ENERGY AT 17:25:12!');

    if (isFounder) {
      console.log('👑🔥👑 RICKROLL187 FOUNDER ADMIN DASHBOARD ACTIVATED! 👑🔥👑');
      console.log('🚀 LEGENDARY FOUNDER ADMIN DASHBOARD WITH INFINITE CONTROL POWER!');
      console.log('⚙️ SWISS PRECISION FOUNDER ADMIN SYSTEM!');
      
      toast.success('👑 Welcome to your LEGENDARY FOUNDER ADMIN DASHBOARD! Infinite control power activated!', {
        duration: 6000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    } else if (isAdmin) {
      toast.success('🛡️ Admin dashboard loaded with Swiss precision!', {
        duration: 4000,
      });
    }

    loadAdminData();
    
    // Auto refresh every 30 seconds
    const interval = autoRefresh ? setInterval(loadAdminData, 30000) : null;
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isFounder, isAdmin, autoRefresh]);

  // Load admin data
  const loadAdminData = useCallback(async () => {
    try {
      // Generate mock admin data
      await loadSystemMetrics();
      await loadUsers();
      await loadSecurityAlerts();
      
    } catch (error) {
      console.error('🚨 Error loading admin data:', error);
      toast.error('Failed to load admin data');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Load system metrics
  const loadSystemMetrics = useCallback(async () => {
    // Simulate API call with realistic data
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const mockMetrics: SystemMetrics = {
      totalUsers: 1247,
      activeUsers: 892,
      totalOKRs: 3456,
      completedOKRs: 2134,
      systemUptime: 99.7,
      serverLoad: 68.5,
      databaseConnections: 145,
      totalSessions: 432,
      apiRequests: 15742,
      storageUsed: 78.3,
      bandwidthUsed: 456.7,
      errorRate: 0.03,
      averageResponseTime: 127,
    };

    setMetrics(mockMetrics);
  }, []);

  // Load users
  const loadUsers = useCallback(async () => {
    await new Promise(resolve => setTimeout(resolve, 300));
    
    const mockUsers: AdminUser[] = [
      {
        id: 'rickroll187',
        username: 'rickroll187',
        displayName: 'RICKROLL187',
        email: 'letstalktech010@gmail.com',
        avatar: 'https://avatars.githubusercontent.com/rickroll187.png',
        role: 'founder',
        status: 'active',
        isLegendary: true,
        codeBroEnergy: 999999,
        joinedAt: new Date('2025-01-01'),
        lastLogin: new Date('2025-08-06T17:25:12.000Z'),
        totalOKRs: 42,
        completionRate: 96.8,
        location: 'Code Bro Universe',
        timezone: 'UTC',
        verified: true,
      },
      {
        id: 'codebro42',
        username: 'codebro42',
        displayName: 'CodeBro42',
        email: 'codebro42@n3extpath.com',
        avatar: 'https://avatars.githubusercontent.com/codebro42.png',
        role: 'admin',
        status: 'active',
        isLegendary: true,
        codeBroEnergy: 8500,
        joinedAt: new Date('2025-01-15'),
        lastLogin: new Date('2025-08-06T16:45:00.000Z'),
        totalOKRs: 28,
        completionRate: 89.3,
        location: 'Switzerland',
        timezone: 'UTC+1',
        verified: true,
      },
      {
        id: 'swissdev',
        username: 'swissdev',
        displayName: 'SwissDev',
        email: 'swiss@n3extpath.com',
        role: 'moderator',
        status: 'active',
        isLegendary: false,
        codeBroEnergy: 7200,
        joinedAt: new Date('2025-02-01'),
        lastLogin: new Date('2025-08-06T15:30:00.000Z'),
        totalOKRs: 15,
        completionRate: 78.9,
        location: 'Zürich, Switzerland',
        timezone: 'UTC+1',
        verified: true,
      },
      {
        id: 'newuser123',
        username: 'newuser123',
        displayName: 'NewUser123',
        email: 'newuser@example.com',
        role: 'user',
        status: 'pending',
        isLegendary: false,
        codeBroEnergy: 100,
        joinedAt: new Date('2025-08-06'),
        lastLogin: new Date('2025-08-06T17:00:00.000Z'),
        totalOKRs: 1,
        completionRate: 0,
        location: 'Unknown',
        timezone: 'UTC',
        verified: false,
      },
    ];

    setUsers(mockUsers);
  }, []);

  // Load security alerts
  const loadSecurityAlerts = useCallback(async () => {
    await new Promise(resolve => setTimeout(resolve, 200));
    
    const mockAlerts: SecurityAlert[] = [
      {
        id: 'alert-1',
        type: 'login_attempt',
        severity: 'medium',
        message: 'Multiple failed login attempts detected',
        userId: 'suspicious-user',
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        ipAddress: '192.168.1.100',
        timestamp: new Date('2025-08-06T17:20:00.000Z'),
        resolved: false,
      },
      {
        id: 'alert-2',
        type: 'permission_change',
        severity: 'high',
        message: 'User role elevated to admin',
        userId: 'codebro42',
        timestamp: new Date('2025-08-06T16:30:00.000Z'),
        resolved: true,
      },
      {
        id: 'alert-3',
        type: 'system_error',
        severity: 'low',
        message: 'Database connection temporarily unavailable',
        timestamp: new Date('2025-08-06T15:45:00.000Z'),
        resolved: true,
      },
    ];

    setAlerts(mockAlerts);
  }, []);

  // Tab configuration
  const adminTabs = [
    { 
      id: 'overview', 
      label: isFounder ? 'Founder Overview' : 'Overview', 
      icon: Shield,
      description: 'System metrics and key insights'
    },
    { 
      id: 'users', 
      label: 'User Management', 
      icon: Users,
      description: 'Manage users, roles, and permissions'
    },
    { 
      id: 'system', 
      label: 'System Health', 
      icon: Server,
      description: 'Server status, performance, and monitoring'
    },
    { 
      id: 'security', 
      label: 'Security', 
      icon: Shield,
      description: 'Security alerts, logs, and controls'
    },
    ...(isFounder ? [{
      id: 'founder',
      label: 'Founder Control',
      icon: Crown,
      description: 'Legendary founder-only controls and settings'
    }] : []),
    { 
      id: 'settings', 
      label: 'Settings', 
      icon: Settings,
      description: 'System configuration and preferences'
    },
  ];

  // Handle tab change
  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
    
    if (isFounder && tabId === 'founder') {
      toast.success('👑 Entering LEGENDARY FOUNDER CONTROL CENTER!', {
        duration: 3000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    }
  };

  // Quick actions
  const quickActions = [
    {
      title: isFounder ? 'Create Founder Broadcast' : 'Send System Notification',
      description: isFounder ? 'Send legendary message to all users' : 'Send notification to all users',
      icon: Bell,
      action: () => {
        if (isFounder) {
          toast.success('👑 Founder broadcast system activated!');
        } else {
          toast.success('📢 Notification system activated!');
        }
      },
      color: isFounder ? 'text-yellow-600 bg-yellow-100' : 'text-blue-600 bg-blue-100',
    },
    {
      title: 'Export System Data',
      description: 'Download comprehensive system reports',
      icon: Download,
      action: () => toast.success('📊 System data export initiated!'),
      color: 'text-green-600 bg-green-100',
    },
    {
      title: 'Refresh All Data',
      description: 'Force refresh all admin dashboard data',
      icon: RefreshCw,
      action: () => {
        setIsLoading(true);
        loadAdminData();
        toast.success('🔄 Admin data refreshed!');
      },
      color: 'text-purple-600 bg-purple-100',
    },
    {
      title: isFounder ? 'Legendary Backup' : 'System Backup',
      description: isFounder ? 'Create legendary system backup' : 'Create full system backup',
      icon: Database,
      action: () => {
        if (isFounder) {
          toast.success('👑 LEGENDARY BACKUP initiated with infinite precision!');
        } else {
          toast.success('💾 System backup initiated!');
        }
      },
      color: isFounder ? 'text-yellow-600 bg-yellow-100' : 'text-orange-600 bg-orange-100',
    },
  ];

  // Render tab content
  const renderTabContent = () => {
    if (isLoading) {
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
                ? 'Loading legendary founder admin data...'
                : 'Loading admin dashboard...'
              }
            </p>
          </div>
        </div>
      );
    }

    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-6">
            {/* Quick Stats */}
            {metrics && (
              <AdminStats 
                metrics={metrics} 
                isFounder={isFounder}
              />
            )}

            {/* Quick Actions */}
            <div>
              <h3 className={cn(
                'text-lg font-semibold mb-4',
                isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
              )}>
                {isFounder ? 'Legendary Quick Actions' : 'Quick Actions'}
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
                {quickActions.map((action, index) => (
                  <motion.div
                    key={action.title}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                  >
                    <LegendaryCard 
                      variant={isFounder ? 'founder' : 'elevated'}
                      className="p-4 cursor-pointer transition-all hover:scale-105"
                      onClick={action.action}
                    >
                      <div className="flex items-start gap-3">
                        <div className={cn(
                          'p-2 rounded-lg',
                          action.color
                        )}>
                          <action.icon className="w-5 h-5" />
                        </div>
                        
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-900 dark:text-white">
                            {action.title}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {action.description}
                          </p>
                        </div>
                      </div>
                    </LegendaryCard>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Recent Activity */}
            <div>
              <h3 className={cn(
                'text-lg font-semibold mb-4',
                isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
              )}>
                Recent System Activity
              </h3>
              
              <LegendaryCard variant={isFounder ? 'founder' : 'elevated'}>
                <div className="p-4 space-y-4">
                  {alerts.slice(0, 5).map((alert) => (
                    <div key={alert.id} className="flex items-start gap-3 pb-3 border-b border-gray-100 dark:border-gray-700 last:border-0 last:pb-0">
                      <div className={cn(
                        'w-2 h-2 rounded-full mt-2',
                        alert.severity === 'critical' ? 'bg-red-500' :
                        alert.severity === 'high' ? 'bg-orange-500' :
                        alert.severity === 'medium' ? 'bg-yellow-500' : 'bg-blue-500'
                      )} />
                      
                      <div className="flex-1">
                        <p className="text-sm text-gray-900 dark:text-white">
                          {alert.message}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          {alert.timestamp.toLocaleString()}
                          {alert.userId && ` • User: ${alert.userId}`}
                        </p>
                      </div>
                      
                      <span className={cn(
                        'text-xs px-2 py-1 rounded-full',
                        alert.resolved 
                          ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
                          : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
                      )}>
                        {alert.resolved ? 'Resolved' : 'Active'}
                      </span>
                    </div>
                  ))}
                </div>
              </LegendaryCard>
            </div>
          </div>
        );

      case 'users':
        return (
          <UserManagement 
            users={users}
            onUserUpdate={(updatedUser) => {
              setUsers(prev => prev.map(u => u.id === updatedUser.id ? updatedUser : u));
            }}
            isFounder={isFounder}
          />
        );

      case 'system':
        return (
          <SystemHealth 
            metrics={metrics}
            isFounder={isFounder}
            onRefresh={loadAdminData}
          />
        );

      case 'security':
        return (
          <SecurityPanel 
            alerts={alerts}
            onAlertResolve={(alertId) => {
              setAlerts(prev => prev.map(a => a.id === alertId ? { ...a, resolved: true } : a));
            }}
            isFounder={isFounder}
          />
        );

      case 'founder':
        return isFounder ? (
          <div className="space-y-6">
            <LegendaryCard variant="founder" className="p-6">
              <div className="text-center">
                <Crown className="w-16 h-16 text-yellow-600 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-yellow-900 dark:text-yellow-100 mb-2">
                  👑 LEGENDARY FOUNDER CONTROL CENTER 👑
                </h2>
                <p className="text-yellow-700 dark:text-yellow-300 mb-6">
                  🚀 Infinite administrative power with Swiss precision control! This is where legendary decisions are made! 🚀
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <LegendaryButton
                    variant="founder"
                    leftIcon={Sparkles}
                    onClick={() => toast.success('✨ Legendary feature unleashed!')}
                  >
                    Activate Legendary Mode
                  </LegendaryButton>
                  
                  <LegendaryButton
                    variant="founder"
                    leftIcon={Zap}
                    onClick={() => toast.success('⚡ Infinite energy boost activated!')}
                  >
                    Energy Boost All Users
                  </LegendaryButton>
                  
                  <LegendaryButton
                    variant="founder"
                    leftIcon={Trophy}
                    onClick={() => toast.success('🏆 Platform celebration initiated!')}
                  >
                    Celebrate Platform Success
                  </LegendaryButton>
                </div>
              </div>
            </LegendaryCard>
            
            {/* Founder Statistics */}
            <LegendaryCard variant="founder" className="p-6">
              <h3 className="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-4">
                👑 FOUNDER IMPACT METRICS 👑
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600 mb-1">999,999</div>
                  <div className="text-sm text-yellow-700">Legendary Energy Created</div>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600 mb-1">42</div>
                  <div className="text-sm text-yellow-700">Founder OKRs Completed</div>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600 mb-1">100%</div>
                  <div className="text-sm text-yellow-700">Swiss Precision Achieved</div>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600 mb-1">∞</div>
                  <div className="text-sm text-yellow-700">Code Bro Inspiration</div>
                </div>
              </div>
            </LegendaryCard>
          </div>
        ) : null;

      case 'settings':
        return (
          <div className="space-y-6">
            <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-6">
              <h3 className={cn(
                'text-lg font-semibold mb-4',
                isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
              )}>
                {isFounder ? 'Legendary System Settings' : 'System Settings'}
              </h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">Auto Refresh</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Automatically refresh dashboard data every 30 seconds</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={autoRefresh}
                      onChange={(e) => setAutoRefresh(e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>
                
                {isFounder && (
                  <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Crown className="w-4 h-4 text-yellow-600" />
                      <p className="font-medium text-yellow-900 dark:text-yellow-100">Founder Settings</p>
                    </div>
                    <p className="text-sm text-yellow-700 dark:text-yellow-300">
                      👑 Additional legendary founder settings and controls coming soon with infinite customization power!
                    </p>
                  </div>
                )}
              </div>
            </LegendaryCard>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <>
      <Helmet>
        <title>
          {isFounder ? '👑 Founder Admin Dashboard | N3EXTPATH' : 'Admin Dashboard | N3EXTPATH'}
        </title>
        <meta 
          name="description" 
          content={isFounder 
            ? "RICKROLL187 founder admin dashboard with infinite control power and Swiss precision management" 
            : "Legendary admin dashboard with Swiss precision system management, user control, and infinite monitoring power"
          } 
        />
      </Helmet>

      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Header */}
        <motion.div 
          className={cn(
            'bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700',
            isFounder && 'bg-gradient-to-r from-yellow-50 via-orange-50 to-yellow-50 dark:from-yellow-900/20 dark:via-orange-900/20 dark:to-yellow-900/20'
          )}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              {/* Title Section */}
              <div className="flex items-center gap-4">
                <div className={cn(
                  'p-3 rounded-xl',
                  isFounder 
                    ? 'bg-gradient-to-r from-yellow-100 to-orange-100 dark:from-yellow-900/30 dark:to-orange-900/30'
                    : 'bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30'
                )}>
                  {isFounder && <Crown className="w-8 h-8 text-yellow-600" />}
                  <Shield className={cn(
                    'w-8 h-8',
                    isFounder ? 'text-yellow-600' : 'text-blue-600'
                  )} />
                </div>
                
                <div>
                  <h1 className={cn(
                    'text-3xl font-bold',
                    isFounder 
                      ? 'text-yellow-900 dark:text-yellow-100' 
                      : 'text-gray-900 dark:text-white'
                  )}>
                    {isFounder ? 'Founder Admin Command Center' : 'Admin Dashboard'}
                    {isFounder && (
                      <span className="ml-3 text-2xl">👑</span>
                    )}
                  </h1>
                  
                  <p className={cn(
                    'text-lg mt-1',
                    isFounder 
                      ? 'text-yellow-700 dark:text-yellow-300' 
                      : 'text-gray-600 dark:text-gray-400'
                  )}>
                    {isFounder 
                      ? '🚀 Infinite system control with legendary Swiss precision!'
                      : '🛡️ System management with Swiss precision and code bro energy!'
                    }
                  </p>
                </div>
              </div>

              {/* Status Indicators */}
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className={cn(
                    'w-2 h-2 rounded-full',
                    metrics && metrics.systemUptime > 99 ? 'bg-green-500' : 'bg-yellow-500'
                  )} />
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    System {metrics && metrics.systemUptime > 99 ? 'Healthy' : 'Warning'}
                  </span>
                </div>
                
                <div className="text-sm text-gray-500 dark:text-gray-400 font-mono">
                  17:25:12 UTC
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {/* Tab Navigation */}
          <motion.div 
            className="mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="border-b border-gray-200 dark:border-gray-700">
              <nav className="-mb-px flex space-x-8 overflow-x-auto">
                {adminTabs.map((tab) => {
                  const TabIcon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => handleTabChange(tab.id)}
                      className={cn(
                        'group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap',
                        'transition-colors duration-200',
                        activeTab === tab.id
                          ? isFounder
                            ? 'border-yellow-500 text-yellow-600 dark:text-yellow-400'
                            : 'border-blue-500 text-blue-600 dark:text-blue-400'
                          : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 hover:border-gray-300'
                      )}
                    >
                      <TabIcon className={cn(
                        'w-5 h-5 mr-2',
                        activeTab === tab.id
                          ? isFounder ? 'text-yellow-600' : 'text-blue-600'
                          : 'text-gray-400 group-hover:text-gray-500'
                      )} />
                      {tab.label}
                    </button>
                  );
                })}
              </nav>
            </div>
          </motion.div>

          {/* Tab Content */}
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4 }}
          >
            {renderTabContent()}
          </motion.div>
        </div>

        {/* Bottom Status Bar */}
        <motion.div
          className={cn(
            'border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800',
            isFounder && 'bg-gradient-to-r from-yellow-50/30 to-orange-50/30 dark:from-yellow-900/10 dark:to-orange-900/10'
          )}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-6 text-gray-500 dark:text-gray-400">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4" />
                  <span>Swiss precision admin system</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4" />
                  <span>Real-time monitoring active</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <Globe className="w-4 h-4" />
                  <span>Global admin control</span>
                </div>
              </div>
              
              <div className="font-mono text-gray-400">
                Admin Session: 17:25:12 UTC
              </div>
            </div>
            
            {isFounder && (
              <div className="text-center mt-2">
                <span className="text-yellow-700 dark:text-yellow-300 font-bold text-sm">
                  👑 RICKROLL187 FOUNDER ADMIN DASHBOARD • INFINITE CONTROL POWER! 👑
                </span>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </>
  );
};

console.log('🎸🎸🎸 LEGENDARY ADMIN DASHBOARD PAGE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Admin dashboard page completed at: 2025-08-06 17:25:12 UTC`);
console.log('👑 Admin control: SWISS PRECISION');
console.log('👑 RICKROLL187 founder admin: LEGENDARY');
console.log('🛡️ System management: MAXIMUM CONTROL');
console.log('🌅 LATE AFTERNOON LEGENDARY ADMIN ENERGY: INFINITE AT 17:25:12!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
