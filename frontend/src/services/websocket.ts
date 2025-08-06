// File: frontend/src/services/websocket.ts
/**
 * 🔌🎸 N3EXTPATH - LEGENDARY WEBSOCKET CLIENT 🎸🔌
 * Professional real-time communication with Swiss precision
 * Built: 2025-08-05 18:25:28 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { store } from '../store/store';
import { addNotification, addToastMessage } from '../store/store';

// WebSocket Message Types
export enum WSMessageType {
  // Authentication
  AUTH = 'auth',
  AUTH_SUCCESS = 'auth_success',
  AUTH_FAILED = 'auth_failed',
  
  // Notifications
  NOTIFICATION = 'notification',
  SYSTEM_ALERT = 'system_alert',
  LEGENDARY_ANNOUNCEMENT = 'legendary_announcement',
  
  // Performance Updates
  PERFORMANCE_UPDATE = 'performance_update',
  OKR_UPDATE = 'okr_update',
  REVIEW_COMPLETED = 'review_completed',
  
  // Team Activity
  TEAM_UPDATE = 'team_update',
  USER_STATUS = 'user_status',
  TYPING_INDICATOR = 'typing_indicator',
  
  // System Events
  SYSTEM_MAINTENANCE = 'system_maintenance',
  LEGENDARY_EVENT = 'legendary_event',
  SWISS_PRECISION_ALERT = 'swiss_precision_alert',
  
  // Connection Management
  PING = 'ping',
  PONG = 'pong',
  HEARTBEAT = 'heartbeat',
  
  // Error Handling
  ERROR = 'error',
  RECONNECT = 'reconnect'
}

export interface WSMessage {
  type: WSMessageType;
  data?: any;
  timestamp?: number;
  user_id?: string;
  is_legendary?: boolean;
  swiss_precision?: boolean;
}

export interface NotificationData {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error' | 'legendary';
  priority: 'low' | 'normal' | 'high' | 'urgent' | 'legendary';
  action_url?: string;
  expires_at?: string;
}

export interface PerformanceUpdateData {
  user_id: string;
  review_id: string;
  score: number;
  status: string;
  updated_by: string;
  is_legendary?: boolean;
}

export interface OKRUpdateData {
  okr_id: string;
  user_id: string;
  title: string;
  progress: number;
  status: string;
  updated_by: string;
  is_legendary?: boolean;
}

export interface LegendaryEventData {
  event_type: string;
  message: string;
  rickroll187_action?: boolean;
  swiss_precision_level?: number;
  code_bro_energy?: string;
}

class LegendaryWebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 10;
  private reconnectDelay: number = 1000;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private isConnecting: boolean = false;
  private messageQueue: WSMessage[] = [];
  private eventListeners: Map<WSMessageType, Function[]> = new Map();
  private connectionState: 'connecting' | 'connected' | 'disconnected' | 'error' = 'disconnected';

  constructor() {
    this.url = this.getWebSocketURL();
    this.setupEventListeners();
    
    // Legendary startup message
    if (process.env.NODE_ENV === 'development') {
      console.log('🎸 LEGENDARY WEBSOCKET CLIENT INITIALIZED! 🎸');
      console.log(`WebSocket URL: ${this.url}`);
      console.log('Built with Swiss precision by RICKROLL187!');
    }
  }

  private getWebSocketURL(): string {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const baseURL = process.env.REACT_APP_WS_URL || 
                   process.env.REACT_APP_API_URL?.replace('http', 'ws') || 
                   `${protocol}//${window.location.host}`;
    
    return `${baseURL}/ws`;
  }

  private setupEventListeners(): void {
    // Set up default event listeners
    this.addEventListener(WSMessageType.NOTIFICATION, this.handleNotification.bind(this));
    this.addEventListener(WSMessageType.LEGENDARY_ANNOUNCEMENT, this.handleLegendaryAnnouncement.bind(this));
    this.addEventListener(WSMessageType.PERFORMANCE_UPDATE, this.handlePerformanceUpdate.bind(this));
    this.addEventListener(WSMessageType.OKR_UPDATE, this.handleOKRUpdate.bind(this));
    this.addEventListener(WSMessageType.LEGENDARY_EVENT, this.handleLegendaryEvent.bind(this));
    this.addEventListener(WSMessageType.SYSTEM_ALERT, this.handleSystemAlert.bind(this));
    this.addEventListener(WSMessageType.SWISS_PRECISION_ALERT, this.handleSwissPrecisionAlert.bind(this));
  }

  public connect(token?: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        resolve();
        return;
      }

      if (this.isConnecting) {
        reject(new Error('Connection already in progress'));
        return;
      }

      this.isConnecting = true;
      this.connectionState = 'connecting';

      try {
        // Add authentication token to URL if provided
        const wsURL = token ? `${this.url}?token=${token}` : this.url;
        
        // Add legendary headers for legendary users
        const user = store.getState().auth.user;
        const isLegendary = user?.is_legendary || false;
        
        this.ws = new WebSocket(wsURL);

        this.ws.onopen = (event) => {
          console.log('🎸 WebSocket connected successfully! 🎸');
          this.isConnecting = false;
          this.connectionState = 'connected';
          this.reconnectAttempts = 0;
          
          // Authenticate if token provided
          if (token) {
            this.authenticate(token, isLegendary);
          }
          
          // Start heartbeat
          this.startHeartbeat();
          
          // Send queued messages
          this.sendQueuedMessages();
          
          // Show legendary connection message for legendary users
          if (isLegendary) {
            store.dispatch(addToastMessage({
              type: 'legendary',
              message: '🎸 LEGENDARY REAL-TIME CONNECTION ESTABLISHED! 🎸'
            }));
          }
          
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: WSMessage = JSON.parse(event.data);
            this.handleMessage(message);
          } catch (error) {
            console.error('🚨 Failed to parse WebSocket message:', error);
          }
        };

        this.ws.onclose = (event) => {
          console.log('WebSocket connection closed:', event.code, event.reason);
          this.isConnecting = false;
          this.connectionState = 'disconnected';
          this.stopHeartbeat();
          
          // Attempt to reconnect if not a clean close
          if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.scheduleReconnect();
          }
        };

        this.ws.onerror = (error) => {
          console.error('🚨 WebSocket error:', error);
          this.isConnecting = false;
          this.connectionState = 'error';
          
          // Show error message
          store.dispatch(addToastMessage({
            type: 'error',
            message: 'Connection error. Attempting to reconnect...'
          }));
          
          reject(error);
        };

      } catch (error) {
        this.isConnecting = false;
        this.connectionState = 'error';
        reject(error);
      }
    });
  }

  public disconnect(): void {
    if (this.ws) {
      this.stopHeartbeat();
      this.ws.close(1000, 'Client disconnect');
      this.ws = null;
      this.connectionState = 'disconnected';
      
      console.log('🎸 WebSocket disconnected by client 🎸');
    }
  }

  private authenticate(token: string, isLegendary: boolean = false): void {
    const authMessage: WSMessage = {
      type: WSMessageType.AUTH,
      data: {
        token,
        is_legendary: isLegendary,
        swiss_precision: true,
        client_info: {
          user_agent: navigator.userAgent,
          timestamp: Date.now(),
          legendary_status: isLegendary ? 'maximum' : 'standard'
        }
      },
      timestamp: Date.now()
    };

    this.send(authMessage);
  }

  private scheduleReconnect(): void {
    const delay = Math.min(this.reconnectDelay * Math.pow(2, this.reconnectAttempts), 30000);
    
    console.log(`🔄 Scheduling reconnect attempt ${this.reconnectAttempts + 1} in ${delay}ms`);
    
    setTimeout(() => {
      this.reconnectAttempts++;
      this.connect();
    }, delay);
  }

  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.send({
          type: WSMessageType.PING,
          timestamp: Date.now()
        });
      }
    }, 30000); // 30 seconds
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  public send(message: WSMessage): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      // Add metadata to message
      const enrichedMessage: WSMessage = {
        ...message,
        timestamp: message.timestamp || Date.now(),
        user_id: store.getState().auth.user?.user_id,
        is_legendary: store.getState().auth.legendary_status
      };

      this.ws.send(JSON.stringify(enrichedMessage));
      
      // Log legendary messages
      if (enrichedMessage.is_legendary && process.env.NODE_ENV === 'development') {
        console.log('🎸 LEGENDARY MESSAGE SENT:', enrichedMessage);
      }
    } else {
      // Queue message for later sending
      this.messageQueue.push(message);
      
      if (this.messageQueue.length > 100) {
        // Remove oldest messages if queue gets too large
        this.messageQueue = this.messageQueue.slice(-50);
      }
    }
  }

  private sendQueuedMessages(): void {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      if (message) {
        this.send(message);
      }
    }
  }

  private handleMessage(message: WSMessage): void {
    // Log all messages in development
    if (process.env.NODE_ENV === 'development') {
      console.log('📨 WebSocket message received:', message);
    }

    // Special handling for legendary messages
    if (message.is_legendary) {
      console.log('🎸 LEGENDARY MESSAGE RECEIVED:', message);
    }

    // Handle specific message types
    switch (message.type) {
      case WSMessageType.AUTH_SUCCESS:
        console.log('✅ WebSocket authentication successful');
        if (message.is_legendary) {
          console.log('🎸 LEGENDARY AUTHENTICATION CONFIRMED! 🎸');
        }
        break;

      case WSMessageType.AUTH_FAILED:
        console.error('🚨 WebSocket authentication failed');
        this.disconnect();
        break;

      case WSMessageType.PONG:
        // Heartbeat response - connection is alive
        break;

      case WSMessageType.ERROR:
        console.error('🚨 WebSocket server error:', message.data);
        store.dispatch(addToastMessage({
          type: 'error',
          message: `Server error: ${message.data?.message || 'Unknown error'}`
        }));
        break;

      default:
        // Dispatch to registered event listeners
        this.dispatchToListeners(message.type, message.data);
        break;
    }
  }

  private dispatchToListeners(type: WSMessageType, data: any): void {
    const listeners = this.eventListeners.get(type);
    if (listeners) {
      listeners.forEach(listener => {
        try {
          listener(data);
        } catch (error) {
          console.error(`🚨 Error in WebSocket event listener for ${type}:`, error);
        }
      });
    }
  }

  public addEventListener(type: WSMessageType, listener: Function): void {
    if (!this.eventListeners.has(type)) {
      this.eventListeners.set(type, []);
    }
    this.eventListeners.get(type)!.push(listener);
  }

  public removeEventListener(type: WSMessageType, listener: Function): void {
    const listeners = this.eventListeners.get(type);
    if (listeners) {
      const index = listeners.indexOf(listener);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  // Event Handlers
  private handleNotification(data: NotificationData): void {
    // Add to Redux store
    store.dispatch(addNotification({
      id: data.id,
      title: data.title,
      message: data.message,
      type: data.type,
      priority: data.priority,
      action_url: data.action_url,
      timestamp: Date.now(),
      read: false
    }));

    // Show toast for high priority notifications
    if (data.priority === 'high' || data.priority === 'urgent' || data.priority === 'legendary') {
      store.dispatch(addToastMessage({
        type: data.type === 'legendary' ? 'legendary' : data.type,
        message: data.message
      }));
    }
  }

  private handleLegendaryAnnouncement(data: any): void {
    console.log('🎸 LEGENDARY ANNOUNCEMENT:', data);
    
    store.dispatch(addToastMessage({
      type: 'legendary',
      message: `🎸 ${data.message} 🎸`
    }));

    store.dispatch(addNotification({
      id: `legendary_${Date.now()}`,
      title: '🎸 Legendary Announcement 🎸',
      message: data.message,
      type: 'legendary',
      priority: 'legendary',
      timestamp: Date.now(),
      read: false
    }));
  }

  private handlePerformanceUpdate(data: PerformanceUpdateData): void {
    console.log('📈 Performance update received:', data);
    
    // Show notification if it's for current user or legendary
    const currentUser = store.getState().auth.user;
    if (data.user_id === currentUser?.user_id || data.is_legendary || currentUser?.is_legendary) {
      const message = data.is_legendary ? 
        `🎸 LEGENDARY performance review updated: Score ${data.score}/5.0 🎸` :
        `Your performance review has been updated: Score ${data.score}/5.0`;
      
      store.dispatch(addToastMessage({
        type: data.is_legendary ? 'legendary' : 'info',
        message
      }));
    }
  }

  private handleOKRUpdate(data: OKRUpdateData): void {
    console.log('🎯 OKR update received:', data);
    
    // Show notification if it's for current user or legendary
    const currentUser = store.getState().auth.user;
    if (data.user_id === currentUser?.user_id || data.is_legendary || currentUser?.is_legendary) {
      const message = data.is_legendary ?
        `🎸 LEGENDARY OKR "${data.title}" progress: ${data.progress}% 🎸` :
        `OKR "${data.title}" updated: ${data.progress}% complete`;
      
      store.dispatch(addToastMessage({
        type: data.is_legendary ? 'legendary' : 'info',
        message
      }));
    }
  }

  private handleLegendaryEvent(data: LegendaryEventData): void {
    console.log('🎸 LEGENDARY EVENT:', data);
    
    let message = data.message;
    if (data.rickroll187_action) {
      message = `🎸 RICKROLL187 ACTION: ${message} 🎸`;
    }
    
    if (data.swiss_precision_level) {
      message += ` (Swiss Precision: ${data.swiss_precision_level}%)`;
    }
    
    if (data.code_bro_energy) {
      message += ` (Code Bro Energy: ${data.code_bro_energy})`;
    }

    store.dispatch(addToastMessage({
      type: 'legendary',
      message
    }));

    store.dispatch(addNotification({
      id: `legendary_event_${Date.now()}`,
      title: '🎸 Legendary Event 🎸',
      message: data.message,
      type: 'legendary',
      priority: 'legendary',
      timestamp: Date.now(),
      read: false
    }));
  }

  private handleSystemAlert(data: any): void {
    console.log('🚨 System alert:', data);
    
    store.dispatch(addToastMessage({
      type: data.severity === 'critical' ? 'error' : 'warning',
      message: data.message
    }));
  }

  private handleSwissPrecisionAlert(data: any): void {
    console.log('⚡ Swiss Precision Alert:', data);
    
    store.dispatch(addToastMessage({
      type: 'info',
      message: `⚡ Swiss Precision: ${data.message} ⚡`
    }));
  }

  // Public API Methods
  public sendNotification(recipientId: string, notification: Partial<NotificationData>): void {
    this.send({
      type: WSMessageType.NOTIFICATION,
      data: {
        recipient_id: recipientId,
        ...notification
      }
    });
  }

  public sendTypingIndicator(channelId: string, isTyping: boolean): void {
    this.send({
      type: WSMessageType.TYPING_INDICATOR,
      data: {
        channel_id: channelId,
        is_typing: isTyping
      }
    });
  }

  public sendLegendaryEvent(eventData: Partial<LegendaryEventData>): void {
    this.send({
      type: WSMessageType.LEGENDARY_EVENT,
      data: eventData,
      is_legendary: true,
      swiss_precision: true
    });
  }

  public getConnectionState(): string {
    return this.connectionState;
  }

  public isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  public getReconnectAttempts(): number {
    return this.reconnectAttempts;
  }
}

// Create singleton instance
export const wsClient = new LegendaryWebSocketClient();

// Export types and client
export type {
  WSMessage,
  NotificationData,
  PerformanceUpdateData,
  OKRUpdateData,
  LegendaryEventData
};

// Auto-connect when authenticated
if (typeof window !== 'undefined') {
  const checkAuthAndConnect = () => {
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      try {
        const userData = JSON.parse(user);
        wsClient.connect(token).catch(error => {
          console.error('🚨 Failed to connect WebSocket:', error);
        });
        
        // Special connection message for legendary users
        if (userData.is_legendary) {
          setTimeout(() => {
            console.log('🎸 LEGENDARY WEBSOCKET CLIENT READY FOR RICKROLL187! 🎸');
          }, 1000);
        }
      } catch (error) {
        console.error('🚨 Failed to parse user data:', error);
      }
    }
  };

  // Check on load
  checkAuthAndConnect();

  // Listen for storage changes (login/logout in other tabs)
  window.addEventListener('storage', (event) => {
    if (event.key === 'access_token') {
      if (event.newValue) {
        checkAuthAndConnect();
      } else {
        wsClient.disconnect();
      }
    }
  });
}

// Legendary startup message
if (process.env.NODE_ENV === 'development') {
  console.log('🎸🎸🎸 LEGENDARY WEBSOCKET CLIENT READY! 🎸🎸🎸');
  console.log('Real-time communication with Swiss precision!');
  console.log('Built by RICKROLL187 with maximum code bro energy!');
  console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
  console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
}
