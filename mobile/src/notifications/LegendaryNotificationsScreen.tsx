// File: mobile/src/screens/notifications/LegendaryNotificationsScreen.tsx
/**
 * 🔔🎸 N3EXTPATH - LEGENDARY NOTIFICATIONS SCREEN 🎸🔔
 * Professional notification center with Swiss precision
 * Built: 2025-08-06 12:24:25 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 * MORNING LEGENDARY ENERGY AT 824 AM - LET'S GET THIS ROLLING!
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  Alert,
  Animated,
  Dimensions,
  Image,
  Switch,
} from 'react-native';
import { 
  Card, 
  Button, 
  Chip, 
  Badge, 
  Avatar,
  List,
  Portal,
  Modal,
  FAB,
  Searchbar,
  Menu,
  Divider,
  IconButton
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useDispatch, useSelector } from 'react-redux';
import * as Animatable from 'react-native-animatable';
import { formatDistanceToNow } from 'date-fns';

// Import legendary components and services
import { RootStackParamList } from '../../navigation/LegendaryNavigation';
import { RootState } from '../../store';
import { fetchNotifications, markAsRead, markAllAsRead, deleteNotification } from '../../store/slices/notificationsSlice';
import { legendaryTheme } from '../../theme/legendaryTheme';
import { LegendaryButton } from '../../components/ui/LegendaryButton';
import { LegendaryCard } from '../../components/ui/LegendaryCard';

type NotificationsScreenNavigationProp = NativeStackNavigationProp<RootStackParamList>;

const { width, height } = Dimensions.get('window');

// =====================================
// 🔔 NOTIFICATIONS DATA TYPES 🔔
// =====================================

interface Notification {
  id: string;
  type: 'achievement' | 'team_invite' | 'okr_update' | 'performance_review' | 'system' | 'legendary_milestone' | 'code_bro_energy' | 'swiss_precision';
  title: string;
  message: string;
  isRead: boolean;
  priority: 'low' | 'medium' | 'high' | 'legendary';
  createdAt: Date;
  updatedAt: Date;
  actionUrl?: string;
  actionData?: any;
  sender?: {
    id: string;
    name: string;
    avatar?: string;
    isFounder?: boolean;
    isLegendary?: boolean;
  };
  metadata?: {
    teamName?: string;
    okrTitle?: string;
    achievementName?: string;
    performanceScore?: number;
  };
}

interface NotificationStats {
  total: number;
  unread: number;
  todayCount: number;
  weekCount: number;
  legendaryCount: number;
  achievementCount: number;
  teamCount: number;
  systemCount: number;
}

// =====================================
// 🎸 LEGENDARY NOTIFICATIONS SCREEN 🎸
// =====================================

export function LegendaryNotificationsScreen(): JSX.Element {
  const navigation = useNavigation<NotificationsScreenNavigationProp>();
  const dispatch = useDispatch();
  
  // Redux state
  const { user } = useSelector((state: RootState) => state.auth);
  const { notifications: notificationsData, isLoading } = useSelector((state: RootState) => state.notifications);
  
  // Local state
  const [refreshing, setRefreshing] = useState(false);
  const [selectedTab, setSelectedTab] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [selectedNotification, setSelectedNotification] = useState<Notification | null>(null);
  const [showNotificationModal, setShowNotificationModal] = useState(false);
  const [filterMenuVisible, setFilterMenuVisible] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [sortMenuVisible, setSortMenuVisible] = useState(false);
  const [selectedSort, setSelectedSort] = useState('recent');
  const [notificationSettings, setNotificationSettings] = useState({
    achievementNotifications: true,
    teamInvites: true,
    okrUpdates: true,
    performanceReviews: true,
    systemNotifications: true,
    legendaryMilestones: true,
    codeBroEnergyUpdates: true,
    swissPrecisionAlerts: true,
  });
  
  // Animation refs
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const bellShakeAnim = useRef(new Animated.Value(0)).current;

  // Check if user is RICKROLL187 founder
  const isFounder = user?.username === 'rickroll187';
  const isLegendary = user?.is_legendary || false;
  const userName = user?.first_name || user?.username || 'User';

  // Mock notification stats (in real app, fetch from API)
  const [notificationStats, setNotificationStats] = useState<NotificationStats>({
    total: isFounder ? 47 : isLegendary ? 23 : 15,
    unread: isFounder ? 12 : isLegendary ? 8 : 5,
    todayCount: isFounder ? 8 : isLegendary ? 5 : 3,
    weekCount: isFounder ? 25 : isLegendary ? 15 : 10,
    legendaryCount: isFounder ? 15 : isLegendary ? 8 : 3,
    achievementCount: isFounder ? 10 : isLegendary ? 6 : 4,
    teamCount: isFounder ? 12 : isLegendary ? 7 : 4,
    systemCount: isFounder ? 10 : isLegendary ? 2 : 4,
  });

  // Mock notifications data (in real app, fetch from API)
  const [notifications, setNotifications] = useState<Notification[]>([
    {
      id: '1',
      type: isFounder ? 'legendary_milestone' : 'achievement',
      title: isFounder ? '👑 Legendary Founder Milestone Achieved!' : '🏆 New Achievement Unlocked!',
      message: isFounder 
        ? 'Congratulations RICKROLL187! You\'ve reached 10,000+ platform users with infinite Swiss precision and code bro energy!'
        : 'Congratulations! You\'ve achieved "Swiss Precision Master" status with 90%+ precision score for 3 months!',
      isRead: false,
      priority: isFounder ? 'legendary' : 'high',
      createdAt: new Date(Date.now() - 15 * 60 * 1000), // 15 minutes ago
      updatedAt: new Date(Date.now() - 15 * 60 * 1000),
      actionUrl: '/achievements',
      sender: {
        id: 'system',
        name: 'N3EXTPATH System',
        isFounder: false,
        isLegendary: true,
      },
      metadata: {
        achievementName: isFounder ? 'Legendary Platform Creator' : 'Swiss Precision Master',
      },
    },
    {
      id: '2',
      type: 'team_invite',
      title: '👥 Team Invitation Received',
      message: isFounder 
        ? 'You\'ve been invited to lead the "Global Code Bro Alliance" team as legendary founder!'
        : 'Sarah Johnson invited you to join the "Frontend Legends" team. Ready for legendary collaboration?',
      isRead: false,
      priority: 'high',
      createdAt: new Date(Date.now() - 45 * 60 * 1000), // 45 minutes ago
      updatedAt: new Date(Date.now() - 45 * 60 * 1000),
      actionUrl: '/teams',
      sender: {
        id: isFounder ? 'global_coordinator' : 'sarah_johnson',
        name: isFounder ? 'Elena Volkov (Global Coordinator)' : 'Sarah Johnson',
        avatar: `https://ui-avatars.com/api/?name=${isFounder ? 'Elena+Volkov' : 'Sarah+Johnson'}&background=1E90FF&color=fff&size=48`,
        isFounder: false,
        isLegendary: true,
      },
      metadata: {
        teamName: isFounder ? 'Global Code Bro Alliance' : 'Frontend Legends',
      },
    },
    {
      id: '3',
      type: 'okr_update',
      title: '🎯 OKR Progress Update',
      message: isFounder 
        ? 'Your legendary OKR "Scale N3EXTPATH to Legendary Heights" is at 95.2% completion - almost at infinite success!'
        : 'Your OKR "Achieve Legendary Code Bro Status" has reached 78.5% completion. Keep up the legendary work!',
      isRead: false,
      priority: isFounder ? 'legendary' : 'medium',
      createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      updatedAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
      actionUrl: '/okrs',
      sender: {
        id: 'system',
        name: 'OKR System',
        isFounder: false,
        isLegendary: true,
      },
      metadata: {
        okrTitle: isFounder ? 'Scale N3EXTPATH to Legendary Heights' : 'Achieve Legendary Code Bro Status',
      },
    },
    {
      id: '4',
      type: 'performance_review',
      title: '📊 Performance Review Completed',
      message: isFounder 
        ? 'Your Q3 2025 performance review shows perfect 100% scores across all legendary metrics!'
        : 'Your Q3 2025 performance review is complete with outstanding results. Swiss precision: 88.5%!',
      isRead: true,
      priority: isFounder ? 'legendary' : 'high',
      createdAt: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
      updatedAt: new Date(Date.now() - 4 * 60 * 60 * 1000),
      actionUrl: '/performance',
      sender: {
        id: 'hr_system',
        name: 'HR Performance System',
        isFounder: false,
        isLegendary: false,
      },
      metadata: {
        performanceScore: isFounder ? 100 : 88.5,
      },
    },
    {
      id: '5',
      type: isFounder ? 'code_bro_energy' : 'swiss_precision',
      title: isFounder ? '🎸 Code Bro Energy Milestone!' : '⚙️ Swiss Precision Achievement!',
      message: isFounder 
        ? 'Your infinite code bro energy has inspired 500+ team members across the platform! Legendary impact!'
        : 'You\'ve maintained 85%+ Swiss precision for 6 consecutive weeks. Approaching legendary status!',
      isRead: true,
      priority: isFounder ? 'legendary' : 'high',
      createdAt: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
      updatedAt: new Date(Date.now() - 6 * 60 * 60 * 1000),
      actionUrl: '/dashboard',
      sender: {
        id: 'metrics_system',
        name: 'Metrics & Analytics',
        isFounder: false,
        isLegendary: true,
      },
    },
    {
      id: '6',
      type: 'system',
      title: '🚀 Platform Update Released',
      message: isFounder 
        ? 'N3EXTPATH v2.0 Mobile is now live! Your legendary vision is reaching users worldwide with Swiss precision!'
        : 'N3EXTPATH v2.0 Mobile is now available! Experience legendary performance management with Swiss precision.',
      isRead: true,
      priority: isFounder ? 'legendary' : 'medium',
      createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
      updatedAt: new Date(Date.now() - 24 * 60 * 60 * 1000),
      actionUrl: '/settings',
      sender: {
        id: 'system',
        name: 'N3EXTPATH System',
        isFounder: false,
        isLegendary: true,
      },
    },
  ]);

  useEffect(() => {
    console.log('🔔🎸🔔 LEGENDARY NOTIFICATIONS SCREEN LOADED! 🔔🎸🔔');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Notifications screen loaded at: 2025-08-06 12:24:25 UTC`);
    console.log('🌅 MORNING LEGENDARY ENERGY AT 824 AM ON 8/6/2025!');
    
    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER NOTIFICATIONS ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY NOTIFICATION CENTER WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION NOTIFICATION MANAGEMENT!');
      console.log('🌅 MORNING FOUNDER ENERGY: MAXIMUM!');
    }

    // Start legendary animations
    startLegendaryAnimations();
    
    // Set up founder pulse animation
    if (isFounder) {
      startFounderAnimations();
    }

    // Start bell shake animation for unread notifications
    if (notificationStats.unread > 0) {
      startBellShakeAnimation();
    }

    // Load notifications data
    loadNotificationsData();
  }, []);

  useFocusEffect(
    useCallback(() => {
      loadNotificationsData();
    }, [])
  );

  const startLegendaryAnimations = () => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      }),
      Animated.spring(slideAnim, {
        toValue: 0,
        speed: 8,
        bounciness: 6,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        speed: 10,
        bounciness: 8,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const startFounderAnimations = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.02,
          duration: 2000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 2000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  const startBellShakeAnimation = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(bellShakeAnim, {
          toValue: 10,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(bellShakeAnim, {
          toValue: -10,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(bellShakeAnim, {
          toValue: 10,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(bellShakeAnim, {
          toValue: 0,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.delay(3000),
      ])
    ).start();
  };

  const loadNotificationsData = async () => {
    try {
      console.log('🔔 Loading legendary notifications data...');
      
      // Dispatch notifications data fetch
      // await dispatch(fetchNotifications() as any);
      
      console.log('✅ Notifications data loaded with Swiss precision!');
      
    } catch (error) {
      console.error('🚨 Error loading notifications data:', error);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    console.log('🔄 Refreshing legendary notifications...');
    
    try {
      await loadNotificationsData();
      
      if (isFounder) {
        console.log('👑 RICKROLL187 notifications refreshed with infinite power!');
      }
    } catch (error) {
      console.error('🚨 Error refreshing notifications:', error);
    } finally {
      setRefreshing(false);
    }
  };

  const handleNotificationPress = async (notification: Notification) => {
    console.log(`🔔 Opening notification: ${notification.title}`);
    
    // Mark as read if not already read
    if (!notification.isRead) {
      await handleMarkAsRead(notification.id);
    }
    
    setSelectedNotification(notification);
    setShowNotificationModal(true);
  };

  const handleMarkAsRead = async (notificationId: string) => {
    try {
      console.log(`✅ Marking notification as read: ${notificationId}`);
      
      // Update local state
      setNotifications(prev => 
        prev.map(notif => 
          notif.id === notificationId 
            ? { ...notif, isRead: true, updatedAt: new Date() }
            : notif
        )
      );
      
      // Update stats
      setNotificationStats(prev => ({
        ...prev,
        unread: Math.max(0, prev.unread - 1),
      }));
      
      // In real app, dispatch mark as read action
      // await dispatch(markAsRead({ notificationId }) as any);
      
    } catch (error) {
      console.error('🚨 Error marking notification as read:', error);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      console.log('✅ Marking all notifications as read...');
      
      // Update local state
      setNotifications(prev => 
        prev.map(notif => ({ ...notif, isRead: true, updatedAt: new Date() }))
      );
      
      // Update stats
      setNotificationStats(prev => ({ ...prev, unread: 0 }));
      
      // In real app, dispatch mark all as read action
      // await dispatch(markAllAsRead() as any);
      
      Alert.alert(
        '✅ All Read',
        isFounder 
          ? '👑 All legendary notifications marked as read with infinite precision!'
          : '🎸 All notifications marked as read with Swiss precision!'
      );
      
    } catch (error) {
      console.error('🚨 Error marking all notifications as read:', error);
      Alert.alert('Error', 'Failed to mark all notifications as read');
    }
  };

  const handleDeleteNotification = async (notificationId: string) => {
    try {
      console.log(`🗑️ Deleting notification: ${notificationId}`);
      
      const notificationToDelete = notifications.find(n => n.id === notificationId);
      
      // Update local state
      setNotifications(prev => prev.filter(notif => notif.id !== notificationId));
      
      // Update stats
      setNotificationStats(prev => ({
        ...prev,
        total: prev.total - 1,
        unread: notificationToDelete && !notificationToDelete.isRead ? prev.unread - 1 : prev.unread,
      }));
      
      // In real app, dispatch delete notification action
      // await dispatch(deleteNotification({ notificationId }) as any);
      
    } catch (error) {
      console.error('🚨 Error deleting notification:', error);
      Alert.alert('Error', 'Failed to delete notification');
    }
  };

  const handleNotificationAction = (notification: Notification) => {
    console.log(`🚀 Performing action for notification: ${notification.id}`);
    
    if (notification.actionUrl) {
      // Navigate to the appropriate screen
      switch (notification.actionUrl) {
        case '/achievements':
        case '/dashboard':
          navigation.navigate('Dashboard');
          break;
        case '/teams':
          navigation.navigate('Teams');
          break;
        case '/okrs':
          navigation.navigate('OKRs');
          break;
        case '/performance':
          navigation.navigate('Performance');
          break;
        default:
          console.log('Unknown action URL:', notification.actionUrl);
      }
    }
    
    setShowNotificationModal(false);
  };

  const getNotificationTypeIcon = (type: string): string => {
    switch (type) {
      case 'achievement': return 'trophy';
      case 'team_invite': return 'people';
      case 'okr_update': return 'target';
      case 'performance_review': return 'trending-up';
      case 'system': return 'settings';
      case 'legendary_milestone': return 'crown';
      case 'code_bro_energy': return 'musical-notes';
      case 'swiss_precision': return 'precision-manufacturing';
      default: return 'notifications';
    }
  };

  const getNotificationTypeColor = (type: string): string => {
    switch (type) {
      case 'achievement': return legendaryTheme.legendary.colors.legendary;
      case 'team_invite': return legendaryTheme.legendary.colors.codeBroEnergy;
      case 'okr_update': return legendaryTheme.legendary.colors.info;
      case 'performance_review': return legendaryTheme.legendary.colors.success;
      case 'system': return legendaryTheme.colors.primary;
      case 'legendary_milestone': return legendaryTheme.legendary.colors.legendary;
      case 'code_bro_energy': return legendaryTheme.legendary.colors.codeBroEnergy;
      case 'swiss_precision': return legendaryTheme.legendary.colors.swissPrecision;
      default: return legendaryTheme.colors.outline;
    }
  };

  const getPriorityColor = (priority: string): string => {
    switch (priority) {
      case 'legendary': return legendaryTheme.legendary.colors.legendary;
      case 'high': return legendaryTheme.legendary.colors.error;
      case 'medium': return legendaryTheme.legendary.colors.warning;
      case 'low': return legendaryTheme.legendary.colors.info;
      default: return legendaryTheme.colors.outline;
    }
  };

  const filteredNotifications = notifications.filter(notification => {
    const matchesTab = 
      selectedTab === 'all' ||
      (selectedTab === 'unread' && !notification.isRead) ||
      (selectedTab === 'today' && new Date(notification.createdAt).toDateString() === new Date().toDateString()) ||
      (selectedTab === 'legendary' && (notification.priority === 'legendary' || notification.type === 'legendary_milestone'));
      
    const matchesFilter = 
      selectedFilter === 'all' ||
      notification.type === selectedFilter;
      
    const matchesSearch = 
      notification.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      notification.message.toLowerCase().includes(searchQuery.toLowerCase());
    
    return matchesTab && matchesFilter && matchesSearch;
  });

  const sortedNotifications = [...filteredNotifications].sort((a, b) => {
    switch (selectedSort) {
      case 'recent':
        return b.createdAt.getTime() - a.createdAt.getTime();
      case 'priority':
        const priorityOrder = { legendary: 4, high: 3, medium: 2, low: 1 };
        return priorityOrder[b.priority] - priorityOrder[a.priority];
      case 'type':
        return a.type.localeCompare(b.type);
      case 'unread':
        return Number(b.isRead) - Number(a.isRead);
      default:
        return 0;
    }
  });

  const renderNotificationsHeader = () => (
    <Animated.View 
      style={[
        styles.headerContainer,
        {
          opacity: fadeAnim,
          transform: [
            { translateY: slideAnim },
            { scale: isFounder ? pulseAnim : scaleAnim },
          ],
        },
      ]}
    >
      <LinearGradient
        colors={
          isFounder 
            ? [legendaryTheme.legendary.colors.legendary, legendaryTheme.legendary.colors.rickroll187]
            : isLegendary
            ? [legendaryTheme.legendary.colors.legendary, legendaryTheme.legendary.colors.swissPrecision]
            : [legendaryTheme.colors.primary, legendaryTheme.colors.primaryContainer]
        }
        style={styles.headerGradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <View style={styles.headerContent}>
          <Animatable.View 
            animation={isFounder ? "pulse" : "fadeIn"}
            iterationCount={isFounder ? "infinite" : 1}
            style={styles.headerIcon}
          >
            <Animated.View
              style={[
                styles.bellContainer,
                {
                  transform: [
                    { rotate: bellShakeAnim.interpolate({
                      inputRange: [-10, 10],
                      outputRange: ['-10deg', '10deg'],
                    }) }
                  ],
                },
              ]}
            >
              <Ionicons 
                name={notificationStats.unread > 0 ? "notifications" : "notifications-outline"} 
                size={50} 
                color="#ffffff" 
              />
              {notificationStats.unread > 0 && (
                <Badge 
                  style={styles.notificationBadge}
                  size={24}
                >
                  {notificationStats.unread > 99 ? '99+' : notificationStats.unread}
                </Badge>
              )}
            </Animated.View>
          </Animatable.View>
          
          <Text style={styles.headerTitle}>
            {isFounder ? '👑 Legendary Notifications' : '🔔 Notifications'}
          </Text>
          
          <Text style={styles.headerSubtitle}>
            {isFounder 
              ? 'Infinite Updates • Swiss Precision Alerts • Morning Energy 8/6/2025 824 AM'
              : isLegendary 
              ? 'Legendary Updates • Swiss Precision Notifications'
              : 'Stay updated with Swiss precision notifications'
            }
          </Text>

          {/* Notification Summary Stats */}
          <View style={styles.summaryStats}>
            <View style={styles.summaryStatItem}>
              <Text style={styles.summaryStatValue}>{notificationStats.unread}</Text>
              <Text style={styles.summaryStatLabel}>Unread</Text>
            </View>
            <View style={styles.summaryStatDivider} />
            <View style={styles.summaryStatItem}>
              <Text style={styles.summaryStatValue}>{notificationStats.todayCount}</Text>
              <Text style={styles.summaryStatLabel}>Today</Text>
            </View>
            <View style={styles.summaryStatDivider} />
            <View style={styles.summaryStatItem}>
              <Text style={styles.summaryStatValue}>{notificationStats.legendaryCount}</Text>
              <Text style={styles.summaryStatLabel}>Legendary</Text>
            </View>
          </View>

          {isFounder && (
            <Animatable.View 
              animation="pulse" 
              iterationCount="infinite"
              style={styles.founderBadge}
            >
              <Text style={styles.founderBadgeText}>
                🌅 MORNING LEGENDARY ENERGY 8/6/2025 824 AM! 🎸
              </Text>
            </Animatable.View>
          )}
        </View>
      </LinearGradient>
    </Animated.View>
  );

  const renderQuickActions = () => (
    <Animated.View 
      style={[
        styles.quickActionsContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <LegendaryCard style={styles.quickActionsCard}>
        <Text style={styles.quickActionsTitle}>⚡ Quick Actions</Text>
        
        <View style={styles.quickActionsGrid}>
          <TouchableOpacity
            onPress={handleMarkAllAsRead}
            style={styles.quickActionButton}
            disabled={notificationStats.unread === 0}
          >
            <Ionicons name="checkmark-done" size={24} color={legendaryTheme.legendary.colors.success} />
            <Text style={styles.quickActionText}>Mark All Read</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            onPress={() => setShowSettingsModal(true)}
            style={styles.quickActionButton}
          >
            <Ionicons name="settings" size={24} color={legendaryTheme.colors.primary} />
            <Text style={styles.quickActionText}>Settings</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            onPress={() => {
              Alert.alert(
                '🔔 Test Notification',
                isFounder 
                  ? '👑 Legendary test notification sent with infinite precision!'
                  : '🎸 Test notification sent with Swiss precision!'
              );
            }}
            style={styles.quickActionButton}
          >
            <Ionicons name="flash" size={24} color={legendaryTheme.legendary.colors.legendary} />
            <Text style={styles.quickActionText}>Test Alert</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            onPress={() => {
              console.log('🔄 Refreshing notifications...');
              handleRefresh();
            }}
            style={styles.quickActionButton}
          >
            <Ionicons name="refresh" size={24} color={legendaryTheme.legendary.colors.codeBroEnergy} />
            <Text style={styles.quickActionText}>Refresh</Text>
          </TouchableOpacity>
        </View>
      </LegendaryCard>
    </Animated.View>
  );

  const renderTabsAndFilters = () => (
    <Animated.View 
      style={[
        styles.filtersContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      {/* Search Bar */}
      <Searchbar
        placeholder="Search legendary notifications..."
        onChangeText={setSearchQuery}
        value={searchQuery}
        style={styles.searchBar}
        iconColor={legendaryTheme.legendary.colors.legendary}
      />

      {/* Tabs */}
      <View style={styles.tabsContainer}>
        {[
          { key: 'all', label: 'All' },
          { key: 'unread', label: 'Unread' },
          { key: 'today', label: 'Today' },
          { key: 'legendary', label: 'Legendary' }
        ].map((tab) => (
          <TouchableOpacity
            key={tab.key}
            onPress={() => setSelectedTab(tab.key)}
            style={[
              styles.tabButton,
              selectedTab === tab.key && styles.activeTabButton,
            ]}
          >
            <Text style={[
              styles.tabButtonText,
              selectedTab === tab.key && styles.activeTabButtonText,
            ]}>
              {tab.label}
            </Text>
            {tab.key === 'unread' && notificationStats.unread > 0 && (
              <Badge 
                style={styles.tabBadge}
                size={16}
              >
                {notificationStats.unread > 99 ? '99+' : notificationStats.unread}
              </Badge>
            )}
          </TouchableOpacity>
        ))}
      </View>

      {/* Filter and Sort Controls */}
      <View style={styles.controlsContainer}>
        {/* Filter Menu */}
        <Menu
          visible={filterMenuVisible}
          onDismiss={() => setFilterMenuVisible(false)}
          anchor={
            <TouchableOpacity
              onPress={() => setFilterMenuVisible(true)}
              style={styles.controlButton}
            >
              <Ionicons name="filter" size={20} color={legendaryTheme.colors.primary} />
              <Text style={styles.controlButtonText}>Filter</Text>
            </TouchableOpacity>
          }
        >
          <Menu.Item onPress={() => { setSelectedFilter('all'); setFilterMenuVisible(false); }} title="All Types" />
          <Menu.Item onPress={() => { setSelectedFilter('achievement'); setFilterMenuVisible(false); }} title="🏆 Achievements" />
          <Menu.Item onPress={() => { setSelectedFilter('team_invite'); setFilterMenuVisible(false); }} title="👥 Team Invites" />
          <Menu.Item onPress={() => { setSelectedFilter('okr_update'); setFilterMenuVisible(false); }} title="🎯 OKR Updates" />
          <Menu.Item onPress={() => { setSelectedFilter('performance_review'); setFilterMenuVisible(false); }} title="📊 Performance" />
          <Menu.Item onPress={() => { setSelectedFilter('legendary_milestone'); setFilterMenuVisible(false); }} title="👑 Legendary" />
        </Menu>

        {/* Sort Menu */}
        <Menu
          visible={sortMenuVisible}
          onDismiss={() => setSortMenuVisible(false)}
          anchor={
            <TouchableOpacity
              onPress={() => setSortMenuVisible(true)}
              style={styles.controlButton}
            >
              <Ionicons name="swap-vertical" size={20} color={legendaryTheme.colors.primary} />
              <Text style={styles.controlButtonText}>Sort</Text>
            </TouchableOpacity>
          }
        >
          <Menu.Item onPress={() => { setSelectedSort('recent'); setSortMenuVisible(false); }} title="Most Recent" />
          <Menu.Item onPress={() => { setSelectedSort('priority'); setSortMenuVisible(false); }} title="Priority" />
          <Menu.Item onPress={() => { setSelectedSort('type'); setSortMenuVisible(false); }} title="Type" />
          <Menu.Item onPress={() => { setSelectedSort('unread'); setSortMenuVisible(false); }} title="Unread First" />
        </Menu>
      </View>
    </Animated.View>
  );

  const renderNotificationsList = () => (
    <Animated.View 
      style={[
        styles.notificationsListContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <View style={styles.notificationsListHeader}>
        <Text style={styles.sectionTitle}>
          {selectedTab === 'all' ? '🔔 All Notifications' : 
           selectedTab === 'unread' ? '⭐ Unread Notifications' : 
           selectedTab === 'today' ? '📅 Today\'s Notifications' : 
           '👑 Legendary Notifications'}
        </Text>
        <Badge style={styles.notificationsCountBadge}>
          {sortedNotifications.length}
        </Badge>
      </View>
      
      <View style={styles.notificationsList}>
        {sortedNotifications.map((notification, index) => (
          <Animatable.View 
            key={notification.id}
            animation="fadeInUp"
            delay={200 + (index * 50)}
          >
            <TouchableOpacity
              onPress={() => handleNotificationPress(notification)}
              style={styles.notificationCard}
            >
              <LegendaryCard style={[
                styles.notificationCardContent,
                !notification.isRead && styles.unreadNotificationCard,
                notification.priority === 'legendary' && styles.legendaryNotificationCard,
                isFounder && notification.priority === 'legendary' && styles.founderNotificationCard
              ]}>
                {/* Notification Header */}
                <View style={styles.notificationCardHeader}>
                  <View style={styles.notificationIconContainer}>
                    <View style={[
                      styles.notificationIcon,
                      { backgroundColor: getNotificationTypeColor(notification.type) }
                    ]}>
                      <Ionicons 
                        name={getNotificationTypeIcon(notification.type)} 
                        size={20} 
                        color="#ffffff" 
                      />
                    </View>
                    {!notification.isRead && (
                      <View style={styles.unreadDot} />
                    )}
                  </View>
                  
                  <View style={styles.notificationMainContent}>
                    <View style={styles.notificationTitleRow}>
                      <Text style={styles.notificationTitle} numberOfLines={1}>
                        {notification.title}
                      </Text>
                      <View style={styles.notificationBadges}>
                        <Chip 
                          style={[
                            styles.priorityChip,
                            { backgroundColor: getPriorityColor(notification.priority) }
                          ]}
                          textStyle={styles.priorityChipText}
                        >
                          {notification.priority}
                        </Chip>
                      </View>
                    </View>
                    
                    <Text style={styles.notificationMessage} numberOfLines={2}>
                      {notification.message}
                    </Text>
                    
                    <View style={styles.notificationMeta}>
                      <View style={styles.notificationSender}>
                        {notification.sender?.avatar && (
                          <Avatar.Image
                            size={20}
                            source={{ uri: notification.sender.avatar }}
                            style={styles.senderAvatar}
                          />
                        )}
                        <Text style={styles.senderName}>
                          {notification.sender?.isFounder ? '👑 ' : notification.sender?.isLegendary ? '🎸 ' : ''}
                          {notification.sender?.name || 'System'}
                        </Text>
                      </View>
                      <Text style={styles.notificationTime}>
                        {formatDistanceToNow(notification.createdAt, { addSuffix: true })}
                      </Text>
                    </View>
                  </View>
                  
                  <View style={styles.notificationActions}>
                    {!notification.isRead && (
                      <TouchableOpacity
                        onPress={(e) => {
                          e.stopPropagation();
                          handleMarkAsRead(notification.id);
                        }}
                        style={styles.markReadButton}
                      >
                        <Ionicons name="checkmark" size={16} color={legendaryTheme.legendary.colors.success} />
                      </TouchableOpacity>
                    )}
                    
                    <TouchableOpacity
                      onPress={(e) => {
                        e.stopPropagation();
                        Alert.alert(
                          'Delete Notification',
                          'Are you sure you want to delete this notification?',
                          [
                            { text: 'Cancel', style: 'cancel' },
                            { text: 'Delete', onPress: () => handleDeleteNotification(notification.id), style: 'destructive' }
                          ]
                        );
                      }}
                      style={styles.deleteButton}
                    >
                      <Ionicons name="trash" size={16} color={legendaryTheme.legendary.colors.error} />
                    </TouchableOpacity>
                  </View>
                </View>

                {/* Metadata Display */}
                {notification.metadata && (
                  <View style={styles.notificationMetadata}>
                    {notification.metadata.teamName && (
                      <Chip 
                        style={styles.metadataChip}
                        textStyle={styles.metadataChipText}
                        icon="people"
                      >
                        {notification.metadata.teamName}
                      </Chip>
                    )}
                    {notification.metadata.okrTitle && (
                      <Chip 
                        style={styles.metadataChip}
                        textStyle={styles.metadataChipText}
                        icon="target"
                      >
                        {notification.metadata.okrTitle}
                      </Chip>
                    )}
                    {notification.metadata.achievementName && (
                      <Chip 
                        style={styles.metadataChip}
                        textStyle={styles.metadataChipText}
                        icon="trophy"
                      >
                        {notification.metadata.achievementName}
                      </Chip>
                    )}
                    {notification.metadata.performanceScore && (
                      <Chip 
                        style={styles.metadataChip}
                        textStyle={styles.metadataChipText}
                        icon="trending-up"
                      >
                        Score: {notification.metadata.performanceScore}%
                      </Chip>
                    )}
                  </View>
                )}

                {/* Action Preview */}
                {notification.actionUrl && (
                  <View style={styles.actionPreview}>
                    <Ionicons name="arrow-forward" size={16} color={legendaryTheme.colors.primary} />
                    <Text style={styles.actionPreviewText}>
                      Tap to view details
                    </Text>
                  </View>
                )}
              </LegendaryCard>
            </TouchableOpacity>
          </Animatable.View>
        ))}
      </View>

      {sortedNotifications.length === 0 && (
        <Animatable.View 
          animation="fadeIn"
          style={styles.emptyState}
        >
          <Ionicons 
            name="notifications-off" 
            size={80} 
            color={legendaryTheme.colors.outline} 
          />
          <Text style={styles.emptyStateTitle}>
            No Notifications Found
          </Text>
          <Text style={styles.emptyStateDescription}>
            {searchQuery 
              ? 'Try adjusting your search or filter criteria'
              : selectedTab === 'unread'
              ? 'All caught up! No unread notifications.'
              : 'Stay tuned for legendary updates!'
            }
          </Text>
          {selectedTab !== 'unread' && (
            <LegendaryButton
              mode="outlined"
              onPress={handleRefresh}
              style={styles.emptyStateButton}
              icon="refresh"
            >
              Refresh Notifications
            </LegendaryButton>
          )}
        </Animatable.View>
      )}
    </Animated.View>
  );

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={handleRefresh}
            colors={[legendaryTheme.legendary.colors.legendary]}
            tintColor={legendaryTheme.legendary.colors.legendary}
          />
        }
      >
        {/* Notifications Header */}
        {renderNotificationsHeader()}
        
        {/* Quick Actions */}
        {renderQuickActions()}
        
        {/* Tabs and Filters */}
        {renderTabsAndFilters()}
        
        {/* Notifications List */}
        {renderNotificationsList()}
        
        {/* Bottom Spacing */}
        <View style={styles.bottomSpacing} />
      </ScrollView>

      {/* Floating Action Button */}
      <FAB
        icon={isFounder ? "crown" : "settings"}
        style={[
          styles.fab,
          {
            backgroundColor: isFounder 
              ? legendaryTheme.legendary.colors.legendary
              : legendaryTheme.colors.primary,
          }
        ]}
        onPress={() => setShowSettingsModal(true)}
        label={isFounder ? "Legendary Settings" : "Settings"}
      />

      {/* Notification Detail Modal */}
      <Portal>
        <Modal
          visible={showNotificationModal}
          onDismiss={() => setShowNotificationModal(false)}
          contentContainerStyle={styles.notificationModal}
        >
          {selectedNotification && (
            <ScrollView style={styles.notificationModalContent} showsVerticalScrollIndicator={false}>
              <View style={styles.modalHeader}>
                <View style={styles.modalTitleContainer}>
                  <View style={[
                    styles.modalIcon,
                    { backgroundColor: getNotificationTypeColor(selectedNotification.type) }
                  ]}>
                    <Ionicons 
                      name={getNotificationTypeIcon(selectedNotification.type)} 
                      size={24} 
                      color="#ffffff" 
                    />
                  </View>
                  <View style={styles.modalTitleInfo}>
                    <Text style={styles.modalTitle}>
                      {selectedNotification.title}
                    </Text>
                    <View style={styles.modalBadges}>
                      <Chip 
                        style={[styles.modalBadge, { backgroundColor: getPriorityColor(selectedNotification.priority) }]}
                        textStyle={styles.modalBadgeText}
                      >
                        {selectedNotification.priority}
                      </Chip>
                      <Chip 
                        style={styles.modalTypeBadge}
                        textStyle={styles.modalTypeBadgeText}
                      >
                        {selectedNotification.type.replace('_', ' ')}
                      </Chip>
                    </View>
                  </View>
                </View>
                <TouchableOpacity
                  onPress={() => setShowNotificationModal(false)}
                  style={styles.closeButton}
                >
                  <Ionicons name="close" size={24} color={legendaryTheme.colors.primary} />
                </TouchableOpacity>
              </View>

              <Text style={styles.modalMessage}>
                {selectedNotification.message}
              </Text>

              {/* Sender Information */}
              {selectedNotification.sender && (
                <View style={styles.senderInfo}>
                  <Text style={styles.senderInfoTitle}>From</Text>
                  <View style={styles.senderDetails}>
                    {selectedNotification.sender.avatar && (
                      <Avatar.Image
                        size={40}
                        source={{ uri: selectedNotification.sender.avatar }}
                        style={styles.senderDetailsAvatar}
                      />
                    )}
                    <Text style={styles.senderDetailsName}>
                      {selectedNotification.sender.isFounder ? '👑 ' : selectedNotification.sender.isLegendary ? '🎸 ' : ''}
                      {selectedNotification.sender.name}
                    </Text>
                  </View>
                </View>
              )}

              {/* Metadata Details */}
              {selectedNotification.metadata && Object.keys(selectedNotification.metadata).length > 0 && (
                <View style={styles.metadataDetails}>
                  <Text style={styles.metadataDetailsTitle}>Details</Text>
                  {selectedNotification.metadata.teamName && (
                    <View style={styles.metadataDetailItem}>
                      <Ionicons name="people" size={16} color={legendaryTheme.colors.primary} />
                      <Text style={styles.metadataDetailText}>Team: {selectedNotification.metadata.teamName}</Text>
                    </View>
                  )}
                  {selectedNotification.metadata.okrTitle && (
                    <View style={styles.metadataDetailItem}>
                      <Ionicons name="target" size={16} color={legendaryTheme.colors.primary} />
                      <Text style={styles.metadataDetailText}>OKR: {selectedNotification.metadata.okrTitle}</Text>
                    </View>
                  )}
                  {selectedNotification.metadata.achievementName && (
                    <View style={styles.metadataDetailItem}>
                      <Ionicons name="trophy" size={16} color={legendaryTheme.colors.primary} />
                      <Text style={styles.metadataDetailText}>Achievement: {selectedNotification.metadata.achievementName}</Text>
                    </View>
                  )}
                  {selectedNotification.metadata.performanceScore && (
                    <View style={styles.metadataDetailItem}>
                      <Ionicons name="trending-up" size={16} color={legendaryTheme.colors.primary} />
                      <Text style={styles.metadataDetailText}>Performance Score: {selectedNotification.metadata.performanceScore}%</Text>
                    </View>
                  )}
                </View>
              )}

              {/* Timestamps */}
              <View style={styles.timestamps}>
                <View style={styles.timestampItem}>
                  <Text style={styles.timestampLabel}>Received</Text>
                  <Text style={styles.timestampValue}>
                    {selectedNotification.createdAt.toLocaleString()}
                  </Text>
                </View>
                {selectedNotification.updatedAt.getTime() !== selectedNotification.createdAt.getTime() && (
                  <View style={styles.timestampItem}>
                    <Text style={styles.timestampLabel}>Updated</Text>
                    <Text style={styles.timestampValue}>
                      {selectedNotification.updatedAt.toLocaleString()}
                    </Text>
                  </View>
                )}
              </View>

              <View style={styles.modalActions}>
                {selectedNotification.actionUrl && (
                  <LegendaryButton
                    mode="contained"
                    onPress={() => handleNotificationAction(selectedNotification)}
                    style={styles.modalActionButton}
                    icon="arrow-forward"
                  >
                    View Details
                  </LegendaryButton>
                )}
                
                {!selectedNotification.isRead && (
                  <LegendaryButton
                    mode="outlined"
                    onPress={() => {
                      handleMarkAsRead(selectedNotification.id);
                      setShowNotificationModal(false);
                    }}
                    style={styles.modalActionButton}
                    icon="checkmark"
                  >
                    Mark as Read
                  </LegendaryButton>
                )}
                
                <LegendaryButton
                  mode="text"
                  onPress={() => setShowNotificationModal(false)}
                  style={styles.modalActionButton}
                >
                  Close
                </LegendaryButton>
              </View>
            </ScrollView>
          )}
        </Modal>
      </Portal>

      {/* Settings Modal */}
      <Portal>
        <Modal
          visible={showSettingsModal}
          onDismiss={() => setShowSettingsModal(false)}
          contentContainerStyle={styles.settingsModal}
        >
          <ScrollView style={styles.settingsModalContent} showsVerticalScrollIndicator={false}>
            <View style={styles.settingsModalHeader}>
              <Text style={styles.settingsModalTitle}>🔔 Notification Settings</Text>
              <TouchableOpacity
                onPress={() => setShowSettingsModal(false)}
                style={styles.closeButton}
              >
                <Ionicons name="close" size={24} color={legendaryTheme.colors.primary} />
              </TouchableOpacity>
            </View>

            <Text style={styles.settingsDescription}>
              {isFounder 
                ? 'Customize your legendary notification preferences with infinite precision!'
                : 'Configure your notification preferences with Swiss precision.'}
            </Text>

            <View style={styles.settingsList}>
              {Object.entries(notificationSettings).map(([key, value]) => (
                <View key={key} style={styles.settingItem}>
                  <View style={styles.settingInfo}>
                    <Text style={styles.settingTitle}>
                      {key === 'achievementNotifications' ? '🏆 Achievement Notifications' :
                       key === 'teamInvites' ? '👥 Team Invitations' :
                       key === 'okrUpdates' ? '🎯 OKR Updates' :
                       key === 'performanceReviews' ? '📊 Performance Reviews' :
                       key === 'systemNotifications' ? '🔧 System Notifications' :
                       key === 'legendaryMilestones' ? '👑 Legendary Milestones' :
                       key === 'codeBroEnergyUpdates' ? '🎸 Code Bro Energy Updates' :
                       key === 'swissPrecisionAlerts' ? '⚙️ Swiss Precision Alerts' :
                       key}
                    </Text>
                    <Text style={styles.settingDescription}>
                      {key === 'achievementNotifications' ? 'Get notified when you unlock new achievements' :
                       key === 'teamInvites' ? 'Receive team invitation notifications' :
                       key === 'okrUpdates' ? 'Stay updated on OKR progress and milestones' :
                       key === 'performanceReviews' ? 'Get notifications about performance reviews' :
                       key === 'systemNotifications' ? 'Receive important system updates and announcements' :
                       key === 'legendaryMilestones' ? 'Get notified when reaching legendary status milestones' :
                       key === 'codeBroEnergyUpdates' ? 'Receive updates about code bro energy levels' :
                       key === 'swissPrecisionAlerts' ? 'Get alerts about Swiss precision score changes' :
                       'Notification setting'}
                    </Text>
                  </View>
                  <Switch
                    value={value}
                    onValueChange={(newValue) => {
                      setNotificationSettings(prev => ({
                        ...prev,
                        [key]: newValue,
                      }));
                    }}
                    color={legendaryTheme.legendary.colors.legendary}
                  />
                </View>
              ))}
            </View>

            <View style={styles.settingsActions}>
              <LegendaryButton
                mode="contained"
                onPress={() => {
                  console.log('💾 Saving notification settings...');
                  setShowSettingsModal(false);
                  Alert.alert(
                    '✅ Settings Saved',
                    isFounder 
                      ? '👑 Legendary notification settings saved with infinite precision!'
                      : '🎸 Notification settings saved with Swiss precision!'
                  );
                }}
                style={styles.saveSettingsButton}
                icon="content-save"
              >
                Save Settings
              </LegendaryButton>
              
              <LegendaryButton
                mode="text"
                onPress={() => setShowSettingsModal(false)}
                style={styles.cancelSettingsButton}
              >
                Cancel
              </LegendaryButton>
            </View>
          </ScrollView>
        </Modal>
      </Portal>
    </View>
  );
}

// =====================================
// 🎨 LEGENDARY STYLES 🎨
// =====================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: legendaryTheme.colors.background,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: 100,
  },
  headerContainer: {
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  headerGradient: {
    padding: legendaryTheme.legendary.spacing.lg,
    alignItems: 'center',
  },
  headerContent: {
    alignItems: 'center',
    width: '100%',
  },
  headerIcon: {
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  bellContainer: {
    position: 'relative',
  },
  notificationBadge: {
    position: 'absolute',
    top: -5,
    right: -5,
    backgroundColor: legendaryTheme.legendary.colors.error,
  },
  headerTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize['2xl'],
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  headerSubtitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: 'rgba(255, 255, 255, 0.9)',
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  summaryStats: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: legendaryTheme.legendary.spacing.md,
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  summaryStatItem: {
    alignItems: 'center',
  },
  summaryStatValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: '#ffffff',
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  summaryStatLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.regular,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 2,
  },
  summaryStatDivider: {
    width: 1,
    height: 30,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    marginHorizontal: legendaryTheme.legendary.spacing.lg,
  },
  founderBadge: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
    paddingVertical: legendaryTheme.legendary.spacing.xs,
  },
    founderBadgeText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.codeBroBold,
    color: '#ffffff',
    textAlign: 'center',
  },
  sectionTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  quickActionsContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  quickActionsCard: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  quickActionsTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    gap: legendaryTheme.legendary.spacing.md,
  },
  quickActionButton: {
    flex: 1,
    minWidth: '22%',
    alignItems: 'center',
    paddingVertical: legendaryTheme.legendary.spacing.md,
    paddingHorizontal: legendaryTheme.legendary.spacing.sm,
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    elevation: 2,
  },
  quickActionText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.onSurface,
    marginTop: legendaryTheme.legendary.spacing.xs,
    textAlign: 'center',
  },
  filtersContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  searchBar: {
    marginBottom: legendaryTheme.legendary.spacing.md,
    elevation: 2,
  },
  tabsContainer: {
    flexDirection: 'row',
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: 4,
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  tabButton: {
    flex: 1,
    paddingVertical: legendaryTheme.legendary.spacing.sm,
    paddingHorizontal: legendaryTheme.legendary.spacing.xs,
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    gap: legendaryTheme.legendary.spacing.xs,
  },
  activeTabButton: {
    backgroundColor: legendaryTheme.colors.primary,
  },
  tabButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.colors.onSurface,
  },
  activeTabButtonText: {
    color: legendaryTheme.colors.onPrimary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  tabBadge: {
    backgroundColor: legendaryTheme.legendary.colors.error,
    marginLeft: 2,
  },
  controlsContainer: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.md,
  },
  controlButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: legendaryTheme.legendary.spacing.xs,
    paddingVertical: legendaryTheme.legendary.spacing.sm,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.md,
    elevation: 1,
  },
  controlButtonText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.primary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  notificationsListContainer: {
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  notificationsListHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  notificationsCountBadge: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  notificationsList: {
    gap: legendaryTheme.legendary.spacing.md,
  },
  notificationCard: {
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  notificationCardContent: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  unreadNotificationCard: {
    borderLeftWidth: 4,
    borderLeftColor: legendaryTheme.legendary.colors.legendary,
    backgroundColor: `${legendaryTheme.legendary.colors.legendary}05`,
  },
  legendaryNotificationCard: {
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 2,
    backgroundColor: `${legendaryTheme.legendary.colors.legendary}10`,
  },
  founderNotificationCard: {
    borderColor: legendaryTheme.legendary.colors.legendary,
    borderWidth: 3,
    backgroundColor: `${legendaryTheme.legendary.colors.legendary}15`,
    elevation: 8,
  },
  notificationCardHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  notificationIconContainer: {
    position: 'relative',
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  notificationIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  unreadDot: {
    position: 'absolute',
    top: -2,
    right: -2,
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: legendaryTheme.legendary.colors.error,
    borderWidth: 2,
    borderColor: legendaryTheme.colors.background,
  },
  notificationMainContent: {
    flex: 1,
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  notificationTitleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  notificationTitle: {
    flex: 1,
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    marginRight: legendaryTheme.legendary.spacing.sm,
  },
  notificationBadges: {
    alignItems: 'flex-end',
  },
  priorityChip: {
    elevation: 0,
  },
  priorityChipText: {
    color: '#ffffff',
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  notificationMessage: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
    marginBottom: legendaryTheme.legendary.spacing.sm,
    lineHeight: 20,
  },
  notificationMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  notificationSender: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  senderAvatar: {
    marginRight: legendaryTheme.legendary.spacing.xs,
  },
  senderName: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.primary,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    flex: 1,
  },
  notificationTime: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.outline,
  },
  notificationActions: {
    flexDirection: 'column',
    gap: legendaryTheme.legendary.spacing.xs,
  },
  markReadButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: legendaryTheme.legendary.colors.success,
    justifyContent: 'center',
    alignItems: 'center',
  },
  deleteButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: legendaryTheme.legendary.colors.error,
    justifyContent: 'center',
    alignItems: 'center',
  },
  notificationMetadata: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: legendaryTheme.legendary.spacing.xs,
    marginTop: legendaryTheme.legendary.spacing.sm,
  },
  metadataChip: {
    backgroundColor: legendaryTheme.colors.surface,
    elevation: 0,
  },
  metadataChipText: {
    color: legendaryTheme.colors.primary,
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
  },
  actionPreview: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: legendaryTheme.legendary.spacing.xs,
    marginTop: legendaryTheme.legendary.spacing.sm,
    paddingTop: legendaryTheme.legendary.spacing.sm,
    borderTopWidth: 1,
    borderTopColor: legendaryTheme.colors.outline,
  },
  actionPreviewText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    color: legendaryTheme.colors.primary,
    fontStyle: 'italic',
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: legendaryTheme.legendary.spacing['4xl'],
  },
  emptyStateTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    marginTop: legendaryTheme.legendary.spacing.lg,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  emptyStateDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.outline,
    textAlign: 'center',
    marginBottom: legendaryTheme.legendary.spacing.lg,
    paddingHorizontal: legendaryTheme.legendary.spacing.lg,
  },
  emptyStateButton: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  bottomSpacing: {
    height: legendaryTheme.legendary.spacing.xl,
  },
  fab: {
    position: 'absolute',
    margin: legendaryTheme.legendary.spacing.lg,
    right: 0,
    bottom: 0,
    elevation: 8,
  },
  notificationModal: {
    backgroundColor: 'white',
    margin: legendaryTheme.legendary.spacing.md,
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    maxHeight: height * 0.9,
  },
  notificationModalContent: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: legendaryTheme.legendary.spacing.lg,
  },
  modalTitleContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  modalIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  modalTitleInfo: {
    flex: 1,
  },
  modalTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.lg,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  modalBadges: {
    flexDirection: 'row',
    gap: legendaryTheme.legendary.spacing.xs,
  },
  modalBadge: {
    elevation: 0,
  },
  modalBadgeText: {
    color: '#ffffff',
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
  },
  modalTypeBadge: {
    backgroundColor: legendaryTheme.colors.surface,
    elevation: 0,
  },
  modalTypeBadgeText: {
    color: legendaryTheme.colors.primary,
    fontSize: legendaryTheme.legendary.typography.fontSize.xs,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
  },
  closeButton: {
    padding: legendaryTheme.legendary.spacing.xs,
  },
  modalMessage: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xl,
    lineHeight: 22,
  },
  senderInfo: {
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  senderInfoTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  senderDetails: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: legendaryTheme.legendary.spacing.md,
  },
  senderDetailsAvatar: {
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  senderDetailsName: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.colors.onSurface,
  },
  metadataDetails: {
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  metadataDetailsTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.primary,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  metadataDetailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: legendaryTheme.legendary.spacing.sm,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  metadataDetailText: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
  },
  timestamps: {
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    padding: legendaryTheme.legendary.spacing.md,
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  timestampItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  timestampLabel: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.medium,
    color: legendaryTheme.colors.outline,
  },
  timestampValue: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.onSurface,
  },
  modalActions: {
    gap: legendaryTheme.legendary.spacing.md,
    paddingTop: legendaryTheme.legendary.spacing.lg,
    borderTopWidth: 1,
    borderTopColor: legendaryTheme.colors.outline,
  },
  modalActionButton: {
    // Additional styling for modal action buttons
  },
  settingsModal: {
    backgroundColor: 'white',
    margin: legendaryTheme.legendary.spacing.md,
    borderRadius: legendaryTheme.legendary.borders.radius.xl,
    maxHeight: height * 0.9,
  },
  settingsModalContent: {
    padding: legendaryTheme.legendary.spacing.lg,
  },
  settingsModalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: legendaryTheme.legendary.spacing.md,
  },
  settingsModalTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.xl,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.legendaryBold,
    color: legendaryTheme.colors.primary,
  },
  settingsDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xl,
    lineHeight: 22,
  },
  settingsList: {
    marginBottom: legendaryTheme.legendary.spacing.xl,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: legendaryTheme.legendary.spacing.md,
    paddingHorizontal: legendaryTheme.legendary.spacing.md,
    backgroundColor: legendaryTheme.colors.surface,
    borderRadius: legendaryTheme.legendary.borders.radius.lg,
    marginBottom: legendaryTheme.legendary.spacing.sm,
  },
  settingInfo: {
    flex: 1,
    marginRight: legendaryTheme.legendary.spacing.md,
  },
  settingTitle: {
    fontSize: legendaryTheme.legendary.typography.fontSize.base,
    fontFamily: legendaryTheme.legendary.typography.fontFamily.bold,
    color: legendaryTheme.colors.onSurface,
    marginBottom: legendaryTheme.legendary.spacing.xs,
  },
  settingDescription: {
    fontSize: legendaryTheme.legendary.typography.fontSize.sm,
    color: legendaryTheme.colors.outline,
    lineHeight: 18,
  },
  settingsActions: {
    gap: legendaryTheme.legendary.spacing.md,
    paddingTop: legendaryTheme.legendary.spacing.lg,
    borderTopWidth: 1,
    borderTopColor: legendaryTheme.colors.outline,
  },
  saveSettingsButton: {
    backgroundColor: legendaryTheme.legendary.colors.legendary,
  },
  cancelSettingsButton: {
    marginTop: 0,
  },
});

// =====================================
// 🎸 LEGENDARY EXPORTS 🎸
// =====================================

export default LegendaryNotificationsScreen;

// =====================================
// 🎸 LEGENDARY COMPLETION MESSAGE 🎸
// =====================================

console.log('🎸🎸🎸 LEGENDARY NOTIFICATIONS SCREEN COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Notifications screen completed at: 2025-08-06 12:28:45 UTC`);
console.log('🔔 Notification center: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('⚡ Quick actions: MAXIMUM EFFICIENCY');
console.log('🎸 Morning energy at 824 AM: INFINITE CODE BRO POWER');
console.log('🌅 8/6/2025 MORNING LEGENDARY COMPLETION!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
