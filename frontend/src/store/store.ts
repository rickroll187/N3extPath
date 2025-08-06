// File: frontend/src/store/store.ts
/**
 * 🏪🎸 N3EXTPATH - LEGENDARY STATE MANAGEMENT 🎸🏪
 * Professional Redux store with Swiss precision state management
 * Built: 2025-08-05 18:19:29 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { configureStore, createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { apiService, User, PerformanceReview, OKR, DashboardData } from '../services/api';

// Types
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  legendary_status: boolean;
}

interface DashboardState {
  data: DashboardData | null;
  isLoading: boolean;
  error: string | null;
  last_updated: string | null;
  legendary_metrics: any;
}

interface PerformanceState {
  reviews: PerformanceReview[];
  current_review: PerformanceReview | null;
  isLoading: boolean;
  error: string | null;
}

interface OKRState {
  okrs: OKR[];
  current_okr: OKR | null;
  isLoading: boolean;
  error: string | null;
}

interface UIState {
  theme: 'light' | 'dark' | 'legendary';
  sidebar_collapsed: boolean;
  loading_states: Record<string, boolean>;
  notifications: any[];
  toast_messages: Array<{
    id: string;
    type: 'success' | 'error' | 'warning' | 'info' | 'legendary';
    message: string;
    timestamp: number;
  }>;
}

interface RootState {
  auth: AuthState;
  dashboard: DashboardState;
  performance: PerformanceState;
  okr: OKRState;
  ui: UIState;
}

// Initial States
const initialAuthState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  legendary_status: false
};

const initialDashboardState: DashboardState = {
  data: null,
  isLoading: false,
  error: null,
  last_updated: null,
  legendary_metrics: null
};

const initialPerformanceState: PerformanceState = {
  reviews: [],
  current_review: null,
  isLoading: false,
  error: null
};

const initialOKRState: OKRState = {
  okrs: [],
  current_okr: null,
  isLoading: false,
  error: null
};

const initialUIState: UIState = {
  theme: 'light',
  sidebar_collapsed: false,
  loading_states: {},
  notifications: [],
  toast_messages: []
};

// Async Thunks
export const loginUser = createAsyncThunk(
  'auth/login',
  async (credentials: { username: string; password: string }, { rejectWithValue }) => {
    try {
      const response = await apiService.login(credentials);
      if (response.success && response.data) {
        return response.data;
      } else {
        return rejectWithValue(response.error || 'Login failed');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Login failed');
    }
  }
);

export const fetchUserProfile = createAsyncThunk(
  'auth/fetchProfile',
  async (userId?: string, { rejectWithValue }) => {
    try {
      const response = await apiService.getUserProfile(userId);
      if (response.success && response.data) {
        return response.data;
      } else {
        return rejectWithValue(response.error || 'Failed to fetch profile');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch profile');
    }
  }
);

export const fetchDashboardData = createAsyncThunk(
  'dashboard/fetchData',
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiService.getDashboardData();
      if (response.success && response.data) {
        return response.data;
      } else {
        return rejectWithValue(response.error || 'Failed to fetch dashboard data');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch dashboard data');
    }
  }
);

export const fetchPerformanceReviews = createAsyncThunk(
  'performance/fetchReviews',
  async (userId?: string, { rejectWithValue }) => {
    try {
      const response = await apiService.getPerformanceReviews(userId);
      if (response.success && response.data) {
        return response.data;
      } else {
        return rejectWithValue(response.error || 'Failed to fetch performance reviews');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch performance reviews');
    }
  }
);

export const createPerformanceReview = createAsyncThunk(
  'performance/createReview',
  async (reviewData: Partial<PerformanceReview>, { rejectWithValue }) => {
    try {
      const response = await apiService.createPerformanceReview(reviewData);
      if (response.success && response.data) {
        return response.data;
      } else {
        return rejectWithValue(response.error || 'Failed to create performance review');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create performance review');
    }
  }
);

export const fetchOKRs = createAsyncThunk(
  'okr/fetchOKRs',
  async (userId?: string, { rejectWithValue }) => {
    try {
      const response = await apiService.getOKRs(userId);
      if (response.success && response.data) {
        return response.data;
      } else {
        return rejectWithValue(response.error || 'Failed to fetch OKRs');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch OKRs');
    }
  }
);

export const createOKR = createAsyncThunk(
  'okr/createOKR',
  async (okrData: Partial<OKR>, { rejectWithValue }) => {
    try {
      const response = await apiService.createOKR(okrData);
      if (response.success && response.data) {
        return response.data;
      } else {
        return rejectWithValue(response.error || 'Failed to create OKR');
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create OKR');
    }
  }
);

// Auth Slice
const authSlice = createSlice({
  name: 'auth',
  initialState: initialAuthState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.isAuthenticated = false;
      state.legendary_status = false;
      state.error = null;
      apiService.logout();
    },
    clearError: (state) => {
      state.error = null;
    },
    updateUser: (state, action: PayloadAction<Partial<User>>) => {
      if (state.user) {
        state.user = { ...state.user, ...action.payload };
        state.legendary_status = state.user.is_legendary || false;
      }
    },
    setLegendaryStatus: (state, action: PayloadAction<boolean>) => {
      state.legendary_status = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.isAuthenticated = true;
        state.legendary_status = action.payload.user.is_legendary || false;
        state.error = null;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        state.isAuthenticated = false;
        state.legendary_status = false;
      })
      // Fetch Profile
      .addCase(fetchUserProfile.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchUserProfile.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
        state.legendary_status = action.payload.is_legendary || false;
      })
      .addCase(fetchUserProfile.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  }
});

// Dashboard Slice
const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState: initialDashboardState,
  reducers: {
    clearDashboardError: (state) => {
      state.error = null;
    },
    updateLegendaryMetrics: (state, action: PayloadAction<any>) => {
      state.legendary_metrics = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboardData.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDashboardData.fulfilled, (state, action) => {
        state.isLoading = false;
        state.data = action.payload;
        state.legendary_metrics = action.payload.legendary_metrics;
        state.last_updated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchDashboardData.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  }
});

// Performance Slice
const performanceSlice = createSlice({
  name: 'performance',
  initialState: initialPerformanceState,
  reducers: {
    setCurrentReview: (state, action: PayloadAction<PerformanceReview | null>) => {
      state.current_review = action.payload;
    },
    clearPerformanceError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Reviews
      .addCase(fetchPerformanceReviews.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchPerformanceReviews.fulfilled, (state, action) => {
        state.isLoading = false;
        state.reviews = action.payload;
        state.error = null;
      })
      .addCase(fetchPerformanceReviews.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Create Review
      .addCase(createPerformanceReview.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(createPerformanceReview.fulfilled, (state, action) => {
        state.isLoading = false;
        state.reviews.unshift(action.payload);
        state.current_review = action.payload;
      })
      .addCase(createPerformanceReview.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  }
});

// OKR Slice
const okrSlice = createSlice({
  name: 'okr',
  initialState: initialOKRState,
  reducers: {
    setCurrentOKR: (state, action: PayloadAction<OKR | null>) => {
      state.current_okr = action.payload;
    },
    updateOKRProgress: (state, action: PayloadAction<{ okrId: string; progress: number }>) => {
      const okr = state.okrs.find(o => o.okr_id === action.payload.okrId);
      if (okr) {
        okr.progress = action.payload.progress;
      }
      if (state.current_okr && state.current_okr.okr_id === action.payload.okrId) {
        state.current_okr.progress = action.payload.progress;
      }
    },
    clearOKRError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch OKRs
      .addCase(fetchOKRs.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchOKRs.fulfilled, (state, action) => {
        state.isLoading = false;
        state.okrs = action.payload;
        state.error = null;
      })
      .addCase(fetchOKRs.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Create OKR
      .addCase(createOKR.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(createOKR.fulfilled, (state, action) => {
        state.isLoading = false;
        state.okrs.unshift(action.payload);
        state.current_okr = action.payload;
      })
      .addCase(createOKR.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  }
});

// UI Slice
const uiSlice = createSlice({
  name: 'ui',
  initialState: initialUIState,
  reducers: {
    setTheme: (state, action: PayloadAction<'light' | 'dark' | 'legendary'>) => {
      state.theme = action.payload;
    },
    toggleSidebar: (state) => {
      state.sidebar_collapsed = !state.sidebar_collapsed;
    },
    setSidebarCollapsed: (state, action: PayloadAction<boolean>) => {
      state.sidebar_collapsed = action.payload;
    },
    setLoadingState: (state, action: PayloadAction<{ key: string; loading: boolean }>) => {
      state.loading_states[action.payload.key] = action.payload.loading;
    },
    addToastMessage: (state, action: PayloadAction<Omit<UIState['toast_messages'][0], 'id' | 'timestamp'>>) => {
      const message = {
        ...action.payload,
        id: `toast_${Date.now()}_${Math.random()}`,
        timestamp: Date.now()
      };
      state.toast_messages.push(message);
    },
    removeToastMessage: (state, action: PayloadAction<string>) => {
      state.toast_messages = state.toast_messages.filter(msg => msg.id !== action.payload);
    },
    clearToastMessages: (state) => {
      state.toast_messages = [];
    },
    addNotification: (state, action: PayloadAction<any>) => {
      state.notifications.unshift(action.payload);
    },
    markNotificationRead: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find(n => n.id === action.payload);
      if (notification) {
        notification.read = true;
      }
    },
    clearNotifications: (state) => {
      state.notifications = [];
    }
  }
});

// Export actions
export const { logout, clearError, updateUser, setLegendaryStatus } = authSlice.actions;
export const { clearDashboardError, updateLegendaryMetrics } = dashboardSlice.actions;
export const { setCurrentReview, clearPerformanceError } = performanceSlice.actions;
export const { setCurrentOKR, updateOKRProgress, clearOKRError } = okrSlice.actions;
export const {
  setTheme,
  toggleSidebar,
  setSidebarCollapsed,
  setLoadingState,
  addToastMessage,
  removeToastMessage,
  clearToastMessages,
  addNotification,
  markNotificationRead,
  clearNotifications
} = uiSlice.actions;

// Persist config
const persistConfig = {
  key: 'n3extpath_legendary_store',
  storage,
  whitelist: ['auth', 'ui'], // Only persist auth and UI state
  blacklist: ['dashboard', 'performance', 'okr'] // Don't persist data that should be fresh
};

// Root reducer
const rootReducer = {
  auth: authSlice.reducer,
  dashboard: dashboardSlice.reducer,
  performance: performanceSlice.reducer,
  okr: okrSlice.reducer,
  ui: uiSlice.reducer
};

// Create persisted reducer
const persistedReducer = persistReducer(persistConfig, (state: any, action: any) => {
  // Handle logout - clear all state except UI theme
  if (action.type === 'auth/logout') {
    const theme = state?.ui?.theme || 'light';
    return {
      auth: initialAuthState,
      dashboard: initialDashboardState,
      performance: initialPerformanceState,
      okr: initialOKRState,
      ui: { ...initialUIState, theme }
    };
  }

  // Apply individual reducers
  return {
    auth: rootReducer.auth(state?.auth, action),
    dashboard: rootReducer.dashboard(state?.dashboard, action),
    performance: rootReducer.performance(state?.performance, action),
    okr: rootReducer.okr(state?.okr, action),
    ui: rootReducer.ui(state?.ui, action)
  };
});

// Configure store
export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE']
      }
    }),
  devTools: process.env.NODE_ENV !== 'production'
});

// Create persistor
export const persistor = persistStore(store);

// Types
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Selectors
export const selectAuth = (state: RootState) => state.auth;
export const selectUser = (state: RootState) => state.auth.user;
export const selectIsAuthenticated = (state: RootState) => state.auth.isAuthenticated;
export const selectIsLegendaryUser = (state: RootState) => state.auth.legendary_status;

export const selectDashboard = (state: RootState) => state.dashboard;
export const selectDashboardData = (state: RootState) => state.dashboard.data;
export const selectLegendaryMetrics = (state: RootState) => state.dashboard.legendary_metrics;

export const selectPerformance = (state: RootState) => state.performance;
export const selectPerformanceReviews = (state: RootState) => state.performance.reviews;
export const selectCurrentReview = (state: RootState) => state.performance.current_review;

export const selectOKR = (state: RootState) => state.okr;
export const selectOKRs = (state: RootState) => state.okr.okrs;
export const selectCurrentOKR = (state: RootState) => state.okr.current_okr;

export const selectUI = (state: RootState) => state.ui;
export const selectTheme = (state: RootState) => state.ui.theme;
export const selectSidebarCollapsed = (state: RootState) => state.ui.sidebar_collapsed;
export const selectLoadingStates = (state: RootState) => state.ui.loading_states;
export const selectToastMessages = (state: RootState) => state.ui.toast_messages;
export const selectNotifications = (state: RootState) => state.ui.notifications;

// Legendary startup message
if (process.env.NODE_ENV === 'development') {
  console.log('🎸🎸🎸 LEGENDARY REDUX STORE INITIALIZED! 🎸🎸🎸');
  console.log('Built with Swiss precision by RICKROLL187!');
  console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
  console.log('State management ready with legendary precision!');
  console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
}
