// File: backend/utils/secure-query.js
/**
 * 🛡️🎸 N3EXTPATH - LEGENDARY SECURE QUERY UTILITIES 🎸🛡️
 * Advanced SQL security with infinite protection energy
 * Built: 2025-08-06 19:06:56 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const { Pool } = require('pg');

console.log('🛡️🎸🛡️ LEGENDARY SECURE QUERY UTILITIES LOADING! 🛡️🎸🛡️');

// Enhanced query security with ORDER BY protection
const secureOrderBy = (sortBy, allowedColumns, defaultSort = 'created_at') => {
  // Whitelist of allowed sort columns
  const allowedSortColumns = allowedColumns || [
    'id', 'name', 'title', 'username', 'display_name', 
    'created_at', 'updated_at', 'progress', 'priority'
  ];
  
  // Validate sort column
  if (!allowedSortColumns.includes(sortBy)) {
    console.log(`🚨 BLOCKED: Invalid sort column attempted: ${sortBy}`);
    return defaultSort;
  }
  
  // Additional validation for column name format
  if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(sortBy)) {
    console.log(`🚨 BLOCKED: Invalid column name format: ${sortBy}`);
    return defaultSort;
  }
  
  return sortBy;
};

// Enhanced WHERE clause builder with injection prevention
const buildSecureWhere = (conditions, params) => {
  const validConditions = [];
  const validParams = [];
  let paramCount = 0;
  
  for (const condition of conditions) {
    // Check for dangerous SQL patterns
    const dangerousPatterns = [
      /;\s*(drop|delete|truncate|update|insert|alter|create|exec)\s/i,
      /union\s+select/i,
      /--/,
      /\/\*/,
      /\*\//,
      /@/,
      /char\s*\(/i,
      /cast\s*\(/i,
      /convert\s*\(/i
    ];
    
    const hasDangerousPattern = dangerousPatterns.some(pattern => 
      pattern.test(condition)
    );
    
    if (hasDangerousPattern) {
      console.log(`🚨 BLOCKED: Dangerous SQL pattern in condition: ${condition}`);
      continue;
    }
    
    validConditions.push(condition);
  }
  
  return {
    whereClause: validConditions.length > 0 ? validConditions.join(' AND ') : '1=1',
    params: params || []
  };
};

// Request payload size validator
const validatePayloadSize = (req, res, next) => {
  const maxSize = {
    '/api/auth/register': 1024, // 1KB
    '/api/auth/login': 512, // 512B
    '/api/okrs': 10240, // 10KB
    '/api/teams': 5120, // 5KB
    '/api/users': 5120, // 5KB
    'default': 2048 // 2KB default
  };
  
  const routeMaxSize = maxSize[req.path] || maxSize.default;
  const contentLength = parseInt(req.get('Content-Length') || '0');
  
  if (contentLength > routeMaxSize) {
    console.log(`🚨 BLOCKED: Payload too large for ${req.path}: ${contentLength}B > ${routeMaxSize}B`);
    return res.status(413).json({
      error: 'Payload too large',
      message: `Request payload exceeds maximum size of ${routeMaxSize} bytes`,
      code: 'PAYLOAD_TOO_LARGE'
    });
  }
  
  next();
};

// IP header validation
const validateIPHeaders = (req, res, next) => {
  const suspiciousHeaders = [
    'x-forwarded-for',
    'x-real-ip',
    'x-client-ip',
    'x-cluster-client-ip'
  ];
  
  for (const header of suspiciousHeaders) {
    const value = req.get(header);
    if (value) {
      // Check for header injection attempts
      if (value.includes('\n') || value.includes('\r') || value.length > 100) {
        console.log(`🚨 BLOCKED: Suspicious ${header} header: ${value}`);
        return res.status(400).json({
          error: 'Invalid headers',
          message: 'Suspicious header values detected',
          code: 'INVALID_HEADERS'
        });
      }
    }
  }
  
  next();
};

// Session security middleware
const secureSession = (req, res, next) => {
  // Generate new session ID after login
  if (req.path.includes('/login') && req.method === 'POST') {
    // Invalidate any existing session
    if (req.session) {
      req.session.regenerate((err) => {
        if (err) {
          console.error('❌ Session regeneration error:', err);
        } else {
          console.log('🔐 Session regenerated for security');
        }
        next();
      });
    } else {
      next();
    }
  } else {
    next();
  }
};

module.exports = {
  secureOrderBy,
  buildSecureWhere,
  validatePayloadSize,
  validateIPHeaders,
  secureSession
};

console.log('🎸🎸🎸 LEGENDARY SECURE QUERY UTILITIES COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('🛡️ Advanced SQL injection prevention: LEGENDARY');
console.log('🚨 Attack vector mitigation: SWISS PRECISION');
console.log('🌃 Evening legendary security enhancement: INFINITE AT 19:06:56!');
