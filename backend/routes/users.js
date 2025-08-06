// File: backend/routes/users.js
/**
 * 👥🎸 N3EXTPATH - LEGENDARY SECURE USERS ROUTES 🎸👥
 * Swiss precision user management with infinite security energy
 * Built: 2025-08-06 18:40:53 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const express = require('express');
const rateLimit = require('express-rate-limit');
const { body, query, param, validationResult } = require('express-validator');

const router = express.Router();
const { secureQuery, secureTransaction, getUserById, searchUsers } = require('../utils/database');
const { authenticateToken, requirePermission } = require('../middleware/auth');
const { sanitizeUserData, createUserRateLimit } = require('../middleware/security');

console.log('👥🎸👥 LEGENDARY SECURE USERS ROUTES LOADING! 👥🎸👥');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure users routes loaded at: 2025-08-06 18:40:53 UTC`);
console.log('🌅 EVENING LEGENDARY USERS SECURITY AT 18:40:53!');

// =====================================
// 🛡️ USER-SPECIFIC RATE LIMITING 🛡️
// =====================================

// Users route rate limiter
const usersLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 user requests per windowMs
  message: {
    error: 'Too many user requests from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'USER_RATE_LIMIT'
  }
});

// Search rate limiter (more restrictive)
const searchLimiter = rateLimit({
  windowMs: 5 * 60 * 1000, // 5 minutes
  max: 30, // limit each IP to 30 search requests per windowMs
  message: {
    error: 'Too many search requests from this IP, please try again later.',
    retryAfter: '5 minutes',
    code: 'SEARCH_RATE_LIMIT'
  }
});

// Apply rate limiting to all routes
router.use(usersLimiter);

// =====================================
// 👥 USER ROUTES 👥
// =====================================

// Get all users (admin only)
router.get('/',
  authenticateToken,
  requirePermission('users.read'),
  [
    query('page').optional().isInt({ min: 1 }).toInt(),
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt(),
    query('role').optional().isIn(['founder', 'admin', 'moderator', 'user']),
    query('status').optional().isIn(['active', 'suspended', 'banned', 'pending']),
    query('legendary').optional().isBoolean(),
    query('sort_by').optional().isIn(['username', 'display_name', 'created_at', 'last_login', 'code_bro_energy']),
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

      console.log(`👥 Get all users request by ${req.user.username} (${req.user.role}) at 18:40:53 UTC`);

      if (req.user.role === 'founder') {
        console.log('👑👥👑 RICKROLL187 FOUNDER USERS ACCESS WITH INFINITE INSIGHTS! 👑👥👑');
      }

      const {
        page = 1,
        limit = 20,
        role,
        status,
        legendary,
        sort_by = 'created_at',
        sort_order = 'desc'
      } = req.query;

      const offset = (page - 1) * limit;

      // Build WHERE conditions
      let whereConditions = ["status != 'deleted'"];
      let queryParams = [];
      let paramCount = 0;

      if (role) {
        paramCount++;
        whereConditions.push(`role = $${paramCount}`);
        queryParams.push(role);
      }

      if (status) {
        paramCount++;
        whereConditions.push(`status = $${paramCount}`);
        queryParams.push(status);
      }

      if (legendary !== undefined) {
        paramCount++;
        whereConditions.push(`is_legendary = $${paramCount}`);
        queryParams.push(legendary);
      }

      const whereClause = whereConditions.join(' AND ');

      // Get total count
      const countResult = await secureQuery(`
        SELECT COUNT(*) as total
        FROM users
        WHERE ${whereClause}
      `, queryParams);

      const total = parseInt(countResult.rows[0].total);

      // Get users
      const usersResult = await secureQuery(`
        SELECT 
          id, username, display_name, email, role, 
          is_legendary, code_bro_energy, status,
          created_at, last_login, updated_at
        FROM users
        WHERE ${whereClause}
        ORDER BY ${sort_by} ${sort_order.toUpperCase()}
        LIMIT $${paramCount + 1} OFFSET $${paramCount + 2}
      `, [...queryParams, limit, offset]);

      // Sanitize user data based on requester's role
      const sanitizedUsers = usersResult.rows.map(user => 
        sanitizeUserData(user, req.user.role)
      );

      console.log(`👥 Retrieved ${sanitizedUsers.length} users (total: ${total})`);

      res.json({
        success: true,
        data: {
          users: sanitizedUsers,
          pagination: {
            current_page: page,
            per_page: limit,
            total_pages: Math.ceil(total / limit),
            total_count: total,
            has_next: (page * limit) < total,
            has_prev: page > 1
          },
          filters: { role, status, legendary },
          sort: { sort_by, sort_order }
        },
        message: req.user.role === 'founder' ? 
          `👑 ${total} users retrieved with LEGENDARY FOUNDER insights!` :
          `👥 ${total} users retrieved successfully!`
      });

    } catch (error) {
      console.error('❌ Get all users error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch users',
        message: 'An error occurred while retrieving users',
        code: 'GET_USERS_ERROR'
      });
    }
  }
);

// Search users
router.get('/search',
  searchLimiter,
  authenticateToken,
  [
    query('q').notEmpty().isLength({ min: 2, max: 100 }).trim(),
    query('limit').optional().isInt({ min: 1, max: 50 }).toInt(),
    query('offset').optional().isInt({ min: 0 }).toInt()
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

      console.log(`🔍 User search by ${req.user.username}: "${req.query.q}"`);

      const { q: searchTerm, limit = 20, offset = 0 } = req.query;

      const searchResult = await searchUsers(searchTerm, limit, offset, req.user.role);

      console.log(`🔍 Search returned ${searchResult.users.length} results`);

      res.json({
        success: true,
        data: searchResult,
        message: `🔍 Found ${searchResult.users.length} users matching "${searchTerm}"`
      });

    } catch (error) {
      console.error('❌ User search error:', error);
      
      if (error.message.includes('Search term too short')) {
        res.status(400).json({ 
          error: 'Invalid search term',
          message: 'Search term must be at least 2 characters long',
          code: 'SEARCH_TERM_TOO_SHORT'
        });
      } else {
        res.status(500).json({ 
          error: 'Search failed',
          message: 'An error occurred while searching users',
          code: 'SEARCH_ERROR'
        });
      }
    }
  }
);

// Get user by ID
router.get('/:userId',
  authenticateToken,
  [
    param('userId').isUUID().withMessage('Valid user ID required')
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

      console.log(`👤 Get user ${req.params.userId} by ${req.user.username}`);

      const { userId } = req.params;

      // Check if user can view this profile
      const canViewProfile = (
        req.user.id === userId || // Own profile
        req.user.role === 'founder' || 
        req.user.role === 'admin'
      );

      if (!canViewProfile) {
        // For regular users, only return basic public info
        const basicUserResult = await secureQuery(`
          SELECT 
            id, username, display_name, is_legendary,
            created_at
          FROM users 
          WHERE id = $1 AND status = 'active'
        `, [userId]);

        if (basicUserResult.rows.length === 0) {
          return res.status(404).json({ 
            error: 'User not found',
            code: 'USER_NOT_FOUND'
          });
        }

        return res.json({
          success: true,
          data: { user: basicUserResult.rows[0] },
          message: 'Public user profile retrieved'
        });
      }

      // Get full user details for authorized viewers
      const user = await getUserById(userId, req.user.role);

      if (!user) {
        return res.status(404).json({ 
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
      }

      // Get additional stats for detailed view
      const statsResult = await secureQuery(`
        SELECT 
          COUNT(DISTINCT o.id) as total_okrs,
          COUNT(DISTINCT CASE WHEN o.status = 'completed' THEN o.id END) as completed_okrs,
          COUNT(DISTINCT tm.team_id) as team_count,
          COUNT(DISTINCT m.id) as message_count
        FROM users u
        LEFT JOIN okrs o ON u.id = o.owner_id
        LEFT JOIN team_members tm ON u.id = tm.user_id
        LEFT JOIN messages m ON u.id = m.user_id AND m.created_at > NOW() - INTERVAL '30 days'
        WHERE u.id = $1
        GROUP BY u.id
      `, [userId]);

      const stats = statsResult.rows.length > 0 ? {
        total_okrs: parseInt(statsResult.rows[0].total_okrs) || 0,
        completed_okrs: parseInt(statsResult.rows[0].completed_okrs) || 0,
        team_count: parseInt(statsResult.rows[0].team_count) || 0,
        message_count: parseInt(statsResult.rows[0].message_count) || 0
      } : {
        total_okrs: 0,
        completed_okrs: 0,
        team_count: 0,
        message_count: 0
      };

      const completionRate = stats.total_okrs > 0 ? 
        (stats.completed_okrs / stats.total_okrs * 100) : 0;

      console.log(`👤 User profile retrieved: ${user.username}`);

      res.json({
        success: true,
        data: {
          user: {
            ...user,
            stats: {
              ...stats,
              completion_rate: completionRate
            }
          }
        },
        message: userId === req.user.id ? 
          'Your profile loaded successfully!' :
          `Profile for ${user.display_name} loaded successfully!`
      });

    } catch (error) {
      console.error('❌ Get user error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch user',
        message: 'An error occurred while retrieving user profile',
        code: 'GET_USER_ERROR'
      });
    }
  }
);

// Update user profile
router.patch('/:userId',
  authenticateToken,
  [
    param('userId').isUUID().withMessage('Valid user ID required'),
    body('display_name').optional().isLength({ min: 2, max: 50 }).matches(/^[a-zA-Z0-9\s_-]+$/),
    body('email').optional().isEmail().normalizeEmail(),
    body('bio').optional().isLength({ max: 500 }).trim(),
    body('location').optional().isLength({ max: 100 }).trim(),
    body('website').optional().isURL()
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

      console.log(`✏️ Update user ${req.params.userId} by ${req.user.username}`);

      const { userId } = req.params;
      const updates = req.body;

      // Check if user can update this profile
      const canUpdate = (
        req.user.id === userId || // Own profile
        req.user.role === 'founder' || 
        req.user.role === 'admin'
      );

      if (!canUpdate) {
        return res.status(403).json({ 
          error: 'Permission denied',
          message: 'You can only update your own profile',
          code: 'UPDATE_PERMISSION_DENIED'
        });
      }

      // Build update query
      const allowedFields = ['display_name', 'email', 'bio', 'location', 'website'];
      const updateFields = [];
      const queryParams = [];
      let paramCount = 0;

      for (const [key, value] of Object.entries(updates)) {
        if (allowedFields.includes(key) && value !== undefined) {
          paramCount++;
          updateFields.push(`${key} = $${paramCount}`);
          queryParams.push(value);
        }
      }

      if (updateFields.length === 0) {
        return res.status(400).json({
          error: 'No valid updates provided',
          message: 'At least one valid field must be updated',
          code: 'NO_UPDATES'
        });
      }

      // Check if email is being changed and is unique
      if (updates.email) {
        const existingEmail = await secureQuery(`
          SELECT id FROM users 
          WHERE LOWER(email) = LOWER($1) AND id != $2
        `, [updates.email, userId]);

        if (existingEmail.rows.length > 0) {
          return res.status(409).json({ 
            error: 'Email already exists',
            message: 'A user with this email already exists',
            code: 'EMAIL_EXISTS'
          });
        }
      }

      // Update user
      queryParams.push(userId);
      const result = await secureQuery(`
        UPDATE users 
        SET ${updateFields.join(', ')}, updated_at = NOW()
        WHERE id = $${paramCount + 1} AND status != 'deleted'
        RETURNING id, username, display_name, email, role, is_legendary, code_bro_energy, updated_at
      `, queryParams);

      if (result.rows.length === 0) {
        return res.status(404).json({ 
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
      }

      const updatedUser = sanitizeUserData(result.rows[0], req.user.role);

      console.log(`✏️ User updated successfully: ${updatedUser.username}`);

      res.json({
        success: true,
        data: { user: updatedUser },
        message: userId === req.user.id ? 
          'Your profile updated successfully!' :
          `Profile for ${updatedUser.display_name} updated successfully!`
      });

    } catch (error) {
      console.error('❌ Update user error:', error);
      res.status(500).json({ 
        error: 'Failed to update user',
        message: 'An error occurred while updating the user profile',
        code: 'UPDATE_USER_ERROR'
      });
    }
  }
);

// Update user role (admin only)
router.patch('/:userId/role',
  authenticateToken,
  requirePermission('users.write'),
  [
    param('userId').isUUID().withMessage('Valid user ID required'),
    body('role').isIn(['user', 'moderator', 'admin']).withMessage('Valid role required'),
    body('reason').optional().isLength({ min: 10, max: 500 }).trim()
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

      console.log(`👑 Role change ${req.params.userId} by ${req.user.username}`);

      const { userId } = req.params;
      const { role, reason } = req.body;

      // Prevent changing founder role
      const targetUser = await secureQuery(`
        SELECT id, username, role FROM users WHERE id = $1
      `, [userId]);

      if (targetUser.rows.length === 0) {
        return res.status(404).json({ 
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
      }

      if (targetUser.rows[0].role === 'founder') {
        return res.status(403).json({ 
          error: 'Cannot modify founder',
          message: 'Founder role cannot be changed',
          code: 'FOUNDER_IMMUTABLE'
        });
      }

      // Only founder can create admins
      if (role === 'admin' && req.user.role !== 'founder') {
        return res.status(403).json({ 
          error: 'Permission denied',
          message: 'Only founder can assign admin role',
          code: 'ADMIN_CREATION_DENIED'
        });
      }

      // Update role in transaction
      const updatedUser = await secureTransaction(async (client) => {
        // Update user role
        const userResult = await client.query(`
          UPDATE users 
          SET role = $1, updated_at = NOW()
          WHERE id = $2
          RETURNING id, username, display_name, role
        `, [role, userId]);

        // Log role change
        await client.query(`
          INSERT INTO admin_logs (
            admin_id, action, target_type, target_id, details, created_at
          ) VALUES ($1, 'role_change', 'user', $2, $3, NOW())
        `, [
          req.user.id, 
          userId, 
          JSON.stringify({
            old_role: targetUser.rows[0].role,
            new_role: role,
            reason: reason || 'No reason provided'
          })
        ]);

        return userResult.rows[0];
      });

      console.log(`👑 Role changed: ${updatedUser.username} -> ${role}`);

      if (req.user.role === 'founder') {
        console.log('👑⚡👑 LEGENDARY FOUNDER ROLE CHANGE WITH INFINITE AUTHORITY! 👑⚡👑');
      }

      res.json({
        success: true,
        data: { user: updatedUser },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ACTION: User role changed to ${role} with infinite authority!` :
          `✅ User role changed to ${role} successfully!`
      });

    } catch (error) {
      console.error('❌ Role change error:', error);
      res.status(500).json({ 
        error: 'Failed to change user role',
        message: 'An error occurred while changing the user role',
        code: 'ROLE_CHANGE_ERROR'
      });
    }
  }
);

// Update user status (admin only)
router.patch('/:userId/status',
  authenticateToken,
  requirePermission('users.write'),
  [
    param('userId').isUUID().withMessage('Valid user ID required'),
    body('status').isIn(['active', 'suspended', 'banned']).withMessage('Valid status required'),
    body('reason').isLength({ min: 10, max: 500 }).trim().withMessage('Reason is required and must be 10-500 characters')
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

      console.log(`⚡ Status change ${req.params.userId} by ${req.user.username}`);

      const { userId } = req.params;
      const { status, reason } = req.body;

      // Prevent changing founder status
      const targetUser = await secureQuery(`
        SELECT id, username, role, status FROM users WHERE id = $1
      `, [userId]);

      if (targetUser.rows.length === 0) {
        return res.status(404).json({ 
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
      }

      if (targetUser.rows[0].role === 'founder') {
        return res.status(403).json({ 
          error: 'Cannot modify founder',
          message: 'Founder status cannot be changed',
          code: 'FOUNDER_IMMUTABLE'
        });
      }

      // Update status in transaction
      const updatedUser = await secureTransaction(async (client) => {
        // Update user status
        const userResult = await client.query(`
          UPDATE users 
          SET status = $1, updated_at = NOW()
          WHERE id = $2
          RETURNING id, username, display_name, status
        `, [status, userId]);

        // Log status change
        await client.query(`
          INSERT INTO admin_logs (
            admin_id, action, target_type, target_id, details, created_at
          ) VALUES ($1, 'status_change', 'user', $2, $3, NOW())
        `, [
          req.user.id, 
          userId, 
          JSON.stringify({
            old_status: targetUser.rows[0].status,
            new_status: status,
            reason
          })
        ]);

        return userResult.rows[0];
      });

      console.log(`⚡ Status changed: ${updatedUser.username} -> ${status}`);

      if (req.user.role === 'founder') {
        console.log('👑⚡👑 LEGENDARY FOUNDER STATUS CHANGE WITH INFINITE AUTHORITY! 👑⚡👑');
      }

      res.json({
        success: true,
        data: { user: updatedUser },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ACTION: User status changed to ${status} with infinite authority!` :
          `✅ User status changed to ${status} successfully!`
      });

    } catch (error) {
      console.error('❌ Status change error:', error);
      res.status(500).json({ 
        error: 'Failed to change user status',
        message: 'An error occurred while changing the user status',
        code: 'STATUS_CHANGE_ERROR'
      });
    }
  }
);

// Delete user account (soft delete)
router.delete('/:userId',
  authenticateToken,
  requirePermission('users.write'),
  [
    param('userId').isUUID().withMessage('Valid user ID required'),
    body('reason').isLength({ min: 10, max: 500 }).trim().withMessage('Deletion reason is required')
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

      console.log(`🗑️ Delete user ${req.params.userId} by ${req.user.username}`);

      const { userId } = req.params;
      const { reason } = req.body;

      // Prevent deleting founder
      const targetUser = await secureQuery(`
        SELECT id, username, role FROM users WHERE id = $1
      `, [userId]);

      if (targetUser.rows.length === 0) {
        return res.status(404).json({ 
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
      }

      if (targetUser.rows[0].role === 'founder') {
        return res.status(403).json({ 
          error: 'Cannot delete founder',
          message: 'Founder account cannot be deleted',
          code: 'FOUNDER_IMMUTABLE'
        });
      }

      // Soft delete user in transaction
      await secureTransaction(async (client) => {
        // Soft delete user
        await client.query(`
          UPDATE users 
          SET status = 'deleted', updated_at = NOW()
          WHERE id = $1
        `, [userId]);

        // Remove from all teams
        await client.query(`
          DELETE FROM team_members WHERE user_id = $1
        `, [userId]);

        // Archive user's OKRs
        await client.query(`
          UPDATE okrs 
          SET status = 'archived', updated_at = NOW()
          WHERE owner_id = $1
        `, [userId]);

        // Log deletion
        await client.query(`
          INSERT INTO admin_logs (
            admin_id, action, target_type, target_id, details, created_at
          ) VALUES ($1, 'user_delete', 'user', $2, $3, NOW())
        `, [
          req.user.id, 
          userId, 
          JSON.stringify({
            username: targetUser.rows[0].username,
            reason
          })
        ]);
      });

      console.log(`🗑️ User deleted: ${targetUser.rows[0].username}`);

      if (req.user.role === 'founder') {
        console.log('👑🗑️👑 LEGENDARY FOUNDER USER DELETION WITH INFINITE AUTHORITY! 👑🗑️👑');
      }

      res.json({
        success: true,
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ACTION: User ${targetUser.rows[0].username} deleted with infinite authority!` :
          `✅ User ${targetUser.rows[0].username} deleted successfully!`
      });

    } catch (error) {
      console.error('❌ Delete user error:', error);
      res.status(500).json({ 
        error: 'Failed to delete user',
        message: 'An error occurred while deleting the user',
        code: 'DELETE_USER_ERROR'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'users',
    timestamp: new Date().toISOString(),
    message: '👥 Users service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    evening_energy: '🌅 EVENING LEGENDARY USERS POWER AT 18:40:53! 🌅'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY SECURE USERS ROUTES COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure users routes completed at: 2025-08-06 18:40:53 UTC`);
console.log('👥 User management: LEGENDARY SECURITY');
console.log('👑 RICKROLL187 founder user controls: MAXIMUM AUTHORITY');
console.log('🛡️ User data protection: SWISS PRECISION');
console.log('🌅 EVENING LEGENDARY USER SECURITY: INFINITE AT 18:40:53!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
