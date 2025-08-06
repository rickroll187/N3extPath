// File: backend/routes/auth.js
/**
 * 🔐🎸 N3EXTPATH - LEGENDARY SECURE AUTH ROUTES 🎸🔐
 * Swiss precision authentication with infinite security energy
 * Built: 2025-08-06 18:28:21 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');
const crypto = require('crypto');

const router = express.Router();
const { secureQuery, secureTransaction } = require('../utils/database');
const { authenticateToken, logout } = require('../middleware/auth');
const { validateJWTSecret, sanitizeUserData } = require('../middleware/security');

console.log('🔐🎸🔐 LEGENDARY SECURE AUTH ROUTES LOADING! 🔐🎸🔐');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure auth routes loaded at: 2025-08-06 18:28:21 UTC`);
console.log('🌅 EVENING LEGENDARY AUTH SECURITY AT 18:28:21!');

// Validate JWT secret on startup
const JWT_SECRET = validateJWTSecret();

// =====================================
// 🛡️ AUTH-SPECIFIC RATE LIMITING 🛡️
// =====================================

// Strict rate limiting for auth routes
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // limit each IP to 10 auth requests per windowMs
  message: {
    error: 'Too many authentication attempts from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'AUTH_RATE_LIMIT'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// Very strict rate limiting for login attempts
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // limit each IP to 5 login attempts per windowMs
  message: {
    error: 'Too many login attempts from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'LOGIN_RATE_LIMIT'
  }
});

// =====================================
// 🔐 AUTH HELPER FUNCTIONS 🔐
// =====================================

// Generate secure JWT token
const generateToken = (user) => {
  const payload = {
    userId: user.id,
    username: user.username,
    role: user.role,
    iat: Math.floor(Date.now() / 1000),
    jti: crypto.randomUUID() // JWT ID for tracking
  };
  
  return jwt.sign(payload, JWT_SECRET, { 
    expiresIn: process.env.JWT_EXPIRES_IN || '24h',
    algorithm: 'HS256'
  });
};

// Validate password strength
const validatePassword = (password) => {
  if (password.length < 8) {
    return 'Password must be at least 8 characters long';
  }
  
  if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
    return 'Password must contain at least one lowercase letter, one uppercase letter, and one number';
  }
  
  if (/(.)\1{2,}/.test(password)) {
    return 'Password cannot contain three or more consecutive identical characters';
  }
  
  const commonPasswords = ['password', '12345678', 'qwerty', 'admin', 'letmein'];
  if (commonPasswords.some(common => password.toLowerCase().includes(common))) {
    return 'Password is too common, please choose a stronger password';
  }
  
  return null;
};

// Hash password securely
const hashPassword = async (password) => {
  const saltRounds = 12; // High salt rounds for security
  return await bcrypt.hash(password, saltRounds);
};

// =====================================
// 🚀 AUTH ROUTES 🚀
// =====================================

// Register new user
router.post('/register', 
  authLimiter,
  [
    body('username')
      .isLength({ min: 3, max: 30 })
      .matches(/^[a-zA-Z0-9_-]+$/)
      .withMessage('Username must be 3-30 characters and contain only letters, numbers, hyphens, and underscores'),
    body('display_name')
      .isLength({ min: 2, max: 50 })
      .matches(/^[a-zA-Z0-9\s_-]+$/)
      .withMessage('Display name must be 2-50 characters'),
    body('email')
      .isEmail()
      .normalizeEmail()
      .withMessage('Valid email address required'),
    body('password')
      .isLength({ min: 8, max: 128 })
      .withMessage('Password must be 8-128 characters long')
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ 
          error: 'Validation error',
          details: errors.array(),
          code: 'VALIDATION_FAILED'
        });
      }

      console.log(`🔐 User registration attempt: ${req.body.username} at 18:28:21 UTC`);

      const { username, display_name, email, password } = req.body;

      // Additional password validation
      const passwordError = validatePassword(password);
      if (passwordError) {
        return res.status(400).json({ 
          error: 'Password validation failed',
          message: passwordError,
          code: 'WEAK_PASSWORD'
        });
      }

      // Check for existing user
      const existingUser = await secureQuery(`
        SELECT id, username, email 
        FROM users 
        WHERE LOWER(username) = LOWER($1) OR LOWER(email) = LOWER($2)
      `, [username, email]);

      if (existingUser.rows.length > 0) {
        const existing = existingUser.rows[0];
        const field = existing.username.toLowerCase() === username.toLowerCase() ? 'username' : 'email';
        
        console.log(`🚨 Registration blocked - ${field} already exists: ${username}`);
        
        return res.status(409).json({ 
          error: 'User already exists',
          message: `A user with this ${field} already exists`,
          field,
          code: 'USER_EXISTS'
        });
      }

      // Hash password
      const hashedPassword = await hashPassword(password);

      // Create user in transaction
      const newUser = await secureTransaction(async (client) => {
        const userResult = await client.query(`
          INSERT INTO users (
            username, display_name, email, password_hash, 
            role, is_legendary, code_bro_energy, status, 
            created_at, updated_at
          ) VALUES ($1, $2, $3, $4, 'user', false, 1000, 'active', NOW(), NOW())
          RETURNING id, username, display_name, email, role, is_legendary, code_bro_energy, created_at
        `, [username, display_name, email, hashedPassword]);

        return userResult.rows[0];
      });

      // Generate JWT token
      const token = generateToken(newUser);

      // Sanitize user data for response
      const sanitizedUser = sanitizeUserData(newUser, 'user');

      console.log(`🎉 User registered successfully: ${username}`);
      
      res.status(201).json({
        success: true,
        data: {
          user: sanitizedUser,
          token,
          expires_in: process.env.JWT_EXPIRES_IN || '24h'
        },
        message: `🎉 Welcome to N3EXTPATH, ${display_name}! Your code creator journey begins now!`
      });

    } catch (error) {
      console.error('❌ Registration error:', {
        error: error.message,
        username: req.body?.username,
        email: req.body?.email,
        timestamp: new Date().toISOString()
      });
      
      res.status(500).json({ 
        error: 'Registration failed',
        message: 'An error occurred during registration',
        code: 'REGISTRATION_ERROR'
      });
    }
  }
);

// User login
router.post('/login', 
  loginLimiter,
  [
    body('username')
      .notEmpty()
      .trim()
      .isLength({ min: 3, max: 50 })
      .withMessage('Username or email is required'),
    body('password')
      .notEmpty()
      .isLength({ min: 8, max: 128 })
      .withMessage('Password is required')
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ 
          error: 'Validation error',
          details: errors.array(),
          code: 'VALIDATION_FAILED'
        });
      }

      console.log(`🔐 Login attempt: ${req.body.username} at 18:28:21 UTC`);

      const { username, password } = req.body;

      // Find user by username or email
      const userResult = await secureQuery(`
        SELECT 
          id, username, display_name, email, password_hash, 
          role, is_legendary, code_bro_energy, status,
          last_login, created_at
        FROM users 
        WHERE (LOWER(username) = LOWER($1) OR LOWER(email) = LOWER($1))
        AND status != 'deleted'
      `, [username]);

      if (userResult.rows.length === 0) {
        console.log(`🚨 Login failed - user not found: ${username}`);
        return res.status(401).json({ 
          error: 'Invalid credentials',
          message: 'Username/email or password is incorrect',
          code: 'INVALID_CREDENTIALS'
        });
      }

      const user = userResult.rows[0];

      // Check account status
      if (user.status === 'suspended') {
        console.log(`🚨 Login blocked - account suspended: ${username}`);
        return res.status(403).json({ 
          error: 'Account suspended',
          message: 'Your account has been temporarily suspended',
          code: 'ACCOUNT_SUSPENDED'
        });
      }

      if (user.status === 'banned') {
        console.log(`🚨 Login blocked - account banned: ${username}`);
        return res.status(403).json({ 
          error: 'Account banned',
          message: 'Your account has been permanently banned',
          code: 'ACCOUNT_BANNED'
        });
      }

      if (user.status === 'pending') {
        console.log(`🚨 Login blocked - account pending: ${username}`);
        return res.status(403).json({ 
          error: 'Account pending',
          message: 'Your account is pending approval',
          code: 'ACCOUNT_PENDING'
        });
      }

      // Verify password
      const isPasswordValid = await bcrypt.compare(password, user.password_hash);
      
      if (!isPasswordValid) {
        console.log(`🚨 Login failed - invalid password: ${username}`);
        return res.status(401).json({ 
          error: 'Invalid credentials',
          message: 'Username/email or password is incorrect',
          code: 'INVALID_CREDENTIALS'
        });
      }

      // Update last login
      await secureQuery(`
        UPDATE users 
        SET last_login = NOW(), updated_at = NOW()
        WHERE id = $1
      `, [user.id]);

      // Generate JWT token
      const token = generateToken(user);

      // Sanitize user data for response
      const sanitizedUser = sanitizeUserData(user, user.role);

      console.log(`🎉 Login successful: ${username} (role: ${user.role})`);
      
      if (user.role === 'founder') {
        console.log('👑🚀👑 LEGENDARY FOUNDER RICKROLL187 LOGIN SUCCESS! 👑🚀👑');
        console.log('🎸 INFINITE CODE BRO POWER ACTIVATED!');
      }

      res.json({
        success: true,
        data: {
          user: sanitizedUser,
          token,
          expires_in: process.env.JWT_EXPIRES_IN || '24h'
        },
        message: user.role === 'founder' ? 
          '👑 Welcome back, LEGENDARY FOUNDER! Your infinite power is restored!' :
          `🎉 Welcome back, ${user.display_name}! Ready to create amazing things?`
      });

    } catch (error) {
      console.error('❌ Login error:', {
        error: error.message,
        username: req.body?.username,
        ip: req.ip,
        timestamp: new Date().toISOString()
      });
      
      res.status(500).json({ 
        error: 'Login failed',
        message: 'An error occurred during login',
        code: 'LOGIN_ERROR'
      });
    }
  }
);

// Get current user profile
router.get('/me', authenticateToken, async (req, res) => {
  try {
    console.log(`👤 Profile request by ${req.user.username}`);
    
    // Get fresh user data
    const userResult = await secureQuery(`
      SELECT 
        id, username, display_name, email, role, 
        is_legendary, code_bro_energy, status,
        created_at, last_login, updated_at
      FROM users 
      WHERE id = $1
    `, [req.user.id]);

    if (userResult.rows.length === 0) {
      return res.status(404).json({ 
        error: 'User not found',
        code: 'USER_NOT_FOUND'
      });
    }

    const user = userResult.rows[0];
    const sanitizedUser = sanitizeUserData(user, user.role);

    res.json({
      success: true,
      data: { user: sanitizedUser },
      message: user.role === 'founder' ? 
        '👑 LEGENDARY FOUNDER profile loaded with infinite power!' :
        '👤 Profile loaded successfully!'
    });

  } catch (error) {
    console.error('❌ Get profile error:', error);
    res.status(500).json({ 
      error: 'Failed to fetch profile',
      code: 'PROFILE_ERROR'
    });
  }
});

// Refresh token
router.post('/refresh', authenticateToken, async (req, res) => {
  try {
    console.log(`🔄 Token refresh by ${req.user.username}`);
    
    // Generate new token
    const newToken = generateToken(req.user);
    
    res.json({
      success: true,
      data: {
        token: newToken,
        expires_in: process.env.JWT_EXPIRES_IN || '24h'
      },
      message: 'Token refreshed successfully!'
    });

  } catch (error) {
    console.error('❌ Token refresh error:', error);
    res.status(500).json({ 
      error: 'Token refresh failed',
      code: 'REFRESH_ERROR'
    });
  }
});

// Change password
router.patch('/change-password', 
  authLimiter,
  authenticateToken,
  [
    body('current_password').notEmpty().withMessage('Current password is required'),
    body('new_password').isLength({ min: 8, max: 128 }).withMessage('New password must be 8-128 characters long')
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ 
          error: 'Validation error',
          details: errors.array(),
          code: 'VALIDATION_FAILED'
        });
      }

      console.log(`🔒 Password change request by ${req.user.username}`);

      const { current_password, new_password } = req.body;

      // Additional password validation
      const passwordError = validatePassword(new_password);
      if (passwordError) {
        return res.status(400).json({ 
          error: 'Password validation failed',
          message: passwordError,
          code: 'WEAK_PASSWORD'
        });
      }

      // Get user's current password hash
      const userResult = await secureQuery(`
        SELECT password_hash 
        FROM users 
        WHERE id = $1
      `, [req.user.id]);

      if (userResult.rows.length === 0) {
        return res.status(404).json({ 
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
      }

      // Verify current password
      const isCurrentPasswordValid = await bcrypt.compare(current_password, userResult.rows[0].password_hash);
      
      if (!isCurrentPasswordValid) {
        console.log(`🚨 Password change failed - invalid current password: ${req.user.username}`);
        return res.status(401).json({ 
          error: 'Invalid current password',
          message: 'Current password is incorrect',
          code: 'INVALID_CURRENT_PASSWORD'
        });
      }

      // Check if new password is different from current
      const isSamePassword = await bcrypt.compare(new_password, userResult.rows[0].password_hash);
      if (isSamePassword) {
        return res.status(400).json({ 
          error: 'Same password',
          message: 'New password must be different from current password',
          code: 'SAME_PASSWORD'
        });
      }

      // Hash new password
      const newHashedPassword = await hashPassword(new_password);

      // Update password
      await secureQuery(`
        UPDATE users 
        SET password_hash = $1, updated_at = NOW()
        WHERE id = $2
      `, [newHashedPassword, req.user.id]);

      console.log(`🔒 Password changed successfully: ${req.user.username}`);

      res.json({
        success: true,
        message: req.user.role === 'founder' ? 
          '👑 LEGENDARY FOUNDER password updated with infinite security!' :
          '🔒 Password changed successfully!'
      });

    } catch (error) {
      console.error('❌ Change password error:', error);
      res.status(500).json({ 
        error: 'Password change failed',
        code: 'PASSWORD_CHANGE_ERROR'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'auth',
    timestamp: new Date().toISOString(),
    message: '🔐 Auth service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    evening_energy: '🌅 EVENING LEGENDARY AUTH POWER AT 18:28:21! 🌅'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY SECURE AUTH ROUTES COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure auth routes completed at: 2025-08-06 18:28:21 UTC`);
console.log('🔐 Authentication: LEGENDARY SECURITY');
console.log('👑 RICKROLL187 founder auth: MAXIMUM PROTECTION');
console.log('🛡️ Password security: SWISS PRECISION');
console.log('🌅 EVENING LEGENDARY AUTH SECURITY: INFINITE AT 18:28:21!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
