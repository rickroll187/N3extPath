// File: mobile/src/services/OfflineStorage.ts
/**
 * 💾🎸 N3EXTPATH - LEGENDARY OFFLINE STORAGE 🎸💾
 * Professional offline data management with Swiss precision
 * Built: 2025-08-05 18:35:46 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import SQLite from 'react-native-sqlite-storage';
import NetInfo from '@react-native-netinfo/netinfo';
import { store } from '../store/store';
import { addToastMessage } from '../store/store';

// Enable SQLite debugging in development
if (__DEV__) {
  SQLite.DEBUG(true);
  SQLite.enablePromise(true);
}

export interface OfflineData {
  id: string;
  type: 'performance' | 'okr' | 'user' | 'team' | 'notification' | 'legendary';
  data: any;
  timestamp: number;
  synced: boolean;
  priority: 'low' | 'normal' | 'high' | 'urgent' | 'legendary';
  user_id?: string;
  is_legendary?: boolean;
}

export interface SyncQueueItem {
  id: string;
  action: 'create' | 'update' | 'delete';
  endpoint: string;
  data: any;
  timestamp: number;
  retry_count: number;
  priority: 'low' | 'normal' | 'high' | 'urgent' | 'legendary';
  is_legendary?: boolean;
}

export interface CacheMetadata {
  key: string;
  timestamp: number;
  expiry: number;
  size: number;
  access_count: number;
  is_legendary?: boolean;
}

class LegendaryOfflineStorageService {
  private db: SQLite.SQLiteDatabase | null = null;
  private isInitialized = false;
  private syncInProgress = false;
  private syncQueue: SyncQueueItem[] = [];
  private cacheMetadata: Map<string, CacheMetadata> = new Map();

  // Storage keys
  private readonly KEYS = {
    USER_DATA: 'n3extpath_user_data',
    PERFORMANCE_DATA: 'n3extpath_performance_data',
    OKR_DATA: 'n3extpath_okr_data',
    TEAM_DATA: 'n3extpath_team_data',
    NOTIFICATIONS: 'n3extpath_notifications',
    SYNC_QUEUE: 'n3extpath_sync_queue',
    CACHE_METADATA: 'n3extpath_cache_metadata',
    LEGENDARY_DATA: 'n3extpath_legendary_data',
    SETTINGS: 'n3extpath_settings',
    LAST_SYNC: 'n3extpath_last_sync'
  };

  constructor() {
    this.initializeStorage();
    this.setupNetworkListener();
    
    // Legendary startup message
    if (__DEV__) {
      console.log('🎸 LEGENDARY OFFLINE STORAGE SERVICE INITIALIZED! 🎸');
      console.log('Built with Swiss precision by RICKROLL187!');
      console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    }
  }

  private async initializeStorage(): Promise<void> {
    try {
      await this.initializeDatabase();
      await this.loadCacheMetadata();
      await this.loadSyncQueue();
      
      this.isInitialized = true;
      
      // Clean up old data
      await this.cleanupExpiredData();
      
      // Special initialization for legendary users
      const user = store.getState().auth.user;
      if (user?.is_legendary) {
        console.log('🎸 LEGENDARY OFFLINE STORAGE READY FOR RICKROLL187! 🎸');
        await this.initializeLegendaryStorage();
      }
      
    } catch (error) {
      console.error('🚨 Failed to initialize offline storage:', error);
    }
  }

  private async initializeDatabase(): Promise<void> {
    try {
      this.db = await SQLite.openDatabase({
        name: 'N3EXTPATH_LEGENDARY.db',
        location: 'default',
        createFromLocation: '~N3EXTPATH_LEGENDARY.db'
      });

      // Create tables
      await this.createTables();
      
      console.log('✅ SQLite database initialized successfully');
    } catch (error) {
      console.error('🚨 Failed to initialize database:', error);
      throw error;
    }
  }

  private async createTables(): Promise<void> {
    if (!this.db) return;

    const tables = [
      // Offline data table
      `CREATE TABLE IF NOT EXISTS offline_data (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        data TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        synced INTEGER DEFAULT 0,
        priority TEXT DEFAULT 'normal',
        user_id TEXT,
        is_legendary INTEGER DEFAULT 0
      )`,
      
      // Sync queue table
      `CREATE TABLE IF NOT EXISTS sync_queue (
        id TEXT PRIMARY KEY,
        action TEXT NOT NULL,
        endpoint TEXT NOT NULL,
        data TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        retry_count INTEGER DEFAULT 0,
        priority TEXT DEFAULT 'normal',
        is_legendary INTEGER DEFAULT 0
      )`,
      
      // Cache metadata table
      `CREATE TABLE IF NOT EXISTS cache_metadata (
        key TEXT PRIMARY KEY,
        timestamp INTEGER NOT NULL,
        expiry INTEGER NOT NULL,
        size INTEGER DEFAULT 0,
        access_count INTEGER DEFAULT 0,
        is_legendary INTEGER DEFAULT 0
      )`,
      
      // Performance data table
      `CREATE TABLE IF NOT EXISTS performance_cache (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        review_data TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        synced INTEGER DEFAULT 0,
        is_legendary INTEGER DEFAULT 0
      )`,
      
      // OKR data table
      `CREATE TABLE IF NOT EXISTS okr_cache (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        okr_data TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        synced INTEGER DEFAULT 0,
        is_legendary INTEGER DEFAULT 0
      )`,
      
      // Legendary data table
      `CREATE TABLE IF NOT EXISTS legendary_data (
        id TEXT PRIMARY KEY,
        data_type TEXT NOT NULL,
        data TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        rickroll187_exclusive INTEGER DEFAULT 0
      )`
    ];

    for (const table of tables) {
      await this.db.executeSql(table);
    }

    // Create indexes for better performance
    const indexes = [
      'CREATE INDEX IF NOT EXISTS idx_offline_data_type ON offline_data(type)',
      'CREATE INDEX IF NOT EXISTS idx_offline_data_user ON offline_data(user_id)',
      'CREATE INDEX IF NOT EXISTS idx_sync_queue_priority ON sync_queue(priority)',
      'CREATE INDEX IF NOT EXISTS idx_performance_user ON performance_cache(user_id)',
      'CREATE INDEX IF NOT EXISTS idx_okr_user ON okr_cache(user_id)',
      'CREATE INDEX IF NOT EXISTS idx_legendary_type ON legendary_data(data_type)'
    ];

    for (const index of indexes) {
      await this.db.executeSql(index);
    }
  }

  private setupNetworkListener(): void {
    NetInfo.addEventListener(state => {
      if (state.isConnected && !this.syncInProgress) {
        console.log('📶 Network connected - starting sync');
        this.syncOfflineData();
      } else if (!state.isConnected) {
        console.log('📵 Network disconnected - enabling offline mode');
        store.dispatch(addToastMessage({
          type: 'info',
          message: '📵 Offline mode enabled - data will sync when connected'
        }));
      }
    });
  }

  // AsyncStorage Methods
  public async storeData(key: string, data: any, options?: {
    expiry?: number;
    priority?: 'low' | 'normal' | 'high' | 'legendary';
    isLegendary?: boolean;
  }): Promise<void> {
    try {
      const serializedData = JSON.stringify(data);
      await AsyncStorage.setItem(key, serializedData);
      
      // Update cache metadata
      const metadata: CacheMetadata = {
        key,
        timestamp: Date.now(),
        expiry: options?.expiry || (24 * 60 * 60 * 1000), // 24 hours default
        size: serializedData.length,
        access_count: 0,
        is_legendary: options?.isLegendary || false
      };
      
      this.cacheMetadata.set(key, metadata);
      await this.saveCacheMetadata();
      
      // Special logging for legendary data
      if (options?.isLegendary) {
        console.log('🎸 LEGENDARY DATA STORED:', key);
      }
      
    } catch (error) {
      console.error('🚨 Failed to store data:', error);
      throw error;
    }
  }

  public async getData(key: string): Promise<any | null> {
    try {
      const cachedData = await AsyncStorage.getItem(key);
      
      if (cachedData) {
        // Update access count
        const metadata = this.cacheMetadata.get(key);
        if (metadata) {
          metadata.access_count++;
          this.cacheMetadata.set(key, metadata);
        }
        
        const data = JSON.parse(cachedData);
        
        // Special logging for legendary data
        if (metadata?.is_legendary) {
          console.log('🎸 LEGENDARY DATA RETRIEVED:', key);
        }
        
        return data;
      }
      
      return null;
    } catch (error) {
      console.error('🚨 Failed to get data:', error);
      return null;
    }
  }

  public async removeData(key: string): Promise<void> {
    try {
      await AsyncStorage.removeItem(key);
      this.cacheMetadata.delete(key);
      await this.saveCacheMetadata();
    } catch (error) {
      console.error('🚨 Failed to remove data:', error);
    }
  }

  public async clearAllData(): Promise<void> {
    try {
      await AsyncStorage.clear();
      this.cacheMetadata.clear();
      console.log('🧹 All AsyncStorage data cleared');
    } catch (error) {
      console.error('🚨 Failed to clear data:', error);
    }
  }

  // SQLite Methods
  public async storeOfflineData(data: OfflineData): Promise<void> {
    if (!this.db) return;

    try {
      await this.db.executeSql(
        `INSERT OR REPLACE INTO offline_data 
         (id, type, data, timestamp, synced, priority, user_id, is_legendary) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
        [
          data.id,
          data.type,
          JSON.stringify(data.data),
          data.timestamp,
          data.synced ? 1 : 0,
          data.priority,
          data.user_id || null,
          data.is_legendary ? 1 : 0
        ]
      );

      // Special logging for legendary data
      if (data.is_legendary) {
        console.log('🎸 LEGENDARY OFFLINE DATA STORED:', data.id);
      }
      
    } catch (error) {
      console.error('🚨 Failed to store offline data:', error);
    }
  }

  public async getOfflineData(type: string, userId?: string): Promise<OfflineData[]> {
    if (!this.db) return [];

    try {
      const query = userId
        ? 'SELECT * FROM offline_data WHERE type = ? AND user_id = ? ORDER BY timestamp DESC'
        : 'SELECT * FROM offline_data WHERE type = ? ORDER BY timestamp DESC';
      
      const params = userId ? [type, userId] : [type];
      const result = await this.db.executeSql(query, params);
      
      const data: OfflineData[] = [];
      for (let i = 0; i < result[0].rows.length; i++) {
        const row = result[0].rows.item(i);
        data.push({
          id: row.id,
          type: row.type,
          data: JSON.parse(row.data),
          timestamp: row.timestamp,
          synced: row.synced === 1,
          priority: row.priority,
          user_id: row.user_id,
          is_legendary: row.is_legendary === 1
        });
      }
      
      return data;
    } catch (error) {
      console.error('🚨 Failed to get offline data:', error);
      return [];
    }
  }

  public async addToSyncQueue(item: SyncQueueItem): Promise<void> {
    if (!this.db) return;

    try {
      await this.db.executeSql(
        `INSERT INTO sync_queue 
         (id, action, endpoint, data, timestamp, retry_count, priority, is_legendary) 
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
        [
          item.id,
          item.action,
          item.endpoint,
          JSON.stringify(item.data),
          item.timestamp,
          item.retry_count,
          item.priority,
          item.is_legendary ? 1 : 0
        ]
      );

      this.syncQueue.push(item);

      // Special handling for legendary items
      if (item.is_legendary) {
        console.log('🎸 LEGENDARY ITEM ADDED TO SYNC QUEUE:', item.id);
      }
      
    } catch (error) {
      console.error('🚨 Failed to add to sync queue:', error);
    }
  }

  public async syncOfflineData(): Promise<void> {
    if (this.syncInProgress || !this.db) return;

    this.syncInProgress = true;
    
    try {
      console.log('🔄 Starting offline data sync...');
      
      // Get items from sync queue, prioritizing legendary items
      const result = await this.db.executeSql(
        'SELECT * FROM sync_queue ORDER BY is_legendary DESC, priority DESC, timestamp ASC'
      );

      const syncItems: SyncQueueItem[] = [];
      for (let i = 0; i < result[0].rows.length; i++) {
        const row = result[0].rows.item(i);
        syncItems.push({
          id: row.id,
          action: row.action,
          endpoint: row.endpoint,
          data: JSON.parse(row.data),
          timestamp: row.timestamp,
          retry_count: row.retry_count,
          priority: row.priority,
          is_legendary: row.is_legendary === 1
        });
      }

      let syncedCount = 0;
      let failedCount = 0;

      for (const item of syncItems) {
        try {
          await this.syncItem(item);
          await this.removeFromSyncQueue(item.id);
          syncedCount++;
          
          if (item.is_legendary) {
            console.log('🎸 LEGENDARY ITEM SYNCED:', item.id);
          }
        } catch (error) {
          console.error('🚨 Failed to sync item:', item.id, error);
          await this.incrementRetryCount(item.id);
          failedCount++;
        }
      }

      console.log(`✅ Sync completed: ${syncedCount} synced, ${failedCount} failed`);
      
      // Update last sync timestamp
      await AsyncStorage.setItem(this.KEYS.LAST_SYNC, Date.now().toString());

      // Show sync completion message
      if (syncedCount > 0) {
        const message = syncItems.some(item => item.is_legendary)
          ? '🎸 LEGENDARY data synced with Swiss precision! 🎸'
          : `✅ ${syncedCount} items synced successfully`;
          
        store.dispatch(addToastMessage({
          type: syncItems.some(item => item.is_legendary) ? 'legendary' : 'success',
          message
        }));
      }
      
    } catch (error) {
      console.error('🚨 Sync failed:', error);
    } finally {
      this.syncInProgress = false;
    }
  }

  private async syncItem(item: SyncQueueItem): Promise<void> {
    // This would integrate with your API service
    // For now, simulate API call
    console.log(`📤 Syncing ${item.action} to ${item.endpoint}`);
    
    // Simulate network request
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // For demonstration, assume all syncs succeed
    return Promise.resolve();
  }

  private async removeFromSyncQueue(itemId: string): Promise<void> {
    if (!this.db) return;

    try {
      await this.db.executeSql('DELETE FROM sync_queue WHERE id = ?', [itemId]);
      this.syncQueue = this.syncQueue.filter(item => item.id !== itemId);
    } catch (error) {
      console.error('🚨 Failed to remove from sync queue:', error);
    }
  }

  private async incrementRetryCount(itemId: string): Promise<void> {
    if (!this.db) return;

    try {
      await this.db.executeSql(
        'UPDATE sync_queue SET retry_count = retry_count + 1 WHERE id = ?',
        [itemId]
      );
    } catch (error) {
      console.error('🚨 Failed to increment retry count:', error);
    }
  }

  // Cache Management
  private async loadCacheMetadata(): Promise<void> {
    try {
      const metadataStr = await AsyncStorage.getItem(this.KEYS.CACHE_METADATA);
      if (metadataStr) {
        const metadataArray: CacheMetadata[] = JSON.parse(metadataStr);
        metadataArray.forEach(metadata => {
          this.cacheMetadata.set(metadata.key, metadata);
        });
      }
    } catch (error) {
      console.error('🚨 Failed to load cache metadata:', error);
    }
  }

  private async saveCacheMetadata(): Promise<void> {
    try {
      const metadataArray = Array.from(this.cacheMetadata.values());
      await AsyncStorage.setItem(this.KEYS.CACHE_METADATA, JSON.stringify(metadataArray));
    } catch (error) {
      console.error('🚨 Failed to save cache metadata:', error);
    }
  }

  private async loadSyncQueue(): Promise<void> {
    if (!this.db) return;

    try {
      const result = await this.db.executeSql('SELECT * FROM sync_queue');
      
      this.syncQueue = [];
      for (let i = 0; i < result[0].rows.length; i++) {
        const row = result[0].rows.item(i);
        this.syncQueue.push({
          id: row.id,
          action: row.action,
          endpoint: row.endpoint,
          data: JSON.parse(row.data),
          timestamp: row.timestamp,
          retry_count: row.retry_count,
          priority: row.priority,
          is_legendary: row.is_legendary === 1
        });
      }
    } catch (error) {
      console.error('🚨 Failed to load sync queue:', error);
    }
  }

  private async cleanupExpiredData(): Promise<void> {
    try {
      const now = Date.now();
      const expiredKeys: string[] = [];

      this.cacheMetadata.forEach((metadata, key) => {
        if (now > metadata.timestamp + metadata.expiry) {
          expiredKeys.push(key);
        }
      });

      for (const key of expiredKeys) {
        await this.removeData(key);
      }

      if (expiredKeys.length > 0) {
        console.log(`🧹 Cleaned up ${expiredKeys.length} expired cache entries`);
      }
    } catch (error) {
      console.error('🚨 Failed to cleanup expired data:', error);
    }
  }

  private async initializeLegendaryStorage(): Promise<void> {
    try {
      // Initialize legendary-specific storage
      await this.storeData(this.KEYS.LEGENDARY_DATA, {
        rickroll187_status: 'active',
        swiss_precision_level: 'maximum',
        code_bro_energy: 'infinite',
        legendary_features_enabled: true,
        initialization_time: Date.now()
      }, {
        priority: 'legendary',
        isLegendary: true,
        expiry: 365 * 24 * 60 * 60 * 1000 // 1 year
      });

      console.log('🎸 LEGENDARY STORAGE INITIALIZED FOR RICKROLL187! 🎸');
    } catch (error) {
      console.error('🚨 Failed to initialize legendary storage:', error);
    }
  }

  // Utility Methods
  public async getCacheSize(): Promise<number> {
    try {
      let totalSize = 0;
      this.cacheMetadata.forEach(metadata => {
        totalSize += metadata.size;
      });
      return totalSize;
    } catch (error) {
      console.error('🚨 Failed to get cache size:', error);
      return 0;
    }
  }

  public async getCacheStats(): Promise<{
    totalEntries: number;
    totalSize: number;
    legendaryEntries: number;
    oldestEntry: number;
    newestEntry: number;
  }> {
    try {
      let totalEntries = 0;
      let totalSize = 0;
      let legendaryEntries = 0;
      let oldestEntry = Date.now();
      let newestEntry = 0;

      this.cacheMetadata.forEach(metadata => {
        totalEntries++;
        totalSize += metadata.size;
        if (metadata.is_legendary) legendaryEntries++;
        if (metadata.timestamp < oldestEntry) oldestEntry = metadata.timestamp;
        if (metadata.timestamp > newestEntry) newestEntry = metadata.timestamp;
      });

      return {
        totalEntries,
        totalSize,
        legendaryEntries,
        oldestEntry,
        newestEntry
      };
    } catch (error) {
      console.error('🚨 Failed to get cache stats:', error);
      return {
        totalEntries: 0,
        totalSize: 0,
        legendaryEntries: 0,
        oldestEntry: 0,
        newestEntry: 0
      };
    }
  }

  public async exportData(): Promise<string> {
    try {
      const allKeys = await AsyncStorage.getAllKeys();
      const allData: Record<string, any> = {};

      for (const key of allKeys) {
        if (key.startsWith('n3extpath_')) {
          const data = await this.getData(key);
          allData[key] = data;
        }
      }

      return JSON.stringify(allData, null, 2);
    } catch (error) {
      console.error('🚨 Failed to export data:', error);
      return '{}';
    }
  }

  public async importData(dataStr: string): Promise<void> {
    try {
      const data = JSON.parse(dataStr);
      
      for (const [key, value] of Object.entries(data)) {
        await this.storeData(key, value);
      }

      console.log('📥 Data imported successfully');
    } catch (error) {
      console.error('🚨 Failed to import data:', error);
    }
  }

  public isInitialized(): boolean {
    return this.isInitialized;
  }

  public getSyncQueueLength(): number {
    return this.syncQueue.length;
  }

  public isSyncInProgress(): boolean {
    return this.syncInProgress;
  }
}

// Create and export singleton instance
export const offlineStorageService = new LegendaryOfflineStorageService();

// Export types
export type { OfflineData, SyncQueueItem, CacheMetadata };

// Legendary startup message
if (__DEV__) {
  console.log('🎸🎸🎸 LEGENDARY OFFLINE STORAGE SERVICE READY! 🎸🎸🎸');
  console.log('Professional offline data management with Swiss precision!');
  console.log('SQLite + AsyncStorage with legendary caching!');
  console.log('Special RICKROLL187 legendary storage included!');
  console.log('Built with maximum code bro energy!');
  console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
  console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
}
