// File: web/src/store/slices/uiSlice.ts
/**
 * 🎨🎸 N3EXTPATH - LEGENDARY UI SLICE 🎸🎨
 * Professional UI state management with Swiss precision
 * Built: 2025-08-06 14:41:34 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// =====================================
// 🎨 UI STATE INTERFACE 🎨
// =====================================

interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info' | 'legendary' | 'founder';
  title: string;
  message: string;
  duration?: number;
  isVisible: boolean;
  timestamp: Date;
}

interface Modal {
  id: string;
  type: 'confirmation' | 'info' | 'form' | 'legendary' | 'founder';
  title: string;
  content: string;
  isOpen: boolean;
  data?: any;
  onConfirm?: string; // Action type to dispatch
  onCancel?: string;  // Action type to dispatch
}

interface UIState {
  // Theme and appearance
  theme: 'light' | 'dark' | 'auto';
  sidebarOpen: boolean;
  sidebarCollapsed: boolean;
  
  // Loading states
  globalLoading: boolean;
  pageLoading: boolean;
  loadingMessage: string;
  
  // Toasts
  toasts: Toast[];
  maxToasts: number;
  
  // Modals
  modals: Modal[];
  
  // Notifications
  notificationsPanelOpen: boolean;
  unreadNotificationsCount: number;
  
  // Search
  searchQuery: string;
  searchResults: any[];
  searchLoading: boolean;
  
  // Legendary features
  founderMode: boolean;
  legendaryAnimations: boolean;
  codeBroEnergy: number;
  swissPrecisionMode: boolean;
  
  // Layout preferences
  compactMode: boolean;
  showWelcomeMessage: boolean;
  lastVisited: Date | null;
  
  // Performance
  animationsEnabled: boolean;
  reducedMotion: boolean;
}

// =====================================
// 🎸 INITIAL LEGENDARY STATE 🎸
// =====================================

const initialState: UIState = {
  // Theme and appearance
  theme: 'auto',
  sidebarOpen: false,
  sidebarCollapsed: false,
  
  // Loading states
  globalLoading: false,
  pageLoading: false,
  loadingMessage: '',
  
  // Toasts
  toasts: [],
  maxToasts: 5,
  
  // Modals
  modals: [],
  
  // Notifications
  notificationsPanelOpen: false,
  unreadNotificationsCount: 0,
  
  // Search
  searchQuery: '',
  searchResults: [],
  searchLoading: false,
  
  // Legendary features
  founderMode: false,
  legendaryAnimations: true,
  codeBroEnergy: 8,
  swissPrecisionMode: true,
  
  // Layout preferences
  compactMode: false,
  showWelcomeMessage: true,
  lastVisited: null,
  
  // Performance
  animationsEnabled: true,
  reducedMotion: false,
};

// =====================================
// 🎸 LEGENDARY UI SLICE 🎸
// =====================================

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    // =====================================
    // 🎨 THEME & APPEARANCE 🎨
    // =====================================
    
    setTheme: (state, action: PayloadAction<'light' | 'dark' | 'auto'>) => {
      state.theme = action.payload;
      console.log(`🎨 Theme changed to: ${action.payload}`);
    },
    
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
      console.log(`📋 Sidebar ${state.sidebarOpen ? 'opened' : 'closed'}`);
    },
    
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },
    
    toggleSidebarCollapse: (state) => {
      state.sidebarCollapsed = !state.sidebarCollapsed;
      console.log(`📋 Sidebar ${state.sidebarCollapsed ? 'collapsed' : 'expanded'}`);
    },
    
    // =====================================
    // ⏳ LOADING STATES ⏳
    // =====================================
    
    setGlobalLoading: (state, action: PayloadAction<{ loading: boolean; message?: string }>) => {
      state.globalLoading = action.payload.loading;
      state.loadingMessage = action.payload.message || '';
      
      if (action.payload.loading) {
        console.log(`⏳ Global loading started: ${action.payload.message || 'Loading...'}`);
      } else {
        console.log('✅ Global loading completed');
      }
    },
    
    setPageLoading: (state, action: PayloadAction<boolean>) => {
      state.pageLoading = action.payload;
    },
    
    // =====================================
    // 🍞 TOAST MANAGEMENT 🍞
    // =====================================
    
    addToast: (state, action: PayloadAction<Omit<Toast, 'id' | 'isVisible' | 'timestamp'>>) => {
      const toast: Toast = {
        id: `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        isVisible: true,
        timestamp: new Date(),
        duration: 4000,
        ...action.payload,
      };
      
      state.toasts.unshift(toast);
      
      // Keep only max toasts
      if (state.toasts.length > state.maxToasts) {
        state.toasts = state.toasts.slice(0, state.maxToasts);
      }
      
      console.log(`🍞 Toast added: ${toast.type} - ${toast.title}`);
    },
    
    removeToast: (state, action: PayloadAction<string>) => {
      state.toasts = state.toasts.filter(toast => toast.id !== action.payload);
      console.log(`🗑️ Toast removed: ${action.payload}`);
    },
    
    hideToast: (state, action: PayloadAction<string>) => {
      const toast = state.toasts.find(t => t.id === action.payload);
      if (toast) {
        toast.isVisible = false;
      }
    },
    
    clearAllToasts: (state) => {
      state.toasts = [];
      console.log('🧹 All toasts cleared');
    },
    
    // =====================================
    // 🎭 MODAL MANAGEMENT 🎭
    // =====================================
    
    openModal: (state, action: PayloadAction<Omit<Modal, 'id' | 'isOpen'>>) => {
      const modal: Modal = {
        id: `modal-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        isOpen: true,
        ...action.payload,
      };
      
      state.modals.push(modal);
      console.log(`🎭 Modal opened: ${modal.type} - ${modal.title}`);
    },
    
    closeModal: (state, action: PayloadAction<string>) => {
      const modalIndex = state.modals.findIndex(modal => modal.id === action.payload);
      if (modalIndex !== -1) {
        state.modals[modalIndex].isOpen = false;
        console.log(`🎭 Modal closed: ${action.payload}`);
      }
    },
    
    removeModal: (state, action: PayloadAction<string>) => {
      state.modals = state.modals.filter(modal => modal.id !== action.payload);
    },
    
    closeAllModals: (state) => {
      state.modals.forEach(modal => modal.isOpen = false);
      console.log('🎭 All modals closed');
    },
    
    // =====================================
    // 🔔 NOTIFICATIONS 🔔
    // =====================================
    
    toggleNotificationsPanel: (state) => {
      state.notificationsPanelOpen = !state.notificationsPanelOpen;
      console.log(`🔔 Notifications panel ${state.notificationsPanelOpen ? 'opened' : 'closed'}`);
    },
    
    setNotificationsPanelOpen: (state, action: PayloadAction<boolean>) => {
      state.notificationsPanelOpen = action.payload;
    },
    
    setUnreadNotificationsCount: (state, action: PayloadAction<number>) => {
      state.unreadNotificationsCount = Math.max(0, action.payload);
    },
    
    incrementUnreadNotifications: (state, action: PayloadAction<number>) => {
      state.unreadNotificationsCount += action.payload || 1;
    },
    
    decrementUnreadNotifications: (state, action: PayloadAction<number>) => {
      state.unreadNotificationsCount = Math.max(0, state.unreadNotificationsCount - (action.payload || 1));
    },
    
    // =====================================
    // 🔍 SEARCH 🔍
    // =====================================
    
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
    },
    
    setSearchResults: (state, action: PayloadAction<any[]>) => {
      state.searchResults = action.payload;
    },
    
    setSearchLoading: (state, action: PayloadAction<boolean>) => {
      state.searchLoading = action.payload;
    },
    
    clearSearch: (state) => {
      state.searchQuery = '';
      state.searchResults = [];
      state.searchLoading = false;
      console.log('🔍 Search cleared');
    },
    
    // =====================================
    // 👑 LEGENDARY FEATURES 👑
    // =====================================
    
    setFounderMode: (state, action: PayloadAction<boolean>) => {
      state.founderMode = action.payload;
      
      if (action.payload) {
        console.log('👑🎸👑 RICKROLL187 FOUNDER MODE ACTIVATED! 👑🎸👑');
        console.log('🚀 LEGENDARY FOUNDER UI WITH INFINITE CODE BRO ENERGY!');
        console.log('⚙️ SWISS PRECISION FOUNDER INTERFACE!');
        console.log('🌅 AFTERNOON FOUNDER UI POWER AT 14:41:34!');
        
        // Activate all legendary features for founder
        state.legendaryAnimations = true;
        state.codeBroEnergy = 10; // Maximum energy
        state.swissPrecisionMode = true;
        state.animationsEnabled = true;
      } else {
        console.log('👑 Founder mode deactivated');
      }
    },
    
    setLegendaryAnimations: (state, action: PayloadAction<boolean>) => {
      state.legendaryAnimations = action.payload;
      console.log(`✨ Legendary animations ${action.payload ? 'enabled' : 'disabled'}`);
    },
    
    setCodeBroEnergy: (state, action: PayloadAction<number>) => {
      state.codeBroEnergy = Math.max(0, Math.min(10, action.payload));
      console.log(`🎸 Code bro energy set to: ${state.codeBroEnergy}/10`);
    },
    
    incrementCodeBroEnergy: (state, action: PayloadAction<number>) => {
      const increment = action.payload || 1;
      state.codeBroEnergy = Math.min(10, state.codeBroEnergy + increment);
      console.log(`🎸 Code bro energy increased to: ${state.codeBroEnergy}/10`);
    },
    
    setSwissPrecisionMode: (state, action: PayloadAction<boolean>) => {
      state.swissPrecisionMode = action.payload;
      console.log(`⚙️ Swiss precision mode ${action.payload ? 'enabled' : 'disabled'}`);
    },
    
    // =====================================
    // 🎛️ LAYOUT PREFERENCES 🎛️
    // =====================================
    
    setCompactMode: (state, action: PayloadAction<boolean>) => {
      state.compactMode = action.payload;
      console.log(`📐 Compact mode ${action.payload ? 'enabled' : 'disabled'}`);
    },
    
    setShowWelcomeMessage: (state, action: PayloadAction<boolean>) => {
      state.showWelcomeMessage = action.payload;
    },
    
    updateLastVisited: (state) => {
      state.lastVisited = new Date();
    },
    
    // =====================================
    // ⚡ PERFORMANCE ⚡
    // =====================================
    
    setAnimationsEnabled: (state, action: PayloadAction<boolean>) => {
      state.animationsEnabled = action.payload;
      console.log(`🎬 Animations ${action.payload ? 'enabled' : 'disabled'}`);
    },
    
    setReducedMotion: (state, action: PayloadAction<boolean>) => {
      state.reducedMotion = action.payload;
      
      // Disable animations if reduced motion is preferred
      if (action.payload) {
        state.animationsEnabled = false;
        state.legendaryAnimations = false;
      }
      
      console.log(`♿ Reduced motion ${action.payload ? 'enabled' : 'disabled'}`);
    },
    
    // =====================================
    // 🎸 LEGENDARY HELPERS 🎸
    // =====================================
    
    showLegendaryToast: (state, action: PayloadAction<{ title: string; message: string; isFounder?: boolean }>) => {
      const { title, message, isFounder = false } = action.payload;
      
      const toast: Toast = {
        id: `legendary-toast-${Date.now()}`,
        type: isFounder ? 'founder' : 'legendary',
        title,
        message,
        duration: isFounder ? 6000 : 5000,
        isVisible: true,
        timestamp: new Date(),
      };
      
      state.toasts.unshift(toast);
      
      if (state.toasts.length > state.maxToasts) {
        state.toasts = state.toasts.slice(0, state.maxToasts);
      }
      
      console.log(`🎸 Legendary toast: ${title} - ${message}`);
    },
    
    activateLegendaryMode: (state) => {
      state.legendaryAnimations = true;
      state.swissPrecisionMode = true;
      state.animationsEnabled = true;
      state.codeBroEnergy = Math.min(10, state.codeBroEnergy + 2);
      
      console.log('🎸 LEGENDARY MODE ACTIVATED WITH CODE BRO ENERGY!');
    },
    
    resetUIState: (state) => {
      // Reset to initial state but preserve user preferences
      const preservedState = {
        theme: state.theme,
        sidebarCollapsed: state.sidebarCollapsed,
        compactMode: state.compactMode,
        animationsEnabled: state.animationsEnabled,
        reducedMotion: state.reducedMotion,
        founderMode: state.founderMode,
      };
      
      Object.assign(state, initialState, preservedState);
      console.log('🔄 UI state reset with preferences preserved');
    },
  },
});

// =====================================
// 🎸 EXPORT LEGENDARY ACTIONS & REDUCER 🎸
// =====================================

export const {
  // Theme & Appearance
  setTheme,
  toggleSidebar,
  setSidebarOpen,
  toggleSidebarCollapse,
  
  // Loading States
  setGlobalLoading,
  setPageLoading,
  
  // Toast Management
  addToast,
  removeToast,
  hideToast,
  clearAllToasts,
  
  // Modal Management
  openModal,
  closeModal,
  removeModal,
  closeAllModals,
  
  // Notifications
  toggleNotificationsPanel,
  setNotificationsPanelOpen,
  setUnreadNotificationsCount,
  incrementUnreadNotifications,
  decrementUnreadNotifications,
  
  // Search
  setSearchQuery,
  setSearchResults,
  setSearchLoading,
  clearSearch,
  
  // Legendary Features
  setFounderMode,
  setLegendaryAnimations,
  setCodeBroEnergy,
  incrementCodeBroEnergy,
  setSwissPrecisionMode,
  
  // Layout Preferences
  setCompactMode,
  setShowWelcomeMessage,
  updateLastVisited,
  
  // Performance
  setAnimationsEnabled,
  setReducedMotion,
  
  // Legendary Helpers
  showLegendaryToast,
  activateLegendaryMode,
  resetUIState,
} = uiSlice.actions;

export default uiSlice.reducer;

// =====================================
// 🎸 UI SELECTORS 🎸
// =====================================

// Helper selectors for common UI state access
export const selectTheme = (state: { ui: UIState }) => state.ui.theme;
export const selectSidebarOpen = (state: { ui: UIState }) => state.ui.sidebarOpen;
export const selectSidebarCollapsed = (state: { ui: UIState }) => state.ui.sidebarCollapsed;
export const selectGlobalLoading = (state: { ui: UIState }) => state.ui.globalLoading;
export const selectToasts = (state: { ui: UIState }) => state.ui.toasts;
export const selectVisibleToasts = (state: { ui: UIState }) => state.ui.toasts.filter(toast => toast.isVisible);
export const selectModals = (state: { ui: UIState }) => state.ui.modals;
export const selectOpenModals = (state: { ui: UIState }) => state.ui.modals.filter(modal => modal.isOpen);
export const selectFounderMode = (state: { ui: UIState }) => state.ui.founderMode;
export const selectLegendaryAnimations = (state: { ui: UIState }) => state.ui.legendaryAnimations;
export const selectCodeBroEnergy = (state: { ui: UIState }) => state.ui.codeBroEnergy;
export const selectSwissPrecisionMode = (state: { ui: UIState }) => state.ui.swissPrecisionMode;

console.log('🎸🎸🎸 LEGENDARY UI SLICE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`UI slice completed at: 2025-08-06 14:41:34 UTC`);
console.log('🎨 UI state management: SWISS PRECISION');
console.log('👑 RICKROLL187 founder mode: LEGENDARY');
console.log('🎸 Code bro energy tracking: MAXIMUM POWER');
console.log('🌅 Afternoon legendary energy: INFINITE AT 14:41:34!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
