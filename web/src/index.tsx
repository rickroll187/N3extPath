// File: web/src/index.tsx
/**
 * 🌐🎸 N3EXTPATH - LEGENDARY ENTRY POINT 🎸🌐
 * Professional web application entry with Swiss precision
 * Built: 2025-08-06 13:16:05 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Import legendary styles
import './index.css';

// Get the legendary root element
const container = document.getElementById('root');
if (!container) {
  throw new Error('🚨 Root element not found! Legendary platform cannot initialize!');
}

// Create legendary React root
const root = createRoot(container);

// Initialize legendary error handling
const handleLegendaryError = (error: Error, errorInfo: any) => {
  console.error('🚨 LEGENDARY ERROR DETECTED:', error);
  console.error('🔍 ERROR INFO:', errorInfo);
  
  // In production, send error to monitoring service
  if (import.meta.env.PROD) {
    // Send to error tracking service (Sentry, LogRocket, etc.)
    console.log('📊 Sending error to monitoring service...');
  }
};

// Legendary Error Boundary Component
class LegendaryErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error: Error | null }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    handleLegendaryError(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="legendary-error-boundary">
          <div className="error-content">
            <h1>🎸 Legendary Error Detected!</h1>
            <p>Something went wrong, but we're on it with Swiss precision!</p>
            <details className="error-details">
              <summary>Technical Details</summary>
              <pre>{this.state.error?.toString()}</pre>
              <pre>{this.state.error?.stack}</pre>
            </details>
            <button 
              onClick={() => window.location.reload()}
              className="legendary-retry-button"
            >
              🔄 Retry with Code Bro Energy
            </button>
            <p className="error-footer">
              Built with Swiss precision by RICKROLL187<br />
              Email: letstalktech010@gmail.com
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// Legendary startup logging
console.log('🎸🎸🎸 N3EXTPATH LEGENDARY WEB PLATFORM INITIALIZING 🎸🎸🎸');
console.log('Built: 2025-08-06 13:16:05 UTC by RICKROLL187');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log('🌐 Platform: Web Application');
console.log('⚙️ Framework: React 18 with Swiss Precision');
console.log('👑 Founder Features: LEGENDARY');
console.log('🎸 Code Bro Energy: MAXIMUM');
console.log('🔥 Afternoon Energy at 13:16:05: INFINITE!');

// Performance monitoring
const startTime = performance.now();

// Render the legendary application
root.render(
  <React.StrictMode>
    <LegendaryErrorBoundary>
      <App />
    </LegendaryErrorBoundary>
  </React.StrictMode>
);

// Log rendering performance
const endTime = performance.now();
console.log(`⚡ Legendary render time: ${(endTime - startTime).toFixed(2)}ms`);

// Service Worker Registration for PWA (if available)
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('🚀 Service Worker registered with Swiss precision:', registration);
      })
      .catch((error) => {
        console.log('⚠️ Service Worker registration failed:', error);
      });
  });
}

// Legendary development helpers
if (import.meta.env.DEV) {
  console.log('🔧 LEGENDARY DEVELOPMENT MODE ACTIVE');
  console.log('👑 RICKROLL187 Founder debugging tools enabled');
  console.log('⚙️ Swiss Precision development experience');
  console.log('🎸 Code Bro Energy development vibes');
  
  // Add legendary development globals
  (window as any).__LEGENDARY__ = {
    version: '2.0.0',
    build: '2025-08-06 13:16:05 UTC',
    founder: 'RICKROLL187',
    energy: 'INFINITE CODE BRO ENERGY',
    precision: 'SWISS PRECISION',
    motto: 'WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN',
    contact: 'letstalktech010@gmail.com',
  };
  
  console.log('🎸 Access __LEGENDARY__ object in console for development info!');
}

// Performance observer for legendary optimization
if ('PerformanceObserver' in window) {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.entryType === 'navigation') {
        console.log(`🚀 Page load performance: ${entry.duration.toFixed(2)}ms`);
      }
    }
  });
  observer.observe({ entryTypes: ['navigation'] });
}

console.log('✅ LEGENDARY PLATFORM INITIALIZATION COMPLETE!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
