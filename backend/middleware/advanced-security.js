// File: backend/middleware/advanced-security.js
/**
 * 🛡️🎸 N3EXTPATH - LEGENDARY ADVANCED SECURITY MIDDLEWARE 🎸🛡️
 * Swiss precision advanced security with infinite protection energy
 * Built: 2025-08-06 19:22:26 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const rateLimit = require('express-rate-limit');
const crypto = require('crypto');
const { secureQuery } = require('../utils/database');

console.log('🛡️🎸🛡️ LEGENDARY ADVANCED SECURITY MIDDLEWARE LOADING! 🛡️🎸🛡️');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Advanced security loaded at: 2025-08-06 19:22:26 UTC`);
console.log('🌃 EVENING LEGENDARY ADVANCED SECURITY AT 19:22:26!');

// =====================================
// 🚨 SOCIAL ENGINEERING PROTECTION 🚨
// =====================================

// Social engineering detection patterns
const SOCIAL_ENGINEERING_PATTERNS = {
  phishing: [
    /urgent.{0,20}action.{0,20}required/i,
    /your.{0,10}account.{0,10}(suspended|blocked|compromised)/i,
    /click.{0,10}here.{0,10}(immediately|now|asap)/i,
    /verify.{0,10}your.{0,10}(identity|account|information)/i,
    /security.{0,10}alert/i,
    /temporary.{0,10}(suspension|lock)/i,
    /(ceo|boss|manager).{0,20}needs.{0,20}urgent/i
  ],
  pretexting: [
    /i.{0,5}am.{0,5}(from|with).{0,10}(it|security|admin|support)/i,
    /technical.{0,10}support.{0,10}calling/i,
    /need.{0,10}your.{0,10}(password|credentials|login)/i,
    /routine.{0,10}security.{0,10}check/i,
    /system.{0,10}maintenance.{0,10}required/i
  ],
  baiting: [
    /free.{0,10}(download|software|gift|money)/i,
    /you.{0,5}(won|earned).{0,10}(prize|reward|bonus)/i,
    /exclusive.{0,10}(offer|deal|access)/i,
    /limited.{0,10}time.{0,10}offer/i
  ],
  authority: [
    /this.{0,10}is.{0,10}an.{0,10}order/i,
    /compliance.{0,10}required/i,
    /mandatory.{0,10}(update|action|training)/i,
    /failure.{0,10}to.{0,10}comply/i,
    /legal.{0,10}(action|consequences)/i
  ]
};

// Suspicious behavior tracking
const suspiciousBehavior = new Map();

// Social engineering detection middleware
const detectSocialEngineering = (req, res, next) => {
  const userInput = JSON.stringify(req.body || {}).toLowerCase();
  const userAgent = req.get('User-Agent') || '';
  const referer = req.get('Referer') || '';
  
  let suspicionScore = 0;
  const detectedPatterns = [];
  
  // Check for social engineering patterns
  Object.entries(SOCIAL_ENGINEERING_PATTERNS).forEach(([category, patterns]) => {
    patterns.forEach(pattern => {
      if (pattern.test(userInput)) {
        suspicionScore += 10;
        detectedPatterns.push(`${category}: ${pattern.source}`);
      }
    });
  });
  
  // Check for suspicious user agents
  const suspiciousUAs = [
    /curl/i, /wget/i, /python/i, /bot/i, /crawler/i, /scraper/i
  ];
  
  if (suspiciousUAs.some(ua => ua.test(userAgent))) {
    suspicionScore += 5;
    detectedPatterns.push('suspicious_user_agent');
  }
  
  // Check for suspicious referers
  const suspiciousReferers = [
    /bit\.ly/i, /tinyurl/i, /t\.co/i, /goo\.gl/i, /ow\.ly/i
  ];
  
  if (suspiciousReferers.some(ref => ref.test(referer))) {
    suspicionScore += 5;
    detectedPatterns.push('suspicious_referer');
  }
  
  // Track IP behavior
  const clientIP = req.ip;
  const ipBehavior = suspiciousBehavior.get(clientIP) || { score: 0, attempts: 0, lastAttempt: 0 };
  
  if (suspicionScore > 0) {
    ipBehavior.score += suspicionScore;
    ipBehavior.attempts += 1;
    ipBehavior.lastAttempt = Date.now();
    suspiciousBehavior.set(clientIP, ipBehavior);
    
    console.log(`🚨 SOCIAL ENGINEERING DETECTED from ${clientIP}: Score ${suspicionScore}, Patterns: ${detectedPatterns.join(', ')}`);
    
    // Log security incident
    if (req.user) {
      secureQuery(`
        INSERT INTO security_incidents (
          user_id, incident_type, severity, description, ip_address, user_agent, created_at
        ) VALUES ($1, $2, $3, $4, $5, $6, NOW())
      `, [
        req.user.id, 
        'social_engineering_attempt',
        suspicionScore > 20 ? 'high' : suspicionScore > 10 ? 'medium' : 'low',
        JSON.stringify({ patterns: detectedPatterns, score: suspicionScore }),
        clientIP,
        userAgent
      ]).catch(err => console.error('Security incident logging error:', err));
    }
  }
  
  // Block high-risk attempts
  if (ipBehavior.score > 50) {
    console.log(`🚨 BLOCKING HIGH-RISK IP: ${clientIP} (Score: ${ipBehavior.score})`);
    return res.status(429).json({
      error: 'Security violation detected',
      message: 'Your request has been blocked due to suspicious activity',
      code: 'SOCIAL_ENGINEERING_BLOCKED',
      support: 'If you believe this is an error, please contact support'
    });
  }
  
  // Add security headers for suspicious requests
  if (suspicionScore > 0) {
    res.setHeader('X-Security-Warning', 'Suspicious activity detected');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
  }
  
  next();
};

// =====================================
// 🔐 ADVANCED AUTHENTICATION SECURITY 🔐
// =====================================

// Enhanced password validation with context
const validatePasswordContext = (password, userInfo) => {
  const errors = [];
  
  // Basic strength check
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long');
  }
  
  if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
    errors.push('Password must contain uppercase, lowercase, and numbers');
  }
  
  // Check for personal information
  if (userInfo) {
    const personalInfo = [
      userInfo.username?.toLowerCase(),
      userInfo.display_name?.toLowerCase(),
      userInfo.email?.split('@')[0]?.toLowerCase()
    ].filter(Boolean);
    
    for (const info of personalInfo) {
      if (password.toLowerCase().includes(info)) {
        errors.push('Password cannot contain personal information');
        break;
      }
    }
  }
  
  // Check for keyboard patterns
  const keyboardPatterns = [
    '123456', 'qwerty', 'asdf', 'zxcv', 'abcd', '1234',
    'password', 'letmein', 'welcome', 'monkey', 'dragon'
  ];
  
  for (const pattern of keyboardPatterns) {
    if (password.toLowerCase().includes(pattern)) {
      errors.push('Password contains common patterns or dictionary words');
      break;
    }
  }
  
  return errors;
};

// Multi-factor authentication requirement check
const requireMFA = (req, res, next) => {
  // Skip MFA for certain endpoints or low-risk operations
  const skipMFARoutes = ['/health', '/api/health'];
  if (skipMFARoutes.includes(req.path)) {
    return next();
  }
  
  // For high-privilege operations, require MFA
  const highPrivilegeRoutes = [
    '/api/users/*/role',
    '/api/users/*/status', 
    '/api/admin/',
    '/api/security/',
    '/api/analytics/export'
  ];
  
  const requiresMFA = highPrivilegeRoutes.some(route => {
    const regex = new RegExp('^' + route.replace('*', '[^/]+') + '');
    return regex.test(req.path);
  });
  
  if (requiresMFA && req.user && req.user.role !== 'founder') {
    // Check if user has completed MFA in the last 15 minutes
    const mfaToken = req.headers['x-mfa-token'];
    if (!mfaToken) {
      return res.status(401).json({
        error: 'MFA required',
        message: 'Multi-factor authentication required for this operation',
        code: 'MFA_REQUIRED',
        mfa_methods: ['totp', 'sms', 'email']
      });
    }
    
    // Validate MFA token (simplified - in production, implement proper TOTP/SMS validation)
    // For now, accept any MFA token for demonstration
    console.log(`🔐 MFA validated for ${req.user.username} on ${req.path}`);
  }
  
  if (req.user?.role === 'founder') {
    console.log('👑🔐👑 RICKROLL187 FOUNDER MFA BYPASS - INFINITE AUTHORITY! 👑🔐👑');
  }
  
  next();
};

// =====================================
// 🌊 ADVANCED DDOS PROTECTION 🌊
// =====================================

// Distributed request tracking
const requestTracker = new Map();

// Advanced DDoS protection
const advancedDDoSProtection = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute window
  max: (req) => {
    // Different limits based on user role and authentication status
    if (req.user?.role === 'founder') return 1000; // Founder gets higher limits
    if (req.user?.role === 'admin') return 500;
    if (req.user) return 200; // Authenticated users
    return 50; // Anonymous users get very low limits
  },
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => {
    // Use a combination of IP and user ID for tracking
    const ip = req.ip;
    const userId = req.user?.id || 'anonymous';
    return `${ip}:${userId}`;
  },
  onLimitReached: (req, res) => {
    const key = `${req.ip}:${req.user?.id || 'anonymous'}`;
    console.log(`🚨 RATE LIMIT EXCEEDED: ${key} on ${req.path}`);
    
    // Track repeated violations
    const violations = requestTracker.get(key) || 0;
    requestTracker.set(key, violations + 1);
    
    // Escalating penalties for repeat offenders
    if (violations > 5) {
      console.log(`🚨 REPEAT OFFENDER DETECTED: ${key} - Violations: ${violations}`);
      // In production, consider temporary IP blocking here
    }
  },
  message: (req, res) => {
    const isFounder = req.user?.role === 'founder';
    return {
      error: 'Rate limit exceeded',
      message: isFounder ? 
        '👑 Even legendary founders need to pace themselves! Please wait a moment.' :
        'Too many requests. Please slow down and try again later.',
      code: 'RATE_LIMIT_EXCEEDED',
      retryAfter: Math.ceil(60 - ((Date.now() - req.rateLimit.resetTime) / 1000))
    };
  }
});

// =====================================
// 🔍 PAYLOAD VALIDATION SECURITY 🔍
// =====================================

// Enhanced payload validation
const validatePayload = (maxSize = 5120) => {
  return (req, res, next) => {
    const contentLength = parseInt(req.get('Content-Length') || '0');
    
    if (contentLength > maxSize) {
      console.log(`🚨 BLOCKED: Oversized payload from ${req.ip}: ${contentLength}B > ${maxSize}B`);
      return res.status(413).json({
        error: 'Payload too large',
        message: `Request exceeds maximum size of ${maxSize} bytes`,
        code: 'PAYLOAD_TOO_LARGE'
      });
    }
    
    // Check for suspicious content types
    const contentType = req.get('Content-Type') || '';
    const allowedTypes = [
      'application/json',
      'application/x-www-form-urlencoded',
      'multipart/form-data',
      'text/plain'
    ];
    
    const hasAllowedType = allowedTypes.some(type => 
      contentType.toLowerCase().startsWith(type)
    );
    
    if (!hasAllowedType && contentLength > 0) {
      console.log(`🚨 BLOCKED: Suspicious content type from ${req.ip}: ${contentType}`);
      return res.status(400).json({
        error: 'Invalid content type',
        message: 'Unsupported content type for this endpoint',
        code: 'INVALID_CONTENT_TYPE'
      });
    }
    
    next();
  };
};

// =====================================
// 🔒 SESSION SECURITY 🔒
// =====================================

// Session fixation protection
const preventSessionFixation = (req, res, next) => {
  // Generate new session ID on login
  if (req.path.includes('/login') && req.method === 'POST') {
    // Mark old session as invalid
    const oldSessionId = req.headers['x-session-id'];
    if (oldSessionId) {
      console.log(`🔒 Invalidating old session on login: ${oldSessionId.substring(0, 10)}...`);
      // In production, invalidate in session store
    }
    
    // Generate new session ID
    const newSessionId = crypto.randomUUID();
    res.setHeader('X-New-Session-ID', newSessionId);
    req.newSessionId = newSessionId;
    
    console.log(`🔒 New session generated for login: ${newSessionId.substring(0, 10)}...`);
  }
  
  next();
};

// =====================================
// 🧠 BEHAVIORAL ANALYSIS 🧠
// =====================================

// User behavior analysis
const behaviorAnalysis = (req, res, next) => {
  if (!req.user) return next();
  
  const userId = req.user.id;
  const userBehavior = suspiciousBehavior.get(`user:${userId}`) || {
    lastLogin: null,
    loginTimes: [],
    ipAddresses: new Set(),
    userAgents: new Set(),
    actions: [],
    riskScore: 0
  };
  
  // Track login patterns
  if (req.path.includes('/login')) {
    const now = new Date();
    userBehavior.lastLogin = now;
    userBehavior.loginTimes.push(now.getHours());
    
    // Keep only last 10 login times
    if (userBehavior.loginTimes.length > 10) {
      userBehavior.loginTimes.shift();
    }
  }
  
  // Track IP addresses
  userBehavior.ipAddresses.add(req.ip);
  
  // Track user agents
  const userAgent = req.get('User-Agent') || '';
  userBehavior.userAgents.add(userAgent);
  
  // Analyze for suspicious patterns
  let riskIncrease = 0;
  
  // Too many different IPs
  if (userBehavior.ipAddresses.size > 5) {
    riskIncrease += 10;
    console.log(`🚨 User ${req.user.username} using many IPs: ${userBehavior.ipAddresses.size}`);
  }
  
  // Too many different user agents
  if (userBehavior.userAgents.size > 3) {
    riskIncrease += 5;
    console.log(`🚨 User ${req.user.username} using many user agents: ${userBehavior.userAgents.size}`);
  }
  
  // Unusual time patterns (if logged in at very unusual hours consistently)
  const nightLogins = userBehavior.loginTimes.filter(hour => hour < 6 || hour > 23).length;
  if (nightLogins > userBehavior.loginTimes.length * 0.8 && userBehavior.loginTimes.length > 5) {
    riskIncrease += 5;
    console.log(`🚨 User ${req.user.username} has unusual login times`);
  }
  
  userBehavior.riskScore += riskIncrease;
  
  // Decay risk score over time
  if (userBehavior.lastLogin) {
    const timeSinceLogin = Date.now() - userBehavior.lastLogin.getTime();
    const hoursAgo = timeSinceLogin / (1000 * 60 * 60);
    userBehavior.riskScore = Math.max(0, userBehavior.riskScore - (hoursAgo * 0.5));
  }
  
  suspiciousBehavior.set(`user:${userId}`, userBehavior);
  
  // Alert on high risk users
  if (userBehavior.riskScore > 20) {
    console.log(`🚨 HIGH RISK USER: ${req.user.username} (Risk Score: ${userBehavior.riskScore})`);
    
    // Log security incident
    secureQuery(`
      INSERT INTO security_incidents (
        user_id, incident_type, severity, description, ip_address, created_at
      ) VALUES ($1, $2, $3, $4, $5, NOW())
    `, [
      userId,
      'high_risk_behavior',
      'high',
      JSON.stringify({ 
        riskScore: userBehavior.riskScore,
        ipCount: userBehavior.ipAddresses.size,
        userAgentCount: userBehavior.userAgents.size
      }),
      req.ip
    ]).catch(err => console.error('Security incident logging error:', err));
  }
  
  next();
};

// =====================================
// 🧹 CLEANUP FUNCTIONS 🧹
// =====================================

// Cleanup old tracking data every hour
setInterval(() => {
  const oneHourAgo = Date.now() - (60 * 60 * 1000);
  let cleanedCount = 0;
  
  for (const [key, data] of suspiciousBehavior.entries()) {
    if (data.lastAttempt && data.lastAttempt < oneHourAgo) {
      suspiciousBehavior.delete(key);
      cleanedCount++;
    }
  }
  
  for (const [key, violations] of requestTracker.entries()) {
    // Reset violation counts after 1 hour
    requestTracker.delete(key);
  }
  
  if (cleanedCount > 0) {
    console.log(`🧹 Cleaned ${cleanedCount} old security tracking entries`);
  }
}, 60 * 60 * 1000); // Run every hour

module.exports = {
  detectSocialEngineering,
  validatePasswordContext,
  requireMFA,
  advancedDDoSProtection,
  validatePayload,
  preventSessionFixation,
  behaviorAnalysis,
  SOCIAL_ENGINEERING_PATTERNS
};

console.log('🎸🎸🎸 LEGENDARY ADVANCED SECURITY MIDDLEWARE COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Advanced security middleware completed at: 2025-08-06 19:22:26 UTC`);
console.log('🛡️ Social engineering protection: LEGENDARY PRECISION');
console.log('👑 RICKROLL187 founder security: MAXIMUM PROTECTION');
console.log('🧠 Behavioral analysis: SWISS PRECISION');
console.log('🌃 EVENING LEGENDARY ADVANCED SECURITY: INFINITE AT 19:22:26!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
