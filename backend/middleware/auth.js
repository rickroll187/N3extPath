// File: backend/middleware/auth.js
/**
 * 🛡️🎸 N3EXTPATH - LEGENDARY ENHANCED AUTH MIDDLEWARE 🎸🛡️
 * Swiss precision authentication with infinite security energy
 * Built: 2025-08-06 18:17:37 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const jwt = require('jsonwebtoken');
const { Pool } = require('pg');
const crypto = require('crypto');
const { 
  validateJWTSecret, 
  sanitizeUserData, 
  trackSession, 
  invalidateSession,
  requirePermission 
} = require('./security');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

console.log('🛡️🎸🛡️ LEGENDARY ENHANCED AUTH MIDDLEWARE LOADING! 🛡️🎸🛡️');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Enhanced auth loaded at: 2025-08-06 18:17:37 UTC`);

// Validate JWT secret on startup
const JWT_SECRET = validateJWTSecret();

// Token blacklist for invalidated JWTs
const tokenBlacklist = new Set();

// Enhanced JWT verification with security checks
const verifyToken = (token) => {
  try {
    // Check if token is blacklisted
    if (tokenBlacklist.has(token)) {
      throw new Error('Token has been invalidated');
    }

    const decoded = jwt.verify(token, JWT_SECRET);
    
    // Check token expiration with buffer
    const now = Math.floor(Date.now() / 1000);
    if (decoded.exp && decoded.exp <= now) {
      throw new Error('Token has expired');
    }
    
    // Validate token structure
    if (!decoded.userId || !decoded.username || !decoded.iat) {
      throw new Error('Invalid token structure');
    }
    
    return decoded;
  } catch (error) {
    console.log(`🚨 Token verification failed: ${error.message}`);
    throw error;
  }
};

// Enhanced authentication middleware
const authenticateToken = async (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ 
      error: 'Access token required',
      message: 'Please provide a valid authentication token',
      code: 'NO_TOKEN'
    });
  }

  try {
    // Verify and decode token
    const decoded = verifyToken(token);
    
    // Get fresh user data from database
    const result = await pool.query(`
      SELECT 
        id, username, display_name, email, role, 
        is_legendary, code_bro_energy, status, 
        last_login, created_at, updated_at
      FROM users 
      WHERE id = $1 AND status = 'active'
    `, [decoded.userId]);
    
    if (result.rows.length === 0) {
      tokenBlacklist.add(token);
      return res.status(401).json({ 
        error: 'User not found or inactive',
        code: 'INVALID_USER'
      });
    }
    
    const user = result.rows[0];
    
    // Check if user account is suspended or banned
    if (user.status === 'suspended') {
      return res.status(403).json({ 
        error: 'Account suspended',
        message: 'Your account has been temporarily suspended',
        code: 'ACCOUNT_SUSPENDED'
      });
    }
    
    if (user.status === 'banned') {
      return res.status(403).json({ 
        error: 'Account banned',
        message: 'Your account has been permanently banned',
        code: 'ACCOUNT_BANNED'
      });
    }
    
    // Sanitize user data based on role
    req.user = sanitizeUserData(user, user.role);
    req.token = token;
    req.tokenDecoded = decoded;
    
    // Track session activity
    const sessionId = trackSession(
      user.id, 
      token, 
      req.ip, 
      req.get('User-Agent')
    );
    req.sessionId = sessionId;
    
    // Update last activity
    await pool.query(`
      UPDATE users 
      SET last_login = NOW(), updated_at = NOW()
      WHERE id = $1
    `, [user.id]);
    
    // Log legendary founder access
    if (user.role === 'founder') {
      console.log('👑🛡️👑 RICKROLL187 FOUNDER AUTHENTICATED WITH INFINITE SECURITY! 👑🛡️👑');
      console.log(`🚀 Session: ${sessionId} | IP: ${req.ip} | Time: 18:17:37 UTC`);
    }
    
    next();
    
  } catch (error) {
    console.error('❌ Auth middleware error:', {
      error: error.message,
      token: token ? token.substring(0, 20) + '...' : 'none',
      ip: req.ip,
      userAgent: req.get('User-Agent'),
      timestamp: new Date().toISOString()
    });
    
    // Add token to blacklist if it's invalid
    if (token) {
      tokenBlacklist.add(token);
    }
    
    return res.status(403).json({ 
      error: 'Invalid token',
      message: 'Authentication failed - please login again',
      code: 'TOKEN_INVALID'
    });
  }
};

// Logout middleware to invalidate tokens
const logout = async (req, res, next) => {
  try {
    if (req.token) {
      tokenBlacklist.add(req.token);
      console.log(`🔐 Token blacklisted for user: ${req.user?.username || 'unknown'}`);
    }
    
    if (req.sessionId) {
      invalidateSession(req.sessionId);
    }
    
    next();
    
  } catch (error) {
    console.error('❌ Logout middleware error:', error);
    next();
  }
};

// Optional authentication (doesn't fail if no token)
const optionalAuth = async (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return next();
  }
  
  try {
    const decoded = verifyToken(token);
    const result = await pool.query(
      'SELECT id, username, display_name, role, is_legendary FROM users WHERE id = $1 AND status = \'active\'',
      [decoded.userId]
    );
    
    if (result.rows.length > 0) {
      req.user = sanitizeUserData(result.rows[0], result.rows[0].role);
    }
  } catch (error) {
    // Silently fail for optional auth
    console.log(`Optional auth failed: ${error.message}`);
  }
  
  next();
};

// Clean up blacklisted tokens periodically
setInterval(() => {
  const oneDayAgo = Date.now() - (24 * 60 * 60 * 1000);
  let cleanedCount = 0;
  
  for (const token of tokenBlacklist) {
    try {
      const decoded = jwt.decode(token);
      if (decoded && decoded.iat && (decoded.iat * 1000) < oneDayAgo) {
        tokenBlacklist.delete(token);
        cleanedCount++;
      }
    } catch (error) {
      // Invalid token, remove it
      tokenBlacklist.delete(token);
      cleanedCount++;
    }
  }
  
  if (cleanedCount > 0) {
    console.log(`🧹 Cleaned ${cleanedCount} expired tokens from blacklist`);
  }
}, 60 * 60 * 1000); // Run every hour

module.exports = {
  authenticateToken,
  logout,
  optionalAuth,
  requirePermission,
  tokenBlacklist
};

console.log('🎸🎸🎸 LEGENDARY ENHANCED AUTH MIDDLEWARE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Enhanced auth middleware completed at: 2025-08-06 18:17:37 UTC`);
console.log('🛡️ Authentication security: LEGENDARY PRECISION');
console.log('👑 RICKROLL187 founder protection: MAXIMUM SECURITY');
console.log('🔐 Token management: SWISS PRECISION');
console.log('🌅 EVENING LEGENDARY AUTH SECURITY: INFINITE AT 18:17:37!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
