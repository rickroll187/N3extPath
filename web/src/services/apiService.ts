// File: web/src/services/apiService.ts
/**
 * 🌐🎸 N3EXTPATH - LEGENDARY API SERVICE 🎸🌐
 * Professional API communication with Swiss precision
 * Built: 2025-08-06 15:23:44 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { store } from '@/store';
import { logout } from '@/store/slices/authSlice';
import { setGlobalLoading } from '@/store/slices/uiSlice';
import toast from 'react-hot-toast';

// =====================================
// 🌐 API TYPES 🌐
// =====================================

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  code?: number;
  timestamp?: string;
  requestId?: string;
  founderData?: boolean;
  legendaryLevel?: number;
}

export interface ApiError {
  message: string;
  code?: number;
  field?: string;
  details?: any;
  isFounderError?: boolean;
}

export interface RequestConfig extends AxiosRequestConfig {
  skipAuth?: boolean;
  skipLoading?: boolean;
  skipErrorHandling?: boolean;
  founderRequest?: boolean;
  legendaryTimeout?: number;
}

// =====================================
// 🎸 LEGENDARY API SERVICE 🎸
// =====================================

class LegendaryApiService {
  private client: AxiosInstance;
  private baseURL: string;
  private requestCount: number = 0;
  private founderRequestCount: number = 0;
  private isFounder: boolean = false;

  constructor() {
    console.log('🌐🎸🌐 LEGENDARY API SERVICE INITIALIZING! 🌐🎸🌐');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`API service initialized at: 2025-08-06 15:23:44 UTC`);

    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';
    
    // Check if this is RICKROLL187 founder
    const state = store.getState();
    this.isFounder = state.auth?.user?.email === 'letstalktech010@gmail.com' || 
                     state.auth?.user?.username === 'rickroll187';

    if (this.isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER API DETECTED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER API WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER API SYSTEM!');
      console.log('🌅 AFTERNOON FOUNDER API POWER AT 15:23:44!');
    }

    // Create axios instance with Swiss precision
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: this.isFounder ? 60000 : 30000, // Longer timeout for founder
      headers: {
        'Content-Type': 'application/json',
        'X-Client-Version': '2.0.0',
        'X-Platform': 'N3EXTPATH',
        'X-Built-By': 'RICKROLL187',
        'X-Code-Bro-Energy': '10',
        'X-Swiss-Precision': 'true',
        ...(this.isFounder && {
          'X-Founder-Request': 'true',
          'X-Legendary-Level': '10',
          'X-Infinite-Energy': 'true',
        }),
      },
    });

    this.setupInterceptors();
  }

  // =====================================
  // 🎸 LEGENDARY INTERCEPTORS 🎸
  // =====================================

  private setupInterceptors(): void {
    // Request interceptor with Swiss precision
    this.client.interceptors.request.use(
      (config) => {
        this.requestCount++;
        
        // Add auth token
        const state = store.getState();
        const token = state.auth?.token;
        
        if (token && !config.skipAuth) {
          config.headers.Authorization = `Bearer ${token}`;
        }

        // Add founder headers if applicable
        if (this.isFounder || config.founderRequest) {
          this.founderRequestCount++;
          config.headers['X-Founder-Request'] = 'true';
          config.headers['X-Legendary-Level'] = '10';
          config.headers['X-Request-Count'] = this.founderRequestCount.toString();
          
          console.log(`👑 FOUNDER API REQUEST #${this.founderRequestCount}: ${config.method?.toUpperCase()} ${config.url}`);
        }

        // Add request metadata
        config.headers['X-Request-ID'] = `req-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        config.headers['X-Timestamp'] = new Date().toISOString();
        config.headers['X-Request-Count'] = this.requestCount.toString();

        // Show loading for non-background requests
        if (!config.skipLoading) {
          store.dispatch(setGlobalLoading({ 
            loading: true, 
            message: this.isFounder ? 'Processing founder request with infinite energy...' : 'Loading with code bro energy...' 
          }));
        }

        // Apply legendary timeout if specified
        if (config.legendaryTimeout) {
          config.timeout = config.legendaryTimeout;
        }

        console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        store.dispatch(setGlobalLoading({ loading: false }));
        console.error('🚨 Request interceptor error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor with legendary handling
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        // Hide loading
        store.dispatch(setGlobalLoading({ loading: false }));

        // Log successful response
        console.log(`✅ API Response: ${response.status} ${response.config.url}`);

        // Handle founder responses
        if (response.data?.founderData && this.isFounder) {
          console.log('👑 FOUNDER API RESPONSE RECEIVED WITH LEGENDARY DATA!');
          
          toast.success('👑 Founder API request completed with Swiss precision!', {
            duration: 3000,
            style: {
              background: 'linear-gradient(135deg, #FFD700, #FFA500)',
              color: '#000000',
              fontWeight: '700',
            },
          });
        }

        // Handle legendary responses
        if (response.data?.legendaryLevel && response.data.legendaryLevel >= 5) {
          console.log('🎸 LEGENDARY API RESPONSE RECEIVED!');
        }

        return response;
      },
      (error: AxiosError) => {
        // Hide loading
        store.dispatch(setGlobalLoading({ loading: false }));

        // Handle different error types
        return this.handleApiError(error);
      }
    );
  }

  // =====================================
  // 🚨 ERROR HANDLING 🚨
  // =====================================

  private handleApiError(error: AxiosError): Promise<never> {
    const config = error.config as RequestConfig;
    let apiError: ApiError = {
      message: 'An unexpected error occurred',
      code: error.response?.status,
    };

    // Parse error response
    if (error.response?.data) {
      const data = error.response.data as any;
      apiError = {
        message: data.message || data.error || 'API error occurred',
        code: error.response.status,
        field: data.field,
        details: data.details,
        isFounderError: data.isFounderError,
      };
    } else if (error.request) {
      apiError.message = 'Network error - please check your connection';
    }

    console.error('🚨 API Error:', apiError);

    // Handle specific error codes with Swiss precision
    switch (apiError.code) {
      case 401:
        console.log('🔐 Authentication expired, logging out...');
        store.dispatch(logout());
        
        if (this.isFounder) {
          toast.error('👑 Founder session expired. Please re-authenticate with legendary credentials.', {
            duration: 6000,
            style: {
              background: 'linear-gradient(135deg, #DC2626, #991B1B)',
              color: '#FFFFFF',
              fontWeight: '700',
            },
          });
        } else {
          toast.error('🔐 Session expired. Please log in again.');
        }
        break;

      case 403:
        if (this.isFounder) {
          toast.error('👑 Founder access denied - this should never happen! Contact system admin.', {
            duration: 8000,
            style: {
              background: 'linear-gradient(135deg, #DC2626, #991B1B)',
              color: '#FFFFFF',
              fontWeight: '700',
            },
          });
        } else {
          toast.error('🚫 Access denied. You need legendary permissions for this action.');
        }
        break;

      case 404:
        toast.error('🔍 Resource not found. It might have been moved or deleted.');
        break;

      case 429:
        if (this.isFounder) {
          console.log('👑 Founder rate limit - this should not happen!');
          toast.error('👑 Founder rate limit reached (this is unusual). Please try again.', {
            duration: 5000,
            style: {
              background: 'linear-gradient(135deg, #F59E0B, #D97706)',
              color: '#000000',
              fontWeight: '700',
            },
          });
        } else {
          toast.error('⏳ Too many requests. Please slow down and try again in a moment.');
        }
        break;

      case 500:
        if (this.isFounder) {
          toast.error('👑 Server error detected. Founder alert sent to system administrators.', {
            duration: 8000,
            style: {
              background: 'linear-gradient(135deg, #DC2626, #991B1B)',
              color: '#FFFFFF',
              fontWeight: '700',
            },
          });
        } else {
          toast.error('🚨 Server error. Our code bros are working on it!');
        }
        break;

      default:
        if (!config?.skipErrorHandling) {
          if (apiError.isFounderError) {
            toast.error(`👑 Founder Error: ${apiError.message}`, {
              duration: 6000,
              style: {
                background: 'linear-gradient(135deg, #DC2626, #991B1B)',
                color: '#FFFFFF',
                fontWeight: '700',
              },
            });
          } else {
            toast.error(`🚨 ${apiError.message}`);
          }
        }
    }

    return Promise.reject(apiError);
  }

  // =====================================
  // 🌐 HTTP METHODS 🌐
  // =====================================

  public async get<T = any>(url: string, config?: RequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.get(url, config);
      return this.transformResponse<T>(response);
    } catch (error) {
      throw error;
    }
  }

  public async post<T = any>(url: string, data?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.post(url, data, config);
      return this.transformResponse<T>(response);
    } catch (error) {
      throw error;
    }
  }

  public async put<T = any>(url: string, data?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.put(url, data, config);
      return this.transformResponse<T>(response);
    } catch (error) {
      throw error;
    }
  }

  public async patch<T = any>(url: string, data?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.patch(url, data, config);
      return this.transformResponse<T>(response);
    } catch (error) {
      throw error;
    }
  }

  public async delete<T = any>(url: string, config?: RequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.delete(url, config);
      return this.transformResponse<T>(response);
    } catch (error) {
      throw error;
    }
  }

  // =====================================
  // 🎸 LEGENDARY METHODS 🎸
  // =====================================

  public async founderRequest<T = any>(
    method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE',
    url: string,
    data?: any,
    config: RequestConfig = {}
  ): Promise<ApiResponse<T>> {
    if (!this.isFounder) {
      throw new Error('👑 Founder requests are only available for RICKROLL187!');
    }

    const founderConfig: RequestConfig = {
      ...config,
      founderRequest: true,
      legendaryTimeout: 120000, // 2 minutes for founder requests
      headers: {
        ...config.headers,
        'X-Founder-Priority': 'maximum',
        'X-Legendary-Request': 'true',
        'X-Swiss-Precision': 'infinite',
      },
    };

    console.log(`👑 Executing founder ${method} request: ${url}`);

    switch (method) {
      case 'GET':
        return this.get<T>(url, founderConfig);
      case 'POST':
        return this.post<T>(url, data, founderConfig);
      case 'PUT':
        return this.put<T>(url, data, founderConfig);
      case 'PATCH':
        return this.patch<T>(url, data, founderConfig);
      case 'DELETE':
        return this.delete<T>(url, founderConfig);
      default:
        throw new Error(`Unsupported method: ${method}`);
    }
  }

  public async legendaryBatchRequest<T = any>(
    requests: Array<{
      method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
      url: string;
      data?: any;
      config?: RequestConfig;
    }>
  ): Promise<ApiResponse<T>[]> {
    console.log(`🎸 Executing ${requests.length} legendary batch requests`);

    const promises = requests.map(request => {
      const config = {
        ...request.config,
        skipLoading: true, // Don't show loading for individual requests in batch
        legendaryTimeout: 60000, // 1 minute per request
      };

      switch (request.method) {
        case 'GET':
          return this.get<T>(request.url, config);
        case 'POST':
          return this.post<T>(request.url, request.data, config);
        case 'PUT':
          return this.put<T>(request.url, request.data, config);
        case 'PATCH':
          return this.patch<T>(request.url, request.data, config);
        case 'DELETE':
          return this.delete<T>(request.url, config);
        default:
          throw new Error(`Unsupported method: ${request.method}`);
      }
    });

    try {
      store.dispatch(setGlobalLoading({ 
        loading: true, 
        message: `Processing ${requests.length} legendary requests with Swiss precision...` 
      }));

      const results = await Promise.all(promises);
      
      console.log(`✅ Legendary batch completed: ${results.length} successful requests`);
      
      if (this.isFounder) {
        toast.success(`👑 Founder batch completed: ${results.length} requests processed with infinite energy!`, {
          duration: 4000,
          style: {
            background: 'linear-gradient(135deg, #FFD700, #FFA500)',
            color: '#000000',
            fontWeight: '700',
          },
        });
      } else {
        toast.success(`🎸 Legendary batch completed: ${results.length} requests with code bro energy!`);
      }

      return results;
    } catch (error) {
      console.error('🚨 Legendary batch request failed:', error);
      throw error;
    } finally {
      store.dispatch(setGlobalLoading({ loading: false }));
    }
  }

  // =====================================
  // 🔧 UTILITY METHODS 🔧
  // =====================================

  private transformResponse<T>(response: AxiosResponse): ApiResponse<T> {
    const apiResponse: ApiResponse<T> = {
      success: true,
      data: response.data?.data || response.data,
      message: response.data?.message,
      code: response.status,
      timestamp: response.data?.timestamp || new Date().toISOString(),
      requestId: response.headers['x-request-id'],
      founderData: response.data?.founderData,
      legendaryLevel: response.data?.legendaryLevel,
    };

    return apiResponse;
  }

  public setAuthToken(token: string): void {
    this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    console.log('🔐 Auth token set for API requests');
    
    if (this.isFounder) {
      console.log('👑 Founder auth token activated with legendary privileges!');
    }
  }

  public removeAuthToken(): void {
    delete this.client.defaults.headers.common['Authorization'];
    console.log('🔐 Auth token removed from API requests');
  }

  public getBaseURL(): string {
    return this.baseURL;
  }

  public getRequestCount(): number {
    return this.requestCount;
  }

  public getFounderRequestCount(): number {
    return this.founderRequestCount;
  }

  public isFounderService(): boolean {
    return this.isFounder;
  }

  // =====================================
  // 📊 MONITORING & DEBUGGING 📊
  // =====================================

  public getStats() {
    return {
      baseURL: this.baseURL,
      requestCount: this.requestCount,
      founderRequestCount: this.founderRequestCount,
      isFounder: this.isFounder,
      timestamp: new Date().toISOString(),
    };
  }

  public enableDebugMode(): void {
    this.client.interceptors.request.use(
      (config) => {
        console.log('🔍 Debug Request:', {
          method: config.method?.toUpperCase(),
          url: config.url,
          headers: config.headers,
          data: config.data,
        });
        return config;
      }
    );

    this.client.interceptors.response.use(
      (response) => {
        console.log('🔍 Debug Response:', {
          status: response.status,
          headers: response.headers,
          data: response.data,
        });
        return response;
      }
    );

    console.log('🔍 API debug mode enabled');
  }

  // =====================================
  // 🧹 CLEANUP 🧹
  // =====================================

  public destroy(): void {
    console.log('🧹 Destroying API service...');
    
    // Clear any pending requests
    if (this.client) {
      // Cancel any pending requests would go here if needed
    }
    
    console.log('✅ API service destroyed');
  }
}

// =====================================
// 🎸 EXPORT LEGENDARY API SERVICE 🎸
// =====================================

// Create singleton instance with Swiss precision
export const apiService = new LegendaryApiService();

// Export types
export type { ApiResponse, ApiError, RequestConfig };

// Export the service class for advanced usage
export { LegendaryApiService };

console.log('🎸🎸🎸 LEGENDARY API SERVICE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`API service completed at: 2025-08-06 15:23:44 UTC`);
console.log('🌐 HTTP communication: SWISS PRECISION');
console.log('👑 RICKROLL187 founder API: LEGENDARY');
console.log('📡 Request handling: MAXIMUM RELIABILITY');
console.log('🌅 Afternoon legendary energy: INFINITE AT 15:23:44!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
