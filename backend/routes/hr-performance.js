// File: backend/routes/hr-performance.js
/**
 * 📈🎸 N3EXTPATH - LEGENDARY PERFORMANCE MANAGEMENT SYSTEM 🎸📈
 * Swiss precision performance tracking with infinite excellence energy
 * Built: 2025-08-06 20:52:38 UTC by RICKROLL187
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

console.log('📈🎸📈 LEGENDARY PERFORMANCE MANAGEMENT SYSTEM LOADING! 📈🎸📈');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Performance management system loaded at: 2025-08-06 20:52:38 UTC`);
console.log('🌃 PRIME EVENING LEGENDARY PERFORMANCE POWER AT 20:52:38!');

// =====================================
// 🛡️ PERFORMANCE RATE LIMITING 🛡️
// =====================================

const performanceLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 150, // Performance reviews are less frequent
  message: {
    error: 'Too many performance requests from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'PERFORMANCE_RATE_LIMIT'
  }
});

router.use(performanceLimiter);
router.use(validatePayload(15360)); // 15KB max payload for detailed reviews

// =====================================
// 🎯 PERFORMANCE GOALS & OKR INTEGRATION 🎯
// =====================================

// Create performance goal template
router.post('/goals/template',
  authenticateToken,
  requirePermission('users.write'),
  [
    body('name').isLength({ min: 3, max: 200 }).trim(),
    body('description').optional().isLength({ max: 1000 }).trim(),
    body('category').isIn(['technical', 'leadership', 'communication', 'innovation', 'teamwork', 'customer_focus']),
    body('measurement_criteria').isArray({ min: 1, max: 10 }),
    body('measurement_criteria.*.criterion').isLength({ min: 5, max: 200 }),
    body('measurement_criteria.*.weight').isFloat({ min: 0, max: 100 }),
    body('target_audience').isIn(['individual', 'team_lead', 'manager', 'all']),
    body('difficulty_level').isIn(['beginner', 'intermediate', 'advanced', 'expert'])
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

      console.log(`🎯 Create performance goal template by ${req.user.username} at 20:52:38 UTC`);

      const { 
        name, 
        description, 
        category, 
        measurement_criteria, 
        target_audience, 
        difficulty_level 
      } = req.body;

      // Validate measurement criteria weights sum to 100
      const totalWeight = measurement_criteria.reduce((sum, criteria) => sum + criteria.weight, 0);
      if (Math.abs(totalWeight - 100) > 0.01) {
        return res.status(400).json({
          error: 'Invalid weights',
          message: 'Measurement criteria weights must sum to 100%',
          code: 'INVALID_WEIGHTS',
          current_total: totalWeight
        });
      }

      const goalTemplate = await secureQuery(`
        INSERT INTO performance_goal_templates (
          name, description, category, measurement_criteria, target_audience,
          difficulty_level, created_by, created_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
        RETURNING id, name, category, target_audience, difficulty_level, created_at
      `, [
        name, 
        description, 
        category, 
        JSON.stringify(measurement_criteria), 
        target_audience, 
        difficulty_level, 
        req.user.id
      ]);

      console.log(`🎯 Performance goal template created: ${name}`);

      if (req.user.role === 'founder') {
        console.log('👑🎯👑 LEGENDARY FOUNDER GOAL TEMPLATE CREATION! 👑🎯👑');
      }

      res.status(201).json({
        success: true,
        data: {
          goal_template: {
            ...goalTemplate.rows[0],
            measurement_criteria,
            creator: {
              id: req.user.id,
              username: req.user.username,
              display_name: req.user.display_name
            }
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER GOAL TEMPLATE: "${name}" created with infinite performance standards!` :
          `🎯 Performance goal template "${name}" created successfully!`
      });

    } catch (error) {
      console.error('❌ Create goal template error:', error);
      res.status(500).json({ 
        error: 'Failed to create goal template',
        message: 'An error occurred while creating the performance goal template',
        code: 'CREATE_GOAL_TEMPLATE_ERROR'
      });
    }
  }
);

// Assign performance goals to employee
router.post('/goals/assign/:userId',
  authenticateToken,
  requirePermission('users.write'),
  [
    param('userId').isUUID().withMessage('Valid user ID required'),
    body('goals').isArray({ min: 1, max: 20 }),
    body('goals.*.template_id').optional().isUUID(),
    body('goals.*.custom_title').optional().isLength({ min: 3, max: 200 }),
    body('goals.*.custom_description').optional().isLength({ max: 1000 }),
    body('goals.*.target_completion_date').isISO8601(),
    body('goals.*.priority').isIn(['low', 'medium', 'high', 'critical']),
    body('goals.*.weight').isFloat({ min: 0, max: 100 }),
    body('review_period').isIn(['quarterly', 'semi_annual', 'annual']),
    body('review_cycle_start').isISO8601()
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

      console.log(`📋 Assign performance goals to ${req.params.userId} by ${req.user.username}`);

      const { userId } = req.params;
      const { goals, review_period, review_cycle_start } = req.body;

      // Verify target user exists
      const userCheck = await secureQuery(`
        SELECT id, username, display_name, role FROM users WHERE id = $1
      `, [userId]);

      if (userCheck.rows.length === 0) {
        return res.status(404).json({
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
      }

      const targetUser = userCheck.rows[0];

      // Validate total weight doesn't exceed 100%
      const totalWeight = goals.reduce((sum, goal) => sum + goal.weight, 0);
      if (totalWeight > 100) {
        return res.status(400).json({
          error: 'Excessive weight',
          message: 'Total goal weights cannot exceed 100%',
          code: 'EXCESSIVE_GOAL_WEIGHT',
          current_total: totalWeight
        });
      }

      // Create performance goals in transaction
      const assignedGoals = await secureTransaction(async (client) => {
        // Create performance cycle if it doesn't exist
        const cycleResult = await client.query(`
          INSERT INTO performance_cycles (
            user_id, period_type, start_date, status, created_by, created_at
          ) VALUES ($1, $2, $3, 'active', $4, NOW())
          ON CONFLICT (user_id, start_date) DO UPDATE SET
            period_type = EXCLUDED.period_type,
            updated_at = NOW()
          RETURNING id, start_date, period_type
        `, [userId, review_period, review_cycle_start, req.user.id]);

        const cycle = cycleResult.rows[0];

        // Create individual goals
        const createdGoals = [];
        for (const goal of goals) {
          let goalData = {
            title: goal.custom_title,
            description: goal.custom_description,
            measurement_criteria: null
          };

          // If using template, get template data
          if (goal.template_id) {
            const templateResult = await client.query(`
              SELECT name, description, measurement_criteria FROM performance_goal_templates
              WHERE id = $1
            `, [goal.template_id]);

            if (templateResult.rows.length > 0) {
              const template = templateResult.rows[0];
              goalData.title = goalData.title || template.name;
              goalData.description = goalData.description || template.description;
              goalData.measurement_criteria = template.measurement_criteria;
            }
          }

          const goalResult = await client.query(`
            INSERT INTO performance_goals (
              cycle_id, user_id, template_id, title, description, 
              measurement_criteria, target_completion_date, priority, weight,
              status, progress, created_by, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'active', 0, $10, NOW())
            RETURNING id, title, priority, weight, target_completion_date, status, progress
          `, [
            cycle.id, 
            userId, 
            goal.template_id, 
            goalData.title, 
            goalData.description,
            goalData.measurement_criteria,
            goal.target_completion_date,
            goal.priority,
            goal.weight,
            req.user.id
          ]);

          createdGoals.push(goalResult.rows[0]);
        }

        return { cycle, goals: createdGoals };
      });

      console.log(`📋 ${goals.length} performance goals assigned to ${targetUser.username}`);

      if (req.user.role === 'founder') {
        console.log('👑📋👑 LEGENDARY FOUNDER GOAL ASSIGNMENT WITH INFINITE STANDARDS! 👑📋👑');
      }

      res.status(201).json({
        success: true,
        data: {
          performance_cycle: assignedGoals.cycle,
          assigned_goals: assignedGoals.goals,
          employee: {
            id: targetUser.id,
            username: targetUser.username,
            display_name: targetUser.display_name
          },
          summary: {
            total_goals: goals.length,
            total_weight: totalWeight,
            review_period
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ASSIGNMENT: ${goals.length} performance goals assigned to ${targetUser.display_name} with infinite standards!` :
          `📋 ${goals.length} performance goals assigned to ${targetUser.display_name} successfully!`
      });

    } catch (error) {
      console.error('❌ Assign performance goals error:', error);
      res.status(500).json({ 
        error: 'Failed to assign performance goals',
        message: 'An error occurred while assigning performance goals',
        code: 'ASSIGN_GOALS_ERROR'
      });
    }
  }
);

// =====================================
// 📊 PERFORMANCE REVIEWS 📊
// =====================================

// Start performance review cycle
router.post('/reviews/start-cycle',
  authenticateToken,
  requirePermission('users.write'),
  [
    body('review_type').isIn(['quarterly', 'semi_annual', 'annual', 'probationary', 'project_based']),
    body('review_period_start').isISO8601(),
    body('review_period_end').isISO8601(),
    body('participants').isArray({ min: 1 }),
    body('participants.*.user_id').isUUID(),
    body('participants.*.reviewer_id').isUUID(),
    body('participants.*.review_template_id').optional().isUUID(),
    body('due_date').isISO8601(),
    body('instructions').optional().isLength({ max: 2000 }).trim()
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

      console.log(`📊 Start performance review cycle by ${req.user.username} at 20:52:38 UTC`);

      const { 
        review_type, 
        review_period_start, 
        review_period_end, 
        participants, 
        due_date,
        instructions 
      } = req.body;

      // Validate review period
      if (new Date(review_period_start) >= new Date(review_period_end)) {
        return res.status(400).json({
          error: 'Invalid review period',
          message: 'Review period start must be before end date',
          code: 'INVALID_REVIEW_PERIOD'
        });
      }

      // Create review cycle in transaction
      const reviewCycle = await secureTransaction(async (client) => {
        // Create main review cycle
        const cycleResult = await client.query(`
          INSERT INTO review_cycles (
            review_type, period_start, period_end, due_date, 
            instructions, status, created_by, created_at
          ) VALUES ($1, $2, $3, $4, $5, 'active', $6, NOW())
          RETURNING id, review_type, period_start, period_end, due_date, status, created_at
        `, [review_type, review_period_start, review_period_end, due_date, instructions, req.user.id]);

        const cycle = cycleResult.rows[0];

        // Create individual review assignments
        const reviewAssignments = [];
        for (const participant of participants) {
          const assignmentResult = await client.query(`
            INSERT INTO performance_reviews (
              cycle_id, reviewee_id, reviewer_id, template_id,
              status, due_date, created_at
            ) VALUES ($1, $2, $3, $4, 'pending', $5, NOW())
            RETURNING id, reviewee_id, reviewer_id, status, due_date
          `, [
            cycle.id, 
            participant.user_id, 
            participant.reviewer_id, 
            participant.review_template_id,
            due_date
          ]);

          reviewAssignments.push(assignmentResult.rows[0]);
        }

        // Get participant details
        const participantIds = participants.map(p => p.user_id);
        const reviewerIds = participants.map(p => p.reviewer_id);
        const allUserIds = [...new Set([...participantIds, ...reviewerIds])];

        const usersResult = await client.query(`
          SELECT id, username, display_name FROM users 
          WHERE id = ANY($1)
        `, [allUserIds]);

        const userLookup = {};
        usersResult.rows.forEach(user => {
          userLookup[user.id] = user;
        });

        // Enhance assignments with user details
        const enhancedAssignments = reviewAssignments.map(assignment => ({
          ...assignment,
          reviewee: userLookup[assignment.reviewee_id],
          reviewer: userLookup[assignment.reviewer_id]
        }));

        return { cycle, assignments: enhancedAssignments };
      });

      console.log(`📊 Review cycle started: ${review_type} with ${participants.length} participants`);

      if (req.user.role === 'founder') {
        console.log('👑📊👑 LEGENDARY FOUNDER REVIEW CYCLE WITH INFINITE EVALUATION POWER! 👑📊👑');
      }

      res.status(201).json({
        success: true,
        data: {
          review_cycle: reviewCycle.cycle,
          review_assignments: reviewCycle.assignments,
          summary: {
            total_participants: participants.length,
            review_type,
            due_date
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER REVIEW CYCLE: ${review_type} started for ${participants.length} participants with infinite evaluation standards!` :
          `📊 ${review_type} performance review cycle started for ${participants.length} participants!`
      });

    } catch (error) {
      console.error('❌ Start review cycle error:', error);
      res.status(500).json({ 
        error: 'Failed to start review cycle',
        message: 'An error occurred while starting the performance review cycle',
        code: 'START_REVIEW_CYCLE_ERROR'
      });
    }
  }
);

// Submit performance review
router.post('/reviews/:reviewId/submit',
  authenticateToken,
  [
    param('reviewId').isUUID().withMessage('Valid review ID required'),
    body('sections').isArray({ min: 1 }),
    body('sections.*.section_name').isLength({ min: 2, max: 100 }),
    body('sections.*.rating').isInt({ min: 1, max: 5 }),
    body('sections.*.comments').isLength({ min: 10, max: 2000 }),
    body('sections.*.evidence').optional().isLength({ max: 1000 }),
    body('overall_rating').isInt({ min: 1, max: 5 }),
    body('overall_comments').isLength({ min: 20, max: 3000 }),
    body('strengths').isLength({ min: 10, max: 1500 }),
    body('improvement_areas').isLength({ min: 10, max: 1500 }),
    body('development_recommendations').optional().isLength({ max: 2000 }),
    body('goals_for_next_period').optional().isArray({ max: 10 })
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

      console.log(`📝 Submit performance review ${req.params.reviewId} by ${req.user.username}`);

      const { reviewId } = req.params;
      const { 
        sections, 
        overall_rating, 
        overall_comments, 
        strengths, 
        improvement_areas,
        development_recommendations,
        goals_for_next_period
      } = req.body;

      // Verify review exists and user can submit it
      const reviewCheck = await secureQuery(`
        SELECT 
          pr.id, pr.reviewee_id, pr.reviewer_id, pr.status, pr.due_date,
          u1.username as reviewee_username, u1.display_name as reviewee_name,
          u2.username as reviewer_username, u2.display_name as reviewer_name,
          rc.review_type
        FROM performance_reviews pr
        JOIN users u1 ON pr.reviewee_id = u1.id
        JOIN users u2 ON pr.reviewer_id = u2.id
        JOIN review_cycles rc ON pr.cycle_id = rc.id
        WHERE pr.id = $1
      `, [reviewId]);

      if (reviewCheck.rows.length === 0) {
        return res.status(404).json({
          error: 'Review not found',
          code: 'REVIEW_NOT_FOUND'
        });
      }

      const review = reviewCheck.rows[0];

      // Check if user can submit this review
      const canSubmit = (
        req.user.id === review.reviewer_id || // Assigned reviewer
        req.user.role === 'founder' ||
        req.user.role === 'admin'
      );

      if (!canSubmit) {
        return res.status(403).json({
          error: 'Cannot submit review',
          message: 'You are not authorized to submit this review',
          code: 'REVIEW_SUBMIT_DENIED'
        });
      }

      if (review.status !== 'pending' && review.status !== 'draft') {
        return res.status(409).json({
          error: 'Review already submitted',
          message: `Review is already ${review.status}`,
          code: 'REVIEW_ALREADY_SUBMITTED'
        });
      }

      // Calculate average section rating
      const avgSectionRating = sections.reduce((sum, section) => sum + section.rating, 0) / sections.length;

      // Submit review in transaction
      const submittedReview = await secureTransaction(async (client) => {
        // Update main review
        const reviewResult = await client.query(`
          UPDATE performance_reviews 
          SET 
            overall_rating = $2,
            overall_comments = $3,
            strengths = $4,
            improvement_areas = $5,
            development_recommendations = $6,
            goals_for_next_period = $7,
            avg_section_rating = $8,
            status = 'completed',
            submitted_at = NOW(),
            updated_at = NOW()
          WHERE id = $1
          RETURNING id, overall_rating, avg_section_rating, status, submitted_at
        `, [
          reviewId, 
          overall_rating, 
          overall_comments, 
          strengths, 
          improvement_areas,
          development_recommendations,
          goals_for_next_period ? JSON.stringify(goals_for_next_period) : null,
          avgSectionRating
        ]);

        // Insert section ratings
        for (const section of sections) {
          await client.query(`
            INSERT INTO review_sections (
              review_id, section_name, rating, comments, evidence, created_at
            ) VALUES ($1, $2, $3, $4, $5, NOW())
          `, [reviewId, section.section_name, section.rating, section.comments, section.evidence]);
        }

        return reviewResult.rows[0];
      });

      console.log(`📝 Performance review submitted: ${review.reviewee_username} (${overall_rating}/5)`);

      if (req.user.role === 'founder') {
        console.log('👑📝👑 LEGENDARY FOUNDER REVIEW SUBMISSION WITH INFINITE EVALUATION! 👑📝👑');
      }

      res.json({
        success: true,
        data: {
          review: {
            ...submittedReview,
            reviewee: {
              username: review.reviewee_username,
              display_name: review.reviewee_name
            },
            reviewer: {
              username: review.reviewer_username,
              display_name: review.reviewer_name
            },
            sections_count: sections.length,
            review_type: review.review_type
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER REVIEW: Performance evaluation for ${review.reviewee_name} completed with infinite precision (${overall_rating}/5)!` :
          `📝 Performance review for ${review.reviewee_name} submitted successfully! Overall rating: ${overall_rating}/5`
      });

    } catch (error) {
      console.error('❌ Submit performance review error:', error);
      res.status(500).json({ 
        error: 'Failed to submit performance review',
        message: 'An error occurred while submitting the performance review',
        code: 'SUBMIT_REVIEW_ERROR'
      });
    }
  }
);

// =====================================
// 🔄 360-DEGREE FEEDBACK SYSTEM 🔄
// =====================================

// Create 360-degree feedback request
router.post('/360-feedback/request',
  authenticateToken,
  requirePermission('users.write'),
  [
    body('subject_user_id').isUUID().withMessage('Valid subject user ID required'),
    body('feedback_providers').isArray({ min: 3, max: 15 }),
    body('feedback_providers.*').isUUID(),
    body('feedback_areas').isArray({ min: 1, max: 10 }),
    body('feedback_areas.*').isIn(['leadership', 'communication', 'teamwork', 'problem_solving', 'innovation', 'reliability', 'adaptability', 'customer_focus', 'technical_skills', 'mentoring']),
    body('due_date').isISO8601(),
    body('anonymous').optional().isBoolean(),
    body('instructions').optional().isLength({ max: 1000 }).trim()
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

      console.log(`🔄 Create 360-degree feedback request by ${req.user.username} at 20:52:38 UTC`);

      const { 
        subject_user_id, 
        feedback_providers, 
        feedback_areas, 
        due_date, 
        anonymous = true, 
        instructions 
      } = req.body;

      // Verify subject user exists
      const subjectUserCheck = await secureQuery(`
        SELECT id, username, display_name FROM users WHERE id = $1
      `, [subject_user_id]);

      if (subjectUserCheck.rows.length === 0) {
        return res.status(404).json({
          error: 'Subject user not found',
          code: 'SUBJECT_USER_NOT_FOUND'
        });
      }

      const subjectUser = subjectUserCheck.rows[0];

      // Verify all feedback providers exist
      const providersCheck = await secureQuery(`
        SELECT id, username, display_name FROM users 
        WHERE id = ANY($1) AND status = 'active'
      `, [feedback_providers]);

      if (providersCheck.rows.length !== feedback_providers.length) {
        return res.status(400).json({
          error: 'Invalid feedback providers',
          message: 'Some feedback providers are invalid or inactive',
          code: 'INVALID_FEEDBACK_PROVIDERS'
        });
      }

      // Create 360-degree feedback request in transaction
      const feedbackRequest = await secureTransaction(async (client) => {
        // Create main request
        const requestResult = await client.query(`
          INSERT INTO feedback_360_requests (
            subject_user_id, requested_by, feedback_areas, due_date, 
            anonymous, instructions, status, created_at
          ) VALUES ($1, $2, $3, $4, $5, $6, 'active', NOW())
          RETURNING id, due_date, anonymous, status, created_at
        `, [
          subject_user_id, 
          req.user.id, 
          JSON.stringify(feedback_areas), 
          due_date, 
          anonymous, 
          instructions
        ]);

        const request = requestResult.rows[0];

        // Create individual feedback assignments
        const assignments = [];
        for (const providerId of feedback_providers) {
          const assignmentResult = await client.query(`
            INSERT INTO feedback_360_assignments (
              request_id, provider_id, status, created_at
            ) VALUES ($1, $2, 'pending', NOW())
            RETURNING id, provider_id, status
          `, [request.id, providerId]);

          assignments.push(assignmentResult.rows[0]);
        }

        return { request, assignments };
      });

      console.log(`🔄 360-degree feedback request created for ${subjectUser.username} with ${feedback_providers.length} providers`);

      if (req.user.role === 'founder') {
        console.log('👑🔄👑 LEGENDARY FOUNDER 360-FEEDBACK REQUEST WITH INFINITE INSIGHT GATHERING! 👑🔄👑');
      }

      res.status(201).json({
        success: true,
        data: {
          feedback_request: {
            ...feedbackRequest.request,
            subject_user: subjectUser,
            feedback_areas,
            provider_count: feedback_providers.length,
            assignments: feedbackRequest.assignments
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER 360-FEEDBACK: Request created for ${subjectUser.display_name} with infinite insight gathering from ${feedback_providers.length} providers!` :
          `🔄 360-degree feedback request created for ${subjectUser.display_name} with ${feedback_providers.length} feedback providers!`
      });

    } catch (error) {
      console.error('❌ Create 360-feedback request error:', error);
      res.status(500).json({ 
        error: 'Failed to create 360-feedback request',
        message: 'An error occurred while creating the 360-degree feedback request',
        code: 'CREATE_360_FEEDBACK_ERROR'
      });
    }
  }
);

// Submit 360-degree feedback
router.post('/360-feedback/:assignmentId/submit',
  authenticateToken,
  [
    param('assignmentId').isUUID().withMessage('Valid assignment ID required'),
    body('feedback_ratings').isArray({ min: 1, max: 10 }),
    body('feedback_ratings.*.area').isIn(['leadership', 'communication', 'teamwork', 'problem_solving', 'innovation', 'reliability', 'adaptability', 'customer_focus', 'technical_skills', 'mentoring']),
    body('feedback_ratings.*.rating').isInt({ min: 1, max: 5 }),
    body('feedback_ratings.*.comments').isLength({ min: 10, max: 1000 }),
    body('strengths').isLength({ min: 10, max: 1000 }),
    body('improvement_suggestions').isLength({ min: 10, max: 1000 }),
    body('additional_comments').optional().isLength({ max: 1500 })
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

      console.log(`🔄 Submit 360-degree feedback ${req.params.assignmentId} by ${req.user.username}`);

      const { assignmentId } = req.params;
      const { 
        feedback_ratings, 
        strengths, 
        improvement_suggestions, 
        additional_comments 
      } = req.body;

      // Verify assignment exists and user can submit
      const assignmentCheck = await secureQuery(`
        SELECT 
          fa.id, fa.provider_id, fa.status,
          fr.subject_user_id, fr.anonymous,
          u.username as subject_username, u.display_name as subject_name
        FROM feedback_360_assignments fa
        JOIN feedback_360_requests fr ON fa.request_id = fr.id
        JOIN users u ON fr.subject_user_id = u.id
        WHERE fa.id = $1
      `, [assignmentId]);

      if (assignmentCheck.rows.length === 0) {
        return res.status(404).json({
          error: 'Feedback assignment not found',
          code: 'ASSIGNMENT_NOT_FOUND'
        });
      }

      const assignment = assignmentCheck.rows[0];

      // Check if user can submit this feedback
      if (req.user.id !== assignment.provider_id && req.user.role !== 'founder') {
        return res.status(403).json({
          error: 'Cannot submit feedback',
          message: 'You are not authorized to submit this feedback',
          code: 'FEEDBACK_SUBMIT_DENIED'
        });
      }

      if (assignment.status !== 'pending') {
        return res.status(409).json({
          error: 'Feedback already submitted',
          message: `Feedback is already ${assignment.status}`,
          code: 'FEEDBACK_ALREADY_SUBMITTED'
        });
      }

      // Calculate average rating
      const avgRating = feedback_ratings.reduce((sum, rating) => sum + rating.rating, 0) / feedback_ratings.length;

      // Submit feedback in transaction
      const submittedFeedback = await secureTransaction(async (client) => {
        // Update assignment
        const assignmentResult = await client.query(`
          UPDATE feedback_360_assignments 
          SET 
            strengths = $2,
            improvement_suggestions = $3,
            additional_comments = $4,
            avg_rating = $5,
            status = 'completed',
            submitted_at = NOW()
          WHERE id = $1
          RETURNING id, avg_rating, status, submitted_at
        `, [assignmentId, strengths, improvement_suggestions, additional_comments, avgRating]);

        // Insert individual ratings
        for (const rating of feedback_ratings) {
          await client.query(`
            INSERT INTO feedback_360_ratings (
              assignment_id, feedback_area, rating, comments, created_at
            ) VALUES ($1, $2, $3, $4, NOW())
          `, [assignmentId, rating.area, rating.rating, rating.comments]);
        }

        return assignmentResult.rows[0];
      });

      console.log(`🔄 360-degree feedback submitted for ${assignment.subject_username} (avg: ${avgRating.toFixed(1)}/5)`);

      if (req.user.role === 'founder') {
        console.log('👑🔄👑 LEGENDARY FOUNDER 360-FEEDBACK SUBMISSION WITH INFINITE INSIGHTS! 👑🔄👑');
      }

      res.json({
        success: true,
        data: {
          feedback: {
            ...submittedFeedback,
            subject_user: {
              username: assignment.subject_username,
              display_name: assignment.subject_name
            },
            ratings_count: feedback_ratings.length,
            is_anonymous: assignment.anonymous
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER 360-FEEDBACK: Comprehensive feedback for ${assignment.subject_name} submitted with infinite insights (${avgRating.toFixed(1)}/5)!` :
          `🔄 360-degree feedback for ${assignment.subject_name} submitted successfully! Average rating: ${avgRating.toFixed(1)}/5`
      });

    } catch (error) {
      console.error('❌ Submit 360-feedback error:', error);
      res.status(500).json({ 
        error: 'Failed to submit 360-feedback',
        message: 'An error occurred while submitting the 360-degree feedback',
        code: 'SUBMIT_360_FEEDBACK_ERROR'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'hr-performance',
    timestamp: new Date().toISOString(),
    message: '📈 Performance management service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    evening_energy: '🌃 PRIME EVENING LEGENDARY PERFORMANCE POWER AT 20:52:38! 🌃'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY PERFORMANCE MANAGEMENT SYSTEM COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Performance management system completed at: 2025-08-06 20:52:38 UTC`);
console.log('📈 Performance tracking: LEGENDARY PRECISION');
console.log('👑 RICKROLL187 founder performance controls: MAXIMUM AUTHORITY');
console.log('🔄 360-degree feedback: SWISS PRECISION');
console.log('🌃 PRIME EVENING LEGENDARY PERFORMANCE POWER: INFINITE AT 20:52:38!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
