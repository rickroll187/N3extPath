// File: backend/routes/hr-onboarding.js
/**
 * 🏢🎸 N3EXTPATH - LEGENDARY HR ONBOARDING & LIFECYCLE MANAGEMENT 🎸🏢
 * Swiss precision employee management with infinite HR energy
 * Built: 2025-08-06 20:44:54 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const express = require('express');
const rateLimit = require('express-rate-limit');
const { body, query, param, validationResult } = require('express-validator');

const router = express.Router();
const { secureQuery, secureTransaction } = require('../utils/database');
const { authenticateToken, requirePermission } = require('../middleware/auth');
const { validatePayload } = require('../middleware/advanced-security');

console.log('🏢🎸🏢 LEGENDARY HR ONBOARDING SYSTEM LOADING! 🏢🎸🏢');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`HR onboarding system loaded at: 2025-08-06 20:44:54 UTC`);
console.log('🌃 PRIME EVENING LEGENDARY HR POWER AT 20:44:54!');

// =====================================
// 🛡️ HR-SPECIFIC RATE LIMITING 🛡️
// =====================================

const hrLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 HR requests per windowMs
  message: {
    error: 'Too many HR requests from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'HR_RATE_LIMIT'
  }
});

router.use(hrLimiter);
router.use(validatePayload(10240)); // 10KB max payload

// =====================================
// 👥 ONBOARDING WORKFLOWS 👥
// =====================================

// Get onboarding checklist template
router.get('/onboarding/template',
  authenticateToken,
  requirePermission('users.read'),
  async (req, res) => {
    try {
      console.log(`🏢 Get onboarding template by ${req.user.username} at 20:44:54 UTC`);

      const template = {
        pre_start: [
          {
            id: 'welcome_email',
            title: 'Send Welcome Email',
            description: 'Send personalized welcome email with first day details',
            responsible: 'hr',
            required: true,
            estimated_time: 15
          },
          {
            id: 'equipment_prep',
            title: 'Prepare Equipment',
            description: 'Set up laptop, accounts, and workspace',
            responsible: 'it',
            required: true,
            estimated_time: 60
          },
          {
            id: 'documentation_prep',
            title: 'Prepare Documentation',
            description: 'Gather employee handbook, policies, and forms',
            responsible: 'hr',
            required: true,
            estimated_time: 30
          }
        ],
        first_day: [
          {
            id: 'office_tour',
            title: 'Office Tour & Introductions',
            description: 'Show workspace, introduce team members, explain culture',
            responsible: 'manager',
            required: true,
            estimated_time: 90
          },
          {
            id: 'systems_training',
            title: 'Systems & Tools Training',
            description: 'N3EXTPATH platform, communication tools, and workflows',
            responsible: 'it',
            required: true,
            estimated_time: 120
          },
          {
            id: 'hr_orientation',
            title: 'HR Orientation',
            description: 'Benefits, policies, emergency procedures, forms completion',
            responsible: 'hr',
            required: true,
            estimated_time: 60
          },
          {
            id: 'role_overview',
            title: 'Role & Expectations Overview',
            description: 'Job responsibilities, goals, performance expectations',
            responsible: 'manager',
            required: true,
            estimated_time: 45
          }
        ],
        first_week: [
          {
            id: 'team_meetings',
            title: 'Attend Team Meetings',
            description: 'Participate in regular team meetings and standups',
            responsible: 'employee',
            required: true,
            estimated_time: 180
          },
          {
            id: 'initial_projects',
            title: 'Start Initial Projects',
            description: 'Begin working on starter projects and OKRs',
            responsible: 'employee',
            required: true,
            estimated_time: 300
          },
          {
            id: 'buddy_checkins',
            title: 'Buddy System Check-ins',
            description: 'Regular check-ins with assigned onboarding buddy',
            responsible: 'buddy',
            required: true,
            estimated_time: 60
          }
        ],
        first_month: [
          {
            id: '30_day_review',
            title: '30-Day Review',
            description: 'Performance review and feedback session',
            responsible: 'manager',
            required: true,
            estimated_time: 60
          },
          {
            id: 'goals_setting',
            title: 'Goals & OKR Setting',
            description: 'Set quarterly OKRs and performance goals',
            responsible: 'manager',
            required: true,
            estimated_time: 45
          },
          {
            id: 'culture_integration',
            title: 'Culture Integration Assessment',
            description: 'Evaluate cultural fit and integration progress',
            responsible: 'hr',
            required: false,
            estimated_time: 30
          }
        ]
      };

      if (req.user.role === 'founder') {
        console.log('👑🏢👑 RICKROLL187 FOUNDER HR TEMPLATE ACCESS WITH INFINITE INSIGHTS! 👑🏢👑');
      }

      res.json({
        success: true,
        data: { template },
        message: req.user.role === 'founder' ? 
          '👑 LEGENDARY FOUNDER onboarding template with infinite precision!' :
          '🏢 Onboarding template retrieved with Swiss HR precision!'
      });

    } catch (error) {
      console.error('❌ Get onboarding template error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch onboarding template',
        code: 'ONBOARDING_TEMPLATE_ERROR'
      });
    }
  }
);

// Create employee onboarding plan
router.post('/onboarding/:userId',
  authenticateToken,
  requirePermission('users.write'),
  [
    param('userId').isUUID().withMessage('Valid user ID required'),
    body('start_date').isISO8601().withMessage('Valid start date required'),
    body('manager_id').isUUID().withMessage('Valid manager ID required'),
    body('buddy_id').optional().isUUID(),
    body('department').isLength({ min: 2, max: 100 }).trim(),
    body('role_title').isLength({ min: 2, max: 100 }).trim(),
    body('custom_tasks').optional().isArray({ max: 20 }),
    body('notes').optional().isLength({ max: 1000 }).trim()
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

      console.log(`🏢 Create onboarding plan for ${req.params.userId} by ${req.user.username}`);

      const { userId } = req.params;
      const { 
        start_date, 
        manager_id, 
        buddy_id, 
        department, 
        role_title, 
        custom_tasks = [], 
        notes 
      } = req.body;

      // Verify user exists and is not already onboarded
      const userCheck = await secureQuery(`
        SELECT id, username, display_name, status FROM users WHERE id = $1
      `, [userId]);

      if (userCheck.rows.length === 0) {
        return res.status(404).json({
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
      }

      const user = userCheck.rows[0];

      // Check if onboarding plan already exists
      const existingPlan = await secureQuery(`
        SELECT id FROM employee_onboarding WHERE user_id = $1
      `, [userId]);

      if (existingPlan.rows.length > 0) {
        return res.status(409).json({
          error: 'Onboarding plan already exists',
          message: `User ${user.username} already has an onboarding plan`,
          code: 'ONBOARDING_EXISTS'
        });
      }

      // Verify manager exists
      const managerCheck = await secureQuery(`
        SELECT id, username, display_name FROM users 
        WHERE id = $1 AND role IN ('founder', 'admin', 'moderator')
      `, [manager_id]);

      if (managerCheck.rows.length === 0) {
        return res.status(400).json({
          error: 'Invalid manager',
          message: 'Manager must be founder, admin, or moderator',
          code: 'INVALID_MANAGER'
        });
      }

      // Create onboarding plan in transaction
      const onboardingPlan = await secureTransaction(async (client) => {
        // Create main onboarding record
        const planResult = await client.query(`
          INSERT INTO employee_onboarding (
            user_id, created_by, manager_id, buddy_id, department, role_title,
            start_date, status, notes, created_at, updated_at
          ) VALUES ($1, $2, $3, $4, $5, $6, $7, 'pending', $8, NOW(), NOW())
          RETURNING id, start_date, status, created_at
        `, [userId, req.user.id, manager_id, buddy_id, department, role_title, start_date, notes]);

        const plan = planResult.rows[0];

        // Create default onboarding tasks
        const defaultTasks = [
          // Pre-start tasks
          { phase: 'pre_start', task_id: 'welcome_email', title: 'Send Welcome Email', responsible: 'hr', due_offset: -3 },
          { phase: 'pre_start', task_id: 'equipment_prep', title: 'Prepare Equipment', responsible: 'it', due_offset: -2 },
          { phase: 'pre_start', task_id: 'documentation_prep', title: 'Prepare Documentation', responsible: 'hr', due_offset: -1 },
          
          // First day tasks
          { phase: 'first_day', task_id: 'office_tour', title: 'Office Tour & Introductions', responsible: 'manager', due_offset: 0 },
          { phase: 'first_day', task_id: 'systems_training', title: 'Systems & Tools Training', responsible: 'it', due_offset: 0 },
          { phase: 'first_day', task_id: 'hr_orientation', title: 'HR Orientation', responsible: 'hr', due_offset: 0 },
          
          // First week tasks
          { phase: 'first_week', task_id: 'team_meetings', title: 'Attend Team Meetings', responsible: 'employee', due_offset: 7 },
          { phase: 'first_week', task_id: 'initial_projects', title: 'Start Initial Projects', responsible: 'employee', due_offset: 7 },
          
          // First month tasks
          { phase: 'first_month', task_id: '30_day_review', title: '30-Day Review', responsible: 'manager', due_offset: 30 }
        ];

        // Insert default tasks
        for (const task of defaultTasks) {
          await client.query(`
            INSERT INTO onboarding_tasks (
              onboarding_id, phase, task_id, title, responsible, 
              due_date, status, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, 'pending', NOW())
          `, [
            plan.id, 
            task.phase, 
            task.task_id, 
            task.title, 
            task.responsible,
            new Date(new Date(start_date).getTime() + task.due_offset * 24 * 60 * 60 * 1000)
          ]);
        }

        // Insert custom tasks if provided
        for (const customTask of custom_tasks) {
          await client.query(`
            INSERT INTO onboarding_tasks (
              onboarding_id, phase, task_id, title, responsible, 
              due_date, status, created_at
            ) VALUES ($1, 'custom', $2, $3, $4, $5, 'pending', NOW())
          `, [
            plan.id,
            customTask.id || `custom_${Date.now()}`,
            customTask.title,
            customTask.responsible || 'manager',
            customTask.due_date || start_date
          ]);
        }

        return plan;
      });

      console.log(`🏢 Onboarding plan created for ${user.username}`);

      if (req.user.role === 'founder') {
        console.log('👑🏢👑 LEGENDARY FOUNDER ONBOARDING PLAN CREATION! 👑🏢👑');
      }

      res.status(201).json({
        success: true,
        data: {
          onboarding_plan: {
            id: onboardingPlan.id,
            user: {
              id: user.id,
              username: user.username,
              display_name: user.display_name
            },
            manager: managerCheck.rows[0],
            department,
            role_title,
            start_date: onboardingPlan.start_date,
            status: onboardingPlan.status,
            created_at: onboardingPlan.created_at
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ONBOARDING: Plan created for ${user.username} with infinite precision!` :
          `🏢 Onboarding plan created for ${user.username}! Welcome to the team!`
      });

    } catch (error) {
      console.error('❌ Create onboarding plan error:', error);
      res.status(500).json({ 
        error: 'Failed to create onboarding plan',
        message: 'An error occurred while creating the onboarding plan',
        code: 'CREATE_ONBOARDING_ERROR'
      });
    }
  }
);

// Get employee onboarding status
router.get('/onboarding/:userId',
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

      console.log(`🏢 Get onboarding status ${req.params.userId} by ${req.user.username}`);

      const { userId } = req.params;

      // Check access permissions
      const canAccess = (
        req.user.id === userId || // Own onboarding
        req.user.role === 'founder' ||
        req.user.role === 'admin' ||
        req.user.role === 'moderator'
      );

      if (!canAccess) {
        return res.status(403).json({
          error: 'Access denied',
          message: 'You can only view your own onboarding status',
          code: 'ONBOARDING_ACCESS_DENIED'
        });
      }

      // Get onboarding plan
      const onboardingResult = await secureQuery(`
        SELECT 
          o.id, o.user_id, o.manager_id, o.buddy_id, o.department, o.role_title,
          o.start_date, o.status, o.notes, o.created_at, o.updated_at,
          u.username, u.display_name,
          m.username as manager_username, m.display_name as manager_display_name,
          b.username as buddy_username, b.display_name as buddy_display_name
        FROM employee_onboarding o
        JOIN users u ON o.user_id = u.id
        JOIN users m ON o.manager_id = m.id
        LEFT JOIN users b ON o.buddy_id = b.id
        WHERE o.user_id = $1
      `, [userId]);

      if (onboardingResult.rows.length === 0) {
        return res.status(404).json({
          error: 'Onboarding plan not found',
          code: 'ONBOARDING_NOT_FOUND'
        });
      }

      const onboarding = onboardingResult.rows[0];

      // Get onboarding tasks
      const tasksResult = await secureQuery(`
        SELECT 
          id, phase, task_id, title, description, responsible, 
          due_date, completed_date, status, notes, created_at, updated_at
        FROM onboarding_tasks
        WHERE onboarding_id = $1
        ORDER BY phase, due_date ASC
      `, [onboarding.id]);

      // Calculate progress statistics
      const tasks = tasksResult.rows;
      const totalTasks = tasks.length;
      const completedTasks = tasks.filter(task => task.status === 'completed').length;
      const overdueTasks = tasks.filter(task => 
        task.status !== 'completed' && new Date(task.due_date) < new Date()
      ).length;
      const progressPercentage = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

      // Group tasks by phase
      const tasksByPhase = tasks.reduce((acc, task) => {
        if (!acc[task.phase]) acc[task.phase] = [];
        acc[task.phase].push(task);
        return acc;
      }, {});

      const onboardingData = {
        id: onboarding.id,
        employee: {
          id: onboarding.user_id,
          username: onboarding.username,
          display_name: onboarding.display_name
        },
        manager: {
          id: onboarding.manager_id,
          username: onboarding.manager_username,
          display_name: onboarding.manager_display_name
        },
        buddy: onboarding.buddy_id ? {
          id: onboarding.buddy_id,
          username: onboarding.buddy_username,
          display_name: onboarding.buddy_display_name
        } : null,
        department: onboarding.department,
        role_title: onboarding.role_title,
        start_date: onboarding.start_date,
        status: onboarding.status,
        notes: onboarding.notes,
        created_at: onboarding.created_at,
        updated_at: onboarding.updated_at,
        progress: {
          total_tasks: totalTasks,
          completed_tasks: completedTasks,
          overdue_tasks: overdueTasks,
          progress_percentage: Math.round(progressPercentage),
          current_phase: onboarding.status
        },
        tasks_by_phase: tasksByPhase,
        all_tasks: tasks
      };

      console.log(`🏢 Onboarding status retrieved for ${onboarding.username}`);

      res.json({
        success: true,
        data: { onboarding: onboardingData },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER onboarding insights with infinite precision!` :
          `🏢 Onboarding status loaded successfully!`
      });

    } catch (error) {
      console.error('❌ Get onboarding status error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch onboarding status',
        message: 'An error occurred while retrieving onboarding status',
        code: 'GET_ONBOARDING_ERROR'
      });
    }
  }
);

// Update onboarding task status
router.patch('/onboarding/:userId/tasks/:taskId',
  authenticateToken,
  [
    param('userId').isUUID().withMessage('Valid user ID required'),
    param('taskId').isUUID().withMessage('Valid task ID required'),
    body('status').isIn(['pending', 'in_progress', 'completed', 'skipped']).withMessage('Valid status required'),
    body('notes').optional().isLength({ max: 500 }).trim(),
    body('completed_by').optional().isUUID()
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

      console.log(`✅ Update onboarding task ${req.params.taskId} by ${req.user.username}`);

      const { userId, taskId } = req.params;
      const { status, notes, completed_by } = req.body;

      // Check access permissions
      const canUpdate = (
        req.user.id === userId || // Own tasks
        req.user.role === 'founder' ||
        req.user.role === 'admin' ||
        req.user.role === 'moderator'
      );

      if (!canUpdate) {
        return res.status(403).json({
          error: 'Access denied',
          message: 'You can only update your own onboarding tasks',
          code: 'TASK_UPDATE_ACCESS_DENIED'
        });
      }

      // Get task and verify ownership
      const taskResult = await secureQuery(`
        SELECT 
          ot.id, ot.title, ot.status as current_status, ot.onboarding_id,
          o.user_id, o.status as onboarding_status,
          u.username
        FROM onboarding_tasks ot
        JOIN employee_onboarding o ON ot.onboarding_id = o.id
        JOIN users u ON o.user_id = u.id
        WHERE ot.id = $1 AND o.user_id = $2
      `, [taskId, userId]);

      if (taskResult.rows.length === 0) {
        return res.status(404).json({
          error: 'Task not found',
          code: 'TASK_NOT_FOUND'
        });
      }

      const task = taskResult.rows[0];

      // Update task status
      const updateFields = ['status = $3', 'updated_at = NOW()'];
      const updateParams = [taskId, userId, status];
      let paramCount = 3;

      if (status === 'completed') {
        paramCount++;
        updateFields.push(`completed_date = NOW()`);
        updateFields.push(`completed_by = $${paramCount}`);
        updateParams.push(completed_by || req.user.id);
      }

      if (notes) {
        paramCount++;
        updateFields.push(`notes = $${paramCount}`);
        updateParams.push(notes);
      }

      const updatedTask = await secureQuery(`
        UPDATE onboarding_tasks 
        SET ${updateFields.join(', ')}
        WHERE id = $1 AND onboarding_id IN (
          SELECT id FROM employee_onboarding WHERE user_id = $2
        )
        RETURNING id, title, status, completed_date, notes, updated_at
      `, updateParams);

      console.log(`✅ Onboarding task updated: ${task.title} -> ${status}`);

      if (req.user.role === 'founder') {
        console.log('👑✅👑 LEGENDARY FOUNDER ONBOARDING TASK UPDATE! 👑✅👑');
      }

      res.json({
        success: true,
        data: { task: updatedTask.rows[0] },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER TASK: "${task.title}" updated to ${status} with infinite precision!` :
          status === 'completed' ? 
            `🎉 Task "${task.title}" completed! Great progress!` :
            `✅ Task "${task.title}" updated to ${status}!`
      });

    } catch (error) {
      console.error('❌ Update onboarding task error:', error);
      res.status(500).json({ 
        error: 'Failed to update onboarding task',
        message: 'An error occurred while updating the task',
        code: 'UPDATE_TASK_ERROR'
      });
    }
  }
);

// =====================================
// 🔄 EMPLOYEE OFFBOARDING 🔄
// =====================================

// Create employee offboarding plan
router.post('/offboarding/:userId',
  authenticateToken,
  requirePermission('users.write'),
  [
    param('userId').isUUID().withMessage('Valid user ID required'),
    body('last_day').isISO8601().withMessage('Valid last day required'),
    body('reason').isIn(['resignation', 'termination', 'layoff', 'retirement', 'contract_end']).withMessage('Valid reason required'),
    body('manager_id').isUUID().withMessage('Valid manager ID required'),
    body('notes').optional().isLength({ max: 1000 }).trim(),
    body('knowledge_transfer').optional().isBoolean(),
    body('equipment_return').optional().isBoolean()
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

      console.log(`🔄 Create offboarding plan for ${req.params.userId} by ${req.user.username}`);

      const { userId } = req.params;
      const { 
        last_day, 
        reason, 
        manager_id, 
        notes,
        knowledge_transfer = true,
        equipment_return = true
      } = req.body;

      // Verify user exists
      const userCheck = await secureQuery(`
        SELECT id, username, display_name, status FROM users WHERE id = $1
      `, [userId]);

      if (userCheck.rows.length === 0) {
        return res.status(404).json({
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
      }

      const user = userCheck.rows[0];

      // Prevent offboarding founder
      if (user.status === 'founder') {
        return res.status(403).json({
          error: 'Cannot offboard founder',
          message: 'Founder account cannot be offboarded',
          code: 'FOUNDER_OFFBOARDING_DENIED'
        });
      }

      // Check if offboarding plan already exists
      const existingPlan = await secureQuery(`
        SELECT id FROM employee_offboarding WHERE user_id = $1
      `, [userId]);

      if (existingPlan.rows.length > 0) {
        return res.status(409).json({
          error: 'Offboarding plan already exists',
          message: `User ${user.username} already has an offboarding plan`,
          code: 'OFFBOARDING_EXISTS'
        });
      }

      // Create offboarding plan in transaction
      const offboardingPlan = await secureTransaction(async (client) => {
        // Create main offboarding record
        const planResult = await client.query(`
          INSERT INTO employee_offboarding (
            user_id, created_by, manager_id, last_day, reason,
            knowledge_transfer, equipment_return, status, notes, created_at, updated_at
          ) VALUES ($1, $2, $3, $4, $5, $6, $7, 'pending', $8, NOW(), NOW())
          RETURNING id, last_day, reason, status, created_at
        `, [userId, req.user.id, manager_id, last_day, reason, knowledge_transfer, equipment_return, notes]);

        const plan = planResult.rows[0];

        // Create default offboarding tasks
        const offboardingTasks = [
          { task_id: 'exit_interview', title: 'Conduct Exit Interview', responsible: 'hr', due_offset: -3 },
          { task_id: 'knowledge_transfer', title: 'Complete Knowledge Transfer', responsible: 'employee', due_offset: -5 },
          { task_id: 'equipment_return', title: 'Return Company Equipment', responsible: 'employee', due_offset: 0 },
          { task_id: 'access_revoke', title: 'Revoke System Access', responsible: 'it', due_offset: 0 },
          { task_id: 'final_payroll', title: 'Process Final Payroll', responsible: 'hr', due_offset: 3 },
          { task_id: 'benefits_cobra', title: 'Arrange COBRA Benefits', responsible: 'hr', due_offset: 7 }
        ];

        // Insert offboarding tasks
        for (const task of offboardingTasks) {
          await client.query(`
            INSERT INTO offboarding_tasks (
              offboarding_id, task_id, title, responsible, 
              due_date, status, created_at
            ) VALUES ($1, $2, $3, $4, $5, 'pending', NOW())
          `, [
            plan.id, 
            task.task_id, 
            task.title, 
            task.responsible,
            new Date(new Date(last_day).getTime() + task.due_offset * 24 * 60 * 60 * 1000)
          ]);
        }

        return plan;
      });

      console.log(`🔄 Offboarding plan created for ${user.username}`);

      if (req.user.role === 'founder') {
        console.log('👑🔄👑 LEGENDARY FOUNDER OFFBOARDING PLAN CREATION! 👑🔄👑');
      }

      res.status(201).json({
        success: true,
        data: {
          offboarding_plan: {
            id: offboardingPlan.id,
            user: {
              id: user.id,
              username: user.username,
              display_name: user.display_name
            },
            last_day: offboardingPlan.last_day,
            reason: offboardingPlan.reason,
            status: offboardingPlan.status,
            created_at: offboardingPlan.created_at
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER OFFBOARDING: Plan created for ${user.username} with infinite precision!` :
          `🔄 Offboarding plan created for ${user.username}. Best wishes for their next journey!`
      });

    } catch (error) {
      console.error('❌ Create offboarding plan error:', error);
      res.status(500).json({ 
        error: 'Failed to create offboarding plan',
        message: 'An error occurred while creating the offboarding plan',
        code: 'CREATE_OFFBOARDING_ERROR'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'hr-onboarding',
    timestamp: new Date().toISOString(),
    message: '🏢 HR onboarding service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    evening_energy: '🌃 PRIME EVENING LEGENDARY HR POWER AT 20:44:54! 🌃'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY HR ONBOARDING SYSTEM COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`HR onboarding system completed at: 2025-08-06 20:44:54 UTC`);
console.log('🏢 Employee lifecycle: LEGENDARY PRECISION');
console.log('👑 RICKROLL187 founder HR controls: MAXIMUM AUTHORITY');
console.log('🔄 Onboarding/offboarding: SWISS PRECISION');
console.log('🌃 PRIME EVENING LEGENDARY HR POWER: INFINITE AT 20:44:54!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
