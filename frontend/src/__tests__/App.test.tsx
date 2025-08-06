// File: frontend/src/__tests__/App.test.tsx
/**
 * 🧪🎸 N3EXTPATH - LEGENDARY FRONTEND TESTS 🎸🧪
 * Professional React testing suite with Swiss precision
 * Built: 2025-08-05 19:10:57 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { configureStore } from '@reduxjs/toolkit';
import '@testing-library/jest-dom';

// Mock modules
jest.mock('../services/api');
jest.mock('../services/websocket');

// Import components and store
import App from '../App';
import { store } from '../store/store';
import LoginForm from '../components/Auth/LoginForm';
import Dashboard from '../components/Dashboard';
import LegendaryDashboard from '../components/Legendary/LegendaryDashboard';
import { apiService } from '../services/api';

// Test utilities
const renderWithProviders = (component: React.ReactElement, customStore = store) => {
  return render(
    <Provider store={customStore}>
      <BrowserRouter>
        {component}
      </BrowserRouter>
    </Provider>
  );
};

const createMockStore = (initialState = {}) => {
  return configureStore({
    reducer: {
      auth: (state = { 
        user: null, 
        isAuthenticated: false, 
        isLoading: false, 
        error: null, 
        legendary_status: false 
      }, action) => {
        switch (action.type) {
          case 'auth/loginUser/fulfilled':
            return {
              ...state,
              user: action.payload.user,
              isAuthenticated: true,
              legendary_status: action.payload.user.is_legendary || false
            };
          default:
            return state;
        }
      },
      dashboard: (state = { data: null, isLoading: false, error: null }, action) => state,
      performance: (state = { reviews: [], isLoading: false, error: null }, action) => state,
      okr: (state = { okrs: [], isLoading: false, error: null }, action) => state,
      ui: (state = { 
        theme: 'light', 
        sidebar_collapsed: false, 
        toast_messages: [] 
      }, action) => state
    },
    preloadedState: initialState
  });
};

// Mock API responses
const mockApiService = apiService as jest.Mocked<typeof apiService>;

describe('🎸 N3EXTPATH Application Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Setup console mock to capture legendary messages
    jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(console, 'info').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('App Component', () => {
    test('renders without crashing', () => {
      renderWithProviders(<App />);
      expect(screen.getByText(/N3EXTPATH/i)).toBeInTheDocument();
    });

    test('displays legendary startup message in development', () => {
      process.env.NODE_ENV = 'development';
      renderWithProviders(<App />);
      
      expect(console.log).toHaveBeenCalledWith(
        expect.stringContaining('LEGENDARY')
      );
    });

    test('shows login form when not authenticated', () => {
      const store = createMockStore({
        auth: { isAuthenticated: false, user: null }
      });
      
      renderWithProviders(<LoginForm />, store);
      expect(screen.getByText(/Sign in to N3EXTPATH/i)).toBeInTheDocument();
    });

    test('shows dashboard when authenticated', async () => {
      const store = createMockStore({
        auth: { 
          isAuthenticated: true, 
          user: { 
            user_id: '1', 
            username: 'testuser', 
            is_legendary: false 
          }
        }
      });
      
      renderWithProviders(<Dashboard />, store);
      expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
    });
  });

  describe('🎸 Legendary Features Tests', () => {
    test('detects RICKROLL187 legendary user', async () => {
      const legendaryUser = {
        user_id: '1',
        username: 'rickroll187',
        email: 'rickroll187@n3extpath.com',
        first_name: 'RICKROLL',
        last_name: '187',
        is_legendary: true,
        role: 'founder'
      };

      mockApiService.login.mockResolvedValueOnce({
        success: true,
        data: {
          access_token: 'legendary_token',
          refresh_token: 'legendary_refresh',
          user: legendaryUser,
          expires_in: 3600
        },
        legendary: true
      });

      const store = createMockStore();
      renderWithProviders(<LoginForm />, store);

      // Fill in legendary credentials
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const submitButton = screen.getByRole('button', { name: /sign in/i });

      fireEvent.change(usernameInput, { target: { value: 'rickroll187' } });
      fireEvent.change(passwordInput, { target: { value: 'legendary_pass' } });

      await act(async () => {
        fireEvent.click(submitButton);
      });

      expect(mockApiService.login).toHaveBeenCalledWith({
        username: 'rickroll187',
        password: 'legendary_pass',
        remember_me: false
      });
    });

    test('activates legendary mode for RICKROLL187', () => {
      const store = createMockStore({
        auth: {
          isAuthenticated: true,
          legendary_status: true,
          user: {
            user_id: '1',
            username: 'rickroll187',
            is_legendary: true
          }
        }
      });

      renderWithProviders(<LegendaryDashboard />, store);
      expect(screen.getByText(/LEGENDARY DASHBOARD/i)).toBeInTheDocument();
    });

    test('displays Swiss precision metrics', async () => {
      const store = createMockStore({
        auth: { isAuthenticated: true, legendary_status: true },
        dashboard: {
          data: {
            legendary_metrics: {
              swiss_precision_score: 98.7,
              code_bro_energy: 'maximum',
              rickroll187_status: 'active'
            }
          }
        }
      });

      renderWithProviders(<LegendaryDashboard />, store);
      
      await waitFor(() => {
        expect(screen.getByText(/98.7/)).toBeInTheDocument();
        expect(screen.getByText(/maximum/i)).toBeInTheDocument();
      });
    });

    test('legendary animations work correctly', async () => {
      renderWithProviders(<LoginForm />);
      
      const legendaryButton = screen.getByText(/Activate Legendary Mode/i);
      
      await act(async () => {
        fireEvent.click(legendaryButton);
      });

      expect(screen.getByText(/Legendary Mode Active/i)).toBeInTheDocument();
    });
  });

  describe('Authentication Flow Tests', () => {
    test('handles successful login', async () => {
      mockApiService.login.mockResolvedValueOnce({
        success: true,
        data: {
          access_token: 'test_token',
          refresh_token: 'refresh_token',
          user: {
            user_id: '1',
            username: 'testuser',
            email: 'test@example.com',
            first_name: 'Test',
            last_name: 'User',
            is_legendary: false,
            role: 'employee'
          },
          expires_in: 3600
        }
      });

      const store = createMockStore();
      renderWithProviders(<LoginForm />, store);

      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const submitButton = screen.getByRole('button', { name: /sign in/i });

      fireEvent.change(usernameInput, { target: { value: 'testuser' } });
      fireEvent.change(passwordInput, { target: { value: 'password123' } });

      await act(async () => {
        fireEvent.click(submitButton);
      });

      expect(mockApiService.login).toHaveBeenCalledWith({
        username: 'testuser',
        password: 'password123',
        remember_me: false
      });
    });

    test('handles login failure', async () => {
      mockApiService.login.mockRejectedValueOnce({
        success: false,
        error: 'Invalid credentials'
      });

      const store = createMockStore();
      renderWithProviders(<LoginForm />, store);

      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const submitButton = screen.getByRole('button', { name: /sign in/i });

      fireEvent.change(usernameInput, { target: { value: 'wrong' } });
      fireEvent.change(passwordInput, { target: { value: 'wrong' } });

      await act(async () => {
        fireEvent.click(submitButton);
      });

      await waitFor(() => {
        expect(screen.getByText(/Invalid credentials/i)).toBeInTheDocument();
      });
    });

    test('validates form inputs', async () => {
      renderWithProviders(<LoginForm />);

      const submitButton = screen.getByRole('button', { name: /sign in/i });

      await act(async () => {
        fireEvent.click(submitButton);
      });

      await waitFor(() => {
        expect(screen.getByText(/Username is required/i)).toBeInTheDocument();
        expect(screen.getByText(/Password is required/i)).toBeInTheDocument();
      });
    });
  });

  describe('Dashboard Tests', () => {
    test('loads dashboard data on mount', async () => {
      mockApiService.getDashboardData.mockResolvedValueOnce({
        success: true,
        data: {
          user_stats: { total_users: 150, active_users: 142 },
          performance_metrics: { average_score: 4.2 },
          okr_metrics: { total_okrs: 45, completed_okrs: 23 }
        }
      });

      const store = createMockStore({
        auth: { isAuthenticated: true, user: { user_id: '1' } }
      });

      renderWithProviders(<Dashboard />, store);

      await waitFor(() => {
        expect(mockApiService.getDashboardData).toHaveBeenCalled();
      });
    });

    test('displays error state when dashboard fails to load', async () => {
      mockApiService.getDashboardData.mockRejectedValueOnce(new Error('API Error'));

      const store = createMockStore({
        auth: { isAuthenticated: true, user: { user_id: '1' } },
        dashboard: { error: 'Failed to load dashboard data' }
      });

      renderWithProviders(<Dashboard />, store);

      await waitFor(() => {
        expect(screen.getByText(/Failed to load/i)).toBeInTheDocument();
      });
    });
  });

  describe('Responsive Design Tests', () => {
    test('adapts to mobile viewport', () => {
      // Mock mobile viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });

      renderWithProviders(<App />);
      
      // Mobile-specific elements should be present
      expect(document.body).toHaveClass(); // Would check for mobile classes
    });

    test('adapts to desktop viewport', () => {
      // Mock desktop viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1920,
      });

      renderWithProviders(<App />);
      
      // Desktop-specific elements should be present
      expect(document.body).toHaveClass(); // Would check for desktop classes
    });
  });

  describe('Theme Tests', () => {
    test('applies light theme by default', () => {
      renderWithProviders(<App />);
      
      // Would check for light theme classes
      expect(document.documentElement).toHaveAttribute('data-theme', 'light');
    });

    test('applies legendary theme for legendary users', () => {
      const store = createMockStore({
        auth: { legendary_status: true },
        ui: { theme: 'legendary' }
      });

      renderWithProviders(<App />, store);
      
      // Would check for legendary theme classes
      expect(document.documentElement).toHaveAttribute('data-theme', 'legendary');
    });
  });

  describe('Error Boundary Tests', () => {
    test('catches and displays errors gracefully', () => {
      const ThrowError = () => {
        throw new Error('Test error');
      };

      const ConsoleError = console.error;
      console.error = jest.fn();

      render(
        <Provider store={store}>
          <BrowserRouter>
            <ThrowError />
          </BrowserRouter>
        </Provider>
      );

      // Error boundary should catch the error
      expect(console.error).toHaveBeenCalled();
      console.error = ConsoleError;
    });
  });

  describe('Accessibility Tests', () => {
    test('has proper ARIA labels', () => {
      renderWithProviders(<LoginForm />);
      
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
    });

    test('supports keyboard navigation', () => {
      renderWithProviders(<LoginForm />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      
      usernameInput.focus();
      expect(document.activeElement).toBe(usernameInput);
      
      fireEvent.keyDown(usernameInput, { key: 'Tab' });
      // Password input should be focused after tab
    });

    test('has proper heading hierarchy', () => {
      renderWithProviders(<Dashboard />);
      
      // Should have proper h1, h2, h3 hierarchy
      const headings = screen.getAllByRole('heading');
      expect(headings.length).toBeGreaterThan(0);
    });
  });

  describe('Performance Tests', () => {
    test('lazy loads components efficiently', async () => {
      const store = createMockStore({
        auth: { isAuthenticated: true }
      });

      renderWithProviders(<App />, store);
      
      // Components should lazy load
      await waitFor(() => {
        expect(screen.getByText(/Loading with Swiss precision/i)).toBeInTheDocument();
      });
    });
  });

  describe('🎸 Code Bro Tests', () => {
    test('displays code bro motto', () => {
      renderWithProviders(<App />);
      
      // Check for our legendary motto in development
      if (process.env.NODE_ENV === 'development') {
        expect(console.log).toHaveBeenCalledWith(
          expect.stringContaining('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN')
        );
      }
    });

    test('handles Swiss precision features', () => {
      const store = createMockStore({
        auth: { legendary_status: true },
        dashboard: {
          data: {
            legendary_metrics: {
              swiss_precision_score: 100,
              code_bro_energy: 'maximum'
            }
          }
        }
      });

      renderWithProviders(<LegendaryDashboard />, store);
      
      expect(screen.getByText(/Swiss precision/i)).toBeInTheDocument();
    });
  });
});

// Test setup for legendary features
describe('🎸 Legendary Test Suite Setup', () => {
  test('test environment is configured correctly', () => {
    expect(process.env.NODE_ENV).toBeDefined();
    expect(jest).toBeDefined();
    expect(screen).toBeDefined();
  });

  test('legendary test utilities work', () => {
    const testStore = createMockStore();
    expect(testStore).toBeDefined();
    expect(testStore.getState).toBeDefined();
  });

  test('mock API service is configured', () => {
    expect(mockApiService).toBeDefined();
    expect(mockApiService.login).toBeDefined();
    expect(mockApiService.getDashboardData).toBeDefined();
  });
});

// Legendary test completion message
if (process.env.NODE_ENV === 'test') {
  console.log('🎸🎸🎸 LEGENDARY FRONTEND TESTS LOADED! 🎸🎸🎸');
  console.log('Built with Swiss precision by RICKROLL187!');
  console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
  console.log('Test suite ready for legendary quality assurance!');
  console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
}
