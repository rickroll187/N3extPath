// File: web/src/services/websocketService.ts
/**
 * 🔌🎸 N3EXTPATH - LEGENDARY WEBSOCKET SERVICE 🎸🔌
 * Professional real-time communication with Swiss precision
 * Built: 2025-08-06 15:16:23 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { store } from '@/store';
import { 
  setConnectionStatus, 
  incrementConnectionRetries,
  resetConnectionRetries 
} from '@/store/slices/notificationsSlice';
import { 
  setFounderMode,
  activateLegendaryMode,
  showLegendaryToast,
  incrementCodeBroEnergy
} from '@/store/slices/uiSlice';
import { 
  activateFounderMode as activatePerformanceFounderMode,
  unlockAchievement,
  addXP
} from '@/store/slices/performanceSlice';
import { 
  activateFounderOKRs,
  boostCodeBroEnergy
} from '@/store/slices/okrSlice';
import { 
  activateFounderTeams,
  addTeamActivity,
  boostTeamEnergy
} from '@/store/slices/teamsSlice';
import { createNotification } from '@/store/slices/notificationsSlice';
import toast from 'react-hot-toast';

// =====================================
// 🔌 WEBSOCKET TYPES 🔌
// =====================================

export interface WebSocketMessage {
  id: string;
  type: 'notification' | 'achievement' | 'team_update' | 'okr_update' | 'performance_update' | 'founder_alert' | 'legendary_event' | 'system_message';
  subtype?: string;
  userId: string;
  data: any;
  timestamp: Date;
  priority: 'low' | 'normal' | 'high' | 'urgent' | 'legendary' | 'founder';
  isFounderMessage?: boolean;
  legendaryLevel?: number;
  codeBroEnergy?: number;
}

export interface WebSocketConfig {
  url: string;
  maxReconnectAttempts: number;
  reconnectInterval: number;
  heartbeatInterval: number;
  connectionTimeout: number;
  protocols?: string[];
  founderMode?: boolean;
  legendaryFeatures?: boolean;
}

export interface ConnectionStats {
  isConnected: boolean;
  connectionAttempts: number;
  lastConnected: Date | null;
  lastDisconnected: Date | null;
  lastHeartbeat: Date | null;
  messagesReceived: number;
  messagesSent: number;
  founderMessagesReceived: number;
  legendaryEventsReceived: number;
  uptime: number;
}

// =====================================
// 🎸 LEGENDARY WEBSOCKET SERVICE 🎸
// =====================================

class LegendaryWebSocketService {
  private socket: WebSocket | null = null;
  private config: WebSocketConfig;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private connectionTimer: NodeJS.Timeout | null = null;
  
  // State management
  private isConnecting: boolean = false;
  private shouldReconnect: boolean = true;
  private messageQueue: WebSocketMessage[] = [];
  
  // Statistics
  private stats: ConnectionStats = {
    isConnected: false,
    connectionAttempts: 0,
    lastConnected: null,
    lastDisconnected: null,
    lastHeartbeat: null,
    messagesReceived: 0,
    messagesSent: 0,
    founderMessagesReceived: 0,
    legendaryEventsReceived: 0,
    uptime: 0,
  };
  
  // Event listeners
  private messageHandlers: Map<string, ((message: WebSocketMessage) => void)[]> = new Map();
  private connectionHandlers: ((connected: boolean) => void)[] = [];
  
  constructor(config: Partial<WebSocketConfig> = {}) {
    console.log('🔌🎸🔌 LEGENDARY WEBSOCKET SERVICE INITIALIZING! 🔌🎸🔌');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`WebSocket service initialized at: 2025-08-06 15:16:23 UTC`);
    
    // Default configuration with Swiss precision
    this.config = {
      url: process.env.REACT_APP_WS_URL || 'ws://localhost:8080/ws',
      maxReconnectAttempts: 10,
      reconnectInterval: 3000, // 3 seconds
      heartbeatInterval: 30000, // 30 seconds
      connectionTimeout: 10000, // 10 seconds
      protocols: ['n3extpath-protocol'],
      founderMode: false,
      legendaryFeatures: true,
      ...config,
    };
    
    // Check if this is RICKROLL187 founder
    const state = store.getState();
    const isFounder = state.auth?.user?.email === 'letstalktech010@gmail.com' || 
                     state.auth?.user?.username === 'rickroll187';
    
    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER WEBSOCKET DETECTED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER WEBSOCKET WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER WEBSOCKET SYSTEM!');
      console.log('🌅 AFTERNOON FOUNDER WEBSOCKET POWER AT 15:16:23!');
      
      this.config.founderMode = true;
      this.config.maxReconnectAttempts = 999; // Infinite for founder
      this.config.reconnectInterval = 1000; // Faster reconnection
      this.config.protocols = ['n3extpath-founder-protocol'];
    }
    
    // Set up default message handlers
    this.setupDefaultHandlers();
    
    // Auto-connect if in browser environment
    if (typeof window !== 'undefined') {
      this.connect();
    }
  }
  
  // =====================================
  // 🔌 CONNECTION MANAGEMENT 🔌
  // =====================================
  
  public connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        console.log('🔌 WebSocket already connected');
        resolve();
        return;
      }
      
      if (this.isConnecting) {
        console.log('🔌 WebSocket connection already in progress');
        resolve();
        return;
      }
      
      this.isConnecting = true;
      this.stats.connectionAttempts++;
      
      console.log(`🔌 Connecting to legendary WebSocket: ${this.config.url}`);
      console.log(`🔌 Connection attempt #${this.stats.connectionAttempts}`);
      
      try {
        // Create WebSocket connection with Swiss precision
        this.socket = new WebSocket(this.config.url, this.config.protocols);
        
        // Connection timeout
        this.connectionTimer = setTimeout(() => {
          if (this.socket && this.socket.readyState === WebSocket.CONNECTING) {
            console.log('⏰ WebSocket connection timeout');
            this.socket.close();
            reject(new Error('Connection timeout'));
          }
        }, this.config.connectionTimeout);
        
        // =====================================
        // 🎸 WEBSOCKET EVENT HANDLERS 🎸
        // =====================================
        
        this.socket.onopen = (event) => {
          this.isConnecting = false;
          this.stats.isConnected = true;
          this.stats.lastConnected = new Date();
          
          // Clear connection timer
          if (this.connectionTimer) {
            clearTimeout(this.connectionTimer);
            this.connectionTimer = null;
          }
          
          // Reset reconnection attempts
          store.dispatch(resetConnectionRetries());
          
          // Update connection status in store
          store.dispatch(setConnectionStatus(true));
          
          console.log('✅ WebSocket connected successfully!');
          console.log('🔌 Protocol:', this.socket?.protocol);
          
          if (this.config.founderMode) {
            console.log('👑 FOUNDER WEBSOCKET CONNECTION ESTABLISHED!');
            console.log('🎸 Infinite code bro energy websocket active!');
            
            // Activate founder modes across all slices
            store.dispatch(setFounderMode(true));
            store.dispatch(activatePerformanceFounderMode());
            store.dispatch(activateFounderOKRs());
            store.dispatch(activateFounderTeams());
            
            // Show founder connection toast
            toast.success('👑 RICKROLL187 FOUNDER WEBSOCKET CONNECTED! Infinite code bro energy activated!', {
              duration: 5000,
              style: {
                background: 'linear-gradient(135deg, #FFD700, #FFA500)',
                color: '#000000',
                fontWeight: '700',
              },
            });
          } else {
            // Regular user connection
            console.log('🎸 Code bro WebSocket connection established!');
            
            toast.success('🔌 Connected to N3EXTPATH real-time updates! Code bro energy flowing!', {
              duration: 3000,
            });
          }
          
          // Start heartbeat
          this.startHeartbeat();
          
          // Send queued messages
          this.sendQueuedMessages();
          
          // Notify connection handlers
          this.connectionHandlers.forEach(handler => handler(true));
          
          resolve();
        };
        
        this.socket.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            message.timestamp = new Date(message.timestamp);
            
            this.stats.messagesReceived++;
            
            // Track founder and legendary messages
            if (message.isFounderMessage) {
              this.stats.founderMessagesReceived++;
            }
            if (message.legendaryLevel && message.legendaryLevel >= 5) {
              this.stats.legendaryEventsReceived++;
            }
            
            console.log('📨 WebSocket message received:', message.type, message.subtype);
            
            // Handle the message
            this.handleMessage(message);
            
          } catch (error) {
            console.error('🚨 WebSocket message parsing error:', error);
          }
        };
        
        this.socket.onclose = (event) => {
          this.isConnecting = false;
          this.stats.isConnected = false;
          this.stats.lastDisconnected = new Date();
          
          // Clear timers
          if (this.connectionTimer) {
            clearTimeout(this.connectionTimer);
            this.connectionTimer = null;
          }
          this.stopHeartbeat();
          
          // Update connection status in store
          store.dispatch(setConnectionStatus(false));
          
          console.log(`🔌 WebSocket disconnected - Code: ${event.code}, Reason: ${event.reason}`);
          
          // Notify connection handlers
          this.connectionHandlers.forEach(handler => handler(false));
          
          // Handle reconnection
          if (this.shouldReconnect && this.stats.connectionAttempts < this.config.maxReconnectAttempts) {
            console.log(`🔄 Scheduling reconnection in ${this.config.reconnectInterval}ms...`);
            
            this.reconnectTimer = setTimeout(() => {
              store.dispatch(incrementConnectionRetries());
              this.connect().catch(error => {
                console.error('🚨 Reconnection failed:', error);
              });
            }, this.config.reconnectInterval);
          } else if (this.stats.connectionAttempts >= this.config.maxReconnectAttempts) {
            console.log('🚨 Max reconnection attempts reached');
            
            toast.error('🚨 WebSocket connection lost. Please refresh the page.', {
              duration: 0, // Persistent
            });
          }
          
          if (event.code !== 1000) {
            reject(new Error(`WebSocket closed with code ${event.code}: ${event.reason}`));
          }
        };
        
        this.socket.onerror = (error) => {
          console.error('🚨 WebSocket error:', error);
          this.isConnecting = false;
          
          // Clear connection timer
          if (this.connectionTimer) {
            clearTimeout(this.connectionTimer);
            this.connectionTimer = null;
          }
          
          reject(error);
        };
        
      } catch (error) {
        this.isConnecting = false;
        console.error('🚨 WebSocket connection error:', error);
        reject(error);
      }
    });
  }
  
  public disconnect(): void {
    console.log('🔌 Disconnecting WebSocket...');
    
    this.shouldReconnect = false;
    
    // Clear all timers
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.connectionTimer) {
      clearTimeout(this.connectionTimer);
      this.connectionTimer = null;
    }
    this.stopHeartbeat();
    
    // Close socket
    if (this.socket) {
      this.socket.close(1000, 'Client disconnect');
      this.socket = null;
    }
    
    // Update store
    store.dispatch(setConnectionStatus(false));
    
    console.log('✅ WebSocket disconnected');
  }
  
  public reconnect(): void {
    console.log('🔄 Manual WebSocket reconnection...');
    
    this.disconnect();
    
    setTimeout(() => {
      this.shouldReconnect = true;
      this.connect().catch(error => {
        console.error('🚨 Manual reconnection failed:', error);
      });
    }, 1000);
  }
  
  // =====================================
  // 💓 HEARTBEAT MANAGEMENT 💓
  // =====================================
  
  private startHeartbeat(): void {
    this.stopHeartbeat(); // Clear any existing heartbeat
    
    this.heartbeatTimer = setInterval(() => {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const heartbeat = {
          type: 'heartbeat',
          timestamp: new Date().toISOString(),
          founderMode: this.config.founderMode,
        };
        
        this.socket.send(JSON.stringify(heartbeat));
        this.stats.lastHeartbeat = new Date();
        this.stats.messagesSent++;
        
        // Update uptime
        if (this.stats.lastConnected) {
          this.stats.uptime = Date.now() - this.stats.lastConnected.getTime();
        }
        
        console.log('💓 WebSocket heartbeat sent');
      }
    }, this.config.heartbeatInterval);
  }
  
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }
  
  // =====================================
  // 📨 MESSAGE HANDLING 📨
  // =====================================
  
  private handleMessage(message: WebSocketMessage): void {
    console.log(`📨 Handling ${message.type} message:`, message);
    
    // Handle different message types with Swiss precision
    switch (message.type) {
      case 'notification':
        this.handleNotificationMessage(message);
        break;
        
      case 'achievement':
        this.handleAchievementMessage(message);
        break;
        
      case 'team_update':
        this.handleTeamUpdateMessage(message);
        break;
        
      case 'okr_update':
        this.handleOKRUpdateMessage(message);
        break;
        
      case 'performance_update':
        this.handlePerformanceUpdateMessage(message);
        break;
        
      case 'founder_alert':
        this.handleFounderAlertMessage(message);
        break;
        
      case 'legendary_event':
        this.handleLegendaryEventMessage(message);
        break;
        
      case 'system_message':
        this.handleSystemMessage(message);
        break;
        
      default:
        console.log('📨 Unknown message type:', message.type);
    }
    
    // Call registered message handlers
    const handlers = this.messageHandlers.get(message.type) || [];
    handlers.forEach(handler => {
      try {
        handler(message);
      } catch (error) {
        console.error('🚨 Message handler error:', error);
      }
    });
    
    // Call generic message handlers
    const genericHandlers = this.messageHandlers.get('*') || [];
    genericHandlers.forEach(handler => {
      try {
        handler(message);
      } catch (error) {
        console.error('🚨 Generic message handler error:', error);
      }
    });
  }
  
  private handleNotificationMessage(message: WebSocketMessage): void {
    console.log('🔔 Handling notification message');
    
    // Create notification in store
    store.dispatch(createNotification({
      type: message.data.type || 'system',
      category: message.data.category || 'info',
      priority: message.priority,
      title: message.data.title,
      message: message.data.message,
      description: message.data.description,
      icon: message.data.icon || '📢',
      color: message.data.color,
      userId: message.userId,
      sourceId: message.data.sourceId,
      sourceType: message.data.sourceType,
      isRead: false,
      isArchived: false,
      isPinned: message.priority === 'legendary' || message.priority === 'founder',
      actions: message.data.actions,
      isFounderNotification: message.isFounderMessage,
      legendaryLevel: message.legendaryLevel,
      codeBroEnergy: message.codeBroEnergy,
      imageUrl: message.data.imageUrl,
      linkUrl: message.data.linkUrl,
      data: message.data.metadata,
    }));
    
    // Show toast for high priority notifications
    if (message.priority === 'urgent' || message.priority === 'legendary' || message.priority === 'founder') {
      if (message.isFounderMessage) {
        toast.success(`👑 ${message.data.title}`, {
          duration: 6000,
          style: {
            background: 'linear-gradient(135deg, #FFD700, #FFA500)',
            color: '#000000',
            fontWeight: '700',
          },
        });
      } else if (message.priority === 'legendary') {
        toast.success(`🎸 ${message.data.title}`, {
          duration: 5000,
          style: {
            background: 'linear-gradient(135deg, #8B5CF6, #3B82F6)',
            color: '#FFFFFF',
            fontWeight: '600',
          },
        });
      } else {
        toast.success(message.data.title, { duration: 4000 });
      }
    }
  }
  
  private handleAchievementMessage(message: WebSocketMessage): void {
    console.log('🏆 Handling achievement message');
    
    // Unlock achievement in performance slice
    store.dispatch(unlockAchievement({
      id: message.data.id,
      title: message.data.title,
      description: message.data.description,
      category: message.data.category,
      icon: message.data.icon,
      rarity: message.data.rarity,
      xpReward: message.data.xpReward,
      unlockedAt: new Date(),
      requirements: message.data.requirements || [],
    }));
    
    // Show achievement toast with legendary styling
    if (message.data.rarity === 'founder') {
      toast.success(`👑 LEGENDARY FOUNDER ACHIEVEMENT: ${message.data.title}!`, {
        duration: 8000,
        style: {
          background: 'linear-gradient(135deg, #FFD700, #FFA500)',
          color: '#000000',
          fontWeight: '700',
        },
      });
    } else if (message.data.rarity === 'legendary') {
      toast.success(`🎸 LEGENDARY ACHIEVEMENT: ${message.data.title}!`, {
        duration: 6000,
        style: {
          background: 'linear-gradient(135deg, #8B5CF6, #3B82F6)',
          color: '#FFFFFF',
          fontWeight: '600',
        },
      });
    } else {
      toast.success(`🏆 Achievement Unlocked: ${message.data.title}!`, { duration: 5000 });
    }
    
    // Boost code bro energy for achievements
    if (message.codeBroEnergy) {
      store.dispatch(incrementCodeBroEnergy(message.codeBroEnergy));
    }
  }
  
  private handleTeamUpdateMessage(message: WebSocketMessage): void {
    console.log('👥 Handling team update message');
    
    // Add team activity
    store.dispatch(addTeamActivity({
      teamId: message.data.teamId,
      type: message.data.activityType,
      title: message.data.title,
      description: message.data.description,
      actor: message.data.actor,
      target: message.data.target,
      metadata: message.data.metadata,
    }));
    
    // Boost team energy for positive events
    if (message.data.energyBoost) {
      store.dispatch(boostTeamEnergy({
        teamId: message.data.teamId,
        boost: message.data.energyBoost,
      }));
    }
  }
  
  private handleOKRUpdateMessage(message: WebSocketMessage): void {
    console.log('🎯 Handling OKR update message');
    
    // Boost OKR code bro energy
    if (message.data.objectiveId && message.codeBroEnergy) {
      store.dispatch(boostCodeBroEnergy({
        objectiveId: message.data.objectiveId,
        boost: message.codeBroEnergy,
      }));
    }
  }
  
  private handlePerformanceUpdateMessage(message: WebSocketMessage): void {
    console.log('📊 Handling performance update message');
    
    // Add XP if provided
    if (message.data.xpReward) {
      store.dispatch(addXP(message.data.xpReward));
    }
  }
  
  private handleFounderAlertMessage(message: WebSocketMessage): void {
    console.log('👑 Handling founder alert message');
    
    if (this.config.founderMode) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER ALERT RECEIVED! 👑🎸👑');
      
      // Show legendary founder toast
      store.dispatch(showLegendaryToast({
        title: `👑 FOUNDER ALERT: ${message.data.title}`,
        message: message.data.message,
        isFounder: true,
      }));
      
      // Activate legendary mode for special alerts
      if (message.priority === 'legendary') {
        store.dispatch(activateLegendaryMode());
      }
    }
  }
  
  private handleLegendaryEventMessage(message: WebSocketMessage): void {
    console.log('🎸 Handling legendary event message');
    
    // Show legendary toast
    store.dispatch(showLegendaryToast({
      title: `🎸 LEGENDARY EVENT: ${message.data.title}`,
      message: message.data.message,
      isFounder: message.isFounderMessage,
    }));
    
    // Boost code bro energy for legendary events
    if (message.codeBroEnergy) {
      store.dispatch(incrementCodeBroEnergy(message.codeBroEnergy));
    }
  }
  
  private handleSystemMessage(message: WebSocketMessage): void {
    console.log('⚙️ Handling system message');
    
    // Handle system-level messages
    if (message.subtype === 'maintenance') {
      toast.info(`⚙️ System Maintenance: ${message.data.message}`, {
        duration: 8000,
      });
    } else if (message.subtype === 'update') {
      toast.success(`🚀 System Update: ${message.data.message}`, {
        duration: 6000,
      });
    }
  }
  
  // =====================================
  // 📤 MESSAGE SENDING 📤
  // =====================================
  
  public sendMessage(message: Partial<WebSocketMessage>): boolean {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.log('📤 WebSocket not connected, queuing message');
      this.messageQueue.push(message as WebSocketMessage);
      return false;
    }
    
    try {
      const fullMessage: WebSocketMessage = {
        id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        userId: store.getState().auth?.user?.id || 'anonymous',
        timestamp: new Date(),
        priority: 'normal',
        ...message,
      } as WebSocketMessage;
      
      this.socket.send(JSON.stringify(fullMessage));
      this.stats.messagesSent++;
      
      console.log('📤 WebSocket message sent:', fullMessage.type);
      return true;
      
    } catch (error) {
      console.error('🚨 WebSocket send error:', error);
      return false;
    }
  }
  
  private sendQueuedMessages(): void {
    if (this.messageQueue.length === 0) return;
    
    console.log(`📤 Sending ${this.messageQueue.length} queued messages`);
    
    const messages = [...this.messageQueue];
    this.messageQueue = [];
    
    messages.forEach(message => {
      this.sendMessage(message);
    });
  }
  
  // =====================================
  // 🎧 EVENT LISTENERS 🎧
  // =====================================
  
  public onMessage(messageType: string, handler: (message: WebSocketMessage) => void): void {
    if (!this.messageHandlers.has(messageType)) {
      this.messageHandlers.set(messageType, []);
    }
    
    this.messageHandlers.get(messageType)!.push(handler);
    console.log(`🎧 Message handler registered for: ${messageType}`);
  }
  
  public offMessage(messageType: string, handler: (message: WebSocketMessage) => void): void {
    const handlers = this.messageHandlers.get(messageType);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index !== -1) {
        handlers.splice(index, 1);
        console.log(`🎧 Message handler removed for: ${messageType}`);
      }
    }
  }
  
  public onConnection(handler: (connected: boolean) => void): void {
    this.connectionHandlers.push(handler);
    console.log('🎧 Connection handler registered');
  }
  
  public offConnection(handler: (connected: boolean) => void): void {
    const index = this.connectionHandlers.indexOf(handler);
    if (index !== -1) {
      this.connectionHandlers.splice(index, 1);
      console.log('🎧 Connection handler removed');
    }
  }
  
  // =====================================
  // 🎸 DEFAULT MESSAGE HANDLERS 🎸
  // =====================================
  
  private setupDefaultHandlers(): void {
    // Heartbeat response handler
    this.onMessage('heartbeat_response', (message) => {
      console.log('💓 Heartbeat response received');
      this.stats.lastHeartbeat = new Date();
    });
    
    // Connection welcome message
    this.onMessage('welcome', (message) => {
      console.log('👋 Welcome message received:', message.data);
      
      if (message.isFounderMessage) {
        console.log('👑 FOUNDER WELCOME MESSAGE RECEIVED!');
        
        toast.success('👑 Welcome back, LEGENDARY FOUNDER RICKROLL187! Infinite code bro energy activated!', {
          duration: 6000,
          style: {
            background: 'linear-gradient(135deg, #FFD700, #FFA500)',
            color: '#000000',
            fontWeight: '700',
          },
        });
      }
    });
    
    // Error message handler
    this.onMessage('error', (message) => {
      console.error('🚨 WebSocket error message:', message.data);
      
      toast.error(`🚨 ${message.data.title || 'WebSocket Error'}: ${message.data.message}`, {
        duration: 5000,
      });
    });
  }
  
  // =====================================
  // 📊 PUBLIC METHODS 📊
  // =====================================
  
  public isConnected(): boolean {
    return this.socket?.readyState === WebSocket.OPEN;
  }
  
  public getConnectionStats(): ConnectionStats {
    // Update uptime if connected
    if (this.stats.isConnected && this.stats.lastConnected) {
      this.stats.uptime = Date.now() - this.stats.lastConnected.getTime();
    }
    
    return { ...this.stats };
  }
  
  public getConfig(): WebSocketConfig {
    return { ...this.config };
  }
  
  public updateConfig(newConfig: Partial<WebSocketConfig>): void {
    this.config = { ...this.config, ...newConfig };
    console.log('⚙️ WebSocket config updated:', newConfig);
  }
  
  public clearMessageQueue(): void {
    this.messageQueue = [];
    console.log('🧹 Message queue cleared');
  }
  
  public getQueueSize(): number {
    return this.messageQueue.length;
  }
  
  // =====================================
  // 🧹 CLEANUP 🧹
  // =====================================
  
  public destroy(): void {
    console.log('🧹 Destroying WebSocket service...');
    
    this.disconnect();
    
    // Clear all handlers
    this.messageHandlers.clear();
    this.connectionHandlers = [];
    
    // Clear message queue
    this.messageQueue = [];
    
    console.log('✅ WebSocket service destroyed');
  }
}

// =====================================
// 🎸 EXPORT LEGENDARY WEBSOCKET SERVICE 🎸
// =====================================

// Create singleton instance with Swiss precision
export const websocketService = new LegendaryWebSocketService();

// Export types
export type { WebSocketMessage, WebSocketConfig, ConnectionStats };

// Export the service class for advanced usage
export { LegendaryWebSocketService };

console.log('🎸🎸🎸 LEGENDARY WEBSOCKET SERVICE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`WebSocket service completed at: 2025-08-06 15:16:23 UTC`);
console.log('🔌 Real-time communication: SWISS PRECISION');
console.log('👑 RICKROLL187 founder websocket: LEGENDARY');
console.log('💓 Heartbeat system: INFINITE RELIABILITY');
console.log('🌅 Afternoon legendary energy: INFINITE AT 15:16:23!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
