// File: backend/routes/analytics.js
/**
 * 📊🎸 N3EXTPATH - LEGENDARY ANALYTICS API ROUTES 🎸📊
 * Swiss precision analytics with infinite code bro energy
 * Built: 2025-08-06 17:52:57 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const express = require('express');
const { Pool } = require('pg');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const { body, query, validationResult } = require('express-validator');

const router = express.Router();
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

console.log('📊🎸📊 LEGENDARY ANALYTICS ROUTES LOADING! 📊🎸📊');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Analytics routes loaded at: 2025-08-06 17:52:57 UTC`);
console.log('🌅 LATE AFTERNOON LEGENDARY ANALYTICS ENERGY AT 17:52:57!');

// =====================================
// 🛡️ MIDDLEWARE & RATE LIMITING 🛡️
// =====================================

// Analytics rate limiter
const analyticsLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many analytics requests from this IP, please try again later.',
    retryAfter: '15 minutes'
  }
});

// Auth middleware
const authenticateToken = async (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ 
      error: 'Access token required',
      message: 'Please provide a valid authentication token'
    });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const result = await pool.query(
      'SELECT id, username, display_name, email, role, is_legendary, code_bro_energy FROM users WHERE id = $1',
      [decoded.userId]
    );
    
    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Invalid token' });
    }
    
    req.user = result.rows[0];
    
    // Log legendary founder access
    if (req.user.role === 'founder') {
      console.log('👑🎸👑 RICKROLL187 FOUNDER ANALYTICS ACCESS! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER ANALYTICS WITH INFINITE CODE BRO ENERGY!');
    }
    
    next();
  } catch (error) {
    console.error('❌ Auth error:', error);
    return res.status(403).json({ error: 'Invalid token' });
  }
};

// Admin check middleware
const requireAdmin = (req, res, next) => {
  if (req.user.role !== 'founder' && req.user.role !== 'admin') {
    return res.status(403).json({ 
      error: 'Admin access required',
      message: 'This endpoint requires admin privileges'
    });
  }
  next();
};

// =====================================
// 📊 ANALYTICS ROUTES 📊
// =====================================

// Get dashboard analytics
router.get('/dashboard', 
  analyticsLimiter,
  authenticateToken,
  async (req, res) => {
    try {
      console.log(`📊 Dashboard analytics request by ${req.user.username} at 17:52:57 UTC`);

      // Get user analytics
      const userStats = await pool.query(`
        SELECT 
          COUNT(*) as total_users,
          COUNT(CASE WHEN last_login > NOW() - INTERVAL '24 hours' THEN 1 END) as active_users_24h,
          COUNT(CASE WHEN last_login > NOW() - INTERVAL '7 days' THEN 1 END) as active_users_7d,
          COUNT(CASE WHEN is_legendary = true THEN 1 END) as legendary_users,
          AVG(code_bro_energy) as avg_energy
        FROM users
      `);

      // Get OKR analytics
      const okrStats = await pool.query(`
        SELECT 
          COUNT(*) as total_okrs,
          COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_okrs,
          COUNT(CASE WHEN status = 'active' THEN 1 END) as active_okrs,
          COUNT(CASE WHEN is_legendary = true THEN 1 END) as legendary_okrs,
          AVG(progress) as avg_progress,
          AVG(confidence) as avg_confidence
        FROM okrs
      `);

      // Get team analytics
      const teamStats = await pool.query(`
        SELECT 
          COUNT(DISTINCT t.id) as total_teams,
          AVG(team_sizes.member_count) as avg_team_size,
          COUNT(CASE WHEN t.is_legendary = true THEN 1 END) as legendary_teams
        FROM teams t
        LEFT JOIN (
          SELECT team_id, COUNT(*) as member_count 
          FROM team_members 
          GROUP BY team_id
        ) team_sizes ON t.id = team_sizes.team_id
      `);

      // Get chat analytics
      const chatStats = await pool.query(`
        SELECT 
          COUNT(*) as total_messages,
          COUNT(CASE WHEN created_at > NOW() - INTERVAL '24 hours' THEN 1 END) as messages_24h,
          COUNT(CASE WHEN created_at > NOW() - INTERVAL '7 days' THEN 1 END) as messages_7d,
          COUNT(DISTINCT user_id) as active_chatters
        FROM messages
        WHERE created_at > NOW() - INTERVAL '30 days'
      `);

      // Special founder analytics
      let founderStats = null;
      if (req.user.role === 'founder') {
        founderStats = await pool.query(`
          SELECT 
            COUNT(*) as founder_okrs,
            AVG(progress) as founder_avg_progress,
            COUNT(CASE WHEN status = 'legendary' THEN 1 END) as legendary_founder_okrs,
            SUM(code_bro_energy) as total_energy_created
          FROM okrs 
          WHERE owner_id = $1 OR founder_priority = true
        `, [req.user.id]);
      }

      const analytics = {
        timestamp: new Date().toISOString(),
        user: {
          id: req.user.id,
          username: req.user.username,
          role: req.user.role,
          is_legendary: req.user.is_legendary,
          code_bro_energy: req.user.code_bro_energy
        },
        platform: {
          users: {
            total: parseInt(userStats.rows[0].total_users),
            active_24h: parseInt(userStats.rows[0].active_users_24h),
            active_7d: parseInt(userStats.rows[0].active_users_7d),
            legendary: parseInt(userStats.rows[0].legendary_users),
            avg_energy: parseFloat(userStats.rows[0].avg_energy || 0)
          },
          okrs: {
            total: parseInt(okrStats.rows[0].total_okrs),
            completed: parseInt(okrStats.rows[0].completed_okrs),
            active: parseInt(okrStats.rows[0].active_okrs),
            legendary: parseInt(okrStats.rows[0].legendary_okrs),
            avg_progress: parseFloat(okrStats.rows[0].avg_progress || 0),
            avg_confidence: parseFloat(okrStats.rows[0].avg_confidence || 0),
            completion_rate: okrStats.rows[0].total_okrs > 0 ? 
              (okrStats.rows[0].completed_okrs / okrStats.rows[0].total_okrs) * 100 : 0
          },
          teams: {
            total: parseInt(teamStats.rows[0].total_teams),
            avg_size: parseFloat(teamStats.rows[0].avg_team_size || 0),
            legendary: parseInt(teamStats.rows[0].legendary_teams)
          },
          chat: {
            total_messages: parseInt(chatStats.rows[0].total_messages),
            messages_24h: parseInt(chatStats.rows[0].messages_24h),
            messages_7d: parseInt(chatStats.rows[0].messages_7d),
            active_chatters: parseInt(chatStats.rows[0].active_chatters)
          }
        }
      };

      // Add founder stats if applicable
      if (founderStats && founderStats.rows.length > 0) {
        analytics.founder = {
          okrs: parseInt(founderStats.rows[0].founder_okrs),
          avg_progress: parseFloat(founderStats.rows[0].founder_avg_progress || 0),
          legendary_okrs: parseInt(founderStats.rows[0].legendary_founder_okrs),
          total_energy_created: parseInt(founderStats.rows[0].total_energy_created || 0)
        };
        
        console.log('👑 FOUNDER DASHBOARD ANALYTICS SERVED WITH INFINITE PRECISION! 👑');
      }

      console.log('📊 Dashboard analytics served successfully!');
      res.json({
        success: true,
        data: analytics,
        message: req.user.role === 'founder' ? 
          '👑 Legendary founder dashboard analytics with infinite insights!' : 
          '📊 Dashboard analytics with Swiss precision!'
      });

    } catch (error) {
      console.error('❌ Dashboard analytics error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch dashboard analytics',
        message: 'An error occurred while retrieving analytics data'
      });
    }
  }
);

// Get OKR analytics
router.get('/okrs',
  analyticsLimiter,
  authenticateToken,
  [
    query('timeframe').optional().isIn(['7d', '30d', '90d', '1y']),
    query('team_id').optional().isUUID(),
    query('owner_id').optional().isUUID()
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ 
          error: 'Validation error',
          details: errors.array()
        });
      }

      console.log(`🎯 OKR analytics request by ${req.user.username}`);

      const { timeframe = '30d', team_id, owner_id } = req.query;
      
      // Build time condition
      const timeCondition = {
        '7d': "created_at > NOW() - INTERVAL '7 days'",
        '30d': "created_at > NOW() - INTERVAL '30 days'",
        '90d': "created_at > NOW() - INTERVAL '90 days'",
        '1y': "created_at > NOW() - INTERVAL '1 year'"
      }[timeframe];

      let whereConditions = [timeCondition];
      let queryParams = [];
      let paramCount = 0;

      if (team_id) {
        paramCount++;
        whereConditions.push(`team_id = $${paramCount}`);
        queryParams.push(team_id);
      }

      if (owner_id) {
        paramCount++;
        whereConditions.push(`owner_id = $${paramCount}`);
        queryParams.push(owner_id);
      }

      const whereClause = whereConditions.join(' AND ');

      // Get OKR progress trends
      const progressTrends = await pool.query(`
        SELECT 
          DATE_TRUNC('day', created_at) as date,
          COUNT(*) as created_count,
          AVG(progress) as avg_progress,
          COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count
        FROM okrs 
        WHERE ${whereClause}
        GROUP BY DATE_TRUNC('day', created_at)
        ORDER BY date DESC
        LIMIT 30
      `, queryParams);

      // Get status distribution
      const statusDistribution = await pool.query(`
        SELECT 
          status,
          COUNT(*) as count,
          AVG(progress) as avg_progress
        FROM okrs 
        WHERE ${whereClause}
        GROUP BY status
        ORDER BY count DESC
      `, queryParams);

      // Get top performers
      const topPerformers = await pool.query(`
        SELECT 
          u.username,
          u.display_name,
          u.is_legendary,
          COUNT(o.id) as okr_count,
          AVG(o.progress) as avg_progress,
          COUNT(CASE WHEN o.status = 'completed' THEN 1 END) as completed_count
        FROM users u
        JOIN okrs o ON u.id = o.owner_id
        WHERE ${whereClause}
        GROUP BY u.id, u.username, u.display_name, u.is_legendary
        HAVING COUNT(o.id) > 0
        ORDER BY AVG(o.progress) DESC, COUNT(CASE WHEN o.status = 'completed' THEN 1 END) DESC
        LIMIT 10
      `, queryParams);

      const analytics = {
        timeframe,
        filters: { team_id, owner_id },
        trends: progressTrends.rows.map(row => ({
          date: row.date,
          created: parseInt(row.created_count),
          avg_progress: parseFloat(row.avg_progress || 0),
          completed: parseInt(row.completed_count)
        })),
        status_distribution: statusDistribution.rows.map(row => ({
          status: row.status,
          count: parseInt(row.count),
          avg_progress: parseFloat(row.avg_progress || 0)
        })),
        top_performers: topPerformers.rows.map(row => ({
          username: row.username,
          display_name: row.display_name,
          is_legendary: row.is_legendary,
          okr_count: parseInt(row.okr_count),
          avg_progress: parseFloat(row.avg_progress || 0),
          completed_count: parseInt(row.completed_count)
        }))
      };

      console.log('🎯 OKR analytics served successfully!');
      res.json({
        success: true,
        data: analytics,
        message: 'OKR analytics retrieved with Swiss precision!'
      });

    } catch (error) {
      console.error('❌ OKR analytics error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch OKR analytics',
        message: 'An error occurred while retrieving OKR analytics'
      });
    }
  }
);

// Get user analytics
router.get('/users',
  analyticsLimiter,
  authenticateToken,
  requireAdmin,
  [
    query('timeframe').optional().isIn(['7d', '30d', '90d', '1y']),
    query('include_inactive').optional().isBoolean()
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ 
          error: 'Validation error',
          details: errors.array()
        });
      }

      console.log(`👥 User analytics request by ${req.user.username}`);
      
      if (req.user.role === 'founder') {
        console.log('👑 FOUNDER USER ANALYTICS ACCESS WITH INFINITE INSIGHTS! 👑');
      }

      const { timeframe = '30d', include_inactive = false } = req.query;

      // Get user registration trends
      const registrationTrends = await pool.query(`
        SELECT 
          DATE_TRUNC('day', created_at) as date,
          COUNT(*) as new_users,
          COUNT(CASE WHEN is_legendary = true THEN 1 END) as legendary_users
        FROM users 
        WHERE created_at > NOW() - INTERVAL '${timeframe === '7d' ? '7 days' : timeframe === '90d' ? '90 days' : timeframe === '1y' ? '1 year' : '30 days'}'
        GROUP BY DATE_TRUNC('day', created_at)
        ORDER BY date DESC
        LIMIT 30
      `);

      // Get user activity patterns
      const activityPatterns = await pool.query(`
        SELECT 
          DATE_TRUNC('day', last_login) as date,
          COUNT(*) as active_users,
          AVG(code_bro_energy) as avg_energy
        FROM users 
        WHERE last_login > NOW() - INTERVAL '30 days'
        ${!include_inactive ? "AND last_login > NOW() - INTERVAL '7 days'" : ''}
        GROUP BY DATE_TRUNC('day', last_login)
        ORDER BY date DESC
        LIMIT 30
      `);

      // Get role distribution
      const roleDistribution = await pool.query(`
        SELECT 
          role,
          COUNT(*) as count,
          AVG(code_bro_energy) as avg_energy
        FROM users 
        GROUP BY role
        ORDER BY count DESC
      `);

      // Get engagement metrics
      const engagementMetrics = await pool.query(`
        SELECT 
          u.id,
          u.username,
          u.display_name,
          u.role,
          u.is_legendary,
          u.code_bro_energy,
          COUNT(DISTINCT o.id) as okr_count,
          COUNT(DISTINCT m.id) as message_count,
          COUNT(DISTINCT tm.team_id) as team_count
        FROM users u
        LEFT JOIN okrs o ON u.id = o.owner_id
        LEFT JOIN messages m ON u.id = m.user_id AND m.created_at > NOW() - INTERVAL '30 days'
        LEFT JOIN team_members tm ON u.id = tm.user_id
        WHERE u.created_at > NOW() - INTERVAL '${timeframe === '7d' ? '7 days' : timeframe === '90d' ? '90 days' : timeframe === '1y' ? '1 year' : '30 days'}'
        GROUP BY u.id, u.username, u.display_name, u.role, u.is_legendary, u.code_bro_energy
        ORDER BY u.code_bro_energy DESC
        LIMIT 20
      `);

      const analytics = {
        timeframe,
        include_inactive,
        registration_trends: registrationTrends.rows.map(row => ({
          date: row.date,
          new_users: parseInt(row.new_users),
          legendary_users: parseInt(row.legendary_users)
        })),
        activity_patterns: activityPatterns.rows.map(row => ({
          date: row.date,
          active_users: parseInt(row.active_users),
          avg_energy: parseFloat(row.avg_energy || 0)
        })),
        role_distribution: roleDistribution.rows.map(row => ({
          role: row.role,
          count: parseInt(row.count),
          avg_energy: parseFloat(row.avg_energy || 0)
        })),
        top_engaged_users: engagementMetrics.rows.map(row => ({
          id: row.id,
          username: row.username,
          display_name: row.display_name,
          role: row.role,
          is_legendary: row.is_legendary,
          code_bro_energy: parseInt(row.code_bro_energy),
          okr_count: parseInt(row.okr_count),
          message_count: parseInt(row.message_count),
          team_count: parseInt(row.team_count)
        }))
      };

      console.log('👥 User analytics served successfully!');
      res.json({
        success: true,
        data: analytics,
        message: req.user.role === 'founder' ? 
          '👑 Legendary founder user analytics with infinite precision!' : 
          '👥 User analytics with Swiss precision!'
      });

    } catch (error) {
      console.error('❌ User analytics error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch user analytics',
        message: 'An error occurred while retrieving user analytics'
      });
    }
  }
);

// Get team performance analytics
router.get('/teams/performance',
  analyticsLimiter,
  authenticateToken,
  [
    query('team_id').optional().isUUID(),
    query('timeframe').optional().isIn(['7d', '30d', '90d', '1y'])
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ 
          error: 'Validation error',
          details: errors.array()
        });
      }

      console.log(`🏆 Team performance analytics request by ${req.user.username}`);

      const { team_id, timeframe = '30d' } = req.query;

      // Check if user has access to team data
      let accessQuery = '';
      let accessParams = [];
      
      if (req.user.role !== 'founder' && req.user.role !== 'admin') {
        accessQuery = 'AND tm.user_id = $1';
        accessParams = [req.user.id];
      }

      // Get team performance metrics
      const teamPerformance = await pool.query(`
        SELECT 
          t.id,
          t.name,
          t.description,
          t.is_legendary,
          COUNT(DISTINCT tm.user_id) as member_count,
          COUNT(DISTINCT o.id) as okr_count,
          AVG(o.progress) as avg_progress,
          COUNT(CASE WHEN o.status = 'completed' THEN 1 END) as completed_okrs,
          COUNT(DISTINCT CASE WHEN m.created_at > NOW() - INTERVAL '7 days' THEN m.id END) as messages_7d,
          AVG(u.code_bro_energy) as avg_team_energy
        FROM teams t
        JOIN team_members tm ON t.id = tm.team_id
        LEFT JOIN okrs o ON t.id = o.team_id 
          AND o.created_at > NOW() - INTERVAL '${timeframe === '7d' ? '7 days' : timeframe === '90d' ? '90 days' : timeframe === '1y' ? '1 year' : '30 days'}'
        LEFT JOIN messages m ON t.id = m.team_id
        LEFT JOIN users u ON tm.user_id = u.id
        WHERE 1=1 ${team_id ? 'AND t.id = $' + (accessParams.length + 1) : ''} ${accessQuery}
        GROUP BY t.id, t.name, t.description, t.is_legendary
        ORDER BY avg_progress DESC, completed_okrs DESC
        LIMIT 50
      `, team_id ? [...accessParams, team_id] : accessParams);

      // Get team collaboration metrics
      const collaborationMetrics = await pool.query(`
        SELECT 
          t.id,
          t.name,
          COUNT(DISTINCT m.user_id) as active_members,
          COUNT(m.id) as total_messages,
          COUNT(DISTINCT m.user_id) / COUNT(DISTINCT tm.user_id)::float as participation_rate
        FROM teams t
        JOIN team_members tm ON t.id = tm.team_id
        LEFT JOIN messages m ON t.id = m.team_id 
          AND m.created_at > NOW() - INTERVAL '7 days'
        WHERE 1=1 ${team_id ? 'AND t.id = $' + (accessParams.length + 1) : ''} ${accessQuery}
        GROUP BY t.id, t.name
        ORDER BY participation_rate DESC
      `, team_id ? [...accessParams, team_id] : accessParams);

      const analytics = {
        timeframe,
        team_id,
        performance: teamPerformance.rows.map(row => ({
          id: row.id,
          name: row.name,
          description: row.description,
          is_legendary: row.is_legendary,
          member_count: parseInt(row.member_count),
          okr_count: parseInt(row.okr_count),
          avg_progress: parseFloat(row.avg_progress || 0),
          completed_okrs: parseInt(row.completed_okrs),
          completion_rate: row.okr_count > 0 ? (row.completed_okrs / row.okr_count) * 100 : 0,
          messages_7d: parseInt(row.messages_7d),
          avg_team_energy: parseFloat(row.avg_team_energy || 0)
        })),
        collaboration: collaborationMetrics.rows.map(row => ({
          id: row.id,
          name: row.name,
          active_members: parseInt(row.active_members),
          total_messages: parseInt(row.total_messages),
          participation_rate: parseFloat(row.participation_rate || 0) * 100
        }))
      };

      console.log('🏆 Team performance analytics served successfully!');
      res.json({
        success: true,
        data: analytics,
        message: 'Team performance analytics with Swiss precision!'
      });

    } catch (error) {
      console.error('❌ Team performance analytics error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch team performance analytics',
        message: 'An error occurred while retrieving team performance data'
      });
    }
  }
);

// Export analytics data
router.get('/export',
  analyticsLimiter,
  authenticateToken,
  requireAdmin,
  [
    query('type').isIn(['users', 'okrs', 'teams', 'all']),
    query('format').optional().isIn(['json', 'csv']),
    query('timeframe').optional().isIn(['7d', '30d', '90d', '1y'])
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ 
          error: 'Validation error',
          details: errors.array()
        });
      }

      console.log(`📊 Analytics export request by ${req.user.username}`);
      
      if (req.user.role === 'founder') {
        console.log('👑 FOUNDER ANALYTICS EXPORT WITH INFINITE DATA ACCESS! 👑');
      }

      const { type, format = 'json', timeframe = '30d' } = req.query;

      let exportData = {};

      // Export based on type
      switch (type) {
        case 'users':
          const users = await pool.query(`
            SELECT 
              u.id, u.username, u.display_name, u.email, u.role, 
              u.is_legendary, u.code_bro_energy, u.created_at, u.last_login,
              COUNT(DISTINCT o.id) as okr_count,
              COUNT(DISTINCT m.id) as message_count
            FROM users u
            LEFT JOIN okrs o ON u.id = o.owner_id
            LEFT JOIN messages m ON u.id = m.user_id AND m.created_at > NOW() - INTERVAL '30 days'
            GROUP BY u.id, u.username, u.display_name, u.email, u.role, u.is_legendary, u.code_bro_energy, u.created_at, u.last_login
            ORDER BY u.created_at DESC
          `);
          exportData.users = users.rows;
          break;

        case 'okrs':
          const okrs = await pool.query(`
            SELECT 
              o.*, u.username as owner_username, t.name as team_name
            FROM okrs o
            LEFT JOIN users u ON o.owner_id = u.id
            LEFT JOIN teams t ON o.team_id = t.id
            WHERE o.created_at > NOW() - INTERVAL '${timeframe === '7d' ? '7 days' : timeframe === '90d' ? '90 days' : timeframe === '1y' ? '1 year' : '30 days'}'
            ORDER BY o.created_at DESC
          `);
          exportData.okrs = okrs.rows;
          break;

        case 'teams':
          const teams = await pool.query(`
            SELECT 
              t.*, 
              COUNT(DISTINCT tm.user_id) as member_count,
              COUNT(DISTINCT o.id) as okr_count,
              AVG(o.progress) as avg_progress
            FROM teams t
            LEFT JOIN team_members tm ON t.id = tm.team_id
            LEFT JOIN okrs o ON t.id = o.team_id
            GROUP BY t.id
            ORDER BY t.created_at DESC
          `);
          exportData.teams = teams.rows;
          break;

        case 'all':
        default:
          // Get summary of all data
          const summary = await pool.query(`
            SELECT 
              'users' as type,
              COUNT(*) as total,
              COUNT(CASE WHEN created_at > NOW() - INTERVAL '7 days' THEN 1 END) as recent
            FROM users
            UNION ALL
            SELECT 
              'okrs' as type,
              COUNT(*) as total,
              COUNT(CASE WHEN created_at > NOW() - INTERVAL '7 days' THEN 1 END) as recent
            FROM okrs
            UNION ALL
            SELECT 
              'teams' as type,
              COUNT(*) as total,
              COUNT(CASE WHEN created_at > NOW() - INTERVAL '7 days' THEN 1 END) as recent
            FROM teams
            UNION ALL
            SELECT 
              'messages' as type,
              COUNT(*) as total,
              COUNT(CASE WHEN created_at > NOW() - INTERVAL '7 days' THEN 1 END) as recent
            FROM messages
          `);
          exportData.summary = summary.rows;
          break;
      }

      // Add metadata
      const metadata = {
        export_timestamp: new Date().toISOString(),
        exported_by: {
          id: req.user.id,
          username: req.user.username,
          role: req.user.role
        },
        parameters: {
          type,
          format,
          timeframe
        },
        platform: 'N3EXTPATH',
        version: '1.0.0'
      };

      exportData.metadata = metadata;

      // Set appropriate headers
      const filename = `n3extpath_analytics_${type}_${timeframe}_${Date.now()}`;
      
      if (format === 'csv') {
        // TODO: Implement CSV conversion
        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Content-Disposition', `attachment; filename="${filename}.csv"`);
        res.status(501).json({ 
          error: 'CSV export not yet implemented',
          message: 'CSV export functionality coming soon with Swiss precision!'
        });
      } else {
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Content-Disposition', `attachment; filename="${filename}.json"`);
        
        console.log('📊 Analytics export completed successfully!');
        res.json({
          success: true,
          data: exportData,
          message: req.user.role === 'founder' ? 
            '👑 Legendary founder analytics export with infinite data precision!' : 
            '📊 Analytics export with Swiss precision!'
        });
      }

    } catch (error) {
      console.error('❌ Analytics export error:', error);
      res.status(500).json({ 
        error: 'Failed to export analytics',
        message: 'An error occurred while exporting analytics data'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'analytics',
    timestamp: new Date().toISOString(),
    message: '📊 Analytics service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime()
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY ANALYTICS ROUTES COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Analytics routes completed at: 2025-08-06 17:52:57 UTC`);
console.log('📊 Analytics API: SWISS PRECISION');
console.log('👑 RICKROLL187 founder analytics: LEGENDARY');
console.log('🔍 Data insights: MAXIMUM PRECISION');
console.log('🌅 LATE AFTERNOON LEGENDARY ANALYTICS ENERGY: INFINITE AT 17:52:57!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
