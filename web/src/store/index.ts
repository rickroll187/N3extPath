// File: web/src/store/index.ts
/**
 * 🏪🎸 N3EXTPATH - LEGENDARY REDUX STORE 🎸🏪
 * Professional state management with Swiss precision
 * Built: 2025-08-06 13:23:07 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { combineReducers } from '@reduxjs/toolkit';

// Import legendary reducers
import authSlice from './slices/authSlice';
import performanceSlice from './slices/performanceSlice';
import okrSlice from './slices/okrSlice';
import teamsSlice from './slices/teamsSlice';
import notificationsSlice from './slices/notificationsSlice';
import uiSlice from './slices/uiSlice';

// =====================================
// 🎸 LEGENDARY PERSIST CONFIG 🎸
// =====================================

const persistConfig = {
  key: 'n3extpath-legendary-root',
  storage,
  version: 1,
  whitelist: [
    'auth', // Persist authentication state
    'ui',   // Persist UI preferences
  ],
  blacklist: [
    'performance', // Don't persist performance data (fetch fresh)
    'okr',        // Don't persist OKR data (fetch fresh)
    'teams',      // Don't persist teams data (fetch fresh)
    'notifications', // Don't persist notifications (fetch fresh)
  ],
};

// =====================================
// 🎸 ROOT REDUCER COMBINATION 🎸
// =====================================

const rootReducer = combineReducers({
  auth: authSlice,
  performance: performanceSlice,
  okr: okrSlice,
  teams: teamsSlice,
  notifications: notificationsSlice,
  ui: uiSlice,
});

// Create persisted reducer
const persistedReducer = persistReducer(persistConfig, rootReducer);

// =====================================
// 🎸 LEGENDARY STORE CONFIGURATION 🎸
// =====================================

export const store = configureStore({
  reducer: persistedReducer,
  
  // Legendary middleware configuration
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore redux-persist actions
        ignoredActions: [
          'persist/PERSIST',
          'persist/REHYDRATE',
          'persist/PAUSE',
          'persist/PURGE',
          'persist/REGISTER',
        ],
        // Ignore date objects in auth state
        ignoredPaths: [
          'auth.user.joinedAt',
          'auth.user.lastLogin',
          'performance.lastUpdated',
          'okr.lastSync',
          'teams.lastActivity',
          'notifications.lastFetch',
        ],
      },
      thunk: {
        extraArgument: {
          // Add extra services that can be accessed in thunks
          timestamp: () => new Date().toISOString(),
          isFounder: (state: RootState) => state.auth.user?.isFounder || false,
          isLegendary: (state: RootState) => state.auth.user?.is_legendary || false,
        },
      },
    }),
  
  // Enable Redux DevTools in development
  devTools: process.env.NODE_ENV !== 'production' && {
    name: 'N3EXTPATH Legendary Store',
    features: {
      pause: true,
      lock: true,
      persist: true,
      export: true,
      import: 'custom',
      jump: true,
      skip: true,
      reorder: true,
      dispatch: true,
      test: true,
    },
    trace: true,
    traceLimit: 25,
  },
  
  // Preloaded state for legendary features
  preloadedState: undefined,
});

// Create persistor
export const persistor = persistStore(store);

// =====================================
// 🎸 LEGENDARY TYPE EXPORTS 🎸
// =====================================

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export type AppThunk<ReturnType = void> = (
  dispatch: AppDispatch,
  getState: () => RootState
) => ReturnType;

// =====================================
// 🎸 LEGENDARY STORE UTILITIES 🎸
// =====================================

// Get user from state utility
export const selectUser = (state: RootState) => state.auth.user;
export const selectIsFounder = (state: RootState) => state.auth.user?.isFounder || false;
export const selectIsLegendary = (state: RootState) => state.auth.user?.is_legendary || false;
export const selectIsAuthenticated = (state: RootState) => state.auth.isAuthenticated;

// Theme selector
export const selectTheme = (state: RootState) => state.ui.theme;
export const selectSidebarOpen = (state: RootState) => state.ui.sidebarOpen;

// Performance selectors
export const selectPerformanceData = (state: RootState) => state.performance.data;
export const selectPerformanceLoading = (state: RootState) => state.performance.isLoading;

// OKR selectors
export const selectOKRs = (state: RootState) => state.okr.okrs;
export const selectActiveOKRs = (state: RootState) => 
  state.okr.okrs.filter(okr => okr.status === 'active');

// Teams selectors
export const selectTeams = (state: RootState) => state.teams.teams;
export const selectMyTeams = (state: RootState) => {
  const user = selectUser(state);
  return state.teams.teams.filter(team => 
    team.owner.username === user?.username || 
    team.members.some(member => member.username === user?.username)
  );
};

// Notifications selectors
export const selectNotifications = (state: RootState) => state.notifications.notifications;
export const selectUnreadNotifications = (state: RootState) => 
  state.notifications.notifications.filter(notif => !notif.isRead);

// =====================================
// 🎸 LEGENDARY STORE INITIALIZATION 🎸
// =====================================

// Initialize legendary logging
console.log('🎸🎸🎸 LEGENDARY REDUX STORE INITIALIZED! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Store initialized at: 2025-08-06 13:23:07 UTC`);
console.log('🏪 State management: SWISS PRECISION');
console.log('👑 RICKROLL187 founder features: LEGENDARY');
console.log('💾 Persistence: MAXIMUM RELIABILITY');

// Development store debugging
if (process.env.NODE_ENV === 'development') {
  console.log('🔧 LEGENDARY DEVELOPMENT MODE ACTIVE');
  console.log('👑 RICKROLL187 Founder debugging tools enabled');
  console.log('⚙️ Redux DevTools enabled with legendary features');
  
  // Add legendary store to window for debugging
  (window as any).__LEGENDARY_STORE__ = store;
  (window as any).__LEGENDARY_PERSISTOR__ = persistor;
  
  console.log('🎸 Access __LEGENDARY_STORE__ in console for debugging!');
  console.log('💾 Access __LEGENDARY_PERSISTOR__ for persistence debugging!');
}

// Store event listeners for legendary features
store.subscribe(() => {
  const state = store.getState();
  
  // Log founder activities
  if (selectIsFounder(state)) {
    const user = selectUser(state);
    if (user && (window as any).__LEGENDARY_FOUNDER_LOGGING__) {
      console.log('👑 RICKROLL187 FOUNDER ACTIVITY DETECTED!');
    }
  }
});

export default store;

console.log('🎸🎸🎸 LEGENDARY STORE SETUP COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Store setup completed at: 2025-08-06 13:23:07 UTC`);
console.log('🏪 Redux store: LEGENDARY ARCHITECTURE');
console.log('💾 Persistence: SWISS PRECISION STORAGE');
console.log('🎸 Code bro state management: MAXIMUM EFFICIENCY');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
