// File: web/src/services/storageService.ts
/**
 * 💾🎸 N3EXTPATH - LEGENDARY STORAGE SERVICE 🎸💾
 * Professional local/session storage with Swiss precision
 * Built: 2025-08-06 15:23:44 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

// =====================================
// 💾 STORAGE TYPES 💾
// =====================================

export interface StorageItem<T = any> {
  value: T;
  timestamp: number;
  expiry?: number;
  encrypted?: boolean;
  founderData?: boolean;
  legendaryLevel?: number;
  version: string;
}

export interface StorageConfig {
  prefix: string;
  defaultExpiry?: number;
  encryptFounderData?: boolean;
  enableCompression?: boolean;
  maxSize?: number;
}

// =====================================
// 🎸 LEGENDARY STORAGE SERVICE 🎸
// =====================================

class LegendaryStorageService {
  private config: StorageConfig;
  private isFounder: boolean = false;
  private storageCount: number = 0;
  private founderStorageCount: number = 0;

  constructor(config: Partial<StorageConfig> = {}) {
    console.log('💾🎸💾 LEGENDARY STORAGE SERVICE INITIALIZING! 💾🎸💾');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Storage service initialized at: 2025-08-06 15:23:44 UTC`);

    this.config = {
      prefix: 'n3extpath_',
      defaultExpiry: 7 * 24 * 60 * 60 * 1000, // 7 days
      encryptFounderData: true,
      enableCompression: false,
      maxSize: 5 * 1024 * 1024, // 5MB
      ...config,
    };

    // Check if this is RICKROLL187 founder
    this.checkFounderStatus();

    if (this.isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER STORAGE DETECTED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER STORAGE WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER STORAGE SYSTEM!');
      console.log('🌅 AFTERNOON FOUNDER STORAGE POWER AT 15:23:44!');
      
      this.config.prefix = 'n3extpath_founder_';
      this.config.encryptFounderData = true;
      this.config.maxSize = 50 * 1024 * 1024; // 50MB for founder
    }
  }

  // =====================================
  // 👑 FOUNDER DETECTION 👑
  // =====================================

  private checkFounderStatus(): void {
    try {
      // Check if founder data exists in localStorage
      const founderKey = this.getStorageKey('founder_status');
      const founderData = localStorage.getItem(founderKey);
      
      if (founderData) {
        const parsed = JSON.parse(founderData);
        this.isFounder = parsed.value?.isFounder === true;
      }
      
      // Also check for founder email in auth data
      const authKey = this.getStorageKey('auth_user');
      const authData = localStorage.getItem(authKey);
      
      if (authData) {
        const parsed = JSON.parse(authData);
        const email = parsed.value?.email;
        if (email === 'letstalktech010@gmail.com') {
          this.isFounder = true;
        }
      }
    } catch (error) {
      console.error('🚨 Founder status check error:', error);
    }
  }

  // =====================================
  // 🔑 KEY MANAGEMENT 🔑
  // =====================================

  private getStorageKey(key: string): string {
    return `${this.config.prefix}${key}`;
  }

  private isValidKey(key: string): boolean {
    return typeof key === 'string' && key.length > 0;
  }

  // =====================================
  // 🔒 ENCRYPTION HELPERS 🔒
  // =====================================

  private encryptData(data: any): string {
    // Simple base64 encoding for founder data security
    // In production, use proper encryption libraries
    try {
      const jsonString = JSON.stringify(data);
      return btoa(unescape(encodeURIComponent(jsonString)));
    } catch (error) {
      console.error('🔒 Encryption error:', error);
      return JSON.stringify(data);
    }
  }

  private decryptData(encryptedData: string): any {
    // Simple base64 decoding
    try {
      const decrypted = decodeURIComponent(escape(atob(encryptedData)));
      return JSON.parse(decrypted);
    } catch (error) {
      console.error('🔓 Decryption error:', error);
      return null;
    }
  }

  // =====================================
  // 💾 STORAGE OPERATIONS 💾
  // =====================================

  public set<T>(
    key: string,
    value: T,
    options: {
      expiry?: number;
      storage?: 'local' | 'session';
      encrypt?: boolean;
      founderData?: boolean;
      legendaryLevel?: number;
    } = {}
  ): boolean {
    if (!this.isValidKey(key)) {
      console.error('🚨 Invalid storage key:', key);
      return false;
    }

    try {
      const storageKey = this.getStorageKey(key);
      const now = Date.now();
      
      const item: StorageItem<T> = {
        value,
        timestamp: now,
        expiry: options.expiry ? now + options.expiry : (this.config.defaultExpiry ? now + this.config.defaultExpiry : undefined),
        encrypted: options.encrypt || (this.isFounder && options.founderData && this.config.encryptFounderData),
        founderData: options.founderData || this.isFounder,
        legendaryLevel: options.legendaryLevel,
        version: '2.0.0',
      };

      // Encrypt data if needed
      let dataToStore = item;
      if (item.encrypted) {
        dataToStore = {
          ...item,
          value: this.encryptData(value) as T,
        };
        
        console.log(`🔒 Encrypting ${this.isFounder ? 'founder' : 'legendary'} data for key: ${key}`);
      }

      const serialized = JSON.stringify(dataToStore);
      
      // Check size limit
      if (serialized.length > this.config.maxSize!) {
        console.error('🚨 Storage item too large:', key, serialized.length);
        return false;
      }

      // Choose storage type
      const storage = options.storage === 'session' ? sessionStorage : localStorage;
      storage.setItem(storageKey, serialized);

      this.storageCount++;
      if (options.founderData || this.isFounder) {
        this.founderStorageCount++;
        
        if (this.isFounder) {
          console.log(`👑 Founder data stored: ${key} (${this.founderStorageCount} founder items total)`);
        }
      }

      console.log(`💾 Stored: ${key} in ${options.storage || 'local'} storage`);
      return true;

    } catch (error) {
      console.error('🚨 Storage set error:', error);
      return false;
    }
  }

  public get<T>(
    key: string,
    options: {
      storage?: 'local' | 'session';
      defaultValue?: T;
    } = {}
  ): T | null {
    if (!this.isValidKey(key)) {
      console.error('🚨 Invalid storage key:', key);
      return options.defaultValue ?? null;
    }

    try {
      const storageKey = this.getStorageKey(key);
      const storage = options.storage === 'session' ? sessionStorage : localStorage;
      const serialized = storage.getItem(storageKey);

      if (!serialized) {
        return options.defaultValue ?? null;
      }

      const item: StorageItem<T> = JSON.parse(serialized);
      const now = Date.now();

      // Check expiry
      if (item.expiry && now > item.expiry) {
        console.log(`⏰ Storage item expired: ${key}`);
        this.remove(key, { storage: options.storage });
        return options.defaultValue ?? null;
      }

      // Decrypt if needed
      let value = item.value;
      if (item.encrypted) {
        value = this.decryptData(item.value as string) as T;
        
        if (value === null) {
          console.error('🔓 Failed to decrypt data:', key);
          return options.defaultValue ?? null;
        }
        
        console.log(`🔓 Decrypted ${item.founderData ? 'founder' : 'legendary'} data for key: ${key}`);
      }

      // Log founder data access
      if (item.founderData && this.isFounder) {
        console.log(`👑 Founder data accessed: ${key} (legendary level: ${item.legendaryLevel || 0})`);
      }

      console.log(`💾 Retrieved: ${key} from ${options.storage || 'local'} storage`);
      return value;

    } catch (error) {
      console.error('🚨 Storage get error:', error);
      return options.defaultValue ?? null;
    }
  }

  public remove(
    key: string,
    options: { storage?: 'local' | 'session' } = {}
  ): boolean {
    if (!this.isValidKey(key)) {
      console.error('🚨 Invalid storage key:', key);
      return false;
    }

    try {
      const storageKey = this.getStorageKey(key);
      const storage = options.storage === 'session' ? sessionStorage : localStorage;
      
      // Check if it was founder data before removing
      const existing = storage.getItem(storageKey);
      let wasFounderData = false;
      
      if (existing) {
        try {
          const item = JSON.parse(existing);
          wasFounderData = item.founderData || false;
        } catch (e) {
          // Ignore parsing errors for removal
        }
      }

      storage.removeItem(storageKey);
      
      if (wasFounderData) {
        this.founderStorageCount = Math.max(0, this.founderStorageCount - 1);
        
        if (this.isFounder) {
          console.log(`👑 Founder data removed: ${key}`);
        }
      }

      console.log(`🗑️ Removed: ${key} from ${options.storage || 'local'} storage`);
      return true;

    } catch (error) {
      console.error('🚨 Storage remove error:', error);
      return false;
    }
  }

  // =====================================
  // 🎸 LEGENDARY METHODS 🎸
  // =====================================

  public setFounderData<T>(
    key: string,
    value: T,
    options: {
      expiry?: number;
      storage?: 'local' | 'session';
      legendaryLevel?: number;
    } = {}
  ): boolean {
    if (!this.isFounder) {
      console.error('👑 Founder data storage is only available for RICKROLL187!');
      return false;
    }

    return this.set(key, value, {
      ...options,
      founderData: true,
      encrypt: true,
      legendaryLevel: options.legendaryLevel || 10,
    });
  }

  public getFounderData<T>(
    key: string,
    options: {
      storage?: 'local' | 'session';
      defaultValue?: T;
    } = {}
  ): T | null {
    if (!this.isFounder) {
      console.error('👑 Founder data access is only available for RICKROLL187!');
      return options.defaultValue ?? null;
    }

    return this.get<T>(key, options);
  }

  public setLegendaryCache<T>(
    key: string,
    value: T,
    ttl: number = 60000 // 1 minute default
  ): boolean {
    return this.set(`cache_${key}`, value, {
      expiry: ttl,
      storage: 'session',
      legendaryLevel: 5,
    });
  }

  public getLegendaryCache<T>(
    key: string,
    defaultValue?: T
  ): T | null {
    return this.get<T>(`cache_${key}`, {
      storage: 'session',
      defaultValue,
    });
  }

  // =====================================
  // 🧹 CLEANUP METHODS 🧹
  // =====================================

  public clearExpired(): number {
    let clearedCount = 0;
    const now = Date.now();

    // Clear from localStorage
    for (let i = localStorage.length - 1; i >= 0; i--) {
      const key = localStorage.key(i);
      if (key && key.startsWith(this.config.prefix)) {
        try {
          const item: StorageItem = JSON.parse(localStorage.getItem(key)!);
          if (item.expiry && now > item.expiry) {
            localStorage.removeItem(key);
            clearedCount++;
            
            if (item.founderData) {
              this.founderStorageCount = Math.max(0, this.founderStorageCount - 1);
            }
          }
        } catch (e) {
          // Remove invalid items
          localStorage.removeItem(key);
          clearedCount++;
        }
      }
    }

    // Clear from sessionStorage
    for (let i = sessionStorage.length - 1; i >= 0; i--) {
      const key = sessionStorage.key(i);
      if (key && key.startsWith(this.config.prefix)) {
        try {
          const item: StorageItem = JSON.parse(sessionStorage.getItem(key)!);
          if (item.expiry && now > item.expiry) {
            sessionStorage.removeItem(key);
            clearedCount++;
          }
        } catch (e) {
          sessionStorage.removeItem(key);
          clearedCount++;
        }
      }
    }

    if (clearedCount > 0) {
      console.log(`🧹 Cleared ${clearedCount} expired storage items`);
    }

    return clearedCount;
  }

  public clearAll(options: { includeFounderData?: boolean } = {}): number {
    let clearedCount = 0;

    // Clear localStorage
    for (let i = localStorage.length - 1; i >= 0; i--) {
      const key = localStorage.key(i);
      if (key && key.startsWith(this.config.prefix)) {
        try {
          const item: StorageItem = JSON.parse(localStorage.getItem(key)!);
          
          // Skip founder data unless explicitly requested
          if (item.founderData && !options.includeFounderData && this.isFounder) {
            continue;
          }
          
          localStorage.removeItem(key);
          clearedCount++;
        } catch (e) {
          localStorage.removeItem(key);
          clearedCount++;
        }
      }
    }

    // Clear sessionStorage
    for (let i = sessionStorage.length - 1; i >= 0; i--) {
      const key = sessionStorage.key(i);
      if (key && key.startsWith(this.config.prefix)) {
        sessionStorage.removeItem(key);
        clearedCount++;
      }
    }

    if (options.includeFounderData) {
      this.founderStorageCount = 0;
    }

    console.log(`🧹 Cleared ${clearedCount} storage items${options.includeFounderData ? ' (including founder data)' : ''}`);
    return clearedCount;
  }

  // =====================================
  // 📊 UTILITY METHODS 📊
  // =====================================

  public getStorageInfo() {
    const info = {
      prefix: this.config.prefix,
      isFounder: this.isFounder,
      storageCount: this.storageCount,
      founderStorageCount: this.founderStorageCount,
      config: this.config,
      sizes: {
        localStorage: this.getStorageSize(localStorage),
        sessionStorage: this.getStorageSize(sessionStorage),
      },
      timestamp: new Date().toISOString(),
    };

    return info;
  }

  private getStorageSize(storage: Storage): number {
    let size = 0;
    for (let i = 0; i < storage.length; i++) {
      const key = storage.key(i);
      if (key && key.startsWith(this.config.prefix)) {
        const value = storage.getItem(key);
        if (value) {
          size += key.length + value.length;
        }
      }
    }
    return size;
  }

  public listKeys(options: { storage?: 'local' | 'session'; founderOnly?: boolean } = {}): string[] {
    const storage = options.storage === 'session' ? sessionStorage : localStorage;
    const keys: string[] = [];

    for (let i = 0; i < storage.length; i++) {
      const key = storage.key(i);
      if (key && key.startsWith(this.config.prefix)) {
        try {
          const item: StorageItem = JSON.parse(storage.getItem(key)!);
          
          if (options.founderOnly && !item.founderData) {
            continue;
          }
          
          keys.push(key.replace(this.config.prefix, ''));
        } catch (e) {
          // Include invalid items for cleanup
          keys.push(key.replace(this.config.prefix, ''));
        }
      }
    }

    return keys;
  }

  public updateFounderStatus(isFounder: boolean): void {
    this.isFounder = isFounder;
    
    // Store founder status
    this.set('founder_status', { isFounder }, {
      founderData: isFounder,
      encrypt: isFounder,
      legendaryLevel: isFounder ? 10 : 0,
    });

    if (isFounder) {
      console.log('👑 RICKROLL187 FOUNDER STATUS ACTIVATED IN STORAGE!');
      this.config.prefix = 'n3extpath_founder_';
      this.config.maxSize = 50 * 1024 * 1024; // 50MB for founder
    } else {
      console.log('👤 Regular user status set in storage');
      this.config.prefix = 'n3extpath_';
      this.config.maxSize = 5 * 1024 * 1024; // 5MB for regular users
    }
  }
}

// =====================================
// 🎸 EXPORT LEGENDARY STORAGE SERVICE 🎸
// =====================================

// Create singleton instance with Swiss precision
export const storageService = new LegendaryStorageService();

// Export types
export type { StorageItem, StorageConfig };

// Export the service class for advanced usage
export { LegendaryStorageService };

console.log('🎸🎸🎸 LEGENDARY STORAGE SERVICE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Storage service completed at: 2025-08-06 15:23:44 UTC`);
console.log('💾 Data persistence: SWISS PRECISION');
console.log('👑 RICKROLL187 founder storage: LEGENDARY');
console.log('🔒 Encryption system: MAXIMUM SECURITY');
console.log('🌅 Afternoon legendary energy: INFINITE AT 15:23:44!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
