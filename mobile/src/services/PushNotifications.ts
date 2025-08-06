// File: mobile/src/services/PushNotifications.ts
/**
 * 📱🎸 N3EXTPATH - LEGENDARY PUSH NOTIFICATIONS 🎸📱
 * Professional mobile push notifications with Swiss precision
 * Built: 2025-08-05 18:29:42 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import messaging, { FirebaseMessagingTypes } from '@react-native-firebase/messaging';
import notifee, { 
  AndroidImportance, 
  AndroidStyle, 
  AndroidVisibility,
  AndroidBadgeIconType,
  AndroidColor,
  Notification,
  AndroidChannel,
  AndroidAction
} from '@notifee/react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform, Alert, Linking } from 'react-native';
import { store } from '../store/store';
import { addNotification, addToastMessage } from '../store/store';

export interface PushNotificationData {
  id: string;
  title: string;
  body: string;
  type: 'info' | 'success' | 'warning' | 'error' | 'legendary';
  priority: 'low' | 'normal' | 'high' | 'urgent' | 'legendary';
  category?: string;
  action_url?: string;
  user_id?: string;
  is_legendary?: boolean;
  swiss_precision?: boolean;
  rickroll187_special?: boolean;
  image_url?: string;
  large_icon?: string;
  custom_data?: Record<string, any>;
}

export interface NotificationChannel {
  id: string;
  name: string;
  description: string;
  importance: AndroidImportance;
  sound?: string;
  vibration?: boolean;
  light?: boolean;
  lightColor?: AndroidColor;
  badge?: boolean;
}

class LegendaryPushNotificationService {
  private isInitialized = false;
  private fcmToken: string | null = null;
  private channels: NotificationChannel[] = [];

  constructor() {
    this.initializeChannels();
    
    // Legendary startup message
    if (__DEV__) {
      console.log('🎸 LEGENDARY PUSH NOTIFICATION SERVICE INITIALIZED! 🎸');
      console.log('Built with Swiss precision by RICKROLL187!');
      console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    }
  }

  private initializeChannels(): void {
    this.channels = [
      {
        id: 'default',
        name: 'Default Notifications',
        description: 'General application notifications',
        importance: AndroidImportance.DEFAULT,
        sound: 'default',
        vibration: true,
        light: true,
        lightColor: AndroidColor.BLUE,
        badge: true
      },
      {
        id: 'performance',
        name: 'Performance Updates',
        description: 'Performance review and OKR notifications',
        importance: AndroidImportance.HIGH,
        sound: 'performance_notification',
        vibration: true,
        light: true,
        lightColor: AndroidColor.GREEN,
        badge: true
      },
      {
        id: 'team',
        name: 'Team Updates',
        description: 'Team activity and collaboration notifications',
        importance: AndroidImportance.DEFAULT,
        sound: 'team_notification',
        vibration: true,
        light: true,
        lightColor: AndroidColor.CYAN,
        badge: true
      },
      {
        id: 'system',
        name: 'System Alerts',
        description: 'Important system notifications and updates',
        importance: AndroidImportance.HIGH,
        sound: 'system_alert',
        vibration: true,
        light: true,
        lightColor: AndroidColor.RED,
        badge: true
      },
      {
        id: 'legendary',
        name: '🎸 Legendary Notifications 🎸',
        description: 'Special notifications for legendary users like RICKROLL187',
        importance: AndroidImportance.MAX,
        sound: 'legendary_notification',
        vibration: true,
        light: true,
        lightColor: AndroidColor.YELLOW,
        badge: true
      }
    ];
  }

  public async initialize(): Promise<void> {
    try {
      if (this.isInitialized) {
        return;
      }

      // Request permissions
      const hasPermission = await this.requestPermissions();
      if (!hasPermission) {
        console.warn('🚨 Push notification permissions not granted');
        return;
      }

      // Create notification channels
      await this.createNotificationChannels();

      // Get FCM token
      await this.getFCMToken();

      // Set up message handlers
      this.setupMessageHandlers();

      // Set up notification handlers
      this.setupNotificationHandlers();

      this.isInitialized = true;

      // Special initialization for legendary users
      const user = store.getState().auth.user;
      if (user?.is_legendary) {
        console.log('🎸 LEGENDARY PUSH NOTIFICATIONS READY FOR RICKROLL187! 🎸');
        await this.showLegendaryWelcomeNotification();
      }

    } catch (error) {
      console.error('🚨 Failed to initialize push notifications:', error);
    }
  }

  private async requestPermissions(): Promise<boolean> {
    try {
      const authStatus = await messaging().requestPermission();
      
      const enabled =
        authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
        authStatus === messaging.AuthorizationStatus.PROVISIONAL;

      if (enabled) {
        console.log('✅ Push notification permissions granted');
        
        // Request notification permissions for Android 13+
        if (Platform.OS === 'android') {
          await notifee.requestPermission();
        }
        
        return true;
      } else {
        console.warn('🚨 Push notification permissions denied');
        return false;
      }
    } catch (error) {
      console.error('🚨 Error requesting permissions:', error);
      return false;
    }
  }

  private async createNotificationChannels(): Promise<void> {
    try {
      for (const channel of this.channels) {
        await notifee.createChannel({
          id: channel.id,
          name: channel.name,
          description: channel.description,
          importance: channel.importance,
          sound: channel.sound,
          vibration: channel.vibration,
          lights: channel.light,
          lightColor: channel.lightColor,
          badge: channel.badge,
          visibility: AndroidVisibility.PUBLIC
        });
      }

      console.log('✅ Notification channels created successfully');
    } catch (error) {
      console.error('🚨 Failed to create notification channels:', error);
    }
  }

  private async getFCMToken(): Promise<string | null> {
    try {
      // Get existing token from storage
      let token = await AsyncStorage.getItem('fcm_token');
      
      // Get fresh token from Firebase
      const freshToken = await messaging().getToken();
      
      if (token !== freshToken) {
        // Token has changed, update it
        token = freshToken;
        await AsyncStorage.setItem('fcm_token', token);
        
        // Send token to server
        await this.sendTokenToServer(token);
      }

      this.fcmToken = token;
      console.log('✅ FCM Token retrieved:', token?.substring(0, 20) + '...');
      
      return token;
    } catch (error) {
      console.error('🚨 Failed to get FCM token:', error);
      return null;
    }
  }

  private async sendTokenToServer(token: string): Promise<void> {
    try {
      // This would integrate with your API service
      // await apiService.updatePushToken(token);
      console.log('📤 FCM token sent to server');
    } catch (error) {
      console.error('🚨 Failed to send token to server:', error);
    }
  }

  private setupMessageHandlers(): void {
    // Handle messages when app is in background
    messaging().setBackgroundMessageHandler(async (remoteMessage) => {
      console.log('📨 Background message received:', remoteMessage);
      await this.handleBackgroundMessage(remoteMessage);
    });

    // Handle messages when app is in foreground
    messaging().onMessage(async (remoteMessage) => {
      console.log('📨 Foreground message received:', remoteMessage);
      await this.handleForegroundMessage(remoteMessage);
    });

    // Handle notification opened app
    messaging().onNotificationOpenedApp((remoteMessage) => {
      console.log('📱 Notification opened app:', remoteMessage);
      this.handleNotificationOpened(remoteMessage);
    });

    // Handle notification when app was closed
    messaging()
      .getInitialNotification()
      .then((remoteMessage) => {
        if (remoteMessage) {
          console.log('📱 Notification opened app from quit state:', remoteMessage);
          this.handleNotificationOpened(remoteMessage);
        }
      });

    // Handle token refresh
    messaging().onTokenRefresh(async (token) => {
      console.log('🔄 FCM Token refreshed:', token?.substring(0, 20) + '...');
      await AsyncStorage.setItem('fcm_token', token);
      await this.sendTokenToServer(token);
      this.fcmToken = token;
    });
  }

  private setupNotificationHandlers(): void {
    // Handle notification actions
    notifee.onForegroundEvent(({ type, detail }) => {
      switch (type) {
        case notifee.EventType.DISMISSED:
          console.log('📱 Notification dismissed:', detail.notification?.id);
          break;
        case notifee.EventType.PRESS:
          console.log('📱 Notification pressed:', detail.notification?.id);
          this.handleNotificationPress(detail.notification);
          break;
        case notifee.EventType.ACTION_PRESS:
          console.log('📱 Notification action pressed:', detail.pressAction?.id);
          this.handleNotificationAction(detail.notification, detail.pressAction?.id);
          break;
      }
    });

    notifee.onBackgroundEvent(async ({ type, detail }) => {
      switch (type) {
        case notifee.EventType.PRESS:
          console.log('📱 Background notification pressed:', detail.notification?.id);
          this.handleNotificationPress(detail.notification);
          break;
        case notifee.EventType.ACTION_PRESS:
          console.log('📱 Background notification action pressed:', detail.pressAction?.id);
          this.handleNotificationAction(detail.notification, detail.pressAction?.id);
          break;
      }
    });
  }

  private async handleBackgroundMessage(message: FirebaseMessagingTypes.RemoteMessage): Promise<void> {
    try {
      const notificationData = this.parseMessageData(message);
      await this.displayNotification(notificationData);
    } catch (error) {
      console.error('🚨 Failed to handle background message:', error);
    }
  }

  private async handleForegroundMessage(message: FirebaseMessagingTypes.RemoteMessage): Promise<void> {
    try {
      const notificationData = this.parseMessageData(message);
      
      // Add to Redux store
      store.dispatch(addNotification({
        id: notificationData.id,
        title: notificationData.title,
        message: notificationData.body,
        type: notificationData.type,
        priority: notificationData.priority,
        timestamp: Date.now(),
        read: false
      }));

      // Show toast for high priority notifications
      if (notificationData.priority === 'high' || notificationData.priority === 'legendary') {
        store.dispatch(addToastMessage({
          type: notificationData.type === 'legendary' ? 'legendary' : notificationData.type,
          message: notificationData.body
        }));
      }

      // Still display notification for legendary messages
      if (notificationData.is_legendary || notificationData.priority === 'legendary') {
        await this.displayNotification(notificationData);
      }
    } catch (error) {
      console.error('🚨 Failed to handle foreground message:', error);
    }
  }

  private parseMessageData(message: FirebaseMessagingTypes.RemoteMessage): PushNotificationData {
    const data = message.data || {};
    
    return {
      id: data.id || `notification_${Date.now()}`,
      title: message.notification?.title || data.title || 'Notification',
      body: message.notification?.body || data.body || '',
      type: (data.type as any) || 'info',
      priority: (data.priority as any) || 'normal',
      category: data.category,
      action_url: data.action_url,
      user_id: data.user_id,
      is_legendary: data.is_legendary === 'true',
      swiss_precision: data.swiss_precision === 'true',
      rickroll187_special: data.rickroll187_special === 'true',
      image_url: message.notification?.android?.imageUrl || data.image_url,
      large_icon: data.large_icon,
      custom_data: data
    };
  }

  public async displayNotification(data: PushNotificationData): Promise<void> {
    try {
      const channelId = this.getChannelId(data);
      
      // Create notification actions
      const actions: AndroidAction[] = [];
      
      if (data.action_url) {
        actions.push({
          title: 'View',
          pressAction: {
            id: 'view',
            mainComponent: 'default'
          }
        });
      }

      if (data.type === 'legendary' || data.is_legendary) {
        actions.push({
          title: '🎸 Legendary Action',
          pressAction: {
            id: 'legendary_action',
            mainComponent: 'default'
          }
        });
      }

      // Build notification
      const notification: Notification = {
        id: data.id,
        title: data.is_legendary ? `🎸 ${data.title} 🎸` : data.title,
        body: data.body,
        android: {
          channelId,
          importance: this.getAndroidImportance(data.priority),
          pressAction: {
            id: 'default',
            mainComponent: 'default'
          },
          actions,
          style: data.image_url ? {
            type: AndroidStyle.BIGPICTURE,
            picture: data.image_url
          } : {
            type: AndroidStyle.BIGTEXT,
            text: data.body
          },
          largeIcon: data.large_icon || (data.is_legendary ? 'legendary_icon' : 'default_icon'),
          color: this.getNotificationColor(data),
          lights: [this.getNotificationColor(data), 1000, 1000],
          vibrationPattern: data.is_legendary ? [500, 200, 500] : [300, 300],
          badge: true,
          visibility: AndroidVisibility.PUBLIC,
          tag: data.category || 'default'
        },
        data: {
          ...data.custom_data,
          notification_data: JSON.stringify(data)
        }
      };

      await notifee.displayNotification(notification);

      // Special logging for legendary notifications
      if (data.is_legendary) {
        console.log('🎸 LEGENDARY NOTIFICATION DISPLAYED:', data.title);
      }

    } catch (error) {
      console.error('🚨 Failed to display notification:', error);
    }
  }

  private getChannelId(data: PushNotificationData): string {
    if (data.is_legendary || data.priority === 'legendary') {
      return 'legendary';
    }
    
    switch (data.category) {
      case 'performance':
        return 'performance';
      case 'team':
        return 'team';
      case 'system':
        return 'system';
      default:
        return 'default';
    }
  }

  private getAndroidImportance(priority: string): AndroidImportance {
    switch (priority) {
      case 'urgent':
      case 'legendary':
        return AndroidImportance.MAX;
      case 'high':
        return AndroidImportance.HIGH;
      case 'normal':
        return AndroidImportance.DEFAULT;
      case 'low':
        return AndroidImportance.LOW;
      default:
        return AndroidImportance.DEFAULT;
    }
  }

  private getNotificationColor(data: PushNotificationData): AndroidColor {
    if (data.is_legendary || data.priority === 'legendary') {
      return AndroidColor.YELLOW;
    }
    
    switch (data.type) {
      case 'success':
        return AndroidColor.GREEN;
      case 'warning':
        return AndroidColor.ORANGE;
      case 'error':
        return AndroidColor.RED;
      default:
        return AndroidColor.BLUE;
    }
  }

  private handleNotificationPress(notification: any): void {
    try {
      const data = JSON.parse(notification?.data?.notification_data || '{}');
      
      if (data.action_url) {
        // Navigate to specific screen or URL
        this.handleNotificationNavigation(data.action_url);
      }

      // Mark as read in Redux store
      store.dispatch(addNotification({
        id: data.id,
        title: data.title,
        message: data.body,
        type: data.type,
        priority: data.priority,
        timestamp: Date.now(),
        read: true
      }));

      // Special handling for legendary notifications
      if (data.is_legendary) {
        console.log('🎸 LEGENDARY NOTIFICATION PRESSED:', data.title);
        store.dispatch(addToastMessage({
          type: 'legendary',
          message: '🎸 Legendary notification activated! 🎸'
        }));
      }

    } catch (error) {
      console.error('🚨 Failed to handle notification press:', error);
    }
  }

  private handleNotificationAction(notification: any, actionId?: string): void {
    try {
      const data = JSON.parse(notification?.data?.notification_data || '{}');
      
      switch (actionId) {
        case 'view':
          if (data.action_url) {
            this.handleNotificationNavigation(data.action_url);
          }
          break;
        case 'legendary_action':
          console.log('🎸 LEGENDARY ACTION PRESSED! 🎸');
          store.dispatch(addToastMessage({
            type: 'legendary',
            message: '🎸 LEGENDARY ACTION ACTIVATED! Swiss precision engaged! 🎸'
          }));
          break;
      }
    } catch (error) {
      console.error('🚨 Failed to handle notification action:', error);
    }
  }

  private handleNotificationNavigation(actionUrl: string): void {
    try {
      // Handle deep links or navigation
      if (actionUrl.startsWith('http')) {
        Linking.openURL(actionUrl);
      } else {
        // Handle internal navigation
        // This would integrate with your navigation system
        console.log('📱 Navigate to:', actionUrl);
      }
    } catch (error) {
      console.error('🚨 Failed to handle navigation:', error);
    }
  }

  private handleNotificationOpened(message: FirebaseMessagingTypes.RemoteMessage): void {
    try {
      const data = this.parseMessageData(message);
      
      if (data.action_url) {
        // Delay navigation to allow app to fully load
        setTimeout(() => {
          this.handleNotificationNavigation(data.action_url!);
        }, 1000);
      }

      // Special handling for legendary notifications
      if (data.is_legendary) {
        console.log('🎸 APP OPENED FROM LEGENDARY NOTIFICATION! 🎸');
        setTimeout(() => {
          store.dispatch(addToastMessage({
            type: 'legendary',
            message: '🎸 Welcome back, legendary user! 🎸'
          }));
        }, 2000);
      }

    } catch (error) {
      console.error('🚨 Failed to handle notification opened:', error);
    }
  }

  private async showLegendaryWelcomeNotification(): Promise<void> {
    try {
      const welcomeData: PushNotificationData = {
        id: `legendary_welcome_${Date.now()}`,
        title: 'LEGENDARY MODE ACTIVATED',
        body: '🎸 Welcome back, RICKROLL187! Your legendary notifications are ready with Swiss precision! 🎸',
        type: 'legendary',
        priority: 'legendary',
        is_legendary: true,
        swiss_precision: true,
        rickroll187_special: true
      };

      await this.displayNotification(welcomeData);
    } catch (error) {
      console.error('🚨 Failed to show legendary welcome notification:', error);
    }
  }

  // Public API Methods
  public async sendLocalNotification(data: Partial<PushNotificationData>): Promise<void> {
    const notificationData: PushNotificationData = {
      id: `local_${Date.now()}`,
      title: 'Local Notification',
      body: '',
      type: 'info',
      priority: 'normal',
      ...data
    };

    await this.displayNotification(notificationData);
  }

  public async scheduleNotification(data: Partial<PushNotificationData>, scheduleTime: Date): Promise<void> {
    try {
      const notificationData: PushNotificationData = {
        id: `scheduled_${Date.now()}`,
        title: 'Scheduled Notification',
        body: '',
        type: 'info',
        priority: 'normal',
        ...data
      };

      const channelId = this.getChannelId(notificationData);

      await notifee.createTriggerNotification(
        {
          id: notificationData.id,
          title: notificationData.title,
          body: notificationData.body,
          android: {
            channelId,
            importance: this.getAndroidImportance(notificationData.priority),
            color: this.getNotificationColor(notificationData)
          }
        },
        {
          type: notifee.TriggerType.TIMESTAMP,
          timestamp: scheduleTime.getTime()
        }
      );

      console.log('⏰ Notification scheduled for:', scheduleTime);
    } catch (error) {
      console.error('🚨 Failed to schedule notification:', error);
    }
  }

  public async cancelNotification(notificationId: string): Promise<void> {
    try {
      await notifee.cancelNotification(notificationId);
      console.log('❌ Notification cancelled:', notificationId);
    } catch (error) {
      console.error('🚨 Failed to cancel notification:', error);
    }
  }

  public async clearAllNotifications(): Promise<void> {
    try {
      await notifee.cancelAllNotifications();
      console.log('🧹 All notifications cleared');
    } catch (error) {
      console.error('🚨 Failed to clear notifications:', error);
    }
  }

  public getFCMToken(): string | null {
    return this.fcmToken;
  }

  public async updateNotificationSettings(settings: Record<string, boolean>): Promise<void> {
    try {
      await AsyncStorage.setItem('notification_settings', JSON.stringify(settings));
      console.log('⚙️ Notification settings updated:', settings);
    } catch (error) {
      console.error('🚨 Failed to update notification settings:', error);
    }
  }

  public async getNotificationSettings(): Promise<Record<string, boolean>> {
    try {
      const settings = await AsyncStorage.getItem('notification_settings');
      return settings ? JSON.parse(settings) : {};
    } catch (error) {
      console.error('🚨 Failed to get notification settings:', error);
      return {};
    }
  }
}

// Create and export singleton instance
export const pushNotificationService = new LegendaryPushNotificationService();

// Export types
export type { PushNotificationData, NotificationChannel };

// Auto-initialize on import
pushNotificationService.initialize().catch(error => {
  console.error('🚨 Failed to auto-initialize push notifications:', error);
});

// Legendary startup message
if (__DEV__) {
  console.log('🎸🎸🎸 LEGENDARY PUSH NOTIFICATION SERVICE READY! 🎸🎸🎸');
  console.log('Professional mobile notifications with Swiss precision!');
  console.log('Special RICKROLL187 legendary notifications included!');
  console.log('Built with maximum code bro energy!');
  console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
  console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
}
