// File: backend/routes/okrs.js
/**
 * 🎯🎸 N3EXTPATH - LEGENDARY SECURE OKRS ROUTES 🎸🎯
 * Swiss precision objective management with infinite security energy
 * Built: 2025-08-06 19:00:15 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const express = require('express');
const rateLimit = require('express-rate-limit');
const { body, query, param, validationResult } = require('express-validator');

const router = express.Router();
const { secureQuery, secureTransaction } = require('../utils/database');
const { authenticateToken, requirePermission } = require('../middleware/auth');
const { sanitizeUserData, createUserRateLimit } = require('../middleware/security');

console.log('🎯🎸🎯 LEGENDARY SECURE OKRS ROUTES LOADING! 🎯🎸🎯');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure OKRs routes loaded at: 2025-08-06 19:00:15 UTC`);
console.log('🌃 EVENING LEGENDARY OKRS SECURITY AT 19:00:15!');

// =====================================
// 🛡️ OKR-SPECIFIC RATE LIMITING 🛡️
// =====================================

// OKRs route rate limiter
const okrsLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 200, // limit each IP to 200 OKR requests per windowMs
  message: {
    error: 'Too many OKR requests from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'OKR_RATE_LIMIT'
  }
});

// OKR creation rate limiter (more restrictive)
const createOKRLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 10, // limit each IP to 10 OKR creations per hour
  message: {
    error: 'Too many OKR creation requests from this IP, please try again later.',
    retryAfter: '1 hour',
    code: 'OKR_CREATE_RATE_LIMIT'
  }
});

// Apply rate limiting to all routes
router.use(okrsLimiter);

// =====================================
// 🎯 OKR HELPER FUNCTIONS 🎯
// =====================================

// Check if user can access OKR
const checkOKRAccess = async (okrId, userId, requiredPermission = 'read') => {
  const access = await secureQuery(`
    SELECT 
      o.id, o.title, o.owner_id, o.team_id, o.status,
      o.is_legendary, o.created_at,
      u.role as user_role,
      u.username as owner_username,
      tm.role as team_role,
      t.name as team_name
    FROM okrs o
    JOIN users u ON o.owner_id = u.id
    LEFT JOIN team_members tm ON o.team_id = tm.team_id AND tm.user_id = $2
    LEFT JOIN teams t ON o.team_id = t.id
    WHERE o.id = $1
  `, [okrId, userId]);

  if (access.rows.length === 0) {
    return { hasAccess: false, reason: 'OKR not found' };
  }

  const okr = access.rows[0];
  
  // System admins have access to everything
  if (okr.user_role === 'founder' || okr.user_role === 'admin') {
    return { hasAccess: true, role: 'admin', okr };
  }

  // Owner has full access
  if (okr.owner_id === userId) {
    return { hasAccess: true, role: 'owner', okr };
  }

  // Team member access
  if (okr.team_id && okr.team_role) {
    const canRead = ['member', 'moderator', 'admin'].includes(okr.team_role);
    const canWrite = ['moderator', 'admin'].includes(okr.team_role);
    
    if (requiredPermission === 'read' && canRead) {
      return { hasAccess: true, role: 'team_member', okr };
    }
    
    if (requiredPermission === 'write' && canWrite) {
      return { hasAccess: true, role: 'team_moderator', okr };
    }
  }

  return { hasAccess: false, reason: 'Insufficient permissions' };
};

// Validate OKR data
const validateOKRData = (data) => {
  const errors = [];
  
  if (data.progress !== undefined) {
    if (data.progress < 0 || data.progress > 100) {
      errors.push('Progress must be between 0 and 100');
    }
  }
  
  if (data.confidence !== undefined) {
    if (data.confidence < 0 || data.confidence > 100) {
      errors.push('Confidence must be between 0 and 100');
    }
  }
  
  if (data.due_date && new Date(data.due_date) < new Date()) {
    errors.push('Due date cannot be in the past');
  }
  
  return errors;
};

// =====================================
// 🎯 OKR ROUTES 🎯
// =====================================

// Get all OKRs (with filtering)
router.get('/',
  authenticateToken,
  [
    query('page').optional().isInt({ min: 1 }).toInt(),
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt(),
    query('owner_id').optional().isUUID(),
    query('team_id').optional().isUUID(),
    query('status').optional().isIn(['draft', 'active', 'completed', 'cancelled', 'archived']),
    query('legendary_only').optional().isBoolean(),
    query('my_okrs_only').optional().isBoolean(),
    query('search').optional().isLength({ min: 2, max: 100 }).trim(),
    query('sort_by').optional().isIn(['title', 'created_at', 'due_date', 'progress', 'priority']),
    query('sort_order').optional().isIn(['asc', 'desc'])
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

      console.log(`🎯 Get OKRs request by ${req.user.username} at 19:00:15 UTC`);

      const {
        page = 1,
        limit = 20,
        owner_id,
        team_id,
        status,
        legendary_only = false,
        my_okrs_only = false,
        search,
        sort_by = 'created_at',
        sort_order = 'desc'
      } = req.query;

      const offset = (page - 1) * limit;

      // Build WHERE conditions
      let whereConditions = ["1=1"];
      let queryParams = [];
      let paramCount = 0;

      // Access control based on user role
      if (req.user.role !== 'founder' && req.user.role !== 'admin') {
        // Regular users can only see:
        // 1. Their own OKRs
        // 2. OKRs from teams they're members of
        whereConditions.push(`(
          o.owner_id = $${paramCount + 1} OR 
          EXISTS (
            SELECT 1 FROM team_members tm 
            WHERE tm.team_id = o.team_id AND tm.user_id = $${paramCount + 1}
          )
        )`);
        paramCount++;
        queryParams.push(req.user.id);
      }

      if (my_okrs_only) {
        paramCount++;
        whereConditions.push(`o.owner_id = $${paramCount}`);
        queryParams.push(req.user.id);
      }

      if (owner_id) {
        paramCount++;
        whereConditions.push(`o.owner_id = $${paramCount}`);
        queryParams.push(owner_id);
      }

      if (team_id) {
        paramCount++;
        whereConditions.push(`o.team_id = $${paramCount}`);
        queryParams.push(team_id);
      }

      if (status) {
        paramCount++;
        whereConditions.push(`o.status = $${paramCount}`);
        queryParams.push(status);
      }

      if (legendary_only) {
        whereConditions.push("o.is_legendary = true");
      }

      if (search) {
        paramCount++;
        whereConditions.push(`(o.title ILIKE $${paramCount} OR o.description ILIKE $${paramCount})`);
        queryParams.push(`%${search}%`);
      }

      const whereClause = whereConditions.join(' AND ');

      // Build ORDER BY clause
      let orderByClause;
      switch (sort_by) {
        case 'title':
          orderByClause = `o.title ${sort_order.toUpperCase()}`;
          break;
        case 'due_date':
          orderByClause = `o.due_date ${sort_order.toUpperCase()} NULLS LAST`;
          break;
        case 'progress':
          orderByClause = `o.progress ${sort_order.toUpperCase()}`;
          break;
        case 'priority':
          orderByClause = `
            CASE o.priority 
              WHEN 'urgent' THEN 4 
              WHEN 'high' THEN 3 
              WHEN 'medium' THEN 2 
              WHEN 'low' THEN 1 
              ELSE 0 
            END ${sort_order.toUpperCase()}`;
          break;
        default:
          orderByClause = `o.created_at ${sort_order.toUpperCase()}`;
      }

      // Get OKRs with owner and team info
      const okrsResult = await secureQuery(`
        SELECT 
          o.id, o.title, o.description, o.status, o.priority, o.progress, 
          o.confidence, o.is_legendary, o.due_date, o.created_at, o.updated_at,
          o.owner_id, o.team_id,
          u.username as owner_username,
          u.display_name as owner_display_name,
          u.is_legendary as owner_legendary,
          t.name as team_name,
          COUNT(kr.id) as key_results_count
        FROM okrs o
        JOIN users u ON o.owner_id = u.id
        LEFT JOIN teams t ON o.team_id = t.id
        LEFT JOIN key_results kr ON o.id = kr.okr_id
        WHERE ${whereClause}
        GROUP BY o.id, o.title, o.description, o.status, o.priority, o.progress, 
                 o.confidence, o.is_legendary, o.due_date, o.created_at, o.updated_at,
                 o.owner_id, o.team_id, u.username, u.display_name, u.is_legendary, t.name
        ORDER BY ${orderByClause}
        LIMIT $${paramCount + 1} OFFSET $${paramCount + 2}
      `, [...queryParams, limit, offset]);

      // Get total count
      const countResult = await secureQuery(`
        SELECT COUNT(DISTINCT o.id) as total
        FROM okrs o
        JOIN users u ON o.owner_id = u.id
        LEFT JOIN teams t ON o.team_id = t.id
        WHERE ${whereClause}
      `, queryParams);

      const total = parseInt(countResult.rows[0].total);

      // Format response
      const okrs = okrsResult.rows.map(okr => ({
        id: okr.id,
        title: okr.title,
        description: okr.description,
        status: okr.status,
        priority: okr.priority,
        progress: okr.progress,
        confidence: okr.confidence,
        is_legendary: okr.is_legendary,
        due_date: okr.due_date,
        created_at: okr.created_at,
        updated_at: okr.updated_at,
        owner: {
          id: okr.owner_id,
          username: okr.owner_username,
          display_name: okr.owner_display_name,
          is_legendary: okr.owner_legendary
        },
        team: okr.team_id ? {
          id: okr.team_id,
          name: okr.team_name
        } : null,
        stats: {
          key_results_count: parseInt(okr.key_results_count) || 0
        }
      }));

      console.log(`🎯 Retrieved ${okrs.length} OKRs (total: ${total})`);

      if (req.user.role === 'founder') {
        console.log('👑🎯👑 RICKROLL187 FOUNDER OKRS ACCESS WITH INFINITE INSIGHTS! 👑🎯👑');
      }

      res.json({
        success: true,
        data: {
          okrs,
          pagination: {
            current_page: page,
            per_page: limit,
            total_pages: Math.ceil(total / limit),
            total_count: total,
            has_next: (page * limit) < total,
            has_prev: page > 1
          },
          filters: { owner_id, team_id, status, legendary_only, my_okrs_only, search },
          sort: { sort_by, sort_order }
        },
        message: req.user.role === 'founder' ? 
          `👑 ${total} OKRs retrieved with LEGENDARY FOUNDER insights!` :
          `🎯 ${total} OKRs retrieved successfully!`
      });

    } catch (error) {
      console.error('❌ Get OKRs error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch OKRs',
        message: 'An error occurred while retrieving OKRs',
        code: 'GET_OKRS_ERROR'
      });
    }
  }
);

// Create new OKR
router.post('/',
  createOKRLimiter,
  authenticateToken,
  [
    body('title').isLength({ min: 3, max: 200 }).trim(),
    body('description').optional().isLength({ max: 1000 }).trim(),
    body('team_id').optional().isUUID(),
    body('priority').optional().isIn(['low', 'medium', 'high', 'urgent']),
    body('due_date').optional().isISO8601(),
    body('key_results').optional().isArray({ max: 10 }),
    body('key_results.*.title').optional().isLength({ min: 3, max: 200 }),
    body('key_results.*.description').optional().isLength({ max: 500 }),
    body('key_results.*.target_value').optional().isNumeric(),
    body('key_results.*.unit').optional().isLength({ max: 50 })
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

      console.log(`🎯 Create OKR request by ${req.user.username} at 19:00:15 UTC`);

      const { 
        title, 
        description = '', 
        team_id,
        priority = 'medium',
        due_date,
        key_results = []
      } = req.body;

      // Validate OKR data
      const validationErrors = validateOKRData({ due_date });
      if (validationErrors.length > 0) {
        return res.status(400).json({
          error: 'OKR validation failed',
          details: validationErrors,
          code: 'OKR_VALIDATION_ERROR'
        });
      }

      // Check team access if team_id provided
      if (team_id) {
        const teamAccess = await secureQuery(`
          SELECT tm.role as team_role, t.name as team_name
          FROM teams t
          LEFT JOIN team_members tm ON t.id = tm.team_id AND tm.user_id = $2
          WHERE t.id = $1 AND t.status = 'active'
        `, [team_id, req.user.id]);

        if (teamAccess.rows.length === 0) {
          return res.status(404).json({
            error: 'Team not found',
            code: 'TEAM_NOT_FOUND'
          });
        }

        // Non-admins need team membership to create team OKRs
        if (req.user.role !== 'founder' && req.user.role !== 'admin' && !teamAccess.rows[0].team_role) {
          return res.status(403).json({
            error: 'Team membership required',
            message: 'You must be a team member to create OKRs for this team',
            code: 'TEAM_MEMBERSHIP_REQUIRED'
          });
        }
      }

      // Create OKR in transaction
      const newOKR = await secureTransaction(async (client) => {
        // Create OKR
        const okrResult = await client.query(`
          INSERT INTO okrs (
            title, description, owner_id, team_id, priority, status,
            progress, confidence, is_legendary, due_date, 
            created_at, updated_at
          ) VALUES ($1, $2, $3, $4, $5, 'draft', 0, 50, false, $6, NOW(), NOW())
          RETURNING id, title, description, owner_id, team_id, priority, status,
                    progress, confidence, is_legendary, due_date, created_at
        `, [title, description, req.user.id, team_id, priority, due_date]);

        const okr = okrResult.rows[0];

        // Create key results if provided
        const createdKeyResults = [];
        for (const kr of key_results) {
          const krResult = await client.query(`
            INSERT INTO key_results (
              okr_id, title, description, target_value, current_value, unit, created_at
            ) VALUES ($1, $2, $3, $4, 0, $5, NOW())
            RETURNING id, title, description, target_value, current_value, unit, created_at
          `, [okr.id, kr.title, kr.description || '', kr.target_value || 100, kr.unit || '']);
          
          createdKeyResults.push(krResult.rows[0]);
        }

        return { ...okr, key_results: createdKeyResults };
      });

      console.log(`🎯 OKR created: "${title}" by ${req.user.username}`);

      if (req.user.role === 'founder') {
        console.log('👑🎯👑 LEGENDARY FOUNDER OKR CREATION WITH INFINITE POWER! 👑🎯👑');
      }

      res.status(201).json({
        success: true,
        data: {
          okr: {
            ...newOKR,
            owner: {
              id: req.user.id,
              username: req.user.username,
              display_name: req.user.display_name,
              is_legendary: req.user.is_legendary
            },
            team: team_id ? { id: team_id } : null
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER OKR: "${title}" created with infinite precision!` :
          `🎯 OKR "${title}" created successfully! Ready to achieve amazing results!`
      });

    } catch (error) {
      console.error('❌ Create OKR error:', error);
      res.status(500).json({ 
        error: 'Failed to create OKR',
        message: 'An error occurred while creating the OKR',
        code: 'CREATE_OKR_ERROR'
      });
    }
  }
);

// Get OKR by ID
router.get('/:okrId',
  authenticateToken,
  [
    param('okrId').isUUID().withMessage('Valid OKR ID required')
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

      console.log(`🎯 Get OKR ${req.params.okrId} by ${req.user.username}`);

      const { okrId } = req.params;

      // Check OKR access
      const accessCheck = await checkOKRAccess(okrId, req.user.id, 'read');
      
      if (!accessCheck.hasAccess) {
        return res.status(accessCheck.reason === 'OKR not found' ? 404 : 403).json({ 
          error: accessCheck.reason === 'OKR not found' ? 'OKR not found' : 'Access denied',
          message: accessCheck.reason,
          code: accessCheck.reason === 'OKR not found' ? 'OKR_NOT_FOUND' : 'OKR_ACCESS_DENIED'
        });
      }

      // Get detailed OKR information
      const okrResult = await secureQuery(`
        SELECT 
          o.id, o.title, o.description, o.status, o.priority, o.progress, 
          o.confidence, o.is_legendary, o.due_date, o.created_at, o.updated_at,
          o.owner_id, o.team_id,
          u.username as owner_username,
          u.display_name as owner_display_name,
          u.is_legendary as owner_legendary,
          u.code_bro_energy as owner_energy,
          t.name as team_name,
          t.is_legendary as team_legendary
        FROM okrs o
        JOIN users u ON o.owner_id = u.id
        LEFT JOIN teams t ON o.team_id = t.id
        WHERE o.id = $1
      `, [okrId]);

      const okr = okrResult.rows[0];

      // Get key results
      const keyResultsResult = await secureQuery(`
        SELECT 
          id, title, description, target_value, current_value, unit,
          progress_percentage, created_at, updated_at
        FROM key_results
        WHERE okr_id = $1
        ORDER BY created_at ASC
      `, [okrId]);

      // Get OKR activity/updates (last 30 days)
      const activityResult = await secureQuery(`
        SELECT 
          id, update_type, old_value, new_value, comment,
          created_at, updated_by
        FROM okr_updates
        WHERE okr_id = $1 AND created_at > NOW() - INTERVAL '30 days'
        ORDER BY created_at DESC
        LIMIT 20
      `, [okrId]);

      // Calculate overall progress from key results
      const keyResults = keyResultsResult.rows;
      const avgKeyResultProgress = keyResults.length > 0 ? 
        keyResults.reduce((sum, kr) => sum + (kr.progress_percentage || 0), 0) / keyResults.length : 0;

      // Format OKR data
      const okrData = {
        id: okr.id,
        title: okr.title,
        description: okr.description,
        status: okr.status,
        priority: okr.priority,
        progress: okr.progress,
        confidence: okr.confidence,
        is_legendary: okr.is_legendary,
        due_date: okr.due_date,
        created_at: okr.created_at,
        updated_at: okr.updated_at,
        owner: {
          id: okr.owner_id,
          username: okr.owner_username,
          display_name: okr.owner_display_name,
          is_legendary: okr.owner_legendary,
          code_bro_energy: okr.owner_energy
        },
        team: okr.team_id ? {
          id: okr.team_id,
          name: okr.team_name,
          is_legendary: okr.team_legendary
        } : null,
        key_results: keyResults,
        stats: {
          key_results_count: keyResults.length,
          avg_key_result_progress: avgKeyResultProgress,
          days_remaining: okr.due_date ? 
            Math.max(0, Math.ceil((new Date(okr.due_date) - new Date()) / (1000 * 60 * 60 * 24))) : null,
          recent_updates: activityResult.rows.length
        },
        recent_activity: activityResult.rows
      };

      console.log(`🎯 OKR details retrieved: ${okr.title}`);

      if (req.user.role === 'founder') {
        console.log('👑🎯👑 FOUNDER OKR ACCESS WITH INFINITE INSIGHTS! 👑🎯👑');
      }

      res.json({
        success: true,
        data: { okr: okrData },
        message: req.user.role === 'founder' ? 
          `👑 OKR "${okr.title}" loaded with LEGENDARY FOUNDER insights!` :
          `🎯 OKR "${okr.title}" loaded successfully!`
      });

    } catch (error) {
      console.error('❌ Get OKR error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch OKR',
        message: 'An error occurred while retrieving OKR details',
        code: 'GET_OKR_ERROR'
      });
    }
  }
);

// Update OKR progress
router.patch('/:okrId/progress',
  authenticateToken,
  [
    param('okrId').isUUID().withMessage('Valid OKR ID required'),
    body('progress').isInt({ min: 0, max: 100 }).withMessage('Progress must be between 0 and 100'),
    body('confidence').optional().isInt({ min: 0, max: 100 }).withMessage('Confidence must be between 0 and 100'),
    body('comment').optional().isLength({ max: 500 }).trim()
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

      console.log(`📈 Update OKR progress ${req.params.okrId} by ${req.user.username}`);

      const { okrId } = req.params;
      const { progress, confidence, comment } = req.body;

      // Check OKR access (write permission)
      const accessCheck = await checkOKRAccess(okrId, req.user.id, 'write');
      
      if (!accessCheck.hasAccess) {
        return res.status(accessCheck.reason === 'OKR not found' ? 404 : 403).json({ 
          error: accessCheck.reason === 'OKR not found' ? 'OKR not found' : 'Access denied',
          message: accessCheck.reason,
          code: accessCheck.reason === 'OKR not found' ? 'OKR_NOT_FOUND' : 'OKR_ACCESS_DENIED'
        });
      }

      const currentOKR = accessCheck.okr;

      // Update OKR progress in transaction
      const updatedOKR = await secureTransaction(async (client) => {
        // Update OKR
        const updateFields = ['progress = $2', 'updated_at = NOW()'];
        const updateParams = [okrId, progress];
        let paramCount = 2;

        if (confidence !== undefined) {
          paramCount++;
          updateFields.push(`confidence = $${paramCount}`);
          updateParams.push(confidence);
        }

        // Automatically update status based on progress
        let newStatus = currentOKR.status;
        if (progress >= 100 && currentOKR.status !== 'completed') {
          newStatus = 'completed';
          paramCount++;
          updateFields.push(`status = $${paramCount}`);
          updateParams.push(newStatus);
        } else if (progress > 0 && currentOKR.status === 'draft') {
          newStatus = 'active';
          paramCount++;
          updateFields.push(`status = $${paramCount}`);
          updateParams.push(newStatus);
        }

        const okrResult = await client.query(`
          UPDATE okrs 
          SET ${updateFields.join(', ')}
          WHERE id = $1
          RETURNING id, title, progress, confidence, status, updated_at
        `, updateParams);

        // Log progress update
        await client.query(`
          INSERT INTO okr_updates (
            okr_id, update_type, old_value, new_value, comment, updated_by, created_at
          ) VALUES ($1, 'progress', $2, $3, $4, $5, NOW())
        `, [okrId, currentOKR.progress, progress, comment || '', req.user.id]);

        // If confidence was updated, log that too
        if (confidence !== undefined && confidence !== currentOKR.confidence) {
          await client.query(`
            INSERT INTO okr_updates (
              okr_id, update_type, old_value, new_value, comment, updated_by, created_at
            ) VALUES ($1, 'confidence', $2, $3, $4, $5, NOW())
          `, [okrId, currentOKR.confidence, confidence, comment || '', req.user.id]);
        }

        return okrResult.rows[0];
      });

      console.log(`📈 OKR progress updated: ${currentOKR.title} -> ${progress}%`);

      if (progress >= 100) {
        console.log(`🎉 OKR COMPLETED: ${currentOKR.title} by ${req.user.username}`);
        
        if (req.user.role === 'founder') {
          console.log('👑🎉👑 LEGENDARY FOUNDER OKR COMPLETION WITH INFINITE SUCCESS! 👑🎉👑');
        }
      }

      res.json({
        success: true,
        data: { okr: updatedOKR },
        message: progress >= 100 ? 
          (req.user.role === 'founder' ? 
            `👑 LEGENDARY FOUNDER OKR COMPLETION: "${currentOKR.title}" achieved with infinite precision!` :
            `🎉 Congratulations! OKR "${currentOKR.title}" completed at ${progress}%!`
          ) :
          `📈 OKR progress updated to ${progress}%`
      });

    } catch (error) {
      console.error('❌ Update OKR progress error:', error);
      res.status(500).json({ 
        error: 'Failed to update OKR progress',
        message: 'An error occurred while updating OKR progress',
        code: 'UPDATE_OKR_PROGRESS_ERROR'
      });
    }
  }
);

// Update OKR status (complete, cancel, archive)
router.patch('/:okrId/status',
  authenticateToken,
  [
    param('okrId').isUUID().withMessage('Valid OKR ID required'),
    body('status').isIn(['active', 'completed', 'cancelled', 'archived']).withMessage('Valid status required'),
    body('reason').optional().isLength({ min: 5, max: 500 }).trim()
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

      console.log(`⚡ Update OKR status ${req.params.okrId} by ${req.user.username}`);

      const { okrId } = req.params;
      const { status, reason } = req.body;

      // Check OKR access (write permission)
      const accessCheck = await checkOKRAccess(okrId, req.user.id, 'write');
      
      if (!accessCheck.hasAccess) {
        return res.status(accessCheck.reason === 'OKR not found' ? 404 : 403).json({ 
          error: accessCheck.reason === 'OKR not found' ? 'OKR not found' : 'Access denied',
          message: accessCheck.reason,
          code: accessCheck.reason === 'OKR not found' ? 'OKR_NOT_FOUND' : 'OKR_ACCESS_DENIED'
        });
      }

      const currentOKR = accessCheck.okr;

      // Validate status transition
      const validTransitions = {
        draft: ['active', 'cancelled'],
        active: ['completed', 'cancelled', 'archived'],
        completed: ['archived'],
        cancelled: ['active', 'archived'],
        archived: ['active']
      };

      if (!validTransitions[currentOKR.status]?.includes(status)) {
        return res.status(400).json({
          error: 'Invalid status transition',
          message: `Cannot change status from ${currentOKR.status} to ${status}`,
          code: 'INVALID_STATUS_TRANSITION'
        });
      }

      // Update OKR status in transaction
      const updatedOKR = await secureTransaction(async (client) => {
        // Auto-update progress for certain statuses
        let updateFields = ['status = $2', 'updated_at = NOW()'];
        let updateParams = [okrId, status];

        if (status === 'completed') {
          updateFields.push('progress = 100');
        }

        const okrResult = await client.query(`
          UPDATE okrs 
          SET ${updateFields.join(', ')}
          WHERE id = $1
          RETURNING id, title, status, progress, updated_at
        `, updateParams);

        // Log status change
        await client.query(`
          INSERT INTO okr_updates (
            okr_id, update_type, old_value, new_value, comment, updated_by, created_at
          ) VALUES ($1, 'status', $2, $3, $4, $5, NOW())
        `, [okrId, currentOKR.status, status, reason || `Status changed to ${status}`, req.user.id]);

        return okrResult.rows[0];
      });

      console.log(`⚡ OKR status updated: ${currentOKR.title} -> ${status}`);

      if (req.user.role === 'founder') {
        console.log('👑⚡👑 LEGENDARY FOUNDER OKR STATUS CHANGE WITH INFINITE AUTHORITY! 👑⚡👑');
      }

      const statusMessages = {
        active: 'activated and ready for progress',
        completed: '🎉 completed successfully',
        cancelled: 'cancelled',
        archived: 'archived for future reference'
      };

      res.json({
        success: true,
        data: { okr: updatedOKR },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ACTION: OKR "${currentOKR.title}" ${statusMessages[status]} with infinite authority!` :
          `⚡ OKR "${currentOKR.title}" ${statusMessages[status]}!`
      });

    } catch (error) {
      console.error('❌ Update OKR status error:', error);
      res.status(500).json({ 
        error: 'Failed to update OKR status',
        message: 'An error occurred while updating OKR status',
        code: 'UPDATE_OKR_STATUS_ERROR'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'okrs',
    timestamp: new Date().toISOString(),
    message: '🎯 OKRs service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    evening_energy: '🌃 EVENING LEGENDARY OKRS POWER AT 19:00:15! 🌃'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY SECURE OKRS ROUTES COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure OKRs routes completed at: 2025-08-06 19:00:15 UTC`);
console.log('🎯 OKR management: LEGENDARY SECURITY');
console.log('👑 RICKROLL187 founder OKR controls: MAXIMUM AUTHORITY');
console.log('🛡️ OKR data protection: SWISS PRECISION');
console.log('🌃 EVENING LEGENDARY OKR SECURITY: INFINITE AT 19:00:15!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
