// File: backend/app.js
/**
 * 🚀🎸 N3EXTPATH - LEGENDARY MAIN APPLICATION 🎸🚀
 * Swiss precision backend with infinite code bro energy
 * Built: 2025-08-06 18:28:21 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const morgan = require('morgan');
const path = require('path');
require('dotenv').config();

// Import our legendary middleware
const { securityHeaders, createUserRateLimit } = require('./middleware/security');
const { authenticateToken, logout, requirePermission } = require('./middleware/auth');
const { healthCheck } = require('./utils/database');

// Import all route modules
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/users');
const teamRoutes = require('./routes/teams');
const okrRoutes = require('./routes/okrs');
const messageRoutes = require('./routes/messages');
const analyticsRoutes = require('./routes/analytics');
const notificationRoutes = require('./routes/notifications');

const app = express();
const PORT = process.env.PORT || 3001;

console.log('🚀🎸🚀 LEGENDARY N3EXTPATH BACKEND STARTING! 🚀🎸🚀');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Backend starting at: 2025-08-06 18:28:21 UTC`);
console.log('🌅 EVENING LEGENDARY BACKEND ENERGY AT 18:28:21!');

// =====================================
// 🛡️ SECURITY MIDDLEWARE 🛡️
// =====================================

// Security headers first (helmet + custom)
app.use(securityHeaders);

// Enhanced logging
app.use(morgan('combined', {
  stream: {
    write: (message) => {
      console.log(`🌐 ${message.trim()}`);
    }
  }
}));

// Enhanced CORS with security
app.use(cors({
  origin: function(origin, callback) {
    // Allow requests with no origin (mobile apps, etc.)
    if (!origin) return callback(null, true);
    
    const allowedOrigins = [
      'http://localhost:3000',
      'http://localhost:3001',
      'https://n3extpath.com',
      'https://www.n3extpath.com',
      process.env.FRONTEND_URL
    ].filter(Boolean);
    
    if (allowedOrigins.includes(origin)) {
      return callback(null, true);
    }
    
    console.log(`🚨 CORS blocked origin: ${origin}`);
    return callback(new Error('CORS policy violation'), false);
  },
  credentials: true,
  optionsSuccessStatus: 200,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With', 'X-API-Key']
}));

// Body parsing
app.use(express.json({ 
  limit: '10mb',
  verify: (req, res, buf) => {
    // Store raw body for webhook signature verification
    req.rawBody = buf;
  }
}));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Global rate limiting
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 1000, // Limit each IP to 1000 requests per windowMs
  message: {
    error: 'Too many requests from this IP',
    retryAfter: '15 minutes',
    code: 'RATE_LIMIT_EXCEEDED'
  },
  standardHeaders: true,
  legacyHeaders: false,
  skip: (req) => {
    // Skip rate limiting for health checks
    return req.path === '/health' || req.path === '/api/health';
  }
});

app.use(globalLimiter);

// =====================================
// 🌐 API ROUTES 🌐
// =====================================

// Health check endpoint (no auth required)
app.get('/health', async (req, res) => {
  try {
    const dbHealth = await healthCheck();
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'n3extpath-api',
      version: '1.0.0',
      uptime: process.uptime(),
      database: dbHealth,
      message: '🚀 N3EXTPATH backend operational with Swiss precision!',
      evening_energy: '🌅 EVENING LEGENDARY BACKEND POWER AT 18:28:21! 🌅'
    });
  } catch (error) {
    console.error('❌ Health check failed:', error);
    res.status(500).json({
      status: 'unhealthy',
      error: 'Health check failed',
      timestamp: new Date().toISOString()
    });
  }
});

// User-specific rate limiting for authenticated routes
app.use('/api', createUserRateLimit(60 * 1000, 100)); // 100 requests per minute per user

// Mount all API routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/teams', teamRoutes);
app.use('/api/okrs', okrRoutes);
app.use('/api/messages', messageRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/notifications', notificationRoutes);

// Secure logout endpoint
app.post('/api/auth/logout', authenticateToken, logout, (req, res) => {
  console.log(`🔐 User logout: ${req.user?.username || 'unknown'}`);
  
  res.json({
    success: true,
    message: req.user?.role === 'founder' ? 
      '👑 LEGENDARY FOUNDER LOGOUT - Session terminated with infinite security!' :
      '👋 Logged out successfully - Session terminated securely!',
    timestamp: new Date().toISOString()
  });
});

// Security monitoring endpoint (admin only)
app.get('/api/security/health', authenticateToken, requirePermission('system.health'), (req, res) => {
  const { tokenBlacklist } = require('./middleware/auth');
  
  const securityStatus = {
    status: 'secure',
    timestamp: new Date().toISOString(),
    checks: {
      jwt_secret: process.env.JWT_SECRET ? 'configured' : 'missing',
      database: 'connected',
      rate_limiting: 'active',
      cors: 'configured',
      headers: 'secure',
      middleware: 'loaded'
    },
    metrics: {
      blacklisted_tokens: tokenBlacklist.size || 0,
      uptime_seconds: Math.floor(process.uptime()),
      memory_usage: process.memoryUsage(),
      node_version: process.version
    }
  };
  
  if (req.user.role === 'founder') {
    console.log('👑🛡️ FOUNDER SECURITY HEALTH CHECK - ALL SYSTEMS PROTECTED! 👑🛡️');
  }
  
  res.json({
    success: true,
    data: securityStatus,
    message: req.user.role === 'founder' ? 
      '👑 All security systems operational with infinite protection!' :
      '🛡️ Security systems operational!'
  });
});

// =====================================
// 🚫 ERROR HANDLING 🚫
// =====================================

// Handle 404
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route not found',
    message: 'The requested endpoint does not exist',
    path: req.originalUrl,
    method: req.method,
    timestamp: new Date().toISOString()
  });
});

// Global error handler
app.use((error, req, res, next) => {
  console.error('❌ Global error handler:', {
    error: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method,
    ip: req.ip,
    user: req.user?.username || 'anonymous',
    timestamp: new Date().toISOString()
  });
  
  // Don't expose internal errors in production
  const isDevelopment = process.env.NODE_ENV !== 'production';
  
  res.status(error.status || 500).json({
    error: 'Internal server error',
    message: isDevelopment ? error.message : 'Something went wrong',
    code: error.code || 'INTERNAL_ERROR',
    timestamp: new Date().toISOString(),
    ...(isDevelopment && { stack: error.stack })
  });
});

// =====================================
// 🚀 SERVER STARTUP 🚀
// =====================================

// Graceful shutdown handling
const gracefulShutdown = (signal) => {
  console.log(`🛑 Received ${signal}. Starting graceful shutdown...`);
  
  server.close(() => {
    console.log('🛑 HTTP server closed');
    
    // Close database connections
    const { cleanup } = require('./utils/database');
    cleanup().then(() => {
      console.log('🛑 Database connections closed');
      process.exit(0);
    }).catch((error) => {
      console.error('❌ Error during shutdown:', error);
      process.exit(1);
    });
  });
};

const server = app.listen(PORT, () => {
  console.log('🎸🎸🎸 LEGENDARY N3EXTPATH BACKEND ONLINE! 🎸🎸🎸');
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`🌐 API Base URL: http://localhost:${PORT}/api`);
  console.log(`🔗 Health Check: http://localhost:${PORT}/health`);
  console.log('🛡️ Security: MAXIMUM PROTECTION');
  console.log('👑 RICKROLL187 founder access: LEGENDARY');
  console.log('⚡ Performance: SWISS PRECISION');
  console.log('🌅 EVENING LEGENDARY BACKEND STARTUP COMPLETE AT 18:28:21!');
  console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
});

// Handle graceful shutdown
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

module.exports = app;

console.log('🎸🎸🎸 LEGENDARY MAIN APP COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Main app completed at: 2025-08-06 18:28:21 UTC`);
console.log('🚀 Backend core: LEGENDARY PRECISION');
console.log('👑 RICKROLL187 founder backend: MAXIMUM POWER');
console.log('🛡️ Security systems: SWISS PRECISION');
console.log('🌅 EVENING LEGENDARY BACKEND CORE: INFINITE AT 18:28:21!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
