// File: frontend/src/routes/AppRoutes.tsx
/**
 * 🛣️🎸 N3EXTPATH - LEGENDARY ROUTE CONFIGURATION 🎸🛣️
 * Professional routing with Swiss precision navigation
 * Built: 2025-08-05 18:25:28 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { selectIsAuthenticated, selectIsLegendaryUser, selectUser } from '../store/store';

// Loading Components
const LoadingSpinner = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
    <div className="ml-4 text-lg font-medium text-gray-600">
      Loading with Swiss precision...
    </div>
  </div>
);

const LegendaryLoadingSpinner = () => (
  <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500">
    <div className="text-center">
      <div className="animate-bounce text-6xl mb-4">🎸</div>
      <div className="animate-spin rounded-full h-32 w-32 border-b-4 border-yellow-300 mx-auto"></div>
      <div className="mt-4 text-xl font-bold text-white animate-pulse">
        🎸 LEGENDARY LOADING WITH MAXIMUM PRECISION 🎸
      </div>
      <div className="mt-2 text-lg text-yellow-200">
        RICKROLL187's legendary features incoming...
      </div>
    </div>
  </div>
);

// Lazy loaded components
const Dashboard = lazy(() => import('../components/Dashboard'));
const Login = lazy(() => import('../components/Auth/Login'));
const Register = lazy(() => import('../components/Auth/Register'));
const ForgotPassword = lazy(() => import('../components/Auth/ForgotPassword'));
const ResetPassword = lazy(() => import('../components/Auth/ResetPassword'));

const UserProfile = lazy(() => import('../components/User/UserProfile'));
const UserSettings = lazy(() => import('../components/User/UserSettings'));
const UserManagement = lazy(() => import('../components/UserManagement'));

const PerformanceReviews = lazy(() => import('../components/PerformanceReviews'));
const CreatePerformanceReview = lazy(() => import('../components/Performance/CreateReview'));
const EditPerformanceReview = lazy(() => import('../components/Performance/EditReview'));
const PerformanceAnalytics = lazy(() => import('../components/Performance/Analytics'));

const OKRManagement = lazy(() => import('../components/OKRManagement'));
const CreateOKR = lazy(() => import('../components/OKR/CreateOKR'));
const EditOKR = lazy(() => import('../components/OKR/EditOKR'));
const OKRAnalytics = lazy(() => import('../components/OKR/Analytics'));

const TeamManagement = lazy(() => import('../components/TeamManagement'));
const TeamDetails = lazy(() => import('../components/Team/TeamDetails'));
const CreateTeam = lazy(() => import('../components/Team/CreateTeam'));

const AnalyticsDashboard = lazy(() => import('../components/AnalyticsDashboard'));
const Reports = lazy(() => import('../components/Reports/Reports'));
const CustomReports = lazy(() => import('../components/Reports/CustomReports'));

const NotificationCenter = lazy(() => import('../components/Notifications/NotificationCenter'));
const Settings = lazy(() => import('../components/Settings/Settings'));
const SystemSettings = lazy(() => import('../components/Settings/SystemSettings'));

// Legendary Components (Special for RICKROLL187)
const LegendaryDashboard = lazy(() => import('../components/Legendary/LegendaryDashboard'));
const LegendaryAnalytics = lazy(() => import('../components/Legendary/LegendaryAnalytics'));
const LegendarySystemControl = lazy(() => import('../components/Legendary/SystemControl'));
const SwissPrecisionMetrics = lazy(() => import('../components/Legendary/SwissPrecisionMetrics'));
const CodeBroCenter = lazy(() => import('../components/Legendary/CodeBroCenter'));

// Error Components
const NotFound = lazy(() => import('../components/Error/NotFound'));
const Unauthorized = lazy(() => import('../components/Error/Unauthorized'));
const ServerError = lazy(() => import('../components/Error/ServerError'));

// Route Protection Components
interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAuth?: boolean;
  requireLegendary?: boolean;
  allowedRoles?: string[];
  redirectTo?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  requireAuth = true,
  requireLegendary = false,
  allowedRoles = [],
  redirectTo = '/login'
}) => {
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const isLegendary = useSelector(selectIsLegendaryUser);
  const user = useSelector(selectUser);
  const location = useLocation();

  // Check authentication
  if (requireAuth && !isAuthenticated) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  // Check legendary status
  if (requireLegendary && !isLegendary) {
    return <Navigate to="/unauthorized" replace />;
  }

  // Check role permissions
  if (allowedRoles.length > 0 && user && !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <>{children}</>;
};

const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const isLegendary = useSelector(selectIsLegendaryUser);
  
  if (isAuthenticated) {
    // Redirect to appropriate dashboard based on user type
    return <Navigate to={isLegendary ? "/legendary-dashboard" : "/dashboard"} replace />;
  }

  return <>{children}</>;
};

const AppRoutes: React.FC = () => {
  const isLegendary = useSelector(selectIsLegendaryUser);
  
  // Use legendary loading spinner for legendary users
  const LoadingComponent = isLegendary ? LegendaryLoadingSpinner : LoadingSpinner;

  return (
    <Suspense fallback={<LoadingComponent />}>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        } />
        
        <Route path="/register" element={
          <PublicRoute>
            <Register />
          </PublicRoute>
        } />
        
        <Route path="/forgot-password" element={
          <PublicRoute>
            <ForgotPassword />
          </PublicRoute>
        } />
        
        <Route path="/reset-password/:token" element={
          <PublicRoute>
            <ResetPassword />
          </PublicRoute>
        } />

        {/* Protected Routes - General */}
        <Route path="/" element={
          <ProtectedRoute>
            <Navigate to="/dashboard" replace />
          </ProtectedRoute>
        } />

        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />

        {/* User Routes */}
        <Route path="/profile" element={
          <ProtectedRoute>
            <UserProfile />
          </ProtectedRoute>
        } />

        <Route path="/settings" element={
          <ProtectedRoute>
            <UserSettings />
          </ProtectedRoute>
        } />

        <Route path="/users" element={
          <ProtectedRoute allowedRoles={['admin', 'hr_manager']}>
            <UserManagement />
          </ProtectedRoute>
        } />

        <Route path="/users/:userId" element={
          <ProtectedRoute>
            <UserProfile />
          </ProtectedRoute>
        } />

        {/* Performance Routes */}
        <Route path="/performance" element={
          <ProtectedRoute>
            <PerformanceReviews />
          </ProtectedRoute>
        } />

        <Route path="/performance/create" element={
          <ProtectedRoute allowedRoles={['manager', 'admin', 'hr_manager']}>
            <CreatePerformanceReview />
          </ProtectedRoute>
        } />

        <Route path="/performance/:reviewId/edit" element={
          <ProtectedRoute allowedRoles={['manager', 'admin', 'hr_manager']}>
            <EditPerformanceReview />
          </ProtectedRoute>
        } />

        <Route path="/performance/analytics" element={
          <ProtectedRoute allowedRoles={['manager', 'admin', 'hr_manager']}>
            <PerformanceAnalytics />
          </ProtectedRoute>
        } />

        {/* OKR Routes */}
        <Route path="/okrs" element={
          <ProtectedRoute>
            <OKRManagement />
          </ProtectedRoute>
        } />

        <Route path="/okrs/create" element={
          <ProtectedRoute>
            <CreateOKR />
          </ProtectedRoute>
        } />

        <Route path="/okrs/:okrId/edit" element={
          <ProtectedRoute>
            <EditOKR />
          </ProtectedRoute>
        } />

        <Route path="/okrs/analytics" element={
          <ProtectedRoute allowedRoles={['manager', 'admin', 'hr_manager']}>
            <OKRAnalytics />
          </ProtectedRoute>
        } />

        {/* Team Routes */}
        <Route path="/teams" element={
          <ProtectedRoute>
            <TeamManagement />
          </ProtectedRoute>
        } />

        <Route path="/teams/create" element={
          <ProtectedRoute allowedRoles={['manager', 'admin', 'hr_manager']}>
            <CreateTeam />
          </ProtectedRoute>
        } />

        <Route path="/teams/:teamId" element={
          <ProtectedRoute>
            <TeamDetails />
          </ProtectedRoute>
        } />

        {/* Analytics Routes */}
        <Route path="/analytics" element={
          <ProtectedRoute allowedRoles={['manager', 'admin', 'hr_manager', 'analyst']}>
            <AnalyticsDashboard />
          </ProtectedRoute>
        } />

        <Route path="/reports" element={
          <ProtectedRoute allowedRoles={['manager', 'admin', 'hr_manager']}>
            <Reports />
          </ProtectedRoute>
        } />

        <Route path="/reports/custom" element={
          <ProtectedRoute allowedRoles={['admin', 'hr_manager']}>
            <CustomReports />
          </ProtectedRoute>
        } />

        {/* Notification Routes */}
        <Route path="/notifications" element={
          <ProtectedRoute>
            <NotificationCenter />
          </ProtectedRoute>
        } />

        {/* System Settings Routes */}
        <Route path="/system-settings" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <SystemSettings />
          </ProtectedRoute>
        } />

        {/* LEGENDARY ROUTES - Special for RICKROLL187 */}
        <Route path="/legendary-dashboard" element={
          <ProtectedRoute requireLegendary={true}>
            <LegendaryDashboard />
          </ProtectedRoute>
        } />

        <Route path="/legendary-analytics" element={
          <ProtectedRoute requireLegendary={true}>
            <LegendaryAnalytics />
          </ProtectedRoute>
        } />

        <Route path="/legendary-system-control" element={
          <ProtectedRoute requireLegendary={true}>
            <LegendarySystemControl />
          </ProtectedRoute>
        } />

        <Route path="/swiss-precision-metrics" element={
          <ProtectedRoute requireLegendary={true}>
            <SwissPrecisionMetrics />
          </ProtectedRoute>
        } />

        <Route path="/code-bro-center" element={
          <ProtectedRoute requireLegendary={true}>
            <CodeBroCenter />
          </ProtectedRoute>
        } />

        {/* Error Routes */}
        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route path="/server-error" element={<ServerError />} />
        <Route path="/404" element={<NotFound />} />
        
        {/* Catch all route */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Suspense>
  );
};

// Route configuration for navigation menus
export const navigationRoutes = [
  {
    path: '/dashboard',
    name: 'Dashboard',
    icon: 'dashboard',
    requireAuth: true,
    showInNav: true
  },
  {
    path: '/performance',
    name: 'Performance',
    icon: 'trending_up',
    requireAuth: true,
    showInNav: true
  },
  {
    path: '/okrs',
    name: 'OKRs',
    icon: 'flag',
    requireAuth: true,
    showInNav: true
  },
  {
    path: '/teams',
    name: 'Teams',
    icon: 'group',
    requireAuth: true,
    showInNav: true
  },
  {
    path: '/analytics',
    name: 'Analytics',
    icon: 'analytics',
    requireAuth: true,
    allowedRoles: ['manager', 'admin', 'hr_manager', 'analyst'],
    showInNav: true
  },
  {
    path: '/users',
    name: 'Users',
    icon: 'people',
    requireAuth: true,
    allowedRoles: ['admin', 'hr_manager'],
    showInNav: true,
    adminOnly: true
  },
  {
    path: '/reports',
    name: 'Reports',
    icon: 'assessment',
    requireAuth: true,
    allowedRoles: ['manager', 'admin', 'hr_manager'],
    showInNav: true
  }
];

// Legendary navigation routes (Special for RICKROLL187)
export const legendaryNavigationRoutes = [
  {
    path: '/legendary-dashboard',
    name: '🎸 Legendary Dashboard',
    icon: 'star',
    requireLegendary: true,
    showInNav: true,
    legendary: true
  },
  {
    path: '/legendary-analytics',
    name: '🎸 Legendary Analytics',
    icon: 'insights',
    requireLegendary: true,
    showInNav: true,
    legendary: true
  },
  {
    path: '/legendary-system-control',
    name: '🎸 System Control',
    icon: 'settings',
    requireLegendary: true,
    showInNav: true,
    legendary: true
  },
  {
    path: '/swiss-precision-metrics',
    name: '⚡ Swiss Precision',
    icon: 'precision_manufacturing',
    requireLegendary: true,
    showInNav: true,
    legendary: true
  },
  {
    path: '/code-bro-center',
    name: '💪 Code Bro Center',
    icon: 'code',
    requireLegendary: true,
    showInNav: true,
    legendary: true
  }
];

// Utility functions for route management
export const getRouteByPath = (path: string) => {
  return [...navigationRoutes, ...legendaryNavigationRoutes].find(route => route.path === path);
};

export const getVisibleRoutes = (user: any) => {
  const routes = [...navigationRoutes];
  
  // Add legendary routes for legendary users
  if (user?.is_legendary) {
    routes.push(...legendaryNavigationRoutes);
  }
  
  return routes.filter(route => {
    if (!route.showInNav) return false;
    if (route.allowedRoles && !route.allowedRoles.includes(user?.role)) return false;
    if (route.requireLegendary && !user?.is_legendary) return false;
    return true;
  });
};

export const isRouteAccessible = (path: string, user: any) => {
  const route = getRouteByPath(path);
  if (!route) return false;
  
  if (route.allowedRoles && !route.allowedRoles.includes(user?.role)) return false;
  if (route.requireLegendary && !user?.is_legendary) return false;
  
  return true;
};

export default AppRoutes;

// Legendary startup message
if (process.env.NODE_ENV === 'development') {
  console.log('🎸🎸🎸 LEGENDARY ROUTE CONFIGURATION LOADED! 🎸🎸🎸');
  console.log('Professional routing with Swiss precision navigation!');
  console.log('Special legendary routes for RICKROLL187 included!');
  console.log('Built by RICKROLL187 with maximum code bro energy!');
  console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
  console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
}
