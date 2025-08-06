// File: web/src/store/slices/notificationsSlice.ts
/**
 * 🔔🎸 N3EXTPATH - LEGENDARY NOTIFICATIONS SLICE 🎸🔔
 * Professional notification system with Swiss precision
 * Built: 2025-08-06 15:01:43 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// =====================================
// 🔔 NOTIFICATIONS TYPES 🔔
// =====================================

export interface Notification {
  id: string;
  type: 'system' | 'performance' | 'achievement' | 'team' | 'okr' | 'review' | 'founder' | 'legendary';
  category: 'info' | 'success' | 'warning' | 'error' | 'celebration' | 'founder' | 'legendary';
  priority: 'low' | 'normal' | 'high' | 'urgent' | 'legendary';
  
  // Content
  title: string;
  message: string;
  description?: string;
  icon: string;
  color?: string;
  
  // Metadata
  userId: string;
  sourceId?: string; // ID of the source object (team, OKR, etc.)
  sourceType?: 'team' | 'okr' | 'achievement' | 'review' | 'user' | 'system';
  
  // State
  isRead: boolean;
  isArchived: boolean;
  isPinned: boolean;
  
  // Actions
  actions?: NotificationAction[];
  
  // Timestamps
  createdAt: Date;
  readAt?: Date;
  archivedAt?: Date;
  expiresAt?: Date;
  
  // Legendary features
  isFounderNotification?: boolean;
  legendaryLevel?: number;
  codeBroEnergy?: number;
  
  // Rich content
  imageUrl?: string;
  linkUrl?: string;
  data?: Record<string, any>;
}

export interface NotificationAction {
  id: string;
  label: string;
  type: 'primary' | 'secondary' | 'danger' | 'founder';
  action: string; // Action type to dispatch
  data?: Record<string, any>;
  icon?: string;
}

export interface NotificationPreferences {
  userId: string;
  
  // Channel preferences
  email: boolean;
  push: boolean;
  inApp: boolean;
  sms: boolean;
  
  // Type preferences
  system: boolean;
  performance: boolean;
  achievements: boolean;
  teams: boolean;
  okrs: boolean;
  reviews: boolean;
  
  // Timing preferences
  quietHours: {
    enabled: boolean;
    start: string; // HH:MM format
    end: string;   // HH:MM format
    timezone: string;
  };
  
  // Frequency preferences
  digest: 'immediate' | 'hourly' | 'daily' | 'weekly' | 'never';
  maxPerDay: number;
  
  // Legendary preferences
  founderNotifications: boolean;
  legendaryAchievements: boolean;
}

interface NotificationsState {
  // Notifications data
  notifications: Notification[];
  unreadNotifications: Notification[];
  readNotifications: Notification[];
  archivedNotifications: Notification[];
  pinnedNotifications: Notification[];
  founderNotifications: Notification[];
  legendaryNotifications: Notification[];
  
  // Counts
  totalCount: number;
  unreadCount: number;
  founderCount: number;
  legendaryCount: number;
  
  // Filtering and search
  filters: {
    type: string[];
    category: string[];
    priority: string[];
    isRead: boolean | null;
    dateRange: { start: Date; end: Date } | null;
  };
  searchQuery: string;
  filteredNotifications: Notification[];
  
  // Selected notification
  selectedNotificationId: string | null;
  selectedNotification: Notification | null;
  
  // User preferences
  preferences: NotificationPreferences | null;
  
  // User state
  currentUserId: string | null;
  isFounder: boolean;
  
  // UI states
  isLoading: boolean;
  isMarkingAsRead: boolean;
  isArchiving: boolean;
  isClearingAll: boolean;
  panelOpen: boolean;
  
  // Real-time features
  isConnected: boolean;
  lastPing: Date | null;
  connectionRetries: number;
  
  // Error handling
  error: string | null;
  
  // Data management
  lastSync: Date | null;
  lastNotification: Date | null;
}

// =====================================
// 🎸 INITIAL LEGENDARY STATE 🎸
// =====================================

const initialState: NotificationsState = {
  // Notifications data
  notifications: [],
  unreadNotifications: [],
  readNotifications: [],
  archivedNotifications: [],
  pinnedNotifications: [],
  founderNotifications: [],
  legendaryNotifications: [],
  
  // Counts
  totalCount: 0,
  unreadCount: 0,
  founderCount: 0,
  legendaryCount: 0,
  
  // Filtering and search
  filters: {
    type: [],
    category: [],
    priority: [],
    isRead: null,
    dateRange: null,
  },
  searchQuery: '',
  filteredNotifications: [],
  
  // Selected notification
  selectedNotificationId: null,
  selectedNotification: null,
  
  // User preferences
  preferences: null,
  
  // User state
  currentUserId: null,
  isFounder: false,
  
  // UI states
  isLoading: false,
  isMarkingAsRead: false,
  isArchiving: false,
  isClearingAll: false,
  panelOpen: false,
  
  // Real-time features
  isConnected: false,
  lastPing: null,
  connectionRetries: 0,
  
  // Error handling
  error: null,
  
  // Data management
  lastSync: null,
  lastNotification: null,
};

// =====================================
// 🎸 LEGENDARY ASYNC THUNKS 🎸
// =====================================

export const fetchNotifications = createAsyncThunk(
  'notifications/fetchNotifications',
  async (userId: string, { rejectWithValue }) => {
    try {
      console.log('🔔 Fetching legendary notifications...');
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Check if this is RICKROLL187 founder
      const isFounder = userId === 'founder-rickroll187';
      
      if (isFounder) {
        console.log('👑 RICKROLL187 FOUNDER NOTIFICATIONS DETECTED!');
        console.log('🚀 LOADING LEGENDARY FOUNDER NOTIFICATIONS!');
        console.log('⚙️ SWISS PRECISION FOUNDER NOTIFICATION SYSTEM!');
        console.log('🌅 AFTERNOON FOUNDER NOTIFICATION POWER AT 15:01:43!');
        
        // Founder notifications
        const founderNotifications: Notification[] = [
          {
            id: 'founder-milestone-75k',
            type: 'founder',
            category: 'celebration',
            priority: 'legendary',
            title: '🎉 LEGENDARY MILESTONE ACHIEVED!',
            message: 'Platform has reached 75,000+ legendary code bros!',
            description: 'Your legendary platform N3EXTPATH has surpassed 75K users with Swiss precision and infinite code bro energy! This is a testament to your visionary leadership.',
            icon: '👑',
            color: '#FFD700',
            userId: 'founder-rickroll187',
            sourceId: 'platform-growth',
            sourceType: 'system',
            isRead: false,
            isArchived: false,
            isPinned: true,
            actions: [
              {
                id: 'view-analytics',
                label: 'View Platform Analytics',
                type: 'founder',
                action: 'VIEW_PLATFORM_ANALYTICS',
                icon: '📊',
              },
              {
                id: 'celebrate',
                label: 'Celebrate with Team',
                type: 'primary',
                action: 'CELEBRATE_MILESTONE',
                icon: '🎉',
              },
            ],
            createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
            isFounderNotification: true,
            legendaryLevel: 10,
            codeBroEnergy: 10,
            linkUrl: '/founder/analytics',
            data: { userCount: 75000, milestone: '75K', growth: '+15K this month' },
          },
          {
            id: 'founder-feature-shipped',
            type: 'founder',
            category: 'success',
            priority: 'high',
            title: '🚀 Legendary Feature Shipped!',
            message: 'Swiss Precision Performance Analytics v2.0 is now live!',
            description: 'Your latest legendary feature has been deployed with Swiss precision. User engagement increased by 40% in the first 24 hours!',
            icon: '⚙️',
            color: '#10B981',
            userId: 'founder-rickroll187',
            sourceId: 'feature-analytics-v2',
            sourceType: 'system',
            isRead: false,
            isArchived: false,
            isPinned: false,
            actions: [
              {
                id: 'view-metrics',
                label: 'View Feature Metrics',
                type: 'founder',
                action: 'VIEW_FEATURE_METRICS',
                icon: '📈',
              },
            ],
            createdAt: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
            isFounderNotification: true,
            legendaryLevel: 9,
            codeBroEnergy: 9,
            data: { featureName: 'Performance Analytics v2.0', engagement: '+40%' },
          },
          {
            id: 'founder-team-achievement',
            type: 'team',
            category: 'celebration',
            priority: 'high',
            title: '🏆 Frontend Legends Achievement!',
            message: 'Frontend Legends team achieved "Swiss Precision Masters" status!',
            description: 'Your legendary Frontend team has achieved the highest precision score in platform history with 98.5% Swiss precision!',
            icon: '🎸',
            color: '#8B5CF6',
            userId: 'founder-rickroll187',
            sourceId: 'legendary-frontend-team',
            sourceType: 'team',
            isRead: true,
            isArchived: false,
            isPinned: false,
            readAt: new Date(Date.now() - 30 * 60 * 1000),
            actions: [
              {
                id: 'view-team',
                label: 'View Team Details',
                type: 'primary',
                action: 'VIEW_TEAM',
                data: { teamId: 'legendary-frontend-team' },
                icon: '👥',
              },
            ],
            createdAt: new Date(Date.now() - 12 * 60 * 60 * 1000), // 12 hours ago
            legendaryLevel: 8,
            codeBroEnergy: 9,
            data: { teamName: 'Frontend Legends', precisionScore: 98.5, achievement: 'Swiss Precision Masters' },
          },
          {
            id: 'system-backup-complete',
            type: 'system',
            category: 'success',
            priority: 'normal',
            title: '✅ System Backup Complete',
            message: 'Daily platform backup completed with Swiss precision',
            description: 'All platform data has been successfully backed up with 100% integrity verification.',
            icon: '💾',
            color: '#3B82F6',
            userId: 'founder-rickroll187',
            sourceId: 'daily-backup-20250806',
            sourceType: 'system',
            isRead: true,
            isArchived: false,
            isPinned: false,
            readAt: new Date(Date.now() - 15 * 60 * 1000),
            createdAt: new Date(Date.now() - 18 * 60 * 60 * 1000), // 18 hours ago
            data: { backupSize: '2.4GB', integrity: '100%', duration: '3.2 minutes' },
          },
        ];
        
        const founderPreferences: NotificationPreferences = {
          userId: 'founder-rickroll187',
          email: true,
          push: true,
          inApp: true,
          sms: true,
          system: true,
          performance: true,
          achievements: true,
          teams: true,
          okrs: true,
          reviews: true,
          quietHours: {
            enabled: false, // Founders never sleep!
            start: '22:00',
            end: '08:00',
            timezone: 'UTC',
          },
          digest: 'immediate',
          maxPerDay: 999, // Unlimited for founders
          founderNotifications: true,
          legendaryAchievements: true,
        };
        
        return {
          notifications: founderNotifications,
          preferences: founderPreferences,
          isFounder: true,
          currentUserId: 'founder-rickroll187',
        };
      }
      
      // Regular user notifications
      const regularNotifications: Notification[] = [
        {
          id: 'achievement-precision-master',
          type: 'achievement',
          category: 'celebration',
          priority: 'high',
          title: '🏆 Achievement Unlocked!',
          message: 'You earned "Swiss Precision Apprentice"!',
          description: 'Congratulations! You achieved 85%+ Swiss precision score and joined the ranks of legendary code bros!',
          icon: '⚙️',
          color: '#F59E0B',
          userId: 'user-regular',
          sourceId: 'achievement-precision-apprentice',
          sourceType: 'achievement',
          isRead: false,
          isArchived: false,
          isPinned: false,
          actions: [
            {
              id: 'view-achievement',
              label: 'View Achievement',
              type: 'primary',
              action: 'VIEW_ACHIEVEMENT',
              icon: '🏆',
            },
            {
              id: 'share',
              label: 'Share with Team',
              type: 'secondary',
              action: 'SHARE_ACHIEVEMENT',
              icon: '📢',
            },
          ],
          createdAt: new Date(Date.now() - 3 * 60 * 60 * 1000), // 3 hours ago
          legendaryLevel: 3,
          codeBroEnergy: 8,
          data: { achievementName: 'Swiss Precision Apprentice', xpReward: 250, precisionScore: 85 },
        },
        {
          id: 'performance-review-ready',
          type: 'review',
          category: 'info',
          priority: 'normal',
          title: '📊 Performance Review Ready',
          message: 'Your Q3 performance review is available',
          description: 'Your quarterly performance review has been completed and is ready for your review. Great progress on your code bro journey!',
          icon: '📈',
          color: '#3B82F6',
          userId: 'user-regular',
          sourceId: 'review-q3-2025',
          sourceType: 'review',
          isRead: false,
          isArchived: false,
          isPinned: false,
          actions: [
            {
              id: 'view-review',
              label: 'View Review',
              type: 'primary',
              action: 'VIEW_REVIEW',
              data: { reviewId: 'review-q3-2025' },
              icon: '👁️',
            },
          ],
          createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
          codeBroEnergy: 7,
          data: { quarter: 'Q3 2025', overallScore: 85, reviewer: 'Sarah Johnson' },
        },
        {
          id: 'team-invitation',
          type: 'team',
          category: 'info',
          priority: 'normal',
          title: '👥 Team Invitation',
          message: 'You were invited to join "Mobile Development" team',
          description: 'Sarah Johnson invited you to join the Mobile Development team. Join to collaborate with fellow code bros!',
          icon: '📱',
          color: '#8B5CF6',
          userId: 'user-regular',
          sourceId: 'team-mobile-dev',
          sourceType: 'team',
          isRead: true,
          isArchived: false,
          isPinned: false,
          readAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
          actions: [
            {
              id: 'accept-invite',
              label: 'Accept Invitation',
              type: 'primary',
              action: 'ACCEPT_TEAM_INVITATION',
              data: { teamId: 'team-mobile-dev', invitationId: 'invite-mobile-123' },
              icon: '✅',
            },
            {
              id: 'decline-invite',
              label: 'Decline',
              type: 'secondary',
              action: 'DECLINE_TEAM_INVITATION',
              data: { invitationId: 'invite-mobile-123' },
              icon: '❌',
            },
          ],
          createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
          data: { teamName: 'Mobile Development', inviterName: 'Sarah Johnson', role: 'member' },
        },
      ];
      
      const regularPreferences: NotificationPreferences = {
        userId: 'user-regular',
        email: true,
        push: true,
        inApp: true,
        sms: false,
        system: true,
        performance: true,
        achievements: true,
        teams: true,
        okrs: true,
        reviews: true,
        quietHours: {
          enabled: true,
          start: '22:00',
          end: '08:00',
          timezone: 'America/New_York',
        },
        digest: 'daily',
        maxPerDay: 20,
        founderNotifications: false,
        legendaryAchievements: true,
      };
      
      return {
        notifications: regularNotifications,
        preferences: regularPreferences,
        isFounder: false,
        currentUserId: 'user-regular',
      };
      
    } catch (error) {
      console.error('🚨 Notifications fetch error:', error);
      return rejectWithValue('Failed to fetch notifications');
    }
  }
);

export const markAsRead = createAsyncThunk(
  'notifications/markAsRead',
  async (notificationIds: string[], { rejectWithValue }) => {
    try {
      console.log(`🔔 Marking notifications as read: ${notificationIds.join(', ')}`);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 300));
      
      return { notificationIds, readAt: new Date() };
      
    } catch (error) {
      console.error('🚨 Mark as read error:', error);
      return rejectWithValue('Failed to mark notifications as read');
    }
  }
);

export const createNotification = createAsyncThunk(
  'notifications/createNotification',
  async (notificationData: Omit<Notification, 'id' | 'createdAt'>, { rejectWithValue }) => {
    try {
      console.log('🔔 Creating new notification...');
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 200));
      
      const newNotification: Notification = {
        id: `notif-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        createdAt: new Date(),
        ...notificationData,
      };
      
      console.log(`✅ Notification created: ${newNotification.title}`);
      return newNotification;
      
    } catch (error) {
      console.error('🚨 Notification creation error:', error);
      return rejectWithValue('Failed to create notification');
    }
  }
);

// =====================================
// 🎸 LEGENDARY NOTIFICATIONS SLICE 🎸
// =====================================

const notificationsSlice = createSlice({
  name: 'notifications',
  initialState,
  reducers: {
    // =====================================
    // 🔔 NOTIFICATION MANAGEMENT 🔔
    // =====================================
    
    selectNotification: (state, action: PayloadAction<string>) => {
      const notificationId = action.payload;
      state.selectedNotificationId = notificationId;
      state.selectedNotification = state.notifications.find(n => n.id === notificationId) || null;
      
      console.log(`🔔 Notification selected: ${notificationId}`);
    },
    
    clearSelectedNotification: (state) => {
      state.selectedNotification = null;
      state.selectedNotificationId = null;
    },
    
    markNotificationAsRead: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find(n => n.id === action.payload);
      
      if (notification && !notification.isRead) {
        notification.isRead = true;
        notification.readAt = new Date();
        
        // Update categorized arrays
        state.unreadNotifications = state.unreadNotifications.filter(n => n.id !== notification.id);
        if (!state.readNotifications.find(n => n.id === notification.id)) {
          state.readNotifications.push(notification);
        }
        
        // Update counts
        state.unreadCount = Math.max(0, state.unreadCount - 1);
        
        console.log(`🔔 Notification marked as read: ${notification.title}`);
      }
    },
    
    markAllAsRead: (state) => {
      state.notifications.forEach(notification => {
        if (!notification.isRead) {
          notification.isRead = true;
          notification.readAt = new Date();
        }
      });
      
      // Update categorized arrays
      state.readNotifications = [...state.notifications.filter(n => n.isRead)];
      state.unreadNotifications = [];
      
      // Reset counts
      state.unreadCount = 0;
      state.founderCount = 0;
      state.legendaryCount = 0;
      
      console.log('🔔 All notifications marked as read');
    },
    
    archiveNotification: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find(n => n.id === action.payload);
      
      if (notification && !notification.isArchived) {
        notification.isArchived = true;
        notification.archivedAt = new Date();
        
        // Remove from main arrays
        state.notifications = state.notifications.filter(n => n.id !== notification.id);
        state.unreadNotifications = state.unreadNotifications.filter(n => n.id !== notification.id);
        state.readNotifications = state.readNotifications.filter(n => n.id !== notification.id);
        
        // Add to archived
        state.archivedNotifications.push(notification);
        
        // Update counts
        if (!notification.isRead) {
          state.unreadCount = Math.max(0, state.unreadCount - 1);
        }
        state.totalCount = Math.max(0, state.totalCount - 1);
        
        console.log(`🗄️ Notification archived: ${notification.title}`);
      }
    },
    
    pinNotification: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find(n => n.id === action.payload);
      
      if (notification) {
        notification.isPinned = !notification.isPinned;
        
        if (notification.isPinned) {
          if (!state.pinnedNotifications.find(n => n.id === notification.id)) {
            state.pinnedNotifications.push(notification);
          }
          console.log(`📌 Notification pinned: ${notification.title}`);
        } else {
          state.pinnedNotifications = state.pinnedNotifications.filter(n => n.id !== notification.id);
          console.log(`📌 Notification unpinned: ${notification.title}`);
        }
      }
    },
    
    deleteNotification: (state, action: PayloadAction<string>) => {
      const notificationId = action.payload;
      const notification = state.notifications.find(n => n.id === notificationId);
      
      if (notification) {
        // Remove from all arrays
        state.notifications = state.notifications.filter(n => n.id !== notificationId);
        state.unreadNotifications = state.unreadNotifications.filter(n => n.id !== notificationId);
        state.readNotifications = state.readNotifications.filter(n => n.id !== notificationId);
        state.pinnedNotifications = state.pinnedNotifications.filter(n => n.id !== notificationId);
        state.founderNotifications = state.founderNotifications.filter(n => n.id !== notificationId);
        state.legendaryNotifications = state.legendaryNotifications.filter(n => n.id !== notificationId);
        state.archivedNotifications = state.archivedNotifications.filter(n => n.id !== notificationId);
        
        // Update counts
        if (!notification.isRead) {
          state.unreadCount = Math.max(0, state.unreadCount - 1);
        }
        if (notification.isFounderNotification) {
          state.founderCount = Math.max(0, state.founderCount - 1);
        }
        if (notification.legendaryLevel && notification.legendaryLevel >= 5) {
          state.legendaryCount = Math.max(0, state.legendaryCount - 1);
        }
        state.totalCount = Math.max(0, state.totalCount - 1);
        
        console.log(`🗑️ Notification deleted: ${notification.title}`);
      }
    },
    
    // =====================================
    // 🔍 FILTERING & SEARCH 🔍
    // =====================================
    
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
      
      // Apply search filter
      state.filteredNotifications = state.notifications.filter(notification =>
        notification.title.toLowerCase().includes(action.payload.toLowerCase()) ||
        notification.message.toLowerCase().includes(action.payload.toLowerCase()) ||
        (notification.description && notification.description.toLowerCase().includes(action.payload.toLowerCase()))
      );
    },
    
    setTypeFilter: (state, action: PayloadAction<string[]>) => {
      state.filters.type = action.payload;
      console.log(`🔍 Type filter applied: ${action.payload.join(', ')}`);
    },
    
    setCategoryFilter: (state, action: PayloadAction<string[]>) => {
      state.filters.category = action.payload;
      console.log(`🔍 Category filter applied: ${action.payload.join(', ')}`);
    },
    
    setPriorityFilter: (state, action: PayloadAction<string[]>) => {
      state.filters.priority = action.payload;
      console.log(`🔍 Priority filter applied: ${action.payload.join(', ')}`);
    },
    
    setReadFilter: (state, action: PayloadAction<boolean | null>) => {
      state.filters.isRead = action.payload;
      console.log(`🔍 Read filter applied: ${action.payload}`);
    },
    
    setDateRangeFilter: (state, action: PayloadAction<{ start: Date; end: Date } | null>) => {
      state.filters.dateRange = action.payload;
      console.log(`🔍 Date range filter applied:`, action.payload);
    },
    
    clearFilters: (state) => {
      state.filters = {
        type: [],
        category: [],
        priority: [],
        isRead: null,
        dateRange: null,
      };
      state.searchQuery = '';
      state.filteredNotifications = state.notifications;
      console.log('🔍 All notification filters cleared');
    },
    
    // =====================================
    // ⚙️ PREFERENCES 🔗
    // =====================================
    
    updatePreferences: (state, action: PayloadAction<Partial<NotificationPreferences>>) => {
      if (state.preferences) {
        state.preferences = { ...state.preferences, ...action.payload };
        console.log('⚙️ Notification preferences updated');
      }
    },
    
    togglePreference: (state, action: PayloadAction<keyof NotificationPreferences>) => {
      const key = action.payload;
      if (state.preferences && typeof state.preferences[key] === 'boolean') {
        (state.preferences as any)[key] = !(state.preferences as any)[key];
        console.log(`⚙️ Preference toggled: ${key}`);
      }
    },
    
    // =====================================
    // 👑 LEGENDARY FEATURES 👑
    // =====================================
    
    activateFounderNotifications: (state) => {
      state.isFounder = true;
      
      if (state.preferences) {
        state.preferences.founderNotifications = true;
        state.preferences.legendaryAchievements = true;
        state.preferences.digest = 'immediate';
        state.preferences.maxPerDay = 999;
        state.preferences.quietHours.enabled = false; // Founders never sleep!
      }
      
      console.log('👑🎸👑 RICKROLL187 FOUNDER NOTIFICATIONS ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER NOTIFICATIONS WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER NOTIFICATION SYSTEM!');
      console.log('🌅 AFTERNOON FOUNDER NOTIFICATION POWER AT 15:01:43!');
    },
    
    promoteToLegendaryNotification: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find(n => n.id === action.payload);
      
      if (notification) {
        notification.category = 'legendary';
        notification.priority = 'legendary';
        notification.legendaryLevel = Math.min(10, (notification.legendaryLevel || 0) + 2);
        notification.codeBroEnergy = Math.min(10, (notification.codeBroEnergy || 0) + 1);
        
        if (!state.legendaryNotifications.find(n => n.id === notification.id)) {
          state.legendaryNotifications.push(notification);
          state.legendaryCount += 1;
        }
        
        console.log(`🎸 Notification promoted to legendary: ${notification.title}`);
      }
    },
    
    // =====================================
    // 🎛️ UI MANAGEMENT 🎛️
    // =====================================
    
    togglePanel: (state) => {
      state.panelOpen = !state.panelOpen;
      console.log(`🔔 Notifications panel ${state.panelOpen ? 'opened' : 'closed'}`);
    },
    
    setPanelOpen: (state, action: PayloadAction<boolean>) => {
      state.panelOpen = action.payload;
    },
    
    // =====================================
    // 🔄 REAL-TIME MANAGEMENT 🔄
    // =====================================
    
    setConnectionStatus: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload;
      state.lastPing = new Date();
      
      if (action.payload) {
        state.connectionRetries = 0;
        console.log('🔔 Notifications real-time connection established');
      } else {
        state.connectionRetries += 1;
        console.log(`🔔 Notifications connection lost (retry ${state.connectionRetries})`);
      }
    },
    
    incrementConnectionRetries: (state) => {
      state.connectionRetries += 1;
    },
    
    resetConnectionRetries: (state) => {
      state.connectionRetries = 0;
    },
    
    // =====================================
    // 🧹 CLEANUP & MAINTENANCE 🧹
    // =====================================
    
    clearAllNotifications: (state) => {
      state.notifications.forEach(notification => {
        notification.isArchived = true;
        notification.archivedAt = new Date();
      });
      
      state.archivedNotifications = [...state.archivedNotifications, ...state.notifications];
      state.notifications = [];
      state.unreadNotifications = [];
      state.readNotifications = [];
      state.pinnedNotifications = [];
      
      // Reset counts
      state.totalCount = 0;
      state.unreadCount = 0;
      state.founderCount = 0;
      state.legendaryCount = 0;
      
      console.log('🧹 All notifications cleared and archived');
    },
    
    clearExpiredNotifications: (state) => {
      const now = new Date();
      const expiredNotifications = state.notifications.filter(n => 
        n.expiresAt && new Date(n.expiresAt) < now
      );
      
      expiredNotifications.forEach(notification => {
        state.notifications = state.notifications.filter(n => n.id !== notification.id);
        state.unreadNotifications = state.unreadNotifications.filter(n => n.id !== notification.id);
        state.readNotifications = state.readNotifications.filter(n => n.id !== notification.id);
        
        if (!notification.isRead) {
          state.unreadCount = Math.max(0, state.unreadCount - 1);
        }
        state.totalCount = Math.max(0, state.totalCount - 1);
      });
      
      if (expiredNotifications.length > 0) {
        console.log(`🧹 Cleared ${expiredNotifications.length} expired notifications`);
      }
    },
    
    clearError: (state) => {
      state.error = null;
    },
    
    resetNotificationsState: (state) => {
      // Reset to initial state but preserve founder status and user ID
      const preservedState = {
        isFounder: state.isFounder,
        currentUserId: state.currentUserId,
      };
      
      Object.assign(state, initialState, preservedState);
      console.log('🔄 Notifications state reset');
    },
  },
  
  // =====================================
  // 🎸 ASYNC THUNK HANDLERS 🎸
  // =====================================
  
  extraReducers: (builder) => {
    // Fetch notifications
    builder
      .addCase(fetchNotifications.pending, (state) => {
        state.isLoading = true;
        state.error = null;
        console.log('⏳ Fetching notifications...');
      })
      .addCase(fetchNotifications.fulfilled, (state, action) => {
        const data = action.payload;
        
        state.notifications = data.notifications;
        state.preferences = data.preferences;
        state.isFounder = data.isFounder;
        state.currentUserId = data.currentUserId;
        
        // Categorize notifications
        state.unreadNotifications = data.notifications.filter(n => !n.isRead);
        state.readNotifications = data.notifications.filter(n => n.isRead);
        state.pinnedNotifications = data.notifications.filter(n => n.isPinned);
        state.founderNotifications = data.notifications.filter(n => n.isFounderNotification);
        state.legendaryNotifications = data.notifications.filter(n => n.legendaryLevel && n.legendaryLevel >= 5);
        state.filteredNotifications = data.notifications;
        
        // Update counts
        state.totalCount = data.notifications.length;
        state.unreadCount = state.unreadNotifications.length;
        state.founderCount = state.founderNotifications.length;
        state.legendaryCount = state.legendaryNotifications.length;
        
        state.isLoading = false;
        state.lastSync = new Date();
        state.lastNotification = data.notifications[0]?.createdAt || null;
        
        console.log('✅ Notifications loaded successfully');
        
        if (data.isFounder) {
          console.log('👑 RICKROLL187 FOUNDER NOTIFICATIONS LOADED WITH LEGENDARY ALERTS!');
        }
      })
      .addCase(fetchNotifications.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string || 'Failed to fetch notifications';
        console.error('🚨 Notifications fetch failed:', state.error);
      });
    
    // Mark as read
    builder
      .addCase(markAsRead.fulfilled, (state, action) => {
        const { notificationIds, readAt } = action.payload;
        
        notificationIds.forEach(id => {
          const notification = state.notifications.find(n => n.id === id);
          if (notification && !notification.isRead) {
            notification.isRead = true;
            notification.readAt = readAt;
            
            // Update arrays
            state.unreadNotifications = state.unreadNotifications.filter(n => n.id !== id);
            if (!state.readNotifications.find(n => n.id === id)) {
              state.readNotifications.push(notification);
            }
            
            state.unreadCount = Math.max(0, state.unreadCount - 1);
          }
        });
        
        console.log(`✅ Marked ${notificationIds.length} notifications as read`);
      });
    
    // Create notification
    builder
      .addCase(createNotification.fulfilled, (state, action) => {
        const newNotification = action.payload;
        
        state.notifications.unshift(newNotification);
        
        if (!newNotification.isRead) {
          state.unreadNotifications.unshift(newNotification);
          state.unreadCount += 1;
        }
        
        if (newNotification.isFounderNotification) {
          state.founderNotifications.unshift(newNotification);
          state.founderCount += 1;
        }
        
        if (newNotification.legendaryLevel && newNotification.legendaryLevel >= 5) {
          state.legendaryNotifications.unshift(newNotification);
          state.legendaryCount += 1;
        }
        
        state.filteredNotifications = state.notifications;
        state.totalCount += 1;
        state.lastNotification = newNotification.createdAt;
        
        console.log(`✅ Notification created: ${newNotification.title}`);
      });
  },
});

// =====================================
// 🎸 EXPORT LEGENDARY ACTIONS & REDUCER 🎸
// =====================================

export const {
  // Notification Management
  selectNotification,
  clearSelectedNotification,
  markNotificationAsRead,
  markAllAsRead,
  archiveNotification,
  pinNotification,
  deleteNotification,
  
  // Filtering & Search
  setSearchQuery,
  setTypeFilter,
  setCategoryFilter,
  setPriorityFilter,
  setReadFilter,
  setDateRangeFilter,
  clearFilters,
  
  // Preferences
  updatePreferences,
  togglePreference,
  
  // Legendary Features
  activateFounderNotifications,
  promoteToLegendaryNotification,
  
  // UI Management
  togglePanel,
  setPanelOpen,
  
  // Real-time Management
  setConnectionStatus,
  incrementConnectionRetries,
  resetConnectionRetries,
  
  // Cleanup & Maintenance
  clearAllNotifications,
  clearExpiredNotifications,
  clearError,
  resetNotificationsState,
} = notificationsSlice.actions;

export default notificationsSlice.reducer;

console.log('🎸🎸🎸 LEGENDARY NOTIFICATIONS SLICE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Notifications slice completed at: 2025-08-06 15:01:43 UTC`);
console.log('🔔 Notification system: SWISS PRECISION');
console.log('👑 RICKROLL187 founder notifications: LEGENDARY');
console.log('📢 Real-time notifications: MAXIMUM ENGAGEMENT');
console.log('🌅 Afternoon legendary energy: INFINITE AT 15:01:43!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
