// File: web/src/hooks/useAuth.ts
/**
 * 🔐🎸 N3EXTPATH - LEGENDARY AUTHENTICATION HOOK 🎸🔐
 * Professional authentication with Swiss precision
 * Built: 2025-08-06 13:23:07 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { useSelector, useDispatch } from 'react-redux';
import { useCallback, useEffect } from 'react';
import toast from 'react-hot-toast';
import { RootState } from '@/store';
import { login, logout, register, refreshToken, setUser } from '@/store/slices/authSlice';
import { authService } from '@/services/authService';

// =====================================
// 🔐 AUTH TYPES 🔐
// =====================================

export interface User {
  id: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  jobTitle?: string;
  department?: string;
  isFounder: boolean;
  is_legendary: boolean;
  swissPrecisionScore: number;
  codeBroEnergy: number;
  profileImage?: string;
  achievements: string[];
  joinedAt: Date;
  lastLogin: Date;
  preferences: {
    theme: 'light' | 'dark' | 'auto';
    notifications: boolean;
    language: string;
  };
}

export interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  jobTitle?: string;
  department?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

// =====================================
// 🎸 LEGENDARY AUTH HOOK 🎸
// =====================================

export function useAuth() {
  const dispatch = useDispatch();
  const authState = useSelector((state: RootState) => state.auth);
  
  const { user, token, isAuthenticated, isLoading, error } = authState;
  
  // Check if user is RICKROLL187 founder
  const isFounder = user?.username === 'rickroll187' || user?.isFounder;
  const isLegendary = user?.is_legendary || isFounder;

  useEffect(() => {
    console.log('🔐🎸🔐 LEGENDARY AUTH HOOK INITIALIZED! 🔐🎸🔐');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`Auth hook initialized at: 2025-08-06 13:23:07 UTC`);
    
    if (isFounder) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER AUTH ACTIVATED! 👑🎸👑');
      console.log('🚀 INFINITE AUTHENTICATION POWER!');
      console.log('⚙️ SWISS PRECISION SECURITY!');
    }

    // Auto-refresh token on app load
    const storedToken = localStorage.getItem('legendary_token');
    const storedRefreshToken = localStorage.getItem('legendary_refresh_token');
    
    if (storedToken && storedRefreshToken && !isAuthenticated) {
      console.log('🔄 Auto-refreshing authentication...');
      handleRefreshToken();
    }
  }, [isFounder, isAuthenticated]);

  // =====================================
  // 🎸 AUTH ACTIONS 🎸
  // =====================================

  const handleLogin = useCallback(async (credentials: LoginCredentials) => {
    try {
      console.log('🔐 Attempting legendary login...');
      
      // Special handling for RICKROLL187 founder
      if (credentials.email === 'letstalktech010@gmail.com' || 
          credentials.email.toLowerCase().includes('rickroll187')) {
        console.log('👑 RICKROLL187 FOUNDER LOGIN DETECTED!');
        
        // Mock founder user (in real app, this comes from API)
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

        dispatch(setUser({
          user: founderUser,
          token: 'legendary-founder-token-' + Date.now(),
          refreshToken: 'legendary-founder-refresh-' + Date.now(),
        }));

        // Store tokens
        localStorage.setItem('legendary_token', 'legendary-founder-token-' + Date.now());
        localStorage.setItem('legendary_refresh_token', 'legendary-founder-refresh-' + Date.now());

        toast.success('👑 Welcome back, RICKROLL187! Infinite code bro energy activated!', {
          duration: 5000,
          style: {
            background: 'linear-gradient(135deg, #FFD700, #FFA500)',
            color: '#000000',
            fontWeight: '700',
          },
        });

        console.log('✅ LEGENDARY FOUNDER LOGIN SUCCESSFUL!');
        return { success: true, user: founderUser };
      }
      
      // Regular user login (mock implementation - in real app, call API)
      const regularUser: User = {
        id: 'user-' + Date.now(),
        username: credentials.email.split('@')[0],
        email: credentials.email,
        firstName: 'John',
        lastName: 'Doe',
        jobTitle: 'Software Developer',
        department: 'Engineering',
        isFounder: false,
        is_legendary: Math.random() > 0.5, // Random legendary status
        swissPrecisionScore: Math.floor(Math.random() * 30) + 70, // 70-100
        codeBroEnergy: Math.floor(Math.random() * 3) + 7, // 7-10
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

      dispatch(setUser({
        user: regularUser,
        token: 'regular-user-token-' + Date.now(),
        refreshToken: 'regular-user-refresh-' + Date.now(),
      }));

      // Store tokens
      localStorage.setItem('legendary_token', 'regular-user-token-' + Date.now());
      localStorage.setItem('legendary_refresh_token', 'regular-user-refresh-' + Date.now());

      toast.success(`🎸 Welcome back, ${regularUser.firstName}! Ready for legendary performance?`, {
        duration: 4000,
      });

      console.log('✅ User login successful!');
      return { success: true, user: regularUser };
      
    } catch (error) {
      console.error('🚨 Login error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Login failed';
      
      toast.error(`🚨 Login failed: ${errorMessage}`, {
        duration: 4000,
      });
      
      return { success: false, error: errorMessage };
    }
  }, [dispatch]);

  const handleRegister = useCallback(async (userData: RegisterData) => {
    try {
      console.log('📝 Attempting legendary registration...');
      
      // Mock registration (in real app, call API)
      const newUser: User = {
        id: 'user-' + Date.now(),
        username: userData.email.split('@')[0],
        email: userData.email,
        firstName: userData.firstName,
        lastName: userData.lastName,
        jobTitle: userData.jobTitle || 'Team Member',
        department: userData.department || 'General',
        isFounder: false,
        is_legendary: false, // New users start as regular
        swissPrecisionScore: 75, // Starting score
        codeBroEnergy: 7, // Starting energy
        profileImage: `https://ui-avatars.com/api/?name=${userData.firstName}+${userData.lastName}&background=6c757d&color=fff&size=200`,
        achievements: [
          '🎉 Welcome to N3EXTPATH!',
          '📝 Profile Completed',
        ],
        joinedAt: new Date(),
        lastLogin: new Date(),
        preferences: {
          theme: 'auto',
          notifications: true,
          language: 'en',
        },
      };

      dispatch(setUser({
        user: newUser,
        token: 'new-user-token-' + Date.now(),
        refreshToken: 'new-user-refresh-' + Date.now(),
      }));

      // Store tokens
      localStorage.setItem('legendary_token', 'new-user-token-' + Date.now());
      localStorage.setItem('legendary_refresh_token', 'new-user-refresh-' + Date.now());

      toast.success(`🎉 Welcome to N3EXTPATH, ${newUser.firstName}! Your legendary journey begins now!`, {
        duration: 5000,
      });

      console.log('✅ User registration successful!');
      return { success: true, user: newUser };
      
    } catch (error) {
      console.error('🚨 Registration error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Registration failed';
      
      toast.error(`🚨 Registration failed: ${errorMessage}`, {
        duration: 4000,
      });
      
      return { success: false, error: errorMessage };
    }
  }, [dispatch]);

  const handleLogout = useCallback(async () => {
    try {
      console.log('🚪 Logging out...');
      
      // Clear tokens
      localStorage.removeItem('legendary_token');
      localStorage.removeItem('legendary_refresh_token');
      
      dispatch(logout());
      
      toast.success('👋 Logged out successfully! See you soon, code bro!', {
        duration: 3000,
      });
      
      console.log('✅ Logout successful!');
      
    } catch (error) {
      console.error('🚨 Logout error:', error);
      toast.error('🚨 Logout failed. Please try again.');
    }
  }, [dispatch]);

  const handleRefreshToken = useCallback(async () => {
    try {
      console.log('🔄 Refreshing authentication token...');
      
      const storedRefreshToken = localStorage.getItem('legendary_refresh_token');
      if (!storedRefreshToken) {
        throw new Error('No refresh token available');
      }
      
      // Mock token refresh (in real app, call API)
      const newToken = 'refreshed-token-' + Date.now();
      const newRefreshToken = 'refreshed-refresh-token-' + Date.now();
      
      localStorage.setItem('legendary_token', newToken);
      localStorage.setItem('legendary_refresh_token', newRefreshToken);
      
      // In a real app, you would also refresh user data here
      console.log('✅ Token refreshed successfully!');
      
      return { success: true, token: newToken };
      
    } catch (error) {
      console.error('🚨 Token refresh failed:', error);
      handleLogout(); // Force logout on refresh failure
      return { success: false, error: 'Session expired' };
    }
  }, [dispatch, handleLogout]);

  const updateUser = useCallback(async (updates: Partial<User>) => {
    try {
      console.log('🔄 Updating user profile...');
      
      if (!user) {
        throw new Error('No user to update');
      }
      
      const updatedUser = { ...user, ...updates };
      
      dispatch(setUser({
        user: updatedUser,
        token,
        refreshToken: authState.refreshToken,
      }));
      
      toast.success('✅ Profile updated with Swiss precision!', {
        duration: 3000,
      });
      
      console.log('✅ User profile updated!');
      return { success: true, user: updatedUser };
      
    } catch (error) {
      console.error('🚨 Profile update error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Profile update failed';
      
      toast.error(`🚨 Profile update failed: ${errorMessage}`, {
        duration: 4000,
      });
      
      return { success: false, error: errorMessage };
    }
  }, [user, token, authState.refreshToken, dispatch]);

  // =====================================
  // 🎸 RETURN LEGENDARY AUTH INTERFACE 🎸
  // =====================================

  return {
    // State
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    isFounder,
    isLegendary,
    
    // Actions
    login: handleLogin,
    register: handleRegister,
    logout: handleLogout,
    refreshToken: handleRefreshToken,
    updateUser,
    
    // Utilities
    hasPermission: useCallback((permission: string) => {
      if (isFounder) return true; // Founder has all permissions
      if (isLegendary && ['read', 'write'].includes(permission)) return true;
      return ['read'].includes(permission); // Regular users have read permission
    }, [isFounder, isLegendary]),
    
    getUserDisplayName: useCallback(() => {
      if (!user) return 'Guest';
      if (isFounder) return `👑 ${user.firstName}`;
      if (isLegendary) return `🎸 ${user.firstName} ${user.lastName}`;
      return `${user.firstName} ${user.lastName}`;
    }, [user, isFounder, isLegendary]),
    
    getGreeting: useCallback(() => {
      if (!user) return 'Welcome to N3EXTPATH!';
      if (isFounder) return `Welcome back, legendary founder ${user.firstName}! 👑`;
      if (isLegendary) return `Welcome back, ${user.firstName}! Ready for legendary performance? 🎸`;
      return `Welcome back, ${user.firstName}! Let's achieve Swiss precision! ⚙️`;
    }, [user, isFounder, isLegendary]),
  };
}

console.log('🎸🎸🎸 LEGENDARY AUTH HOOK COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Auth hook completed at: 2025-08-06 13:23:07 UTC`);
console.log('🔐 Authentication: SWISS PRECISION SECURITY');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('🎸 Code bro authentication: MAXIMUM ENERGY');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
