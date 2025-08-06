// File: web/src/store/slices/authSlice.ts
/**
 * 🔐🎸 N3EXTPATH - LEGENDARY AUTH SLICE 🎸🔐
 * Professional authentication state with Swiss precision
 * Built: 2025-08-06 13:23:07 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { User } from '@/hooks/useAuth';

// =====================================
// 🔐 AUTH STATE INTERFACE 🔐
// =====================================

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  loginAttempts: number;
  lastLoginAttempt: Date | null;
  sessionExpiry: Date | null;
  preferences: {
    rememberMe: boolean;
    biometricEnabled: boolean;
    twoFactorEnabled: boolean;
  };
}

// =====================================
// 🎸 INITIAL LEGENDARY STATE 🎸
// =====================================

const initialState: AuthState = {
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  loginAttempts: 0,
  lastLoginAttempt: null,
  sessionExpiry: null,
  preferences: {
    rememberMe: false,
    biometricEnabled: false,
    twoFactorEnabled: false,
  },
};

// =====================================
// 🎸 LEGENDARY ASYNC THUNKS 🎸
// =====================================

export const loginAsync = createAsyncThunk(
  'auth/loginAsync',
  async (credentials: { email: string; password: string; rememberMe?: boolean }, { rejectWithValue }) => {
    try {
      console.log('🔐 Async login attempt...');
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Special handling for RICKROLL187 founder
      if (credentials.email === 'letstalktech010@gmail.com' || 
          credentials.email.toLowerCase().includes('rickroll187')) {
        
        const founderUser: User = {
          id: 'founder-rickroll187',
          username: 'rickroll187',
          email: 'letstalktech010@gmail.com',
          firstName: 'RICKROLL187',
          lastName: '',
          jobTitle: 'Legendary Founder & Chief Code Bro',
          department: 'Executive Leadership',
          isFounder: true,
          is_legendary: true,
          swissPrecisionScore: 100,
          codeBroEnergy: 10,
          profileImage: 'https://ui-avatars.com/api/?name=RICKROLL187&background=FFD700&color=000&size=200&bold=true',
          achievements: [
            '👑 Platform Founder',
            '🎸 Legendary Code Bro Master',
            '⚙️ Swiss Precision Architect',
            '🚀 Infinite Energy Source',
            '💎 Ultimate Achievement Unlocked',
          ],
          joinedAt: new Date('2025-01-01'),
          lastLogin: new Date(),
          preferences: {
            theme: 'auto',
            notifications: true,
            language: 'en',
          },
        };

        return {
          user: founderUser,
          token: 'legendary-founder-token-' + Date.now(),
          refreshToken: 'legendary-founder-refresh-' + Date.now(),
          sessionExpiry: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
        };
      }
      
      // Regular user login simulation
      const regularUser: User = {
        id: 'user-' + Date.now(),
        username: credentials.email.split('@')[0],
        email: credentials.email,
        firstName: 'John',
        lastName: 'Doe',
        jobTitle: 'Software Developer',
        department: 'Engineering',
        isFounder: false,
        is_legendary: Math.random() > 0.5,
        swissPrecisionScore: Math.floor(Math.random() * 30) + 70,
        codeBroEnergy: Math.floor(Math.random() * 3) + 7,
        profileImage: `https://ui-avatars.com/api/?name=${credentials.email.split('@')[0]}&background=1E90FF&color=fff&size=200`,
        achievements: [
          '🎸 Code Bro Initiate',
          '⚙️ Swiss Precision Apprentice',
          '📊 Performance Tracker',
        ],
        joinedAt: new Date('2025-06-01'),
        lastLogin: new Date(),
        preferences: {
          theme: 'auto',
          notifications: true,
          language: 'en',
        },
      };

      return {
        user: regularUser,
        token: 'regular-user-token-' + Date.now(),
        refreshToken: 'regular-user-refresh-' + Date.now(),
        sessionExpiry: new Date(Date.now() + 8 * 60 * 60 * 1000), // 8 hours
      };
      
    } catch (error) {
      console.error('🚨 Login async error:', error);
      return rejectWithValue(error instanceof Error ? error.message : 'Login failed');
    }
  }
);

export const refreshTokenAsync = createAsyncThunk(
  'auth/refreshTokenAsync',
  async (refreshToken: string, { rejectWithValue }) => {
    try {
      console.log('🔄 Refreshing token...');
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      
      return {
        token: 'refreshed-token-' + Date.now(),
        refreshToken: 'refreshed-refresh-token-' + Date.now(),
        sessionExpiry: new Date(Date.now() + 8 * 60 * 60 * 1000),
      };
      
    } catch (error) {
      console.error('🚨 Token refresh error:', error);
      return rejectWithValue('Token refresh failed');
    }
  }
);

// =====================================
// 🎸 LEGENDARY AUTH SLICE 🎸
// =====================================

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // Set user and tokens (for direct login)
    setUser: (state, action: PayloadAction<{
      user: User;
      token: string;
      refreshToken: string;
    }>) => {
      const { user, token, refreshToken } = action.payload;
      state.user = user;
      state.token = token;
      state.refreshToken = refreshToken;
      state.isAuthenticated = true;
      state.isLoading = false;
      state.error = null;
      state.loginAttempts = 0;
      state.sessionExpiry = new Date(Date.now() + (user.isFounder ? 24 : 8) * 60 * 60 * 1000);
      
      console.log(`✅ User set in state: ${user.isFounder ? '👑 FOUNDER' : '🎸 USER'} ${user.firstName}`);
    },
    
    // Logout user
    logout: (state) => {
      console.log('🚪 Logging out user...');
      
      state.user = null;
      state.token = null;
      state.refreshToken = null;
      state.isAuthenticated = false;
      state.isLoading = false;
      state.error = null;
      state.sessionExpiry = null;
      
      console.log('✅ User logged out successfully');
    },
    
    // Clear auth error
    clearError: (state) => {
      state.error = null;
    },
    
    // Update user profile
    updateUserProfile: (state, action: PayloadAction<Partial<User>>) => {
      if (state.user) {
        state.user = { ...state.user, ...action.payload };
        console.log('✅ User profile updated');
      }
    },
    
    // Update auth preferences
    updatePreferences: (state, action: PayloadAction<Partial<AuthState['preferences']>>) => {
      state.preferences = { ...state.preferences, ...action.payload };
      console.log('✅ Auth preferences updated');
    },
    
    // Increment login attempts
    incrementLoginAttempts: (state) => {
      state.loginAttempts += 1;
      state.lastLoginAttempt = new Date();
      
      if (state.loginAttempts >= 5) {
        state.error = 'Too many login attempts. Please try again later.';
        console.log('🚨 Too many login attempts detected');
      }
    },
    
    // Reset login attempts
    resetLoginAttempts: (state) => {
      state.loginAttempts = 0;
      state.lastLoginAttempt = null;
    },
    
    // Set loading state
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    
    // Check session expiry
    checkSessionExpiry: (state) => {
      if (state.sessionExpiry && new Date() > new Date(state.sessionExpiry)) {
        console.log('⏰ Session expired, logging out...');
        // Reset state like logout
        state.user = null;
        state.token = null;
        state.refreshToken = null;
        state.isAuthenticated = false;
        state.sessionExpiry = null;
        state.error = 'Session expired. Please log in again.';
      }
    },
  },
  
  // =====================================
  // 🎸 ASYNC THUNK HANDLERS 🎸
  // =====================================
  
  extraReducers: (builder) => {
    // Login async handlers
    builder
      .addCase(loginAsync.pending, (state) => {
        state.isLoading = true;
        state.error = null;
        console.log('🔄 Login in progress...');
      })
      .addCase(loginAsync.fulfilled, (state, action) => {
        const { user, token, refreshToken, sessionExpiry } = action.payload;
        
        state.user = user;
        state.token = token;
        state.refreshToken = refreshToken;
        state.isAuthenticated = true;
        state.isLoading = false;
        state.error = null;
        state.loginAttempts = 0;
        state.sessionExpiry = sessionExpiry;
        
        // Store tokens in localStorage
        localStorage.setItem('legendary_token', token);
        localStorage.setItem('legendary_refresh_token', refreshToken);
        
        console.log(`✅ Login successful: ${user.isFounder ? '👑 FOUNDER' : '🎸 USER'} ${user.firstName}`);
      })
      .addCase(loginAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string || 'Login failed';
        state.loginAttempts += 1;
        state.lastLoginAttempt = new Date();
        
        console.log(`🚨 Login failed: ${state.error}`);
      });
    
    // Token refresh async handlers
    builder
      .addCase(refreshTokenAsync.pending, (state) => {
        console.log('🔄 Token refresh in progress...');
      })
      .addCase(refreshTokenAsync.fulfilled, (state, action) => {
        const { token, refreshToken, sessionExpiry } = action.payload;
        
        state.token = token;
        state.refreshToken = refreshToken;
        state.sessionExpiry = sessionExpiry;
        
        // Update tokens in localStorage
        localStorage.setItem('legendary_token', token);
        localStorage.setItem('legendary_refresh_token', refreshToken);
        
        console.log('✅ Token refreshed successfully');
      })
      .addCase(refreshTokenAsync.rejected, (state, action) => {
        console.log('🚨 Token refresh failed, logging out...');
        
        // Clear everything on refresh failure
        state.user = null;
        state.token = null;
        state.refreshToken = null;
        state.isAuthenticated = false;
        state.sessionExpiry = null;
        state.error = 'Session expired. Please log in again.';
        
        // Clear localStorage
        localStorage.removeItem('legendary_token');
        localStorage.removeItem('legendary_refresh_token');
      });
  },
});

// =====================================
// 🎸 EXPORT LEGENDARY ACTIONS & REDUCER 🎸
// =====================================

export const {
  setUser,
  logout,
  clearError,
  updateUserProfile,
  updatePreferences,
  incrementLoginAttempts,
  resetLoginAttempts,
  setLoading,
  checkSessionExpiry,
} = authSlice.actions;

export default authSlice.reducer;

console.log('🎸🎸🎸 LEGENDARY AUTH SLICE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Auth slice completed at: 2025-08-06 13:23:07 UTC`);
console.log('🔐 Authentication state: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('⚡ Async operations: MAXIMUM RELIABILITY');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
