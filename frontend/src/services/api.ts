// File: frontend/src/services/api.ts
/**
 * 🌐🎸 N3EXTPATH - LEGENDARY API SERVICE LAYER 🎸🌐
 * Professional API integration with Swiss precision
 * Built: 2025-08-05 18:19:29 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { toast } from 'react-toastify';

// Types and Interfaces
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  legendary?: boolean;
  swiss_precision?: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
  remember_me?: boolean;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
  expires_in: number;
  legendary_status?: boolean;
}

export interface User {
  user_id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  department: string;
  is_active: boolean;
  is_legendary?: boolean;
  permissions: string[];
  avatar_url?: string;
}

export interface PerformanceReview {
  review_id: string;
  user_id: string;
  reviewer_id: string;
  period_start: string;
  period_end: string;
  overall_score: number;
  goals_met: number;
  areas_for_improvement: string[];
  strengths: string[];
  comments: string;
  status: string;
  is_legendary?: boolean;
}

export interface OKR {
  okr_id: string;
  user_id: string;
  title: string;
  description: string;
  key_results: KeyResult[];
  progress: number;
  status: string;
  target_date: string;
  is_legendary?: boolean;
}

export interface KeyResult {
  key_result_id: string;
  title: string;
  target_value: number;
  current_value: number;
  unit: string;
  progress: number;
}

export interface DashboardData {
  user_stats: {
    total_users: number;
    active_users: number;
    legendary_users: number;
  };
  performance_metrics: {
    average_score: number;
    reviews_completed: number;
    improvement_trend: number;
  };
  okr_metrics: {
    total_okrs: number;
    completed_okrs: number;
    on_track_percentage: number;
  };
  legendary_metrics?: {
    rickroll187_status: string;
    swiss_precision_score: number;
    code_bro_energy: string;
  };
}

// API Configuration
const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'X-Client': 'N3EXTPATH-Frontend',
    'X-Version': '1.0.0',
    'X-Built-By': 'rickroll187',
    'X-Swiss-Precision': 'enabled',
    'X-Code-Bro-Energy': 'maximum'
  }
};

class LegendaryApiService {
  private api: AxiosInstance;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private isRefreshing = false;
  private failedQueue: Array<{
    resolve: (value?: any) => void;
    reject: (error?: any) => void;
  }> = [];

  constructor() {
    this.api = axios.create(API_CONFIG);
    this.setupInterceptors();
    this.loadTokensFromStorage();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.api.interceptors.request.use(
      (config: AxiosRequestConfig) => {
        // Add auth token if available
        if (this.accessToken) {
          config.headers = {
            ...config.headers,
            Authorization: `Bearer ${this.accessToken}`
          };
        }

        // Add legendary headers for legendary users
        const currentUser = this.getCurrentUser();
        if (currentUser?.is_legendary) {
          config.headers = {
            ...config.headers,
            'X-Legendary-User': 'true',
            'X-Legendary-Status': 'maximum',
            'X-Swiss-Precision': 'legendary'
          };
        }

        // Log request for debugging
        if (process.env.NODE_ENV === 'development') {
          console.log('🎸 API Request:', {
            method: config.method?.toUpperCase(),
            url: config.url,
            data: config.data,
            legendary: currentUser?.is_legendary || false
          });
        }

        return config;
      },
      (error: AxiosError) => {
        console.error('🚨 Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response: AxiosResponse) => {
        // Log successful responses
        if (process.env.NODE_ENV === 'development') {
          console.log('✅ API Response:', {
            status: response.status,
            url: response.config.url,
            data: response.data,
            legendary: response.headers['x-legendary-response'] === 'true'
          });
        }

        // Show legendary success messages
        if (response.headers['x-legendary-response'] === 'true') {
          toast.success('🎸 Legendary operation completed with Swiss precision! 🎸');
        }

        return response;
      },
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

        // Handle token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          if (this.isRefreshing) {
            // Wait for token refresh
            return new Promise((resolve, reject) => {
              this.failedQueue.push({ resolve, reject });
            }).then(token => {
              originalRequest.headers = {
                ...originalRequest.headers,
                Authorization: `Bearer ${token}`
              };
              return this.api(originalRequest);
            }).catch(err => {
              return Promise.reject(err);
            });
          }

          originalRequest._retry = true;
          this.isRefreshing = true;

          try {
            const newToken = await this.refreshAccessToken();
            this.processQueue(null, newToken);
            originalRequest.headers = {
              ...originalRequest.headers,
              Authorization: `Bearer ${newToken}`
            };
            return this.api(originalRequest);
          } catch (refreshError) {
            this.processQueue(refreshError, null);
            this.logout();
            return Promise.reject(refreshError);
          } finally {
            this.isRefreshing = false;
          }
        }

        // Handle other errors
        this.handleApiError(error);
        return Promise.reject(error);
      }
    );
  }

  private processQueue(error: any, token: string | null = null): void {
    this.failedQueue.forEach(({ resolve, reject }) => {
      if (error) {
        reject(error);
      } else {
        resolve(token);
      }
    });

    this.failedQueue = [];
  }

  private handleApiError(error: AxiosError): void {
    const response = error.response;
    const message = (response?.data as any)?.message || error.message;

    console.error('🚨 API Error:', {
      status: response?.status,
      message,
      url: error.config?.url
    });

    // Show error messages based on status
    switch (response?.status) {
      case 400:
        toast.error(`Bad Request: ${message}`);
        break;
      case 401:
        toast.error('Authentication required. Please log in.');
        break;
      case 403:
        toast.error('Access denied. Insufficient permissions.');
        break;
      case 404:
        toast.error('Resource not found.');
        break;
      case 429:
        toast.error('Too many requests. Please slow down.');
        break;
      case 500:
        toast.error('🚨 Server error. The legendary team is on it! 🚨');
        break;
      default:
        toast.error(`Error: ${message}`);
    }
  }

  private loadTokensFromStorage(): void {
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  private saveTokensToStorage(accessToken: string, refreshToken: string): void {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }

  private clearTokensFromStorage(): void {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  private async refreshAccessToken(): Promise<string> {
    if (!this.refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await axios.post(`${API_CONFIG.baseURL}/auth/refresh`, {
      refresh_token: this.refreshToken
    });

    const { access_token, refresh_token } = response.data;
    this.saveTokensToStorage(access_token, refresh_token);
    return access_token;
  }

  // Authentication Methods
  async login(credentials: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    try {
      const response = await this.api.post<LoginResponse>('/auth/login', credentials);
      const { access_token, refresh_token, user } = response.data;

      // Save tokens and user data
      this.saveTokensToStorage(access_token, refresh_token);
      localStorage.setItem('user', JSON.stringify(user));

      // Show legendary login message for legendary users
      if (user.is_legendary) {
        toast.success('🎸 LEGENDARY FOUNDER LOGIN SUCCESSFUL! Welcome back, RICKROLL187! 🎸');
      } else {
        toast.success(`Welcome back, ${user.first_name}!`);
      }

      return {
        success: true,
        data: response.data,
        legendary: user.is_legendary
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Login failed',
        message: 'Invalid credentials'
      };
    }
  }

  async logout(): Promise<void> {
    try {
      if (this.accessToken) {
        await this.api.post('/auth/logout');
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.clearTokensFromStorage();
      toast.info('Logged out successfully');
    }
  }

  async register(userData: any): Promise<ApiResponse<User>> {
    try {
      const response = await this.api.post<User>('/auth/register', userData);
      toast.success('Registration successful! Please check your email for verification.');
      
      return {
        success: true,
        data: response.data
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Registration failed'
      };
    }
  }

  // User Methods
  getCurrentUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  }

  async getUserProfile(userId?: string): Promise<ApiResponse<User>> {
    try {
      const url = userId ? `/users/${userId}` : '/users/me';
      const response = await this.api.get<User>(url);
      
      return {
        success: true,
        data: response.data,
        legendary: response.data.is_legendary
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch user profile'
      };
    }
  }

  async updateUserProfile(userId: string, userData: Partial<User>): Promise<ApiResponse<User>> {
    try {
      const response = await this.api.put<User>(`/users/${userId}`, userData);
      
      // Update local storage if it's current user
      const currentUser = this.getCurrentUser();
      if (currentUser && currentUser.user_id === userId) {
        localStorage.setItem('user', JSON.stringify(response.data));
      }

      toast.success('Profile updated successfully!');
      
      return {
        success: true,
        data: response.data,
        legendary: response.data.is_legendary
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to update profile'
      };
    }
  }

  // Dashboard Methods
  async getDashboardData(): Promise<ApiResponse<DashboardData>> {
    try {
      const response = await this.api.get<DashboardData>('/dashboard');
      
      return {
        success: true,
        data: response.data,
        legendary: !!response.data.legendary_metrics,
        swiss_precision: true
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch dashboard data'
      };
    }
  }

  // Performance Review Methods
  async getPerformanceReviews(userId?: string): Promise<ApiResponse<PerformanceReview[]>> {
    try {
      const url = userId ? `/performance/reviews?user_id=${userId}` : '/performance/reviews';
      const response = await this.api.get<PerformanceReview[]>(url);
      
      return {
        success: true,
        data: response.data
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch performance reviews'
      };
    }
  }

  async createPerformanceReview(reviewData: Partial<PerformanceReview>): Promise<ApiResponse<PerformanceReview>> {
    try {
      const response = await this.api.post<PerformanceReview>('/performance/reviews', reviewData);
      
      toast.success('Performance review created successfully!');
      
      return {
        success: true,
        data: response.data,
        legendary: response.data.is_legendary
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to create performance review'
      };
    }
  }

  async updatePerformanceReview(reviewId: string, reviewData: Partial<PerformanceReview>): Promise<ApiResponse<PerformanceReview>> {
    try {
      const response = await this.api.put<PerformanceReview>(`/performance/reviews/${reviewId}`, reviewData);
      
      toast.success('Performance review updated successfully!');
      
      return {
        success: true,
        data: response.data,
        legendary: response.data.is_legendary
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to update performance review'
      };
    }
  }

  // OKR Methods
  async getOKRs(userId?: string): Promise<ApiResponse<OKR[]>> {
    try {
      const url = userId ? `/okrs?user_id=${userId}` : '/okrs';
      const response = await this.api.get<OKR[]>(url);
      
      return {
        success: true,
        data: response.data
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch OKRs'
      };
    }
  }

  async createOKR(okrData: Partial<OKR>): Promise<ApiResponse<OKR>> {
    try {
      const response = await this.api.post<OKR>('/okrs', okrData);
      
      toast.success('OKR created successfully!');
      
      return {
        success: true,
        data: response.data,
        legendary: response.data.is_legendary
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to create OKR'
      };
    }
  }

  async updateOKR(okrId: string, okrData: Partial<OKR>): Promise<ApiResponse<OKR>> {
    try {
      const response = await this.api.put<OKR>(`/okrs/${okrId}`, okrData);
      
      toast.success('OKR updated successfully!');
      
      return {
        success: true,
        data: response.data,
        legendary: response.data.is_legendary
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to update OKR'
      };
    }
  }

  async deleteOKR(okrId: string): Promise<ApiResponse<void>> {
    try {
      await this.api.delete(`/okrs/${okrId}`);
      
      toast.success('OKR deleted successfully!');
      
      return {
        success: true
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to delete OKR'
      };
    }
  }

  // Team Methods
  async getTeams(): Promise<ApiResponse<any[]>> {
    try {
      const response = await this.api.get('/teams');
      
      return {
        success: true,
        data: response.data
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch teams'
      };
    }
  }

  async getTeamMembers(teamId: string): Promise<ApiResponse<User[]>> {
    try {
      const response = await this.api.get<User[]>(`/teams/${teamId}/members`);
      
      return {
        success: true,
        data: response.data
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch team members'
      };
    }
  }

  // Analytics Methods
  async getAnalytics(timeframe?: string): Promise<ApiResponse<any>> {
    try {
      const url = timeframe ? `/analytics?timeframe=${timeframe}` : '/analytics';
      const response = await this.api.get(url);
      
      return {
        success: true,
        data: response.data,
        swiss_precision: true
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch analytics data'
      };
    }
  }

  // Notification Methods
  async getNotifications(): Promise<ApiResponse<any[]>> {
    try {
      const response = await this.api.get('/notifications');
      
      return {
        success: true,
        data: response.data
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch notifications'
      };
    }
  }

  async markNotificationRead(notificationId: string): Promise<ApiResponse<void>> {
    try {
      await this.api.put(`/notifications/${notificationId}/read`);
      
      return {
        success: true
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to mark notification as read'
      };
    }
  }

  // File Upload Methods
  async uploadFile(file: File, type: string = 'general'): Promise<ApiResponse<{ url: string; filename: string }>> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', type);

      const response = await this.api.post('/files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      toast.success('File uploaded successfully!');

      return {
        success: true,
        data: response.data
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to upload file'
      };
    }
  }

  // Utility Methods
  isAuthenticated(): boolean {
    return !!this.accessToken && !!this.getCurrentUser();
  }

  isLegendaryUser(): boolean {
    const user = this.getCurrentUser();
    return user?.is_legendary === true;
  }

  getApiUrl(endpoint: string): string {
    return `${API_CONFIG.baseURL}${endpoint}`;
  }
}

// Create and export singleton instance
export const apiService = new LegendaryApiService();

// Export types
export type {
  User,
  PerformanceReview,
  OKR,
  KeyResult,
  DashboardData,
  LoginRequest,
  LoginResponse,
  ApiResponse
};

// Legendary startup message
if (process.env.NODE_ENV === 'development') {
  console.log('🎸🎸🎸 LEGENDARY API SERVICE INITIALIZED! 🎸🎸🎸');
  console.log('Built with Swiss precision by RICKROLL187!');
  console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
  console.log(`API Base URL: ${API_CONFIG.baseURL}`);
  console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
}
