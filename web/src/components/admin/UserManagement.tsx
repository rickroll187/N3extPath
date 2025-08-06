// File: web/src/components/admin/UserManagement.tsx
/**
 * 👥🎸 N3EXTPATH - LEGENDARY USER MANAGEMENT COMPONENT 🎸👥
 * Swiss precision user administration with infinite code bro energy
 * Built: 2025-08-06 17:37:34 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Crown, 
  Users, 
  User, 
  Shield, 
  UserCheck,
  UserX,
  Ban,
  UnlockKeyhole,
  Eye,
  EyeOff,
  Edit,
  Mail,
  Phone,
  MapPin,
  Clock,
  Calendar,
  Search,
  Filter,
  MoreVertical,
  Star,
  Sparkles,
  Zap,
  Trophy,
  Target,
  Activity,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Settings,
  Download,
  Upload,
  RefreshCw,
  Plus,
  Trash2,
  Lock,
  Unlock
} from 'lucide-react';
import { LegendaryCard } from '@/components/ui/LegendaryCard';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { Modal } from '@/components/ui/Modal';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 👥 USER MANAGEMENT TYPES 👥
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

interface UserFilters {
  role?: string[];
  status?: string[];
  legendary?: boolean;
  verified?: boolean;
  search?: string;
}

interface UserManagementProps {
  users: AdminUser[];
  onUserUpdate: (user: AdminUser) => void;
  isFounder?: boolean;
}

// =====================================
// 🎸 USER ROW COMPONENT 🎸
// =====================================

const UserRow: React.FC<{
  user: AdminUser;
  onUpdate: (user: AdminUser) => void;
  onViewDetails: (user: AdminUser) => void;
  isFounder: boolean;
}> = ({ user, onUpdate, onViewDetails, isFounder }) => {
  const [showActions, setShowActions] = useState(false);

  // Get role styling
  const getRoleInfo = () => {
    switch (user.role) {
      case 'founder':
        return { 
          label: 'FOUNDER', 
          color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
          icon: Crown 
        };
      case 'admin':
        return { 
          label: 'Admin', 
          color: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300',
          icon: Shield 
        };
      case 'moderator':
        return { 
          label: 'Moderator', 
          color: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
          icon: Star 
        };
      default:
        return { 
          label: 'User', 
          color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
          icon: User 
        };
    }
  };

  // Get status styling
  const getStatusInfo = () => {
    switch (user.status) {
      case 'active':
        return { 
          label: 'Active', 
          color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
          icon: CheckCircle 
        };
      case 'suspended':
        return { 
          label: 'Suspended', 
          color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
          icon: Clock 
        };
      case 'banned':
        return { 
          label: 'Banned', 
          color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
          icon: Ban 
        };
      default:
        return { 
          label: 'Pending', 
          color: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300',
          icon: Clock 
        };
    }
  };

  const roleInfo = getRoleInfo();
  const statusInfo = getStatusInfo();
  const RoleIcon = roleInfo.icon;
  const StatusIcon = statusInfo.icon;

  // Handle role change
  const handleRoleChange = (newRole: AdminUser['role']) => {
    if (user.role === 'founder' && !isFounder) {
      toast.error('🚨 Cannot modify founder role!');
      return;
    }

    const updatedUser = { ...user, role: newRole };
    onUpdate(updatedUser);
    
    if (isFounder) {
      toast.success(`👑 FOUNDER ACTION: User role changed to ${newRole}!`, {
        duration: 3000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    } else {
      toast.success(`✅ User role updated to ${newRole}!`);
    }
  };

  // Handle status change
  const handleStatusChange = (newStatus: AdminUser['status']) => {
    if (user.role === 'founder' && newStatus !== 'active') {
      toast.error('🚨 Cannot suspend or ban founder!');
      return;
    }

    const updatedUser = { ...user, status: newStatus };
    onUpdate(updatedUser);
    
    const statusActions = {
      active: 'activated',
      suspended: 'suspended',
      banned: 'banned',
      pending: 'set to pending'
    };

    if (isFounder) {
      toast.success(`👑 FOUNDER ACTION: User ${statusActions[newStatus]}!`, {
        duration: 3000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    } else {
      toast.success(`✅ User ${statusActions[newStatus]}!`);
    }
  };

  // Format energy display
  const formatEnergy = (energy: number) => {
    if (energy >= 1000000) return `${(energy / 1000000).toFixed(1)}M`;
    if (energy >= 1000) return `${(energy / 1000).toFixed(1)}K`;
    return energy.toString();
  };

  return (
    <motion.tr
      className={cn(
        'hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors',
        user.role === 'founder' && 'bg-yellow-50/30 dark:bg-yellow-900/10'
      )}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* User Info */}
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="flex items-center gap-3">
          {/* Avatar */}
          <div className={cn(
            'w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold',
            user.role === 'founder' 
              ? 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white'
              : user.isLegendary
              ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white'
              : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
          )}>
            {user.avatar ? (
              <img 
                src={user.avatar} 
                alt={user.displayName}
                className="w-full h-full rounded-full object-cover"
              />
            ) : (
              <span>{user.displayName.charAt(0).toUpperCase()}</span>
            )}
          </div>

          {/* User Details */}
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className={cn(
                'font-semibold',
                user.role === 'founder' 
                  ? 'text-yellow-800 dark:text-yellow-300'
                  : 'text-gray-900 dark:text-white'
              )}>
                {user.displayName}
              </span>
              
              {user.role === 'founder' && <Crown className="w-4 h-4 text-yellow-600" />}
              {user.isLegendary && user.role !== 'founder' && <Sparkles className="w-4 h-4 text-purple-600" />}
              {user.verified && <CheckCircle className="w-4 h-4 text-blue-600" />}
            </div>
            
            <div className="text-sm text-gray-600 dark:text-gray-400">
              @{user.username}
            </div>
            
            <div className="text-xs text-gray-500 dark:text-gray-500">
              {user.email}
            </div>
          </div>
        </div>
      </td>

      {/* Role */}
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="relative">
          <span className={cn(
            'inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium',
            roleInfo.color
          )}>
            <RoleIcon className="w-3 h-3" />
            {roleInfo.label}
          </span>
        </div>
      </td>

      {/* Status */}
      <td className="px-6 py-4 whitespace-nowrap">
        <span className={cn(
          'inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium',
          statusInfo.color
        )}>
          <StatusIcon className="w-3 h-3" />
          {statusInfo.label}
        </span>
      </td>

      {/* Energy & Stats */}
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="text-sm">
          <div className="flex items-center gap-1 text-gray-900 dark:text-white">
            <Zap className="w-3 h-3 text-yellow-500" />
            <span className="font-semibold">{formatEnergy(user.codeBroEnergy)}</span>
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {user.totalOKRs} OKRs • {user.completionRate.toFixed(1)}%
          </div>
        </div>
      </td>

      {/* Last Login */}
      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
        <div className="flex items-center gap-1">
          <Clock className="w-3 h-3" />
          <span>{user.lastLogin.toLocaleDateString()}</span>
        </div>
        <div className="text-xs text-gray-500">
          {user.lastLogin.toLocaleTimeString()}
        </div>
      </td>

      {/* Location */}
      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
        {user.location && (
          <div className="flex items-center gap-1">
            <MapPin className="w-3 h-3" />
            <span className="truncate max-w-24">{user.location}</span>
          </div>
        )}
        {user.timezone && (
          <div className="text-xs text-gray-500">
            {user.timezone}
          </div>
        )}
      </td>

      {/* Actions */}
      <td className="px-6 py-4 whitespace-nowrap text-right">
        <AnimatePresence>
          {showActions && (
            <motion.div
              className="flex items-center justify-end gap-2"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.2 }}
            >
              {/* View Details */}
              <LegendaryButton
                variant="ghost"
                size="sm"
                onClick={() => onViewDetails(user)}
                className="p-1"
              >
                <Eye className="w-3 h-3" />
              </LegendaryButton>

              {/* Role Actions */}
              {user.role !== 'founder' && (
                <div className="relative group">
                  <LegendaryButton
                    variant="ghost"
                    size="sm"
                    className="p-1"
                  >
                    <Settings className="w-3 h-3" />
                  </LegendaryButton>
                  
                  {/* Dropdown Menu */}
                  <div className="absolute right-0 top-full mt-1 w-48 bg-white dark:bg-gray-700 rounded-lg shadow-xl border border-gray-200 dark:border-gray-600 py-2 z-50 opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto transition-opacity">
                    <div className="px-3 py-1 text-xs font-medium text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-600 mb-2">
                      Role Actions
                    </div>
                    
                    {(['user', 'moderator', 'admin'] as const).map((role) => (
                      <button
                        key={role}
                        onClick={() => handleRoleChange(role)}
                        disabled={user.role === role}
                        className={cn(
                          'w-full px-3 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors',
                          'flex items-center gap-2',
                          user.role === role && 'bg-gray-100 dark:bg-gray-600 text-gray-400'
                        )}
                      >
                        {role === 'admin' && <Shield className="w-3 h-3" />}
                        {role === 'moderator' && <Star className="w-3 h-3" />}
                        {role === 'user' && <User className="w-3 h-3" />}
                        <span className="capitalize">Make {role}</span>
                      </button>
                    ))}

                    <div className="border-t border-gray-200 dark:border-gray-600 my-2" />
                    
                    <div className="px-3 py-1 text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">
                      Status Actions
                    </div>
                    
                    {user.status !== 'active' && (
                      <button
                        onClick={() => handleStatusChange('active')}
                        className="w-full px-3 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors flex items-center gap-2 text-green-600"
                      >
                        <CheckCircle className="w-3 h-3" />
                        Activate User
                      </button>
                    )}
                    
                    {user.status !== 'suspended' && (
                      <button
                        onClick={() => handleStatusChange('suspended')}
                        className="w-full px-3 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors flex items-center gap-2 text-yellow-600"
                      >
                        <Clock className="w-3 h-3" />
                        Suspend User
                      </button>
                    )}
                    
                    {user.status !== 'banned' && (
                      <button
                        onClick={() => handleStatusChange('banned')}
                        className="w-full px-3 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors flex items-center gap-2 text-red-600"
                      >
                        <Ban className="w-3 h-3" />
                        Ban User
                      </button>
                    )}
                  </div>
                </div>
              )}

              {/* More Actions */}
              <LegendaryButton
                variant="ghost"
                size="sm"
                className="p-1"
                onClick={() => {
                  if (user.role === 'founder') {
                    toast.success('👑 LEGENDARY FOUNDER PROFILE ACCESS!', {
                      duration: 3000,
                      style: {
                        background: 'linear-gradient(135deg, #FFD700, #FFA500)',
                        color: '#000000',
                        fontWeight: '700',
                      },
                    });
                  } else {
                    toast.success('⚙️ User actions menu!');
                  }
                }}
              >
                <MoreVertical className="w-3 h-3" />
              </LegendaryButton>
            </motion.div>
          )}
        </AnimatePresence>
      </td>
    </motion.tr>
  );
};

// =====================================
// 🎸 LEGENDARY USER MANAGEMENT 🎸
// =====================================

export const UserManagement: React.FC<UserManagementProps> = ({
  users,
  onUserUpdate,
  isFounder = false,
}) => {
  const [filters, setFilters] = useState<UserFilters>({});
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
  const [showUserDetails, setShowUserDetails] = useState(false);
  const [sortBy, setSortBy] = useState<'name' | 'role' | 'energy' | 'lastLogin'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  useEffect(() => {
    console.log('👥🎸👥 LEGENDARY USER MANAGEMENT LOADED! 👥🎸👥');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`User management loaded at: 2025-08-06 17:37:34 UTC`);
    console.log('🌅 LATE AFTERNOON LEGENDARY USER MANAGEMENT ENERGY AT 17:37:34!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER USER MANAGEMENT ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER USER MANAGEMENT WITH INFINITE CODE BRO ENERGY!');
    }
  }, [isFounder]);

  // Filter and sort users
  const filteredUsers = useMemo(() => {
    let filtered = users;

    // Apply filters
    if (filters.search) {
      const search = filters.search.toLowerCase();
      filtered = filtered.filter(user => 
        user.displayName.toLowerCase().includes(search) ||
        user.username.toLowerCase().includes(search) ||
        user.email.toLowerCase().includes(search)
      );
    }

    if (filters.role?.length) {
      filtered = filtered.filter(user => filters.role?.includes(user.role));
    }

    if (filters.status?.length) {
      filtered = filtered.filter(user => filters.status?.includes(user.status));
    }

    if (filters.legendary !== undefined) {
      filtered = filtered.filter(user => user.isLegendary === filters.legendary);
    }

    if (filters.verified !== undefined) {
      filtered = filtered.filter(user => user.verified === filters.verified);
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue: any, bValue: any;
      
      switch (sortBy) {
        case 'name':
          aValue = a.displayName.toLowerCase();
          bValue = b.displayName.toLowerCase();
          break;
        case 'role':
          const roleOrder = { founder: 4, admin: 3, moderator: 2, user: 1 };
          aValue = roleOrder[a.role];
          bValue = roleOrder[b.role];
          break;
        case 'energy':
          aValue = a.codeBroEnergy;
          bValue = b.codeBroEnergy;
          break;
        case 'lastLogin':
          aValue = a.lastLogin.getTime();
          bValue = b.lastLogin.getTime();
          break;
        default:
          return 0;
      }

      if (aValue < bValue) return sortOrder === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

    return filtered;
  }, [users, filters, sortBy, sortOrder]);

  // Handle filter change
  const handleFilterChange = (key: keyof UserFilters, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  // Handle sort change
  const handleSort = (column: typeof sortBy) => {
    if (sortBy === column) {
      setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
  };

  // Handle user details view
  const handleViewUserDetails = (user: AdminUser) => {
    setSelectedUser(user);
    setShowUserDetails(true);
  };

  // Quick stats
  const stats = useMemo(() => {
    const total = users.length;
    const active = users.filter(u => u.status === 'active').length;
    const legendary = users.filter(u => u.isLegendary).length;
    const admins = users.filter(u => u.role === 'admin' || u.role === 'founder').length;
    
    return { total, active, legendary, admins };
  }, [users]);

  return (
    <div className="space-y-6">
      {/* Header with Quick Stats */}
      <div className="flex flex-col lg:flex-row gap-6 items-start lg:items-center justify-between">
        <div>
          <h2 className={cn(
            'text-xl font-bold mb-2',
            isFounder ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-white'
          )}>
            {isFounder && <Crown className="inline w-5 h-5 mr-2 text-yellow-600" />}
            👥 {isFounder ? 'Legendary User Command Center' : 'User Management'}
          </h2>
          
          <div className="flex items-center gap-6 text-sm text-gray-600 dark:text-gray-400">
            <div className="flex items-center gap-1">
              <Users className="w-4 h-4" />
              <span>{stats.total} total users</span>
            </div>
            
            <div className="flex items-center gap-1">
              <CheckCircle className="w-4 h-4 text-green-600" />
              <span>{stats.active} active</span>
            </div>
            
            <div className="flex items-center gap-1">
              <Sparkles className="w-4 h-4 text-purple-600" />
              <span>{stats.legendary} legendary</span>
            </div>
            
            <div className="flex items-center gap-1">
              <Shield className="w-4 h-4 text-blue-600" />
              <span>{stats.admins} admins</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <LegendaryButton
            variant="ghost"
            size="sm"
            leftIcon={RefreshCw}
            onClick={() => toast.success('🔄 User data refreshed!')}
          >
            Refresh
          </LegendaryButton>
          
          <LegendaryButton
            variant="ghost"
            size="sm"
            leftIcon={Download}
            onClick={() => toast.success('📊 Exporting user data!')}
          >
            Export
          </LegendaryButton>
          
          <LegendaryButton
            variant={isFounder ? "founder" : "primary"}
            leftIcon={Plus}
            onClick={() => toast.success(isFounder ? '👑 Founder user creation!' : '➕ New user invitation!')}
          >
            {isFounder ? 'Create User' : 'Invite User'}
          </LegendaryButton>
        </div>
      </div>

      {/* Filters */}
      <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-4 items-end">
          {/* Search */}
          <div className="lg:col-span-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Search Users
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Name, username, or email..."
                value={filters.search || ''}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                className={cn(
                  'w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  'focus:outline-none focus:ring-2 focus:ring-offset-2',
                  isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
                )}
              />
            </div>
          </div>

          {/* Role Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Role
            </label>
            <select
              value={filters.role?.[0] || ''}
              onChange={(e) => handleFilterChange('role', e.target.value ? [e.target.value] : undefined)}
              className={cn(
                'w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                'focus:outline-none focus:ring-2 focus:ring-offset-2',
                isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
              )}
            >
              <option value="">All Roles</option>
              <option value="founder">Founder</option>
              <option value="admin">Admin</option>
              <option value="moderator">Moderator</option>
              <option value="user">User</option>
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Status
            </label>
            <select
              value={filters.status?.[0] || ''}
              onChange={(e) => handleFilterChange('status', e.target.value ? [e.target.value] : undefined)}
              className={cn(
                'w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                'focus:outline-none focus:ring-2 focus:ring-offset-2',
                isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
              )}
            >
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="suspended">Suspended</option>
              <option value="banned">Banned</option>
              <option value="pending">Pending</option>
            </select>
          </div>

          {/* Legendary Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Legendary
            </label>
            <select
              value={filters.legendary === undefined ? '' : filters.legendary ? 'true' : 'false'}
              onChange={(e) => handleFilterChange('legendary', e.target.value === '' ? undefined : e.target.value === 'true')}
              className={cn(
                'w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                'focus:outline-none focus:ring-2 focus:ring-offset-2',
                isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
              )}
            >
              <option value="">All Users</option>
              <option value="true">Legendary Only</option>
              <option value="false">Standard Only</option>
            </select>
          </div>

          {/* Sort */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Sort By
            </label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
              className={cn(
                'w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                'focus:outline-none focus:ring-2 focus:ring-offset-2',
                isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
              )}
            >
              <option value="name">Name</option>
              <option value="role">Role</option>
              <option value="energy">Energy</option>
              <option value="lastLogin">Last Login</option>
            </select>
          </div>

          {/* Clear Filters */}
          <div className="flex items-end">
            <LegendaryButton
              variant="secondary"
              size="sm"
              onClick={() => {
                setFilters({});
                toast.success('🧹 Filters cleared!');
              }}
              className="w-full"
            >
              Clear
            </LegendaryButton>
          </div>
        </div>
      </LegendaryCard>

      {/* Users Table */}
      <LegendaryCard variant={isFounder ? 'founder' : 'elevated'} className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className={cn(
              'bg-gray-50 dark:bg-gray-800',
              isFounder && 'bg-gradient-to-r from-yellow-50/50 to-orange-50/50 dark:from-yellow-900/10 dark:to-orange-900/10'
            )}>
              <tr>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer hover:text-gray-700"
                  onClick={() => handleSort('name')}
                >
                  <div className="flex items-center gap-1">
                    User
                    {sortBy === 'name' && (
                      <span>{sortOrder === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </div>
                </th>
                
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer hover:text-gray-700"
                  onClick={() => handleSort('role')}
                >
                  <div className="flex items-center gap-1">
                    Role
                    {sortBy === 'role' && (
                      <span>{sortOrder === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </div>
                </th>
                
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Status
                </th>
                
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer hover:text-gray-700"
                  onClick={() => handleSort('energy')}
                >
                  <div className="flex items-center gap-1">
                    Energy & Stats
                    {sortBy === 'energy' && (
                      <span>{sortOrder === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </div>
                </th>
                
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer hover:text-gray-700"
                  onClick={() => handleSort('lastLogin')}
                >
                  <div className="flex items-center gap-1">
                    Last Login
                    {sortBy === 'lastLogin' && (
                      <span>{sortOrder === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </div>
                </th>
                
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Location
                </th>
                
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {filteredUsers.map((user) => (
                <UserRow
                  key={user.id}
                  user={user}
                  onUpdate={onUserUpdate}
                  onViewDetails={handleViewUserDetails}
                  isFounder={isFounder}
                />
              ))}
              
              {filteredUsers.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                    <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p className="text-lg font-medium mb-2">No users found</p>
                    <p className="text-sm">
                      {Object.keys(filters).length > 0 
                        ? 'Try adjusting your filters to find users'
                        : 'No users have been added to the system yet'
                      }
                    </p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        
        {/* Results Summary */}
        <div className={cn(
          'px-6 py-3 border-t border-gray-200 dark:border-gray-700 text-sm text-gray-600 dark:text-gray-400',
          'bg-gray-50 dark:bg-gray-800',
          isFounder && 'bg-gradient-to-r from-yellow-50/30 to-orange-50/30 dark:from-yellow-900/10 dark:to-orange-900/10'
        )}>
          Showing {filteredUsers.length} of {users.length} users
          {isFounder && (
            <span className="ml-4 text-yellow-700 dark:text-yellow-300 font-bold">
              👑 FOUNDER USER MANAGEMENT • 17:37:34 UTC! 👑
            </span>
          )}
        </div>
      </LegendaryCard>

      {/* User Details Modal */}
      <Modal 
        isOpen={showUserDetails} 
        onClose={() => setShowUserDetails(false)}
        size="lg"
      >
        {selectedUser && (
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                User Details
              </h3>
              <button
                onClick={() => setShowUserDetails(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <XCircle className="w-6 h-6" />
              </button>
            </div>
            
            <div className="space-y-6">
              {/* User Profile */}
              <div className="flex items-start gap-4">
                <div className={cn(
                  'w-16 h-16 rounded-full flex items-center justify-center text-lg font-bold',
                  selectedUser.role === 'founder' 
                    ? 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white'
                    : selectedUser.isLegendary
                    ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white'
                    : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                )}>
                  {selectedUser.avatar ? (
                    <img 
                      src={selectedUser.avatar} 
                      alt={selectedUser.displayName}
                      className="w-full h-full rounded-full object-cover"
                    />
                  ) : (
                    <span>{selectedUser.displayName.charAt(0).toUpperCase()}</span>
                  )}
                </div>
                
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="text-lg font-bold text-gray-900 dark:text-white">
                      {selectedUser.displayName}
                    </h4>
                    {selectedUser.role === 'founder' && <Crown className="w-5 h-5 text-yellow-600" />}
                    {selectedUser.isLegendary && <Sparkles className="w-5 h-5 text-purple-600" />}
                    {selectedUser.verified && <CheckCircle className="w-5 h-5 text-blue-600" />}
                  </div>
                  
                  <p className="text-gray-600 dark:text-gray-400 mb-1">@{selectedUser.username}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-500">{selectedUser.email}</p>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">
                    {selectedUser.codeBroEnergy >= 1000000 
                      ? `${(selectedUser.codeBroEnergy / 1000000).toFixed(1)}M`
                      : selectedUser.codeBroEnergy >= 1000 
                        ? `${(selectedUser.codeBroEnergy / 1000).toFixed(1)}K`
                        : selectedUser.codeBroEnergy
                    }
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">Code Bro Energy</div>
                </div>
                
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">
                    {selectedUser.totalOKRs}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">Total OKRs</div>
                </div>
                
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">
                    {selectedUser.completionRate.toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">Completion Rate</div>
                </div>
                
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">
                    {Math.floor((Date.now() - selectedUser.joinedAt.getTime()) / (1000 * 60 * 60 * 24))}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">Days Active</div>
                </div>
              </div>

              {/* Additional Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h5 className="font-semibold text-gray-900 dark:text-white mb-3">Account Info</h5>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Joined:</span>
                      <span className="text-gray-900 dark:text-white">
                        {selectedUser.joinedAt.toLocaleDateString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Last Login:</span>
                      <span className="text-gray-900 dark:text-white">
                        {selectedUser.lastLogin.toLocaleDateString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Status:</span>
                      <span className={cn(
                        'capitalize',
                        selectedUser.status === 'active' ? 'text-green-600' :
                        selectedUser.status === 'suspended' ? 'text-yellow-600' :
                        selectedUser.status === 'banned' ? 'text-red-600' : 'text-gray-600'
                      )}>
                        {selectedUser.status}
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <h5 className="font-semibold text-gray-900 dark:text-white mb-3">Location Info</h5>
                  <div className="space-y-2 text-sm">
                    {selectedUser.location && (
                      <div className="flex justify-between">
                        <span className="text-gray-500">Location:</span>
                        <span className="text-gray-900 dark:text-white">{selectedUser.location}</span>
                      </div>
                    )}
                    {selectedUser.timezone && (
                      <div className="flex justify-between">
                        <span className="text-gray-500">Timezone:</span>
                        <span className="text-gray-900 dark:text-white">{selectedUser.timezone}</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                <LegendaryButton
                  variant="secondary"
                  onClick={() => setShowUserDetails(false)}
                >
                  Close
                </LegendaryButton>
                
                {selectedUser.role !== 'founder' && (
                  <LegendaryButton
                    variant={isFounder ? "founder" : "primary"}
                    leftIcon={Edit}
                    onClick={() => {
                      setShowUserDetails(false);
                      toast.success(isFounder ? '👑 Founder user edit mode!' : '✏️ Edit user mode!');
                    }}
                  >
                    Edit User
                  </LegendaryButton>
                )}
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY USER MANAGEMENT COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`User management component completed at: 2025-08-06 17:37:34 UTC`);
console.log('👥 User administration: SWISS PRECISION');
console.log('👑 RICKROLL187 founder user management: LEGENDARY');
console.log('⚙️ Role & status management: MAXIMUM CONTROL');
console.log('🌅 LATE AFTERNOON LEGENDARY USER MANAGEMENT ENERGY: INFINITE AT 17:37:34!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
