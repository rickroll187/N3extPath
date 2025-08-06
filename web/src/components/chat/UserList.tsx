// File: web/src/components/chat/UserList.tsx
/**
 * 👥🎸 N3EXTPATH - LEGENDARY USER LIST COMPONENT 🎸👥
 * Swiss precision user display with infinite code bro energy
 * Built: 2025-08-06 17:01:18 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Crown, 
  Users, 
  Sparkles, 
  Zap, 
  Circle, 
  Clock,
  MessageCircle,
  UserPlus,
  Settings,
  MoreVertical,
  Star,
  Shield,
  Activity,
  Eye,
  Search
} from 'lucide-react';
import { LegendaryButton } from '@/components/ui/LegendaryButton';
import { cn } from '@/utils/cn';
import toast from 'react-hot-toast';

// =====================================
// 👥 USER LIST TYPES 👥
// =====================================

interface ChatUser {
  id: string;
  username: string;
  displayName: string;
  avatar?: string;
  status: 'online' | 'away' | 'busy' | 'offline';
  isFounder?: boolean;
  isLegendary?: boolean;
  lastSeen?: Date;
  codeBroEnergy?: number;
  role?: 'owner' | 'admin' | 'member';
  customStatus?: string;
}

interface UserListProps {
  users: ChatUser[];
  isFounder?: boolean;
  title?: string;
  compact?: boolean;
  maxVisible?: number;
  showInvite?: boolean;
  onUserClick?: (user: ChatUser) => void;
  onInviteClick?: () => void;
}

// =====================================
// 🎸 USER ITEM COMPONENT 🎸
// =====================================

const UserItem: React.FC<{
  user: ChatUser;
  compact: boolean;
  isFounder: boolean;
  onClick: () => void;
}> = ({ user, compact, isFounder, onClick }) => {
  const [showActions, setShowActions] = useState(false);

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'bg-green-500';
      case 'away': return 'bg-yellow-500';
      case 'busy': return 'bg-red-500';
      default: return 'bg-gray-400';
    }
  };

  // Format last seen
  const formatLastSeen = (date?: Date) => {
    if (!date) return null;
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  };

  // Format energy level
  const formatEnergy = (energy?: number) => {
    if (!energy) return '0';
    if (energy >= 1000000) return `${(energy / 1000000).toFixed(1)}M`;
    if (energy >= 1000) return `${(energy / 1000).toFixed(1)}K`;
    return energy.toString();
  };

  return (
    <motion.div
      className={cn(
        'group flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-all',
        'hover:bg-gray-100 dark:hover:bg-gray-700',
        user.isFounder && 'bg-gradient-to-r from-yellow-50/50 to-orange-50/50 hover:from-yellow-100/50 hover:to-orange-100/50',
        user.isFounder && 'dark:from-yellow-900/20 dark:to-orange-900/20 dark:hover:from-yellow-900/30 dark:hover:to-orange-900/30'
      )}
      onClick={onClick}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      {/* Avatar */}
      <div className="relative flex-shrink-0">
        <div className={cn(
          'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold',
          user.isFounder 
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
        
        {/* Status Indicator */}
        <div className={cn(
          'absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-white dark:border-gray-800',
          getStatusColor(user.status)
        )} />
      </div>

      {/* User Info */}
      {!compact && (
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-1">
            <span className={cn(
              'font-medium text-sm truncate',
              user.isFounder 
                ? 'text-yellow-800 dark:text-yellow-300'
                : user.isLegendary
                ? 'text-purple-800 dark:text-purple-300'
                : 'text-gray-900 dark:text-white'
            )}>
              {user.displayName}
            </span>
            
            {user.isFounder && (
              <Crown className="w-3 h-3 text-yellow-600 flex-shrink-0" />
            )}
            {user.isLegendary && !user.isFounder && (
              <Sparkles className="w-3 h-3 text-purple-600 flex-shrink-0" />
            )}
            {user.role === 'admin' && !user.isFounder && (
              <Shield className="w-3 h-3 text-blue-600 flex-shrink-0" />
            )}
          </div>
          
          <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
            <span className="capitalize">{user.status}</span>
            
            {user.codeBroEnergy && (
              <>
                <span>•</span>
                <div className="flex items-center gap-1">
                  <Zap className="w-3 h-3" />
                  <span>{formatEnergy(user.codeBroEnergy)}</span>
                </div>
              </>
            )}
            
            {user.status === 'offline' && user.lastSeen && (
              <>
                <span>•</span>
                <span>{formatLastSeen(user.lastSeen)}</span>
              </>
            )}
          </div>
          
          {user.customStatus && (
            <div className="text-xs text-gray-600 dark:text-gray-300 mt-1 truncate">
              {user.customStatus}
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <AnimatePresence>
        {!compact && showActions && (
          <motion.div
            className="flex items-center gap-1"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.2 }}
          >
            <LegendaryButton
              variant="ghost"
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                toast.success(`📱 Starting DM with ${user.displayName}!`);
              }}
              className="p-1"
            >
              <MessageCircle className="w-3 h-3" />
            </LegendaryButton>
            
            <LegendaryButton
              variant="ghost"
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                // Show user profile or options
              }}
              className="p-1"
            >
              <MoreVertical className="w-3 h-3" />
            </LegendaryButton>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

// =====================================
// 🎸 LEGENDARY USER LIST 🎸
// =====================================

export const UserList: React.FC<UserListProps> = ({
  users,
  isFounder = false,
  title = "Team Members",
  compact = false,
  maxVisible,
  showInvite = true,
  onUserClick,
  onInviteClick,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    console.log('👥🎸👥 LEGENDARY USER LIST LOADED! 👥🎸👥');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`User list loaded at: 2025-08-06 17:01:18 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY USER LIST ENERGY AT 17:01:18!');

    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER USER LIST ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER USER LIST WITH INFINITE CODE BRO ENERGY!');
    }
  }, [isFounder]);

  // Sort and filter users
  const sortedUsers = useMemo(() => {
    let filtered = users;

    // Filter by search
    if (searchQuery.trim()) {
      filtered = users.filter(user => 
        user.displayName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.username.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Sort by priority: founder -> legendary -> online -> away -> busy -> offline
    return filtered.sort((a, b) => {
      // Founder first
      if (a.isFounder && !b.isFounder) return -1;
      if (!a.isFounder && b.isFounder) return 1;
      
      // Then legendary
      if (a.isLegendary && !b.isLegendary) return -1;
      if (!a.isLegendary && b.isLegendary) return 1;
      
      // Then by status
      const statusOrder = { online: 0, away: 1, busy: 2, offline: 3 };
      const statusDiff = statusOrder[a.status] - statusOrder[b.status];
      if (statusDiff !== 0) return statusDiff;
      
      // Finally by name
      return a.displayName.localeCompare(b.displayName);
    });
  }, [users, searchQuery]);

  // Visible users (with max limit)
  const visibleUsers = useMemo(() => {
    if (!maxVisible || showAll) return sortedUsers;
    return sortedUsers.slice(0, maxVisible);
  }, [sortedUsers, maxVisible, showAll]);

  // Group users by status
  const groupedUsers = useMemo(() => {
    const online = visibleUsers.filter(u => u.status === 'online');
    const away = visibleUsers.filter(u => u.status === 'away');
    const busy = visibleUsers.filter(u => u.status === 'busy');
    const offline = visibleUsers.filter(u => u.status === 'offline');
    
    return { online, away, busy, offline };
  }, [visibleUsers]);

  // Handle user click
  const handleUserClick = (user: ChatUser) => {
    if (onUserClick) {
      onUserClick(user);
    } else {
      if (user.isFounder) {
        toast.success('👑 RICKROLL187 - The LEGENDARY FOUNDER!', {
          duration: 3000,
          style: {
            background: 'linear-gradient(135deg, #FFD700, #FFA500)',
            color: '#000000',
            fontWeight: '700',
          },
        });
      } else {
        toast.success(`✨ ${user.displayName} - Code bro with ${formatEnergy(user.codeBroEnergy)} energy!`);
      }
    }
  };

  // Format energy for display
  const formatEnergy = (energy?: number) => {
    if (!energy) return '0';
    if (energy >= 1000000) return `${(energy / 1000000).toFixed(1)}M`;
    if (energy >= 1000) return `${(energy / 1000).toFixed(1)}K`;
    return energy.toString();
  };

  return (
    <div className={cn(
      'flex flex-col h-full',
      compact ? 'max-h-64' : 'min-h-0'
    )}>
      {/* Header */}
      <div className={cn(
        'flex items-center justify-between p-3 border-b border-gray-200 dark:border-gray-700',
        isFounder && 'bg-gradient-to-r from-yellow-50/30 to-orange-50/30 dark:from-yellow-900/10 dark:to-orange-900/10'
      )}>
        <div className="flex items-center gap-2">
          {isFounder && <Crown className="w-4 h-4 text-yellow-600" />}
          <Users className={cn(
            'w-4 h-4',
            isFounder ? 'text-yellow-600' : 'text-gray-600'
          )} />
          <h3 className={cn(
            'font-semibold text-sm',
            isFounder ? 'text-yellow-800 dark:text-yellow-300' : 'text-gray-900 dark:text-white'
          )}>
            {title}
          </h3>
          <span className={cn(
            'text-xs px-2 py-0.5 rounded-full',
            isFounder 
              ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300'
              : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300'
          )}>
            {users.length}
          </span>
        </div>

        <div className="flex items-center gap-1">
          {showInvite && (
            <LegendaryButton
              variant="ghost"
              size="sm"
              onClick={onInviteClick}
              className="p-1"
            >
              <UserPlus className="w-3 h-3" />
            </LegendaryButton>
          )}
          
          <LegendaryButton
            variant="ghost"
            size="sm"
            className="p-1"
          >
            <Settings className="w-3 h-3" />
          </LegendaryButton>
        </div>
      </div>

      {/* Search */}
      {!compact && users.length > 5 && (
        <div className="p-3 border-b border-gray-200 dark:border-gray-700">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-3 h-3 text-gray-400" />
            <input
              type="text"
              placeholder="Search members..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={cn(
                'w-full pl-9 pr-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600',
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm',
                'focus:outline-none focus:ring-1',
                isFounder ? 'focus:ring-yellow-500' : 'focus:ring-blue-500'
              )}
            />
          </div>
        </div>
      )}

      {/* User List */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-2 space-y-1">
          {/* Online Users */}
          {groupedUsers.online.length > 0 && (
            <div>
              {!compact && (
                <div className="flex items-center gap-2 px-2 py-1 text-xs font-medium text-gray-500 dark:text-gray-400">
                  <Circle className="w-2 h-2 fill-green-500 text-green-500" />
                  <span>Online — {groupedUsers.online.length}</span>
                </div>
              )}
              {groupedUsers.online.map((user) => (
                <UserItem
                  key={user.id}
                  user={user}
                  compact={compact}
                  isFounder={isFounder}
                  onClick={() => handleUserClick(user)}
                />
              ))}
            </div>
          )}

          {/* Away Users */}
          {groupedUsers.away.length > 0 && (
            <div>
              {!compact && (
                <div className="flex items-center gap-2 px-2 py-1 text-xs font-medium text-gray-500 dark:text-gray-400">
                  <Circle className="w-2 h-2 fill-yellow-500 text-yellow-500" />
                  <span>Away — {groupedUsers.away.length}</span>
                </div>
              )}
              {groupedUsers.away.map((user) => (
                <UserItem
                  key={user.id}
                  user={user}
                  compact={compact}
                  isFounder={isFounder}
                  onClick={() => handleUserClick(user)}
                />
              ))}
            </div>
          )}

          {/* Busy Users */}
          {groupedUsers.busy.length > 0 && (
            <div>
              {!compact && (
                <div className="flex items-center gap-2 px-2 py-1 text-xs font-medium text-gray-500 dark:text-gray-400">
                  <Circle className="w-2 h-2 fill-red-500 text-red-500" />
                  <span>Busy — {groupedUsers.busy.length}</span>
                </div>
              )}
              {groupedUsers.busy.map((user) => (
                <UserItem
                  key={user.id}
                  user={user}
                  compact={compact}
                  isFounder={isFounder}
                  onClick={() => handleUserClick(user)}
                />
              ))}
            </div>
          )}

          {/* Offline Users */}
          {groupedUsers.offline.length > 0 && (
            <div>
              {!compact && (
                <div className="flex items-center gap-2 px-2 py-1 text-xs font-medium text-gray-500 dark:text-gray-400">
                  <Circle className="w-2 h-2 fill-gray-400 text-gray-400" />
                  <span>Offline — {groupedUsers.offline.length}</span>
                </div>
              )}
              {groupedUsers.offline.map((user) => (
                <UserItem
                  key={user.id}
                  user={user}
                  compact={compact}
                  isFounder={isFounder}
                  onClick={() => handleUserClick(user)}
                />
              ))}
            </div>
          )}

          {/* Show More Button */}
          {maxVisible && sortedUsers.length > maxVisible && !showAll && (
            <motion.div
              className="px-2 py-1"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <LegendaryButton
                variant="ghost"
                size="sm"
                onClick={() => setShowAll(true)}
                className="w-full justify-center text-xs"
              >
                <Eye className="w-3 h-3 mr-1" />
                Show {sortedUsers.length - maxVisible} more
              </LegendaryButton>
            </motion.div>
          )}

          {/* Empty State */}
          {sortedUsers.length === 0 && (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Users className="w-8 h-8 text-gray-400 mb-2" />
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {searchQuery ? 'No users found' : 'No team members yet'}
              </p>
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="text-xs text-blue-600 hover:text-blue-700 mt-1"
                >
                  Clear search
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className={cn(
        'p-2 border-t border-gray-200 dark:border-gray-700 text-center',
        isFounder && 'bg-gradient-to-r from-yellow-50/30 to-orange-50/30 dark:from-yellow-900/10 dark:to-orange-900/10'
      )}>
        <div className="text-xs text-gray-500 dark:text-gray-400">
          <div className="flex items-center justify-center gap-2">
            <Activity className="w-3 h-3" />
            <span>
              {groupedUsers.online.length} online • Swiss precision networking
            </span>
            <Zap className="w-3 h-3" />
          </div>
          
          {isFounder && (
            <div className="mt-1 text-yellow-700 dark:text-yellow-300 font-bold text-xs">
              👑 FOUNDER USER LIST • 17:01:18 UTC! 👑
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

console.log('🎸🎸🎸 LEGENDARY USER LIST COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`User list component completed at: 2025-08-06 17:01:18 UTC`);
console.log('👥 User management: SWISS PRECISION');
console.log('👑 RICKROLL187 founder users: LEGENDARY');
console.log('⚡ Status & energy tracking: MAXIMUM VISIBILITY');
console.log('🌅 AFTERNOON LEGENDARY USER LIST ENERGY: INFINITE AT 17:01:18!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
