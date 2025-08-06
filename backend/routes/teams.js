// File: backend/routes/teams.js
/**
 * 🏆🎸 N3EXTPATH - LEGENDARY SECURE TEAMS ROUTES 🎸🏆
 * Swiss precision team management with infinite security energy
 * Built: 2025-08-06 18:47:47 UTC by RICKROLL187
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

console.log('🏆🎸🏆 LEGENDARY SECURE TEAMS ROUTES LOADING! 🏆🎸🏆');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure teams routes loaded at: 2025-08-06 18:47:47 UTC`);
console.log('🌅 EVENING LEGENDARY TEAMS SECURITY AT 18:47:47!');

// =====================================
// 🛡️ TEAM-SPECIFIC RATE LIMITING 🛡️
// =====================================

// Teams route rate limiter
const teamsLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 150, // limit each IP to 150 team requests per windowMs
  message: {
    error: 'Too many team requests from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'TEAM_RATE_LIMIT'
  }
});

// Team creation rate limiter (more restrictive)
const createTeamLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // limit each IP to 5 team creations per hour
  message: {
    error: 'Too many team creation requests from this IP, please try again later.',
    retryAfter: '1 hour',
    code: 'TEAM_CREATE_RATE_LIMIT'
  }
});

// Apply rate limiting to all routes
router.use(teamsLimiter);

// =====================================
// 🏆 TEAM HELPER FUNCTIONS 🏆
// =====================================

// Check if user is team member or admin
const checkTeamAccess = async (teamId, userId, requiredRole = 'member') => {
  const access = await secureQuery(`
    SELECT 
      tm.role as member_role,
      t.id as team_id,
      t.name as team_name,
      t.owner_id,
      u.role as user_role
    FROM teams t
    LEFT JOIN team_members tm ON t.id = tm.team_id AND tm.user_id = $2
    LEFT JOIN users u ON u.id = $2
    WHERE t.id = $1 AND t.status != 'deleted'
  `, [teamId, userId]);

  if (access.rows.length === 0) {
    return { hasAccess: false, reason: 'Team not found' };
  }

  const team = access.rows[0];
  
  // Founder and admins have access to everything
  if (team.user_role === 'founder' || team.user_role === 'admin') {
    return { hasAccess: true, role: 'admin', team };
  }

  // Team owner has full access
  if (team.owner_id === userId) {
    return { hasAccess: true, role: 'owner', team };
  }

  // Check team membership
  if (!team.member_role) {
    return { hasAccess: false, reason: 'Not a team member' };
  }

  // Check required role
  const roleHierarchy = { member: 1, moderator: 2, admin: 3 };
  const userRoleLevel = roleHierarchy[team.member_role] || 0;
  const requiredRoleLevel = roleHierarchy[requiredRole] || 1;

  if (userRoleLevel < requiredRoleLevel) {
    return { hasAccess: false, reason: 'Insufficient team permissions' };
  }

  return { hasAccess: true, role: team.member_role, team };
};

// =====================================
// 🏆 TEAM ROUTES 🏆
// =====================================

// Get all teams (with filtering)
router.get('/',
  authenticateToken,
  [
    query('page').optional().isInt({ min: 1 }).toInt(),
    query('limit').optional().isInt({ min: 1, max: 50 }).toInt(),
    query('my_teams_only').optional().isBoolean(),
    query('legendary_only').optional().isBoolean(),
    query('search').optional().isLength({ min: 2, max: 100 }).trim(),
    query('sort_by').optional().isIn(['name', 'created_at', 'member_count', 'energy']),
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

      console.log(`🏆 Get teams request by ${req.user.username} at 18:47:47 UTC`);

      const {
        page = 1,
        limit = 20,
        my_teams_only = false,
        legendary_only = false,
        search,
        sort_by = 'created_at',
        sort_order = 'desc'
      } = req.query;

      const offset = (page - 1) * limit;

      // Build WHERE conditions
      let whereConditions = ["t.status != 'deleted'"];
      let queryParams = [];
      let paramCount = 0;

      if (my_teams_only) {
        paramCount++;
        whereConditions.push(`(tm.user_id = $${paramCount} OR t.owner_id = $${paramCount})`);
        queryParams.push(req.user.id);
      }

      if (legendary_only) {
        whereConditions.push("t.is_legendary = true");
      }

      if (search) {
        paramCount++;
        whereConditions.push(`(t.name ILIKE $${paramCount} OR t.description ILIKE $${paramCount})`);
        queryParams.push(`%${search}%`);
      }

      const whereClause = whereConditions.join(' AND ');

      // Build ORDER BY clause
      let orderByClause;
      switch (sort_by) {
        case 'name':
          orderByClause = `t.name ${sort_order.toUpperCase()}`;
          break;
        case 'member_count':
          orderByClause = `member_count ${sort_order.toUpperCase()}`;
          break;
        case 'energy':
          orderByClause = `total_energy ${sort_order.toUpperCase()}`;
          break;
        default:
          orderByClause = `t.created_at ${sort_order.toUpperCase()}`;
      }

      // Get teams with stats
      const teamsResult = await secureQuery(`
        SELECT 
          t.id, t.name, t.description, t.is_legendary,
          t.created_at, t.owner_id,
          u.username as owner_username,
          u.display_name as owner_display_name,
          COUNT(DISTINCT tm.user_id) as member_count,
          SUM(COALESCE(user_members.code_bro_energy, 0)) as total_energy,
          COUNT(DISTINCT o.id) as okr_count,
          AVG(o.progress) as avg_progress
        FROM teams t
        LEFT JOIN users u ON t.owner_id = u.id
        LEFT JOIN team_members tm ON t.id = tm.team_id
        LEFT JOIN users user_members ON tm.user_id = user_members.id
        LEFT JOIN okrs o ON t.id = o.team_id
        WHERE ${whereClause}
        GROUP BY t.id, t.name, t.description, t.is_legendary, t.created_at, t.owner_id, u.username, u.display_name
        ORDER BY ${orderByClause}
        LIMIT $${paramCount + 1} OFFSET $${paramCount + 2}
      `, [...queryParams, limit, offset]);

      // Get total count
      const countResult = await secureQuery(`
        SELECT COUNT(DISTINCT t.id) as total
        FROM teams t
        LEFT JOIN team_members tm ON t.id = tm.team_id
        WHERE ${whereClause}
      `, queryParams);

      const total = parseInt(countResult.rows[0].total);

      // Format response
      const teams = teamsResult.rows.map(team => ({
        id: team.id,
        name: team.name,
        description: team.description,
        is_legendary: team.is_legendary,
        created_at: team.created_at,
        owner: {
          id: team.owner_id,
          username: team.owner_username,
          display_name: team.owner_display_name
        },
        stats: {
          member_count: parseInt(team.member_count) || 0,
          total_energy: parseInt(team.total_energy) || 0,
          okr_count: parseInt(team.okr_count) || 0,
          avg_progress: parseFloat(team.avg_progress) || 0
        }
      }));

      console.log(`🏆 Retrieved ${teams.length} teams (total: ${total})`);

      if (req.user.role === 'founder') {
        console.log('👑🏆👑 RICKROLL187 FOUNDER TEAMS ACCESS WITH INFINITE INSIGHTS! 👑🏆👑');
      }

      res.json({
        success: true,
        data: {
          teams,
          pagination: {
            current_page: page,
            per_page: limit,
            total_pages: Math.ceil(total / limit),
            total_count: total,
            has_next: (page * limit) < total,
            has_prev: page > 1
          },
          filters: { my_teams_only, legendary_only, search },
          sort: { sort_by, sort_order }
        },
        message: req.user.role === 'founder' ? 
          `👑 ${total} teams retrieved with LEGENDARY FOUNDER insights!` :
          `🏆 ${total} teams retrieved successfully!`
      });

    } catch (error) {
      console.error('❌ Get teams error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch teams',
        message: 'An error occurred while retrieving teams',
        code: 'GET_TEAMS_ERROR'
      });
    }
  }
);

// Create new team
router.post('/',
  createTeamLimiter,
  authenticateToken,
  [
    body('name').isLength({ min: 2, max: 100 }).trim().matches(/^[a-zA-Z0-9\s_-]+$/),
    body('description').optional().isLength({ max: 500 }).trim(),
    body('is_public').optional().isBoolean(),
    body('max_members').optional().isInt({ min: 2, max: 100 })
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

      console.log(`🏆 Create team request by ${req.user.username} at 18:47:47 UTC`);

      const { 
        name, 
        description = '', 
        is_public = true,
        max_members = 50
      } = req.body;

      // Check if team name exists
      const existingTeam = await secureQuery(`
        SELECT id FROM teams 
        WHERE LOWER(name) = LOWER($1) AND status != 'deleted'
      `, [name]);

      if (existingTeam.rows.length > 0) {
        return res.status(409).json({ 
          error: 'Team name already exists',
          message: 'A team with this name already exists',
          code: 'TEAM_NAME_EXISTS'
        });
      }

      // Create team in transaction
      const newTeam = await secureTransaction(async (client) => {
        // Create team
        const teamResult = await client.query(`
          INSERT INTO teams (
            name, description, owner_id, is_public, max_members,
            is_legendary, status, created_at, updated_at
          ) VALUES ($1, $2, $3, $4, $5, false, 'active', NOW(), NOW())
          RETURNING id, name, description, owner_id, is_public, max_members, is_legendary, created_at
        `, [name, description, req.user.id, is_public, max_members]);

        const team = teamResult.rows[0];

        // Add creator as team admin
        await client.query(`
          INSERT INTO team_members (team_id, user_id, role, joined_at)
          VALUES ($1, $2, 'admin', NOW())
        `, [team.id, req.user.id]);

        return team;
      });

      console.log(`🏆 Team created: ${name} by ${req.user.username}`);

      if (req.user.role === 'founder') {
        console.log('👑🏆👑 LEGENDARY FOUNDER TEAM CREATION WITH INFINITE POWER! 👑🏆👑');
      }

      res.status(201).json({
        success: true,
        data: {
          team: {
            ...newTeam,
            owner: {
              id: req.user.id,
              username: req.user.username,
              display_name: req.user.display_name
            },
            stats: {
              member_count: 1,
              total_energy: req.user.code_bro_energy || 0,
              okr_count: 0,
              avg_progress: 0
            }
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER TEAM: "${name}" created with infinite power!` :
          `🏆 Team "${name}" created successfully! Welcome to your new code bro team!`
      });

    } catch (error) {
      console.error('❌ Create team error:', error);
      res.status(500).json({ 
        error: 'Failed to create team',
        message: 'An error occurred while creating the team',
        code: 'CREATE_TEAM_ERROR'
      });
    }
  }
);

// Get team by ID
router.get('/:teamId',
  authenticateToken,
  [
    param('teamId').isUUID().withMessage('Valid team ID required')
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

      console.log(`🏆 Get team ${req.params.teamId} by ${req.user.username}`);

      const { teamId } = req.params;

      // Check team access
      const accessCheck = await checkTeamAccess(teamId, req.user.id);
      
      if (!accessCheck.hasAccess && req.user.role !== 'founder' && req.user.role !== 'admin') {
        return res.status(403).json({ 
          error: 'Access denied',
          message: accessCheck.reason || 'You do not have access to this team',
          code: 'TEAM_ACCESS_DENIED'
        });
      }

      // Get detailed team information
      const teamResult = await secureQuery(`
        SELECT 
          t.id, t.name, t.description, t.is_legendary, t.is_public,
          t.max_members, t.created_at, t.updated_at, t.owner_id,
          u.username as owner_username,
          u.display_name as owner_display_name,
          u.is_legendary as owner_legendary
        FROM teams t
        JOIN users u ON t.owner_id = u.id
        WHERE t.id = $1 AND t.status != 'deleted'
      `, [teamId]);

      if (teamResult.rows.length === 0) {
        return res.status(404).json({ 
          error: 'Team not found',
          code: 'TEAM_NOT_FOUND'
        });
      }

      const team = teamResult.rows[0];

      // Get team members
      const membersResult = await secureQuery(`
        SELECT 
          tm.user_id, tm.role as team_role, tm.joined_at,
          u.username, u.display_name, u.is_legendary, u.code_bro_energy,
          u.role as platform_role
        FROM team_members tm
        JOIN users u ON tm.user_id = u.id
        WHERE tm.team_id = $1 AND u.status = 'active'
        ORDER BY 
          CASE tm.role 
            WHEN 'admin' THEN 1 
            WHEN 'moderator' THEN 2 
            ELSE 3 
          END,
          tm.joined_at ASC
      `, [teamId]);

      // Get team OKRs summary
      const okrStats = await secureQuery(`
        SELECT 
          COUNT(*) as total_okrs,
          COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_okrs,
          AVG(progress) as avg_progress,
          COUNT(CASE WHEN is_legendary = true THEN 1 END) as legendary_okrs
        FROM okrs
        WHERE team_id = $1
      `, [teamId]);

      // Get team messages summary (last 7 days)
      const messageStats = await secureQuery(`
        SELECT 
          COUNT(*) as message_count,
          COUNT(DISTINCT user_id) as active_members
        FROM messages
        WHERE team_id = $1 AND created_at > NOW() - INTERVAL '7 days'
      `, [teamId]);

      // Format team data
      const teamData = {
        id: team.id,
        name: team.name,
        description: team.description,
        is_legendary: team.is_legendary,
        is_public: team.is_public,
        max_members: team.max_members,
        created_at: team.created_at,
        updated_at: team.updated_at,
        owner: {
          id: team.owner_id,
          username: team.owner_username,
          display_name: team.owner_display_name,
          is_legendary: team.owner_legendary
        },
        members: membersResult.rows.map(member => ({
          user_id: member.user_id,
          username: member.username,
          display_name: member.display_name,
          is_legendary: member.is_legendary,
          code_bro_energy: member.code_bro_energy,
          platform_role: member.platform_role,
          team_role: member.team_role,
          joined_at: member.joined_at
        })),
        stats: {
          member_count: membersResult.rows.length,
          total_energy: membersResult.rows.reduce((sum, member) => sum + (member.code_bro_energy || 0), 0),
          okr_stats: okrStats.rows.length > 0 ? {
            total_okrs: parseInt(okrStats.rows[0].total_okrs) || 0,
            completed_okrs: parseInt(okrStats.rows[0].completed_okrs) || 0,
            avg_progress: parseFloat(okrStats.rows[0].avg_progress) || 0,
            legendary_okrs: parseInt(okrStats.rows[0].legendary_okrs) || 0
          } : { total_okrs: 0, completed_okrs: 0, avg_progress: 0, legendary_okrs: 0 },
          activity: messageStats.rows.length > 0 ? {
            messages_7d: parseInt(messageStats.rows[0].message_count) || 0,
            active_members_7d: parseInt(messageStats.rows[0].active_members) || 0
          } : { messages_7d: 0, active_members_7d: 0 }
        }
      };

      console.log(`🏆 Team details retrieved: ${team.name}`);

      if (req.user.role === 'founder') {
        console.log('👑🏆👑 FOUNDER TEAM ACCESS WITH INFINITE INSIGHTS! 👑🏆👑');
      }

      res.json({
        success: true,
        data: { team: teamData },
        message: req.user.role === 'founder' ? 
          `👑 Team "${team.name}" loaded with LEGENDARY FOUNDER insights!` :
          `🏆 Team "${team.name}" loaded successfully!`
      });

    } catch (error) {
      console.error('❌ Get team error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch team',
        message: 'An error occurred while retrieving team details',
        code: 'GET_TEAM_ERROR'
      });
    }
  }
);

// Join team
router.post('/:teamId/join',
  authenticateToken,
  [
    param('teamId').isUUID().withMessage('Valid team ID required')
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

      console.log(`🤝 Join team ${req.params.teamId} by ${req.user.username}`);

      const { teamId } = req.params;

      // Get team info
      const teamResult = await secureQuery(`
        SELECT 
          t.id, t.name, t.is_public, t.max_members, t.status,
          COUNT(tm.user_id) as current_members
        FROM teams t
        LEFT JOIN team_members tm ON t.id = tm.team_id
        WHERE t.id = $1 AND t.status = 'active'
        GROUP BY t.id, t.name, t.is_public, t.max_members, t.status
      `, [teamId]);

      if (teamResult.rows.length === 0) {
        return res.status(404).json({ 
          error: 'Team not found',
          code: 'TEAM_NOT_FOUND'
        });
      }

      const team = teamResult.rows[0];

      // Check if team is public
      if (!team.is_public) {
        return res.status(403).json({ 
          error: 'Private team',
          message: 'This team is private and requires an invitation',
          code: 'PRIVATE_TEAM'
        });
      }

      // Check if team has space
      if (team.current_members >= team.max_members) {
        return res.status(409).json({ 
          error: 'Team full',
          message: 'This team has reached its maximum member limit',
          code: 'TEAM_FULL'
        });
      }

      // Check if user is already a member
      const existingMember = await secureQuery(`
        SELECT id FROM team_members 
        WHERE team_id = $1 AND user_id = $2
      `, [teamId, req.user.id]);

      if (existingMember.rows.length > 0) {
        return res.status(409).json({ 
          error: 'Already a member',
          message: 'You are already a member of this team',
          code: 'ALREADY_MEMBER'
        });
      }

      // Add user to team
      await secureQuery(`
        INSERT INTO team_members (team_id, user_id, role, joined_at)
        VALUES ($1, $2, 'member', NOW())
      `, [teamId, req.user.id]);

      console.log(`🤝 User joined team: ${req.user.username} -> ${team.name}`);

      res.json({
        success: true,
        data: {
          team_id: teamId,
          team_name: team.name,
          user_role: 'member',
          joined_at: new Date().toISOString()
        },
        message: `🎉 Welcome to team "${team.name}"! Ready to create amazing things together!`
      });

    } catch (error) {
      console.error('❌ Join team error:', error);
      res.status(500).json({ 
        error: 'Failed to join team',
        message: 'An error occurred while joining the team',
        code: 'JOIN_TEAM_ERROR'
      });
    }
  }
);

// Leave team
router.post('/:teamId/leave',
  authenticateToken,
  [
    param('teamId').isUUID().withMessage('Valid team ID required')
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

      console.log(`👋 Leave team ${req.params.teamId} by ${req.user.username}`);

      const { teamId } = req.params;

      // Check if user is a member
      const memberResult = await secureQuery(`
        SELECT tm.role, t.name, t.owner_id
        FROM team_members tm
        JOIN teams t ON tm.team_id = t.id
        WHERE tm.team_id = $1 AND tm.user_id = $2
      `, [teamId, req.user.id]);

      if (memberResult.rows.length === 0) {
        return res.status(404).json({ 
          error: 'Not a team member',
          message: 'You are not a member of this team',
          code: 'NOT_MEMBER'
        });
      }

      const member = memberResult.rows[0];

      // Prevent team owner from leaving
      if (member.owner_id === req.user.id) {
        return res.status(409).json({ 
          error: 'Cannot leave as owner',
          message: 'Team owners cannot leave their team. Transfer ownership or delete the team.',
          code: 'OWNER_CANNOT_LEAVE'
        });
      }

      // Remove user from team
      await secureQuery(`
        DELETE FROM team_members 
        WHERE team_id = $1 AND user_id = $2
      `, [teamId, req.user.id]);

      console.log(`👋 User left team: ${req.user.username} -> ${member.name}`);

      res.json({
        success: true,
        data: {
          team_id: teamId,
          team_name: member.name,
          left_at: new Date().toISOString()
        },
        message: `👋 You have left team "${member.name}". Thanks for your contributions!`
      });

    } catch (error) {
      console.error('❌ Leave team error:', error);
      res.status(500).json({ 
        error: 'Failed to leave team',
        message: 'An error occurred while leaving the team',
        code: 'LEAVE_TEAM_ERROR'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'teams',
    timestamp: new Date().toISOString(),
    message: '🏆 Teams service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    evening_energy: '🌅 EVENING LEGENDARY TEAMS POWER AT 18:47:47! 🌅'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY SECURE TEAMS ROUTES COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Secure teams routes completed at: 2025-08-06 18:47:47 UTC`);
console.log('🏆 Team management: LEGENDARY SECURITY');
console.log('👑 RICKROLL187 founder team controls: MAXIMUM AUTHORITY');
console.log('🛡️ Team data protection: SWISS PRECISION');
console.log('🌅 EVENING LEGENDARY TEAM SECURITY: INFINITE AT 18:47:47!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
