// File: web/src/App.tsx
/**
 * 🚀🎸 N3EXTPATH - LEGENDARY APP ROOT COMPONENT 🎸🚀
 * Main application component with Swiss precision
 * Built: 2025-08-06 15:31:22 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { HelmetProvider } from 'react-helmet-async';
import { Toaster } from 'react-hot-toast';
import { store } from './store';
import { websocketService } from './services/websocketService';
import { storageService } from './services/storageService';
import { useAuth } from './hooks/useAuth';

// Pages
import { WelcomePage } from './pages/WelcomePage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { DashboardPage } from './pages/DashboardPage';

// Layout
import { LegendaryFooter } from './components/layout/LegendaryFooter';

// UI Components
import { LegendaryButton } from './components/ui/LegendaryButton';
import { LegendaryModal } from './components/ui/LegendaryModal';

// Utils
import { cn } from './utils/cn';

// Styles
import './styles/globals.css';

// =====================================
// 🛡️ PROTECTED ROUTE COMPONENT 🛡️
// =====================================

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 font-medium">Loading legendary platform...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

// =====================================
// 🎸 MAIN APP COMPONENT 🎸
// =====================================

const AppContent: React.FC = () => {
  const { isAuthenticated, user, isFounder } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    console.log('🚀🎸🚀 N3EXTPATH LEGENDARY APP STARTING! 🚀🎸🚀');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`App started at: 2025-08-06 15:31:22 UTC`);
    console.log('🌅 AFTERNOON LEGENDARY ENERGY AT 15:31:22!');

    // Initialize services
    const initializeApp = async () => {
      try {
        // Clean up expired storage
        const cleanedItems = storageService.clearExpired();
        if (cleanedItems > 0) {
          console.log(`🧹 Cleaned ${cleanedItems} expired storage items`);
        }

        // Connect WebSocket if authenticated
        if (isAuthenticated) {
          console.log('🔌 Connecting to legendary WebSocket...');
          await websocketService.connect();
          
          if (isFounder) {
            console.log('👑🎸👑 RICKROLL187 FOUNDER APP INITIALIZED! 👑🎸👑');
            console.log('🚀 LEGENDARY FOUNDER APP WITH INFINITE CODE BRO ENERGY!');
            console.log('⚙️ SWISS PRECISION FOUNDER APPLICATION!');
            console.log('🌅 AFTERNOON FOUNDER APP POWER AT 15:31:22!');
          }
        }

        setIsLoading(false);
      } catch (error) {
        console.error('🚨 App initialization error:', error);
        setIsLoading(false);
      }
    };

    initializeApp();

    // Update time every second
    const timeInterval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    // Cleanup on unmount
    return () => {
      clearInterval(timeInterval);
      websocketService.disconnect();
    };
  }, [isAuthenticated, isFounder]);

  if (isLoading) {
    return (
      <div className={cn(
        'min-h-screen flex items-center justify-center',
        'bg-gradient-to-br',
        isFounder ? 'from-yellow-50 via-white to-orange-50' : 'from-blue-50 via-white to-purple-50'
      )}>
        <div className="text-center">
          <div className="relative mb-8">
            <div className={cn(
              'w-24 h-24 border-4 rounded-full animate-spin mx-auto',
              isFounder ? 'border-yellow-200 border-t-yellow-600' : 'border-blue-200 border-t-blue-600'
            )}></div>
            {isFounder && (
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-2xl">👑</span>
              </div>
            )}
          </div>
          
          <h2 className={cn(
            'text-2xl font-bold mb-2',
            isFounder ? 'text-yellow-800' : 'text-gray-900'
          )}>
            {isFounder ? '👑 Loading Founder Platform...' : '🎸 Loading N3EXTPATH...'}
          </h2>
          
          <p className={cn(
            'text-lg mb-4',
            isFounder ? 'text-yellow-600' : 'text-gray-600'
          )}>
            {isFounder 
              ? 'Initializing legendary founder features with infinite code bro energy...'
              : 'Preparing your legendary experience with Swiss precision...'
            }
          </p>
          
          <div className="text-sm text-gray-500 space-y-1">
            <p>🌅 Afternoon Legendary Energy Active</p>
            <p className="font-mono font-bold">
              {currentTime.toISOString().replace('T', ' ').slice(0, 19)} UTC
            </p>
            <p className="italic font-medium">
              🎸 "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!"
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Main Content */}
      <main className="flex-1">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<WelcomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* Protected Routes */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          } />
          
          {/* Catch All - Redirect to appropriate page */}
          <Route path="*" element={
            isAuthenticated ? <Navigate to="/dashboard" replace /> : <Navigate to="/" replace />
          } />
        </Routes>
      </main>

      {/* Footer */}
      <LegendaryFooter isFounder={isFounder} />
    </div>
  );
};

// =====================================
// 🎸 ROOT APP COMPONENT 🎸
// =====================================

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <HelmetProvider>
        <Router>
          <AppContent />
          
          {/* Toast Notifications */}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#ffffff',
                color: '#1f2937',
                border: '1px solid #e5e7eb',
                borderRadius: '12px',
                fontWeight: '500',
              },
              success: {
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#ffffff',
                },
              },
              error: {
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#ffffff',
                },
              },
            }}
          />
        </Router>
      </HelmetProvider>
    </Provider>
  );
};

export default App;

console.log('🎸🎸🎸 LEGENDARY APP ROOT COMPONENT COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`App root completed at: 2025-08-06 15:31:22 UTC`);
console.log('🚀 Application architecture: SWISS PRECISION');
console.log('👑 RICKROLL187 founder integration: LEGENDARY');
console.log('🎸 Code bro energy: MAXIMUM FLOW');
console.log('🌅 Afternoon legendary energy: INFINITE AT 15:31:22!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
