// File: backend/routes/hr-learning.js
/**
 * 🎓🎸 N3EXTPATH - LEGENDARY LEARNING & DEVELOPMENT SYSTEM 🎸🎓
 * Swiss precision workforce development with infinite learning energy
 * Built: 2025-08-06 20:56:56 UTC by RICKROLL187
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

console.log('🎓🎸🎓 LEGENDARY LEARNING & DEVELOPMENT SYSTEM LOADING! 🎓🎸🎓');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Learning & development system loaded at: 2025-08-06 20:56:56 UTC`);
console.log('🌃 PRIME EVENING LEGENDARY LEARNING POWER AT 20:56:56!');

// =====================================
// 🛡️ LEARNING RATE LIMITING 🛡️
// =====================================

const learningLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 200, // Higher limit for learning activities
  message: {
    error: 'Too many learning requests from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'LEARNING_RATE_LIMIT'
  }
});

router.use(learningLimiter);
router.use(validatePayload(20480)); // 20KB max payload for course content

// =====================================
// 📚 LEARNING COURSE MANAGEMENT 📚
// =====================================

// Create learning course
router.post('/courses',
  authenticateToken,
  requirePermission('users.write'),
  [
    body('title').isLength({ min: 3, max: 200 }).trim(),
    body('description').isLength({ min: 10, max: 2000 }).trim(),
    body('category').isIn(['technical', 'leadership', 'communication', 'compliance', 'safety', 'product', 'process', 'soft_skills', 'industry_specific']),
    body('difficulty_level').isIn(['beginner', 'intermediate', 'advanced', 'expert']),
    body('estimated_duration_minutes').isInt({ min: 5, max: 10080 }), // 5 minutes to 1 week
    body('learning_objectives').isArray({ min: 1, max: 10 }),
    body('learning_objectives.*').isLength({ min: 10, max: 200 }),
    body('prerequisites').optional().isArray({ max: 10 }),
    body('tags').optional().isArray({ max: 20 }),
    body('is_mandatory').optional().isBoolean(),
    body('expiration_months').optional().isInt({ min: 1, max: 60 }),
    body('course_materials').optional().isArray({ max: 50 })
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

      console.log(`📚 Create learning course by ${req.user.username} at 20:56:56 UTC`);

      const { 
        title, 
        description, 
        category, 
        difficulty_level, 
        estimated_duration_minutes,
        learning_objectives,
        prerequisites = [],
        tags = [],
        is_mandatory = false,
        expiration_months,
        course_materials = []
      } = req.body;

      // Create course in transaction
      const course = await secureTransaction(async (client) => {
        // Create main course
        const courseResult = await client.query(`
          INSERT INTO learning_courses (
            title, description, category, difficulty_level, estimated_duration_minutes,
            learning_objectives, prerequisites, tags, is_mandatory, expiration_months,
            created_by, status, created_at
          ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, 'active', NOW())
          RETURNING id, title, category, difficulty_level, estimated_duration_minutes, 
                    is_mandatory, status, created_at
        `, [
          title, 
          description, 
          category, 
          difficulty_level, 
          estimated_duration_minutes,
          JSON.stringify(learning_objectives),
          JSON.stringify(prerequisites),
          JSON.stringify(tags),
          is_mandatory,
          expiration_months,
          req.user.id
        ]);

        const course = courseResult.rows[0];

        // Create course materials if provided
        for (let i = 0; i < course_materials.length; i++) {
          const material = course_materials[i];
          await client.query(`
            INSERT INTO course_materials (
              course_id, title, type, content_url, content_text, sort_order, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, NOW())
          `, [
            course.id,
            material.title,
            material.type || 'text',
            material.content_url,
            material.content_text,
            i + 1
          ]);
        }

        return course;
      });

      console.log(`📚 Learning course created: ${title} (${difficulty_level})`);

      if (req.user.role === 'founder') {
        console.log('👑📚👑 LEGENDARY FOUNDER COURSE CREATION WITH INFINITE KNOWLEDGE! 👑📚👑');
      }

      res.status(201).json({
        success: true,
        data: {
          course: {
            ...course,
            learning_objectives,
            prerequisites,
            tags,
            materials_count: course_materials.length,
            creator: {
              id: req.user.id,
              username: req.user.username,
              display_name: req.user.display_name
            }
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER COURSE: "${title}" created with infinite knowledge standards!` :
          `📚 Learning course "${title}" created successfully! Ready to empower our team!`
      });

    } catch (error) {
      console.error('❌ Create learning course error:', error);
      res.status(500).json({ 
        error: 'Failed to create learning course',
        message: 'An error occurred while creating the learning course',
        code: 'CREATE_COURSE_ERROR'
      });
    }
  }
);

// Get learning courses (with filtering)
router.get('/courses',
  authenticateToken,
  [
    query('category').optional().isIn(['technical', 'leadership', 'communication', 'compliance', 'safety', 'product', 'process', 'soft_skills', 'industry_specific']),
    query('difficulty_level').optional().isIn(['beginner', 'intermediate', 'advanced', 'expert']),
    query('mandatory_only').optional().isBoolean(),
    query('my_courses_only').optional().isBoolean(),
    query('completed_only').optional().isBoolean(),
    query('search').optional().isLength({ min: 2, max: 100 }).trim(),
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

      console.log(`📚 Get learning courses by ${req.user.username}`);

      const {
        category,
        difficulty_level,
        mandatory_only = false,
        my_courses_only = false,
        completed_only = false,
        search,
        page = 1,
        limit = 20
      } = req.query;

      const offset = (page - 1) * limit;

      // Build WHERE conditions
      let whereConditions = ["lc.status = 'active'"];
      let queryParams = [];
      let paramCount = 0;

      if (category) {
        paramCount++;
        whereConditions.push(`lc.category = $${paramCount}`);
        queryParams.push(category);
      }

      if (difficulty_level) {
        paramCount++;
        whereConditions.push(`lc.difficulty_level = $${paramCount}`);
        queryParams.push(difficulty_level);
      }

      if (mandatory_only) {
        whereConditions.push("lc.is_mandatory = true");
      }

      if (search) {
        paramCount++;
        whereConditions.push(`(lc.title ILIKE $${paramCount} OR lc.description ILIKE $${paramCount})`);
        queryParams.push(`%${search}%`);
      }

      // Add user-specific filters if requested
      let joinClause = '';
      let selectFields = `
        lc.id, lc.title, lc.description, lc.category, lc.difficulty_level,
        lc.estimated_duration_minutes, lc.learning_objectives, lc.prerequisites,
        lc.tags, lc.is_mandatory, lc.expiration_months, lc.created_at,
        u.username as creator_username, u.display_name as creator_name
      `;

      if (my_courses_only || completed_only) {
        joinClause = `LEFT JOIN course_enrollments ce ON lc.id = ce.course_id AND ce.user_id = $${paramCount + 1}`;
        paramCount++;
        queryParams.push(req.user.id);

        selectFields += `, ce.status as enrollment_status, ce.progress, ce.completed_at, ce.enrolled_at`;

        if (my_courses_only) {
          whereConditions.push('ce.user_id IS NOT NULL');
        }

        if (completed_only) {
          whereConditions.push("ce.status = 'completed'");
        }
      }

      const whereClause = whereConditions.join(' AND ');

      // Get courses
      const coursesResult = await secureQuery(`
        SELECT ${selectFields},
               COUNT(ce_all.id) as total_enrollments,
               COUNT(CASE WHEN ce_all.status = 'completed' THEN 1 END) as completed_enrollments,
               AVG(CASE WHEN ce_all.status = 'completed' THEN ce_all.progress END) as avg_completion_rate
        FROM learning_courses lc
        JOIN users u ON lc.created_by = u.id
        ${joinClause}
        LEFT JOIN course_enrollments ce_all ON lc.id = ce_all.course_id
        WHERE ${whereClause}
        GROUP BY lc.id, lc.title, lc.description, lc.category, lc.difficulty_level,
                 lc.estimated_duration_minutes, lc.learning_objectives, lc.prerequisites,
                 lc.tags, lc.is_mandatory, lc.expiration_months, lc.created_at,
                 u.username, u.display_name, ce.status, ce.progress, ce.completed_at, ce.enrolled_at
        ORDER BY 
          CASE WHEN lc.is_mandatory THEN 0 ELSE 1 END,
          lc.created_at DESC
        LIMIT $${paramCount + 1} OFFSET $${paramCount + 2}
      `, [...queryParams, limit, offset]);

      // Get total count
      const countResult = await secureQuery(`
        SELECT COUNT(DISTINCT lc.id) as total
        FROM learning_courses lc
        JOIN users u ON lc.created_by = u.id
        ${joinClause}
        WHERE ${whereClause}
      `, queryParams);

      const total = parseInt(countResult.rows[0].total);
      const courses = coursesResult.rows.map(course => ({
        id: course.id,
        title: course.title,
        description: course.description,
        category: course.category,
        difficulty_level: course.difficulty_level,
        estimated_duration_minutes: course.estimated_duration_minutes,
        learning_objectives: JSON.parse(course.learning_objectives || '[]'),
        prerequisites: JSON.parse(course.prerequisites || '[]'),
        tags: JSON.parse(course.tags || '[]'),
        is_mandatory: course.is_mandatory,
        expiration_months: course.expiration_months,
        created_at: course.created_at,
        creator: {
          username: course.creator_username,
          display_name: course.creator_name
        },
        enrollment_status: course.enrollment_status || null,
        progress: course.progress || 0,
        completed_at: course.completed_at || null,
        enrolled_at: course.enrolled_at || null,
        stats: {
          total_enrollments: parseInt(course.total_enrollments) || 0,
          completed_enrollments: parseInt(course.completed_enrollments) || 0,
          avg_completion_rate: parseFloat(course.avg_completion_rate) || 0
        }
      }));

      console.log(`📚 Retrieved ${courses.length} learning courses (total: ${total})`);

      if (req.user.role === 'founder') {
        console.log('👑📚👑 LEGENDARY FOUNDER COURSES ACCESS WITH INFINITE KNOWLEDGE! 👑📚👑');
      }

      res.json({
        success: true,
        data: {
          courses,
          pagination: {
            current_page: page,
            per_page: limit,
            total_pages: Math.ceil(total / limit),
            total_count: total,
            has_next: (page * limit) < total,
            has_prev: page > 1
          },
          filters: { category, difficulty_level, mandatory_only, my_courses_only, completed_only, search }
        },
        message: req.user.role === 'founder' ? 
          `👑 ${total} learning courses retrieved with LEGENDARY FOUNDER knowledge insights!` :
          `📚 ${total} learning courses retrieved with Swiss precision!`
      });

    } catch (error) {
      console.error('❌ Get learning courses error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch learning courses',
        message: 'An error occurred while retrieving learning courses',
        code: 'GET_COURSES_ERROR'
      });
    }
  }
);

// =====================================
// 🎯 COURSE ENROLLMENT & PROGRESS 🎯
// =====================================

// Enroll in course
router.post('/courses/:courseId/enroll',
  authenticateToken,
  [
    param('courseId').isUUID().withMessage('Valid course ID required'),
    body('enrollment_reason').optional().isLength({ max: 500 }).trim(),
    body('target_completion_date').optional().isISO8601()
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

      console.log(`🎯 Course enrollment ${req.params.courseId} by ${req.user.username} at 20:56:56 UTC`);

      const { courseId } = req.params;
      const { enrollment_reason, target_completion_date } = req.body;

      // Get course details
      const courseResult = await secureQuery(`
        SELECT 
          id, title, description, category, difficulty_level,
          estimated_duration_minutes, prerequisites, is_mandatory, status
        FROM learning_courses 
        WHERE id = $1
      `, [courseId]);

      if (courseResult.rows.length === 0) {
        return res.status(404).json({
          error: 'Course not found',
          code: 'COURSE_NOT_FOUND'
        });
      }

      const course = courseResult.rows[0];

      if (course.status !== 'active') {
        return res.status(400).json({
          error: 'Course not available',
          message: `Course is currently ${course.status}`,
          code: 'COURSE_NOT_AVAILABLE'
        });
      }

      // Check if already enrolled
      const existingEnrollment = await secureQuery(`
        SELECT id, status FROM course_enrollments 
        WHERE course_id = $1 AND user_id = $2
      `, [courseId, req.user.id]);

      if (existingEnrollment.rows.length > 0) {
        const enrollment = existingEnrollment.rows[0];
        return res.status(409).json({
          error: 'Already enrolled',
          message: `You are already enrolled in this course (status: ${enrollment.status})`,
          code: 'ALREADY_ENROLLED',
          current_status: enrollment.status
        });
      }

      // Check prerequisites if any
      const prerequisites = JSON.parse(course.prerequisites || '[]');
      if (prerequisites.length > 0) {
        const prerequisiteCheck = await secureQuery(`
          SELECT course_id FROM course_enrollments 
          WHERE user_id = $1 AND course_id = ANY($2) AND status = 'completed'
        `, [req.user.id, prerequisites]);

        const completedPrereqs = prerequisiteCheck.rows.map(row => row.course_id);
        const missingPrereqs = prerequisites.filter(prereq => !completedPrereqs.includes(prereq));

        if (missingPrereqs.length > 0) {
          return res.status(400).json({
            error: 'Prerequisites not met',
            message: 'You must complete prerequisite courses before enrolling',
            code: 'PREREQUISITES_NOT_MET',
            missing_prerequisites: missingPrereqs
          });
        }
      }

      // Calculate suggested completion date if not provided
      let completionDate = target_completion_date;
      if (!completionDate) {
        const estimatedDays = Math.ceil(course.estimated_duration_minutes / (60 * 8)); // 8 hours per day
        const suggestedDate = new Date();
        suggestedDate.setDate(suggestedDate.getDate() + estimatedDays + 7); // Add 1 week buffer
        completionDate = suggestedDate.toISOString();
      }

      // Create enrollment
      const enrollment = await secureQuery(`
        INSERT INTO course_enrollments (
          course_id, user_id, enrollment_reason, target_completion_date,
          status, progress, enrolled_at, created_at
        ) VALUES ($1, $2, $3, $4, 'enrolled', 0, NOW(), NOW())
        RETURNING id, status, progress, enrolled_at, target_completion_date
      `, [courseId, req.user.id, enrollment_reason, completionDate]);

      console.log(`🎯 Course enrolled: ${req.user.username} -> ${course.title}`);

      if (req.user.role === 'founder') {
        console.log('👑🎯👑 LEGENDARY FOUNDER COURSE ENROLLMENT WITH INFINITE LEARNING! 👑🎯👑');
      }

      res.status(201).json({
        success: true,
        data: {
          enrollment: {
            ...enrollment.rows[0],
            course: {
              id: course.id,
              title: course.title,
              category: course.category,
              difficulty_level: course.difficulty_level,
              estimated_duration_minutes: course.estimated_duration_minutes
            },
            user: {
              id: req.user.id,
              username: req.user.username,
              display_name: req.user.display_name
            }
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ENROLLMENT: Course "${course.title}" enrolled with infinite learning commitment!` :
          `🎯 Successfully enrolled in "${course.title}"! Ready to expand your skills!`
      });

    } catch (error) {
      console.error('❌ Course enrollment error:', error);
      res.status(500).json({ 
        error: 'Failed to enroll in course',
        message: 'An error occurred while enrolling in the course',
        code: 'COURSE_ENROLLMENT_ERROR'
      });
    }
  }
);

// Update course progress
router.patch('/courses/:courseId/progress',
  authenticateToken,
  [
    param('courseId').isUUID().withMessage('Valid course ID required'),
    body('progress').isInt({ min: 0, max: 100 }).withMessage('Progress must be between 0 and 100'),
    body('completed_materials').optional().isArray(),
    body('notes').optional().isLength({ max: 1000 }).trim(),
    body('time_spent_minutes').optional().isInt({ min: 1, max: 10080 })
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

      console.log(`📈 Update course progress ${req.params.courseId} by ${req.user.username}`);

      const { courseId } = req.params;
      const { progress, completed_materials = [], notes, time_spent_minutes } = req.body;

      // Get enrollment details
      const enrollmentResult = await secureQuery(`
        SELECT 
          ce.id, ce.status, ce.progress as current_progress, ce.enrolled_at,
          lc.title, lc.estimated_duration_minutes
        FROM course_enrollments ce
        JOIN learning_courses lc ON ce.course_id = lc.id
        WHERE ce.course_id = $1 AND ce.user_id = $2
      `, [courseId, req.user.id]);

      if (enrollmentResult.rows.length === 0) {
        return res.status(404).json({
          error: 'Enrollment not found',
          message: 'You are not enrolled in this course',
          code: 'ENROLLMENT_NOT_FOUND'
        });
      }

      const enrollment = enrollmentResult.rows[0];

      if (enrollment.status === 'completed') {
        return res.status(409).json({
          error: 'Course already completed',
          message: 'This course has already been completed',
          code: 'COURSE_ALREADY_COMPLETED'
        });
      }

      // Determine new status based on progress
      let newStatus = enrollment.status;
      if (progress === 100 && enrollment.status !== 'completed') {
        newStatus = 'completed';
      } else if (progress > 0 && enrollment.status === 'enrolled') {
        newStatus = 'in_progress';
      }

      // Update enrollment in transaction
      const updatedEnrollment = await secureTransaction(async (client) => {
        // Update main enrollment
        const updateFields = ['progress = $3', 'updated_at = NOW()'];
        const updateParams = [enrollment.id, req.user.id, progress];
        let paramCount = 3;

        if (newStatus !== enrollment.status) {
          paramCount++;
          updateFields.push(`status = $${paramCount}`);
          updateParams.push(newStatus);

          if (newStatus === 'completed') {
            paramCount++;
            updateFields.push(`completed_at = NOW()`);
          }
        }

        if (notes) {
          paramCount++;
          updateFields.push(`notes = $${paramCount}`);
          updateParams.push(notes);
        }

        const enrollmentResult = await client.query(`
          UPDATE course_enrollments 
          SET ${updateFields.join(', ')}
          WHERE id = $1 AND user_id = $2
          RETURNING id, status, progress, completed_at, notes, updated_at
        `, updateParams);

        // Log progress entry
        await client.query(`
          INSERT INTO course_progress_logs (
            enrollment_id, progress, time_spent_minutes, completed_materials, notes, created_at
          ) VALUES ($1, $2, $3, $4, $5, NOW())
        `, [
          enrollment.id, 
          progress, 
          time_spent_minutes || 0, 
          JSON.stringify(completed_materials), 
          notes
        ]);

        return enrollmentResult.rows[0];
      });

      console.log(`📈 Course progress updated: ${enrollment.title} -> ${progress}% (${newStatus})`);

      if (progress === 100) {
        console.log(`🎉 COURSE COMPLETED: ${enrollment.title} by ${req.user.username}`);
        
        if (req.user.role === 'founder') {
          console.log('👑🎉👑 LEGENDARY FOUNDER COURSE COMPLETION WITH INFINITE KNOWLEDGE! 👑🎉👑');
        }
      }

      res.json({
        success: true,
        data: {
          enrollment: {
            ...updatedEnrollment,
            course: {
              title: enrollment.title,
              estimated_duration_minutes: enrollment.estimated_duration_minutes
            }
          }
        },
        message: progress === 100 ? 
          (req.user.role === 'founder' ? 
            `👑 LEGENDARY FOUNDER ACHIEVEMENT: Course "${enrollment.title}" completed with infinite mastery!` :
            `🎉 Congratulations! Course "${enrollment.title}" completed successfully!`
          ) :
          `📈 Course progress updated to ${progress}% for "${enrollment.title}"`
      });

    } catch (error) {
      console.error('❌ Update course progress error:', error);
      res.status(500).json({ 
        error: 'Failed to update course progress',
        message: 'An error occurred while updating course progress',
        code: 'UPDATE_PROGRESS_ERROR'
      });
    }
  }
);

// =====================================
// 🎯 SKILL ASSESSMENT & TRACKING 🎯
// =====================================

// Create skill assessment
router.post('/skills/assessments',
  authenticateToken,
  requirePermission('users.write'),
  [
    body('name').isLength({ min: 3, max: 200 }).trim(),
    body('description').isLength({ min: 10, max: 1000 }).trim(),
    body('skill_areas').isArray({ min: 1, max: 20 }),
    body('skill_areas.*.name').isLength({ min: 2, max: 100 }),
    body('skill_areas.*.category').isIn(['technical', 'leadership', 'communication', 'analytical', 'creative', 'interpersonal']),
    body('skill_areas.*.questions').isArray({ min: 1, max: 20 }),
    body('target_roles').optional().isArray({ max: 10 }),
    body('passing_score').optional().isInt({ min: 1, max: 100 }),
    body('time_limit_minutes').optional().isInt({ min: 5, max: 480 })
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

      console.log(`🎯 Create skill assessment by ${req.user.username} at 20:56:56 UTC`);

      const { 
        name, 
        description, 
        skill_areas, 
        target_roles = [], 
        passing_score = 70,
        time_limit_minutes = 60
      } = req.body;

      // Create skill assessment in transaction
      const assessment = await secureTransaction(async (client) => {
        // Create main assessment
        const assessmentResult = await client.query(`
          INSERT INTO skill_assessments (
            name, description, skill_areas, target_roles, passing_score,
            time_limit_minutes, created_by, status, created_at
          ) VALUES ($1, $2, $3, $4, $5, $6, $7, 'active', NOW())
          RETURNING id, name, passing_score, time_limit_minutes, status, created_at
        `, [
          name, 
          description, 
          JSON.stringify(skill_areas), 
          JSON.stringify(target_roles), 
          passing_score,
          time_limit_minutes,
          req.user.id
        ]);

        return assessmentResult.rows[0];
      });

      console.log(`🎯 Skill assessment created: ${name}`);

      if (req.user.role === 'founder') {
        console.log('👑🎯👑 LEGENDARY FOUNDER SKILL ASSESSMENT CREATION! 👑🎯👑');
      }

      res.status(201).json({
        success: true,
        data: {
          assessment: {
            ...assessment,
            skill_areas,
            target_roles,
            creator: {
              id: req.user.id,
              username: req.user.username,
              display_name: req.user.display_name
            },
            total_skill_areas: skill_areas.length,
            total_questions: skill_areas.reduce((sum, area) => sum + area.questions.length, 0)
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ASSESSMENT: "${name}" created with infinite evaluation standards!` :
          `🎯 Skill assessment "${name}" created successfully! Ready to evaluate team skills!`
      });

    } catch (error) {
      console.error('❌ Create skill assessment error:', error);
      res.status(500).json({ 
        error: 'Failed to create skill assessment',
        message: 'An error occurred while creating the skill assessment',
        code: 'CREATE_ASSESSMENT_ERROR'
      });
    }
  }
);

// Take skill assessment
router.post('/skills/assessments/:assessmentId/take',
  authenticateToken,
  [
    param('assessmentId').isUUID().withMessage('Valid assessment ID required'),
    body('answers').isArray({ min: 1 }),
    body('answers.*.question_id').isLength({ min: 1, max: 100 }),
    body('answers.*.answer').notEmpty(),
    body('answers.*.confidence_level').optional().isInt({ min: 1, max: 5 }),
    body('time_taken_minutes').isInt({ min: 1, max: 480 })
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

      console.log(`🎯 Take skill assessment ${req.params.assessmentId} by ${req.user.username}`);

      const { assessmentId } = req.params;
      const { answers, time_taken_minutes } = req.body;

      // Get assessment details
      const assessmentResult = await secureQuery(`
        SELECT 
          id, name, skill_areas, passing_score, time_limit_minutes, status
        FROM skill_assessments 
        WHERE id = $1
      `, [assessmentId]);

      if (assessmentResult.rows.length === 0) {
        return res.status(404).json({
          error: 'Assessment not found',
          code: 'ASSESSMENT_NOT_FOUND'
        });
      }

      const assessment = assessmentResult.rows[0];

      if (assessment.status !== 'active') {
        return res.status(400).json({
          error: 'Assessment not available',
          message: `Assessment is currently ${assessment.status}`,
          code: 'ASSESSMENT_NOT_AVAILABLE'
        });
      }

      // Check if time limit exceeded
      if (time_taken_minutes > assessment.time_limit_minutes) {
        return res.status(400).json({
          error: 'Time limit exceeded',
          message: `Assessment must be completed within ${assessment.time_limit_minutes} minutes`,
          code: 'TIME_LIMIT_EXCEEDED'
        });
      }

      // Check if already taken recently
      const recentAttempt = await secureQuery(`
        SELECT id, taken_at FROM skill_assessment_results 
        WHERE assessment_id = $1 AND user_id = $2 
        AND taken_at > NOW() - INTERVAL '24 hours'
        ORDER BY taken_at DESC 
        LIMIT 1
      `, [assessmentId, req.user.id]);

      if (recentAttempt.rows.length > 0) {
        return res.status(429).json({
          error: 'Assessment recently taken',
          message: 'You can only take this assessment once per 24 hours',
          code: 'ASSESSMENT_RATE_LIMITED',
          last_attempt: recentAttempt.rows[0].taken_at
        });
      }

      // Process answers and calculate scores
      const skillAreas = JSON.parse(assessment.skill_areas);
      const skillScores = {};
      let totalScore = 0;
      let totalQuestions = 0;

      // Simplified scoring (in real implementation, this would be more sophisticated)
      skillAreas.forEach(area => {
        const areaAnswers = answers.filter(answer => 
          area.questions.some(q => q.id === answer.question_id)
        );
        
        const areaScore = areaAnswers.length > 0 ? 
          (areaAnswers.reduce((sum, answer) => sum + (answer.confidence_level || 3), 0) / areaAnswers.length) * 20 :
          0;
        
        skillScores[area.name] = Math.min(100, Math.max(0, areaScore));
        totalScore += skillScores[area.name];
        totalQuestions += area.questions.length;
      });

      const overallScore = totalScore / skillAreas.length;
      const passed = overallScore >= assessment.passing_score;

      // Save assessment result
      const result = await secureQuery(`
        INSERT INTO skill_assessment_results (
          assessment_id, user_id, answers, skill_scores, overall_score,
          passed, time_taken_minutes, taken_at, created_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
        RETURNING id, overall_score, passed, taken_at
      `, [
        assessmentId, 
        req.user.id, 
        JSON.stringify(answers), 
        JSON.stringify(skillScores), 
        overallScore, 
        passed, 
        time_taken_minutes
      ]);

      console.log(`🎯 Skill assessment completed: ${req.user.username} -> ${overallScore.toFixed(1)}% (${passed ? 'PASSED' : 'FAILED'})`);

      if (req.user.role === 'founder') {
        console.log('👑🎯👑 LEGENDARY FOUNDER SKILL ASSESSMENT WITH INFINITE CAPABILITY! 👑🎯👑');
      }

      res.json({
        success: true,
        data: {
          result: {
            ...result.rows[0],
            assessment: {
              id: assessment.id,
              name: assessment.name,
              passing_score: assessment.passing_score
            },
            skill_scores: skillScores,
            answers_count: answers.length,
            recommendation: passed ? 
              'Excellent performance! Continue developing these skills.' :
              'Consider additional training in areas with lower scores.'
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ASSESSMENT: "${assessment.name}" completed with infinite capability (${overallScore.toFixed(1)}%)!` :
          passed ?
            `🎉 Assessment "${assessment.name}" passed with ${overallScore.toFixed(1)}%! Well done!` :
            `📊 Assessment "${assessment.name}" completed with ${overallScore.toFixed(1)}%. Keep learning and improving!`
      });

    } catch (error) {
      console.error('❌ Take skill assessment error:', error);
      res.status(500).json({ 
        error: 'Failed to complete skill assessment',
        message: 'An error occurred while processing the skill assessment',
        code: 'TAKE_ASSESSMENT_ERROR'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'hr-learning',
    timestamp: new Date().toISOString(),
    message: '🎓 Learning & development service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    evening_energy: '🌃 PRIME EVENING LEGENDARY LEARNING POWER AT 20:56:56! 🌃'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY LEARNING & DEVELOPMENT SYSTEM COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Learning & development system completed at: 2025-08-06 20:56:56 UTC`);
console.log('🎓 Learning management: LEGENDARY PRECISION');
console.log('👑 RICKROLL187 founder learning controls: MAXIMUM AUTHORITY');
console.log('🎯 Skill assessment: SWISS PRECISION');
console.log('🌃 PRIME EVENING LEGENDARY LEARNING POWER: INFINITE AT 20:56:56!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
