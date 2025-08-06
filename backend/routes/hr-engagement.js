// File: backend/routes/hr-engagement.js
/**
 * 🏆🎸 N3EXTPATH - LEGENDARY EMPLOYEE ENGAGEMENT & ANALYTICS SYSTEM 🎸🏆
 * Swiss precision workforce engagement with infinite analytics energy
 * Built: 2025-08-06 21:14:14 UTC by RICKROLL187
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

console.log('🏆🎸🏆 LEGENDARY EMPLOYEE ENGAGEMENT & ANALYTICS SYSTEM LOADING! 🏆🎸🏆');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Employee engagement & analytics system loaded at: 2025-08-06 21:14:14 UTC`);
console.log('🌃 PRIME EVENING LEGENDARY ENGAGEMENT POWER AT 21:14:14!');

// =====================================
// 🛡️ ENGAGEMENT RATE LIMITING 🛡️
// =====================================

const engagementLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 300, // Higher limit for engagement activities
  message: {
    error: 'Too many engagement requests from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'ENGAGEMENT_RATE_LIMIT'
  }
});

router.use(engagementLimiter);
router.use(validatePayload(25600)); // 25KB max payload for surveys

// =====================================
// 📊 EMPLOYEE SATISFACTION SURVEYS 📊
// =====================================

// Create employee satisfaction survey
router.post('/surveys',
  authenticateToken,
  requirePermission('users.write'),
  [
    body('title').isLength({ min: 5, max: 200 }).trim(),
    body('description').isLength({ min: 10, max: 1000 }).trim(),
    body('survey_type').isIn(['satisfaction', 'engagement', 'culture', 'exit', 'pulse', 'onboarding', 'custom']).withMessage('Valid survey type required'),
    body('target_audience').isIn(['all_employees', 'department', 'role', 'specific_users', 'new_hires', 'remote_workers']).withMessage('Valid target audience required'),
    body('questions').isArray({ min: 1, max: 100 }),
    body('questions.*.question_text').isLength({ min: 5, max: 500 }),
    body('questions.*.question_type').isIn(['multiple_choice', 'scale_1_5', 'scale_1_10', 'yes_no', 'text_short', 'text_long']),
    body('questions.*.options').optional().isArray({ max: 10 }),
    body('questions.*.required').optional().isBoolean(),
    body('anonymous').optional().isBoolean(),
    body('start_date').isISO8601(),
    body('end_date').isISO8601(),
    body('reminder_frequency_days').optional().isInt({ min: 1, max: 30 }),
    body('target_departments').optional().isArray({ max: 20 }),
    body('target_roles').optional().isArray({ max: 50 }),
    body('target_user_ids').optional().isArray({ max: 1000 })
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

      console.log(`📊 Create employee survey by ${req.user.username} at 21:14:14 UTC`);

      const { 
        title, 
        description, 
        survey_type, 
        target_audience, 
        questions,
        anonymous = true,
        start_date,
        end_date,
        reminder_frequency_days = 7,
        target_departments = [],
        target_roles = [],
        target_user_ids = []
      } = req.body;

      // Validate date range
      if (new Date(start_date) >= new Date(end_date)) {
        return res.status(400).json({
          error: 'Invalid date range',
          message: 'Survey end date must be after start date',
          code: 'INVALID_DATE_RANGE'
        });
      }

      // Create survey in transaction
      const survey = await secureTransaction(async (client) => {
        // Create main survey
        const surveyResult = await client.query(`
          INSERT INTO employee_surveys (
            title, description, survey_type, target_audience, questions,
            anonymous, start_date, end_date, reminder_frequency_days,
            target_departments, target_roles, target_user_ids,
            status, created_by, created_at
          ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, 'draft', $13, NOW())
          RETURNING id, title, survey_type, anonymous, start_date, end_date, status, created_at
        `, [
          title, 
          description, 
          survey_type, 
          target_audience, 
          JSON.stringify(questions),
          anonymous,
          start_date,
          end_date,
          reminder_frequency_days,
          JSON.stringify(target_departments),
          JSON.stringify(target_roles),
          JSON.stringify(target_user_ids),
          req.user.id
        ]);

        const survey = surveyResult.rows[0];

        // Calculate target audience size
        let targetCount = 0;
        if (target_audience === 'all_employees') {
          const countResult = await client.query(`
            SELECT COUNT(*) as count FROM users WHERE status = 'active'
          `);
          targetCount = parseInt(countResult.rows[0].count);
        } else if (target_audience === 'specific_users' && target_user_ids.length > 0) {
          targetCount = target_user_ids.length;
        }
        // Add more target audience calculations as needed

        // Update survey with target count
        await client.query(`
          UPDATE employee_surveys SET target_count = $2 WHERE id = $1
        `, [survey.id, targetCount]);

        return { ...survey, target_count: targetCount };
      });

      console.log(`📊 Employee survey created: ${title} (${survey_type})`);

      if (req.user.role === 'founder') {
        console.log('👑📊👑 LEGENDARY FOUNDER SURVEY CREATION WITH INFINITE ENGAGEMENT INSIGHTS! 👑📊👑');
      }

      res.status(201).json({
        success: true,
        data: {
          survey: {
            ...survey,
            questions,
            target_departments,
            target_roles,
            questions_count: questions.length,
            creator: {
              id: req.user.id,
              username: req.user.username,
              display_name: req.user.display_name
            }
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER SURVEY: "${title}" created with infinite engagement wisdom!` :
          `📊 Employee survey "${title}" created successfully! Ready to gather valuable insights.`
      });

    } catch (error) {
      console.error('❌ Create employee survey error:', error);
      res.status(500).json({ 
        error: 'Failed to create employee survey',
        message: 'An error occurred while creating the employee survey',
        code: 'CREATE_SURVEY_ERROR'
      });
    }
  }
);

// Launch survey (make it active)
router.patch('/surveys/:surveyId/launch',
  authenticateToken,
  requirePermission('users.write'),
  [
    param('surveyId').isUUID().withMessage('Valid survey ID required')
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

      console.log(`🚀 Launch survey ${req.params.surveyId} by ${req.user.username}`);

      const { surveyId } = req.params;

      // Get survey details
      const surveyResult = await secureQuery(`
        SELECT 
          id, title, target_audience, target_user_ids, target_departments, 
          target_roles, start_date, end_date, status, target_count
        FROM employee_surveys 
        WHERE id = $1
      `, [surveyId]);

      if (surveyResult.rows.length === 0) {
        return res.status(404).json({
          error: 'Survey not found',
          code: 'SURVEY_NOT_FOUND'
        });
      }

      const survey = surveyResult.rows[0];

      if (survey.status !== 'draft') {
        return res.status(409).json({
          error: 'Survey already launched',
          message: `Survey is currently ${survey.status}`,
          code: 'SURVEY_ALREADY_LAUNCHED'
        });
      }

      // Check if survey is within date range
      const now = new Date();
      const startDate = new Date(survey.start_date);
      const endDate = new Date(survey.end_date);

      if (now < startDate) {
        return res.status(400).json({
          error: 'Survey not ready',
          message: 'Survey start date has not arrived yet',
          code: 'SURVEY_NOT_READY'
        });
      }

      if (now > endDate) {
        return res.status(400).json({
          error: 'Survey expired',
          message: 'Survey end date has already passed',
          code: 'SURVEY_EXPIRED'
        });
      }

      // Launch survey and create participant records
      const launchedSurvey = await secureTransaction(async (client) => {
        // Update survey status
        const updateResult = await client.query(`
          UPDATE employee_surveys 
          SET status = 'active', launched_at = NOW(), launched_by = $2
          WHERE id = $1
          RETURNING id, status, launched_at
        `, [surveyId, req.user.id]);

        // Create survey participants based on target audience
        let participantCount = 0;
        
        if (survey.target_audience === 'all_employees') {
          const usersResult = await client.query(`
            SELECT id FROM users WHERE status = 'active'
          `);
          
          for (const user of usersResult.rows) {
            await client.query(`
              INSERT INTO survey_participants (survey_id, user_id, status, created_at)
              VALUES ($1, $2, 'invited', NOW())
            `, [surveyId, user.id]);
            participantCount++;
          }
        } else if (survey.target_audience === 'specific_users') {
          const targetUsers = JSON.parse(survey.target_user_ids || '[]');
          for (const userId of targetUsers) {
            await client.query(`
              INSERT INTO survey_participants (survey_id, user_id, status, created_at)
              VALUES ($1, $2, 'invited', NOW())
              ON CONFLICT (survey_id, user_id) DO NOTHING
            `, [surveyId, userId]);
            participantCount++;
          }
        }

        // Update actual participant count
        await client.query(`
          UPDATE employee_surveys SET actual_participant_count = $2 WHERE id = $1
        `, [surveyId, participantCount]);

        return { ...updateResult.rows[0], participant_count: participantCount };
      });

      console.log(`🚀 Survey launched: ${survey.title} with ${launchedSurvey.participant_count} participants`);

      if (req.user.role === 'founder') {
        console.log('👑🚀👑 LEGENDARY FOUNDER SURVEY LAUNCH WITH INFINITE ENGAGEMENT REACH! 👑🚀👑');
      }

      res.json({
        success: true,
        data: {
          survey: {
            ...launchedSurvey,
            title: survey.title,
            target_audience: survey.target_audience
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER SURVEY LAUNCH: "${survey.title}" launched with infinite engagement power to ${launchedSurvey.participant_count} participants!` :
          `🚀 Survey "${survey.title}" launched successfully! Sent to ${launchedSurvey.participant_count} participants.`
      });

    } catch (error) {
      console.error('❌ Launch survey error:', error);
      res.status(500).json({ 
        error: 'Failed to launch survey',
        message: 'An error occurred while launching the survey',
        code: 'LAUNCH_SURVEY_ERROR'
      });
    }
  }
);

// Submit survey response
router.post('/surveys/:surveyId/respond',
  authenticateToken,
  [
    param('surveyId').isUUID().withMessage('Valid survey ID required'),
    body('responses').isArray({ min: 1 }),
    body('responses.*.question_index').isInt({ min: 0 }),
    body('responses.*.answer').notEmpty(),
    body('responses.*.rating').optional().isInt({ min: 1, max: 10 }),
    body('additional_comments').optional().isLength({ max: 2000 }).trim()
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

      console.log(`📝 Submit survey response ${req.params.surveyId} by ${req.user.username}`);

      const { surveyId } = req.params;
      const { responses, additional_comments } = req.body;

      // Get survey details and check participation
      const surveyCheck = await secureQuery(`
        SELECT 
          s.id, s.title, s.anonymous, s.status, s.end_date,
          sp.id as participant_id, sp.status as participant_status
        FROM employee_surveys s
        LEFT JOIN survey_participants sp ON s.id = sp.survey_id AND sp.user_id = $2
        WHERE s.id = $1
      `, [surveyId, req.user.id]);

      if (surveyCheck.rows.length === 0) {
        return res.status(404).json({
          error: 'Survey not found or not invited',
          code: 'SURVEY_ACCESS_DENIED'
        });
      }

      const survey = surveyCheck.rows[0];

      if (survey.status !== 'active') {
        return res.status(400).json({
          error: 'Survey not active',
          message: `Survey is currently ${survey.status}`,
          code: 'SURVEY_NOT_ACTIVE'
        });
      }

      if (new Date() > new Date(survey.end_date)) {
        return res.status(400).json({
          error: 'Survey expired',
          message: 'Survey has already ended',
          code: 'SURVEY_EXPIRED'
        });
      }

      if (survey.participant_status === 'completed') {
        return res.status(409).json({
          error: 'Already responded',
          message: 'You have already completed this survey',
          code: 'SURVEY_ALREADY_COMPLETED'
        });
      }

      // Submit survey response
      const surveyResponse = await secureTransaction(async (client) => {
        // Create survey response
        const responseResult = await client.query(`
          INSERT INTO survey_responses (
            survey_id, participant_id, user_id, responses, additional_comments,
            is_anonymous, submitted_at, created_at
          ) VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
          RETURNING id, submitted_at
        `, [
          surveyId, 
          survey.participant_id, 
          survey.anonymous ? null : req.user.id, 
          JSON.stringify(responses),
          additional_comments,
          survey.anonymous
        ]);

        // Update participant status
        await client.query(`
          UPDATE survey_participants 
          SET status = 'completed', completed_at = NOW()
          WHERE id = $1
        `, [survey.participant_id]);

        return responseResult.rows[0];
      });

      console.log(`📝 Survey response submitted: ${survey.title} by ${req.user.username}`);

      if (req.user.role === 'founder') {
        console.log('👑📝👑 LEGENDARY FOUNDER SURVEY RESPONSE WITH INFINITE ENGAGEMENT! 👑📝👑');
      }

      res.json({
        success: true,
        data: {
          response: {
            ...surveyResponse,
            survey_title: survey.title,
            is_anonymous: survey.anonymous,
            responses_count: responses.length
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER SURVEY RESPONSE: "${survey.title}" completed with infinite engagement wisdom!` :
          `📝 Survey "${survey.title}" completed successfully! Thank you for your valuable feedback.`
      });

    } catch (error) {
      console.error('❌ Submit survey response error:', error);
      res.status(500).json({ 
        error: 'Failed to submit survey response',
        message: 'An error occurred while submitting your survey response',
        code: 'SUBMIT_SURVEY_RESPONSE_ERROR'
      });
    }
  }
);

// =====================================
// 🏆 EMPLOYEE RECOGNITION SYSTEM 🏆
// =====================================

// Give recognition to employee
router.post('/recognition',
  authenticateToken,
  [
    body('recipient_id').isUUID().withMessage('Valid recipient ID required'),
    body('recognition_type').isIn(['peer_appreciation', 'achievement', 'milestone', 'innovation', 'teamwork', 'leadership', 'customer_service', 'going_above_beyond']).withMessage('Valid recognition type required'),
    body('title').isLength({ min: 5, max: 200 }).trim(),
    body('message').isLength({ min: 10, max: 1000 }).trim(),
    body('points_awarded').optional().isInt({ min: 1, max: 1000 }),
    body('public').optional().isBoolean(),
    body('categories').optional().isArray({ max: 10 }),
    body('associated_project_id').optional().isUUID()
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

      console.log(`🏆 Give recognition by ${req.user.username} at 21:14:14 UTC`);

      const { 
        recipient_id, 
        recognition_type, 
        title, 
        message, 
        points_awarded = 10,
        public = true,
        categories = [],
        associated_project_id
      } = req.body;

      // Verify recipient exists
      const recipientCheck = await secureQuery(`
        SELECT id, username, display_name FROM users WHERE id = $1 AND status = 'active'
      `, [recipient_id]);

      if (recipientCheck.rows.length === 0) {
        return res.status(404).json({
          error: 'Recipient not found',
          code: 'RECIPIENT_NOT_FOUND'
        });
      }

      const recipient = recipientCheck.rows[0];

      // Can't recognize yourself
      if (recipient_id === req.user.id) {
        return res.status(400).json({
          error: 'Cannot recognize yourself',
          message: 'You cannot give recognition to yourself',
          code: 'SELF_RECOGNITION_DENIED'
        });
      }

      // Create recognition in transaction
      const recognition = await secureTransaction(async (client) => {
        // Create recognition record
        const recognitionResult = await client.query(`
          INSERT INTO employee_recognition (
            giver_id, recipient_id, recognition_type, title, message,
            points_awarded, public, categories, associated_project_id,
            status, created_at
          ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'active', NOW())
          RETURNING id, recognition_type, title, points_awarded, public, created_at
        `, [
          req.user.id, 
          recipient_id, 
          recognition_type, 
          title, 
          message,
          points_awarded,
          public,
          JSON.stringify(categories),
          associated_project_id
        ]);

        const recognition = recognitionResult.rows[0];

        // Update recipient's recognition points
        await client.query(`
          INSERT INTO user_recognition_points (user_id, points, created_at)
          VALUES ($1, $2, NOW())
          ON CONFLICT (user_id) DO UPDATE SET
            points = user_recognition_points.points + EXCLUDED.points,
            updated_at = NOW()
        `, [recipient_id, points_awarded]);

        // Update giver's recognition given count
        await client.query(`
          INSERT INTO user_recognition_stats (user_id, recognitions_given, created_at)
          VALUES ($1, 1, NOW())
          ON CONFLICT (user_id) DO UPDATE SET
            recognitions_given = user_recognition_stats.recognitions_given + 1,
            updated_at = NOW()
        `, [req.user.id]);

        return recognition;
      });

      console.log(`🏆 Recognition given: ${req.user.username} -> ${recipient.username} (${points_awarded} points)`);

      if (req.user.role === 'founder') {
        console.log('👑🏆👑 LEGENDARY FOUNDER RECOGNITION WITH INFINITE APPRECIATION! 👑🏆👑');
      }

      res.status(201).json({
        success: true,
        data: {
          recognition: {
            ...recognition,
            giver: {
              id: req.user.id,
              username: req.user.username,
              display_name: req.user.display_name
            },
            recipient: {
              id: recipient.id,
              username: recipient.username,
              display_name: recipient.display_name
            },
            categories
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER RECOGNITION: "${title}" given to ${recipient.display_name} with infinite appreciation and ${points_awarded} points!` :
          `🏆 Recognition "${title}" given to ${recipient.display_name} successfully! ${points_awarded} points awarded.`
      });

    } catch (error) {
      console.error('❌ Give recognition error:', error);
      res.status(500).json({ 
        error: 'Failed to give recognition',
        message: 'An error occurred while giving recognition',
        code: 'GIVE_RECOGNITION_ERROR'
      });
    }
  }
);

// Get recognition feed
router.get('/recognition/feed',
  authenticateToken,
  [
    query('type').optional().isIn(['all', 'given', 'received', 'public']),
    query('recognition_type').optional().isIn(['peer_appreciation', 'achievement', 'milestone', 'innovation', 'teamwork', 'leadership', 'customer_service', 'going_above_beyond']),
    query('page').optional().isInt({ min: 1 }).toInt(),
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt()
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

      console.log(`🏆 Get recognition feed by ${req.user.username}`);

      const {
        type = 'all',
        recognition_type,
        page = 1,
        limit = 20
      } = req.query;

      const offset = (page - 1) * limit;

      // Build WHERE conditions
      let whereConditions = ["er.status = 'active'"];
      let queryParams = [];
      let paramCount = 0;

      if (type === 'given') {
        paramCount++;
        whereConditions.push(`er.giver_id = $${paramCount}`);
        queryParams.push(req.user.id);
      } else if (type === 'received') {
        paramCount++;
        whereConditions.push(`er.recipient_id = $${paramCount}`);
        queryParams.push(req.user.id);
      } else if (type === 'public') {
        whereConditions.push("er.public = true");
      } else if (type === 'all') {
        // Show public recognitions and any involving the user
        paramCount++;
        paramCount++;
        whereConditions.push(`(er.public = true OR er.giver_id = $${paramCount - 1} OR er.recipient_id = $${paramCount})`);
        queryParams.push(req.user.id, req.user.id);
      }

      if (recognition_type) {
        paramCount++;
        whereConditions.push(`er.recognition_type = $${paramCount}`);
        queryParams.push(recognition_type);
      }

      const whereClause = whereConditions.join(' AND ');

      // Get recognition feed
      const recognitionResult = await secureQuery(`
        SELECT 
          er.id, er.recognition_type, er.title, er.message, er.points_awarded,
          er.public, er.categories, er.created_at,
          g.username as giver_username, g.display_name as giver_name, g.is_legendary as giver_legendary,
          r.username as recipient_username, r.display_name as recipient_name, r.is_legendary as recipient_legendary,
          COUNT(erl.id) as likes_count,
          COUNT(CASE WHEN erl.user_id = $${paramCount + 1} THEN 1 END) as user_liked
        FROM employee_recognition er
        JOIN users g ON er.giver_id = g.id
        JOIN users r ON er.recipient_id = r.id
        LEFT JOIN employee_recognition_likes erl ON er.id = erl.recognition_id
        WHERE ${whereClause}
        GROUP BY er.id, er.recognition_type, er.title, er.message, er.points_awarded,
                 er.public, er.categories, er.created_at,
                 g.username, g.display_name, g.is_legendary,
                 r.username, r.display_name, r.is_legendary
        ORDER BY er.created_at DESC
        LIMIT $${paramCount + 2} OFFSET $${paramCount + 3}
      `, [...queryParams, req.user.id, limit, offset]);

      // Get total count
      const countResult = await secureQuery(`
        SELECT COUNT(*) as total
        FROM employee_recognition er
        JOIN users g ON er.giver_id = g.id
        JOIN users r ON er.recipient_id = r.id
        WHERE ${whereClause}
      `, queryParams);

      const total = parseInt(countResult.rows[0].total);
      const recognitions = recognitionResult.rows.map(rec => ({
        id: rec.id,
        recognition_type: rec.recognition_type,
        title: rec.title,
        message: rec.message,
        points_awarded: rec.points_awarded,
        public: rec.public,
        categories: JSON.parse(rec.categories || '[]'),
        created_at: rec.created_at,
        giver: {
          username: rec.giver_username,
          display_name: rec.giver_name,
          is_legendary: rec.giver_legendary
        },
        recipient: {
          username: rec.recipient_username,
          display_name: rec.recipient_name,
          is_legendary: rec.recipient_legendary
        },
        likes_count: parseInt(rec.likes_count) || 0,
        user_liked: parseInt(rec.user_liked) > 0
      }));

      console.log(`🏆 Retrieved ${recognitions.length} recognitions (total: ${total})`);

      if (req.user.role === 'founder') {
        console.log('👑🏆👑 LEGENDARY FOUNDER RECOGNITION FEED WITH INFINITE APPRECIATION INSIGHTS! 👑🏆👑');
      }

      res.json({
        success: true,
        data: {
          recognitions,
          pagination: {
            current_page: page,
            per_page: limit,
            total_pages: Math.ceil(total / limit),
            total_count: total,
            has_next: (page * limit) < total,
            has_prev: page > 1
          },
          filters: { type, recognition_type }
        },
        message: req.user.role === 'founder' ? 
          `👑 ${total} recognitions retrieved with LEGENDARY FOUNDER appreciation insights!` :
          `🏆 ${total} recognitions loaded! Celebrating our amazing team achievements!`
      });

    } catch (error) {
      console.error('❌ Get recognition feed error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch recognition feed',
        message: 'An error occurred while retrieving recognitions',
        code: 'GET_RECOGNITION_ERROR'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'hr-engagement',
    timestamp: new Date().toISOString(),
    message: '🏆 Employee engagement service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    evening_energy: '🌃 PRIME EVENING LEGENDARY ENGAGEMENT POWER AT 21:14:14! 🌃'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY EMPLOYEE ENGAGEMENT & ANALYTICS SYSTEM COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Employee engagement & analytics system completed at: 2025-08-06 21:14:14 UTC`);
console.log('🏆 Employee engagement: LEGENDARY PRECISION');
console.log('👑 RICKROLL187 founder engagement controls: MAXIMUM AUTHORITY');
console.log('📊 Recognition system: SWISS PRECISION');
console.log('🌃 PRIME EVENING LEGENDARY ENGAGEMENT POWER: INFINITE AT 21:14:14!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
