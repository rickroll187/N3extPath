// File: backend/utils/database.js
/**
 * 🗄️🎸 N3EXTPATH - LEGENDARY SECURE DATABASE UTILITIES 🎸🗄️
 * Swiss precision database security with infinite protection energy
 * Built: 2025-08-06 18:17:37 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const { Pool } = require('pg');
const { sanitizeQuery } = require('../middleware/security');

console.log('🗄️🎸🗄️ LEGENDARY SECURE DATABASE UTILITIES LOADING! 🗄️🎸🗄️');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure database utils loaded at: 2025-08-06 18:17:37 UTC`);

// Enhanced database pool with security
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
  max: 20, // Maximum connections
  idleTimeoutMillis: 30000, // 30 seconds
  connectionTimeoutMillis: 5000, // 5 seconds
  statement_timeout: 30000, // 30 second query timeout
  query_timeout: 30000, // 30 second query timeout
  application_name: 'n3extpath-api'
});

// Query execution with security validation
const secureQuery = async (text, params = [], options = {}) => {
  try {
    // Validate query and parameters
    const { query, params: validatedParams } = sanitizeQuery(text, params);
    
    // Log query for audit purposes (without sensitive data)
    const logQuery = query.replace(/\$\d+/g, '?').substring(0, 200);
    console.log(`🗄️ DB Query: ${logQuery}${query.length > 200 ? '...' : ''}`);
    
    // Track query performance
    const startTime = Date.now();
    
    // Execute query
    const result = await pool.query(query, validatedParams);
    
    const duration = Date.now() - startTime;
    
    // Log slow queries
    if (duration > 1000) {
      console.warn(`🐌 SLOW QUERY (${duration}ms): ${logQuery}`);
    }
    
    // Log query stats
    console.log(`🗄️ Query executed: ${result.rowCount} rows, ${duration}ms`);
    
    return result;
    
  } catch (error) {
    console.error('❌ Database query error:', {
      error: error.message,
      query: text.substring(0, 100),
      params: params.length,
      code: error.code,
      timestamp: new Date().toISOString()
    });
    
    // Don't expose internal database errors to clients
    const sanitizedError = new Error('Database operation failed');
    sanitizedError.code = 'DB_ERROR';
    sanitizedError.original = error.code;
    throw sanitizedError;
  }
};

// Transaction wrapper with security
const secureTransaction = async (callback) => {
  const client = await pool.connect();
  
  try {
    await client.query('BEGIN');
    console.log('🗄️ Transaction started');
    
    const result = await callback(client);
    
    await client.query('COMMIT');
    console.log('🗄️ Transaction committed');
    
    return result;
    
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('❌ Transaction rolled back:', error.message);
    throw error;
    
  } finally {
    client.release();
  }
};

// Safe user data retrieval
const getUserById = async (userId, requestingUserRole = 'user') => {
  try {
    const result = await secureQuery(`
      SELECT 
        id, username, display_name, email, role, 
        is_legendary, code_bro_energy, status,
        created_at, last_login
      FROM users 
      WHERE id = $1 AND status != 'deleted'
    `, [userId]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    const user = result.rows[0];
    
    // Sanitize based on requesting user's role
    const { sanitizeUserData } = require('../middleware/security');
    return sanitizeUserData(user, requestingUserRole);
    
  } catch (error) {
    console.error('❌ Get user error:', error);
    throw error;
  }
};

// Safe search with input validation
const searchUsers = async (searchTerm, limit = 20, offset = 0, requestingUserRole = 'user') => {
  try {
    // Validate and sanitize search term
    if (!searchTerm || typeof searchTerm !== 'string') {
      throw new Error('Invalid search term');
    }
    
    const sanitizedTerm = searchTerm.trim().substring(0, 100);
    
    if (sanitizedTerm.length < 2) {
      throw new Error('Search term too short');
    }
    
    // Validate pagination
    const validLimit = Math.min(Math.max(parseInt(limit) || 20, 1), 100);
    const validOffset = Math.max(parseInt(offset) || 0, 0);
    
    const result = await secureQuery(`
      SELECT 
        id, username, display_name, role, is_legendary,
        CASE 
          WHEN $4 = ANY(ARRAY['founder', 'admin']) THEN email
          ELSE NULL
        END as email
      FROM users 
      WHERE 
        (username ILIKE $1 OR display_name ILIKE $1)
        AND status = 'active'
      ORDER BY 
        CASE WHEN username ILIKE $1 THEN 0 ELSE 1 END,
        is_legendary DESC,
        code_bro_energy DESC
      LIMIT $2 OFFSET $3
    `, [`%${sanitizedTerm}%`, validLimit, validOffset, requestingUserRole]);
    
    return {
      users: result.rows,
      total: result.rowCount,
      limit: validLimit,
      offset: validOffset
    };
    
  } catch (error) {
    console.error('❌ Search users error:', error);
    throw error;
  }
};

// Database health check
const healthCheck = async () => {
  try {
    const start = Date.now();
    await secureQuery('SELECT 1 as health_check');
    const duration = Date.now() - start;
    
    return {
      status: 'healthy',
      response_time: duration,
      timestamp: new Date().toISOString(),
      connections: {
        total: pool.totalCount,
        idle: pool.idleCount,
        waiting: pool.waitingCount
      }
    };
    
  } catch (error) {
    console.error('❌ Database health check failed:', error);
    return {
      status: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
};

// Cleanup function for graceful shutdown
const cleanup = async () => {
  try {
    console.log('🗄️ Closing database connections...');
    await pool.end();
    console.log('🗄️ Database connections closed successfully');
  } catch (error) {
    console.error('❌ Error closing database connections:', error);
  }
};

// Handle process shutdown
process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);

module.exports = {
  pool,
  secureQuery,
  secureTransaction,
  getUserById,
  searchUsers,
  healthCheck,
  cleanup
};

console.log('🎸🎸🎸 LEGENDARY SECURE DATABASE UTILITIES COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure database utilities completed at: 2025-08-06 18:17:37 UTC`);
console.log('🗄️ Database security: LEGENDARY PRECISION');
console.log('👑 RICKROLL187 data protection: MAXIMUM SECURITY');
console.log('🔐 Query validation: SWISS PRECISION');
console.log('🌅 EVENING LEGENDARY DATABASE SECURITY: INFINITE AT 18:17:37!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
