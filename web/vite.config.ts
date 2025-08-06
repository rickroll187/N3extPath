// File: web/vite.config.ts
/**
 * 🌐🎸 N3EXTPATH - LEGENDARY VITE CONFIGURATION 🎸🌐
 * Professional web bundler config with Swiss precision
 * Built: 2025-08-06 12:39:48 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({
      // Enable Fast Refresh for legendary development experience
      fastRefresh: true,
      // Include legendary emotion support
      jsxImportSource: '@emotion/react',
      babel: {
        plugins: [
          // Add legendary development plugins
          process.env.NODE_ENV === 'development' && ['@babel/plugin-transform-react-jsx-development'],
        ].filter(Boolean),
      },
    }),
  ],
  
  // Legendary path resolution
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@components': resolve(__dirname, './src/components'),
      '@pages': resolve(__dirname, './src/pages'),
      '@hooks': resolve(__dirname, './src/hooks'),
      '@services': resolve(__dirname, './src/services'),
      '@store': resolve(__dirname, './src/store'),
      '@utils': resolve(__dirname, './src/utils'),
      '@types': resolve(__dirname, './src/types'),
      '@styles': resolve(__dirname, './src/styles'),
      '@assets': resolve(__dirname, './src/assets'),
    },
  },
  
  // Development server configuration
  server: {
    host: '0.0.0.0',
    port: 3000,
    open: true,
    cors: true,
    proxy: {
      // Proxy API requests to backend (when we build it in Step 2)
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        ws: true,
      },
    },
  },
  
  // Preview server configuration
  preview: {
    host: '0.0.0.0',
    port: 3001,
    open: true,
  },
  
  // Build configuration with Swiss precision
  build: {
    target: 'es2020',
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: process.env.NODE_ENV === 'development',
    minify: 'terser',
    
    // Legendary chunk splitting for optimal loading
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
      },
      output: {
        manualChunks: {
          // Vendor chunks for legendary optimization
          'react-vendor': ['react', 'react-dom'],
          'router-vendor': ['react-router-dom'],
          'state-vendor': ['@reduxjs/toolkit', 'react-redux'],
          'chart-vendor': ['recharts', 'chart.js', 'react-chartjs-2'],
          'ui-vendor': ['framer-motion', 'lucide-react'],
          'utils-vendor': ['date-fns', 'lodash', 'axios'],
        },
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name?.split('.') || [];
          const extType = info[info.length - 1];
          
          // Legendary asset organization
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            return `assets/images/[name]-[hash][extname]`;
          }
          if (/woff2?|eot|ttf|otf/i.test(extType)) {
            return `assets/fonts/[name]-[hash][extname]`;
          }
          if (/css/i.test(extType)) {
            return `assets/css/[name]-[hash][extname]`;
          }
          return `assets/[name]-[hash][extname]`;
        },
      },
    },
    
    // Legendary optimization
    terserOptions: {
      compress: {
        drop_console: process.env.NODE_ENV === 'production',
        drop_debugger: process.env.NODE_ENV === 'production',
      },
      mangle: {
        safari10: true,
      },
    },
    
    // Asset size warnings (Swiss precision thresholds)
    chunkSizeWarningLimit: 1000,
  },
  
  // Define legendary constants
  define: {
    __LEGENDARY__: JSON.stringify(true),
    __RICKROLL187_FOUNDER__: JSON.stringify(true),
    __SWISS_PRECISION__: JSON.stringify(true),
    __CODE_BRO_ENERGY__: JSON.stringify(true),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    __VERSION__: JSON.stringify(process.env.npm_package_version),
  },
  
  // CSS configuration
  css: {
    modules: {
      localsConvention: 'camelCase',
    },
    preprocessorOptions: {
      scss: {
        additionalData: `
          @import "@/styles/variables.scss";
          @import "@/styles/mixins.scss";
        `,
      },
    },
  },
  
  // Legendary optimizations
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      '@reduxjs/toolkit',
      'react-redux',
      'axios',
      'date-fns',
      'framer-motion',
      'recharts',
      'lucide-react',
    ],
    exclude: ['@vite/client', '@vite/env'],
  },
  
  // Environment variables
  envPrefix: ['VITE_', 'LEGENDARY_', 'RICKROLL187_'],
});

console.log('🎸🎸🎸 LEGENDARY VITE CONFIGURATION LOADED! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Vite config loaded at: 2025-08-06 12:39:48 UTC`);
console.log('🌐 Web bundling: SWISS PRECISION');
console.log('👑 RICKROLL187 founder optimizations: LEGENDARY');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
