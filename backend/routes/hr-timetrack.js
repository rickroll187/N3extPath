// File: backend/routes/hr-timetrack.js
/**
 * ⏰🎸 N3EXTPATH - LEGENDARY TIME & ATTENDANCE SYSTEM 🎸⏰
 * Swiss precision time tracking with infinite workforce energy
 * Built: 2025-08-06 20:49:03 UTC by RICKROLL187
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

console.log('⏰🎸⏰ LEGENDARY TIME & ATTENDANCE SYSTEM LOADING! ⏰🎸⏰');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Time & attendance system loaded at: 2025-08-06 20:49:03 UTC`);
console.log('🌃 PRIME EVENING LEGENDARY TIME TRACKING AT 20:49:03!');

// =====================================
// 🛡️ TIME TRACKING RATE LIMITING 🛡️
// =====================================

const timeTrackLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 500, // Higher limit for frequent clock operations
  message: {
    error: 'Too many time tracking requests from this IP, please try again later.',
    retryAfter: '15 minutes',
    code: 'TIME_TRACK_RATE_LIMIT'
  }
});

router.use(timeTrackLimiter);
router.use(validatePayload(5120)); // 5KB max payload

// =====================================
// 🕐 TIME CLOCK OPERATIONS 🕐
// =====================================

// Clock in/out endpoint
router.post('/clock/:action',
  authenticateToken,
  [
    param('action').isIn(['in', 'out', 'break_start', 'break_end']).withMessage('Valid action required'),
    body('location').optional().isObject(),
    body('location.latitude').optional().isFloat({ min: -90, max: 90 }),
    body('location.longitude').optional().isFloat({ min: -180, max: 180 }),
    body('notes').optional().isLength({ max: 500 }).trim(),
    body('project_id').optional().isUUID()
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

      console.log(`⏰ Clock ${req.params.action} by ${req.user.username} at 20:49:03 UTC`);

      const { action } = req.params;
      const { location, notes, project_id } = req.body;
      const clockTime = new Date();

      // Get user's current time entry status
      const currentEntry = await secureQuery(`
        SELECT 
          id, clock_in_time, clock_out_time, break_start_time, break_end_time,
          status, total_break_minutes, date
        FROM time_entries 
        WHERE user_id = $1 AND date = CURRENT_DATE AND clock_out_time IS NULL
        ORDER BY clock_in_time DESC 
        LIMIT 1
      `, [req.user.id]);

      let timeEntry;

      if (action === 'in') {
        // Check if already clocked in today
        if (currentEntry.rows.length > 0) {
          return res.status(409).json({
            error: 'Already clocked in',
            message: 'You are already clocked in for today',
            code: 'ALREADY_CLOCKED_IN',
            current_entry: currentEntry.rows[0]
          });
        }

        // Create new time entry
        const result = await secureQuery(`
          INSERT INTO time_entries (
            user_id, date, clock_in_time, clock_in_location, clock_in_notes,
            project_id, status, created_at
          ) VALUES ($1, CURRENT_DATE, $2, $3, $4, $5, 'clocked_in', NOW())
          RETURNING id, clock_in_time, status
        `, [req.user.id, clockTime, location ? JSON.stringify(location) : null, notes, project_id]);

        timeEntry = result.rows[0];

        console.log(`⏰ Clock IN: ${req.user.username} at ${clockTime.toISOString()}`);

        if (req.user.role === 'founder') {
          console.log('👑⏰👑 LEGENDARY FOUNDER CLOCK IN WITH INFINITE TIME POWER! 👑⏰👑');
        }

      } else if (action === 'out') {
        if (currentEntry.rows.length === 0) {
          return res.status(409).json({
            error: 'Not clocked in',
            message: 'You are not currently clocked in',
            code: 'NOT_CLOCKED_IN'
          });
        }

        const entry = currentEntry.rows[0];

        // End any active break
        let breakEndUpdate = '';
        let breakTime = entry.total_break_minutes || 0;
        
        if (entry.break_start_time && !entry.break_end_time) {
          const breakDuration = Math.floor((clockTime - new Date(entry.break_start_time)) / (1000 * 60));
          breakTime += breakDuration;
          breakEndUpdate = ', break_end_time = $6';
        }

        // Calculate total hours worked
        const totalMinutes = Math.floor((clockTime - new Date(entry.clock_in_time)) / (1000 * 60)) - breakTime;
        const hoursWorked = Math.max(0, totalMinutes / 60);

        const result = await secureQuery(`
          UPDATE time_entries 
          SET 
            clock_out_time = $2, 
            clock_out_location = $3, 
            clock_out_notes = $4,
            total_break_minutes = $5,
            hours_worked = $7,
            status = 'clocked_out',
            updated_at = NOW()
            ${breakEndUpdate}
          WHERE id = $1
          RETURNING id, clock_in_time, clock_out_time, hours_worked, status
        `, [
          entry.id, 
          clockTime, 
          location ? JSON.stringify(location) : null, 
          notes,
          breakTime,
          ...(breakEndUpdate ? [clockTime] : []),
          hoursWorked
        ]);

        timeEntry = result.rows[0];

        console.log(`⏰ Clock OUT: ${req.user.username} at ${clockTime.toISOString()} (${hoursWorked.toFixed(2)}h worked)`);

        if (req.user.role === 'founder') {
          console.log('👑⏰👑 LEGENDARY FOUNDER CLOCK OUT WITH INFINITE PRODUCTIVITY! 👑⏰👑');
        }

      } else if (action === 'break_start') {
        if (currentEntry.rows.length === 0) {
          return res.status(409).json({
            error: 'Not clocked in',
            message: 'You must be clocked in to start a break',
            code: 'NOT_CLOCKED_IN'
          });
        }

        const entry = currentEntry.rows[0];

        if (entry.break_start_time && !entry.break_end_time) {
          return res.status(409).json({
            error: 'Already on break',
            message: 'You are already on a break',
            code: 'ALREADY_ON_BREAK'
          });
        }

        const result = await secureQuery(`
          UPDATE time_entries 
          SET break_start_time = $2, status = 'on_break', updated_at = NOW()
          WHERE id = $1
          RETURNING id, break_start_time, status
        `, [entry.id, clockTime]);

        timeEntry = result.rows[0];

        console.log(`☕ Break START: ${req.user.username} at ${clockTime.toISOString()}`);

      } else if (action === 'break_end') {
        if (currentEntry.rows.length === 0) {
          return res.status(409).json({
            error: 'Not clocked in',
            message: 'You must be clocked in to end a break',
            code: 'NOT_CLOCKED_IN'
          });
        }

        const entry = currentEntry.rows[0];

        if (!entry.break_start_time || entry.break_end_time) {
          return res.status(409).json({
            error: 'Not on break',
            message: 'You are not currently on a break',
            code: 'NOT_ON_BREAK'
          });
        }

        // Calculate break duration
        const breakDuration = Math.floor((clockTime - new Date(entry.break_start_time)) / (1000 * 60));
        const totalBreakTime = (entry.total_break_minutes || 0) + breakDuration;

        const result = await secureQuery(`
          UPDATE time_entries 
          SET 
            break_end_time = $2, 
            total_break_minutes = $3,
            status = 'clocked_in', 
            updated_at = NOW()
          WHERE id = $1
          RETURNING id, break_end_time, total_break_minutes, status
        `, [entry.id, clockTime, totalBreakTime]);

        timeEntry = result.rows[0];

        console.log(`☕ Break END: ${req.user.username} at ${clockTime.toISOString()} (${breakDuration}min break)`);
      }

      // Log time tracking activity
      await secureQuery(`
        INSERT INTO time_tracking_logs (
          user_id, action, timestamp, location, notes, ip_address, created_at
        ) VALUES ($1, $2, $3, $4, $5, $6, NOW())
      `, [req.user.id, action, clockTime, location ? JSON.stringify(location) : null, notes, req.ip]);

      res.json({
        success: true,
        data: {
          time_entry: timeEntry,
          action: action,
          timestamp: clockTime,
          user: {
            id: req.user.id,
            username: req.user.username,
            display_name: req.user.display_name
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ${action.toUpperCase()}: Time tracked with infinite precision!` :
          `⏰ ${action.charAt(0).toUpperCase() + action.slice(1)} successful! Time tracked with Swiss precision!`
      });

    } catch (error) {
      console.error('❌ Clock operation error:', error);
      res.status(500).json({ 
        error: 'Failed to process clock operation',
        message: 'An error occurred while processing the time clock operation',
        code: 'CLOCK_OPERATION_ERROR'
      });
    }
  }
);

// Get current time status
router.get('/status',
  authenticateToken,
  async (req, res) => {
    try {
      console.log(`📊 Get time status for ${req.user.username}`);

      // Get today's time entry
      const todayEntry = await secureQuery(`
        SELECT 
          id, date, clock_in_time, clock_out_time, break_start_time, break_end_time,
          total_break_minutes, hours_worked, status, project_id
        FROM time_entries 
        WHERE user_id = $1 AND date = CURRENT_DATE
        ORDER BY clock_in_time DESC 
        LIMIT 1
      `, [req.user.id]);

      // Get this week's summary
      const weekSummary = await secureQuery(`
        SELECT 
          COUNT(*) as days_worked,
          SUM(hours_worked) as total_hours,
          AVG(hours_worked) as avg_hours_per_day,
          SUM(total_break_minutes) as total_break_minutes
        FROM time_entries 
        WHERE user_id = $1 
          AND date >= DATE_TRUNC('week', CURRENT_DATE)
          AND date <= CURRENT_DATE
          AND hours_worked IS NOT NULL
      `, [req.user.id]);

      // Get this month's summary
      const monthSummary = await secureQuery(`
        SELECT 
          COUNT(*) as days_worked,
          SUM(hours_worked) as total_hours
        FROM time_entries 
        WHERE user_id = $1 
          AND date >= DATE_TRUNC('month', CURRENT_DATE)
          AND date <= CURRENT_DATE
          AND hours_worked IS NOT NULL
      `, [req.user.id]);

      const currentEntry = todayEntry.rows.length > 0 ? todayEntry.rows[0] : null;
      let currentStatus = 'not_clocked_in';
      let timeWorkedToday = 0;
      let currentSessionDuration = 0;

      if (currentEntry) {
        currentStatus = currentEntry.status;
        
        if (currentEntry.clock_out_time) {
          timeWorkedToday = currentEntry.hours_worked || 0;
        } else if (currentEntry.clock_in_time) {
          // Calculate current session duration
          const now = new Date();
          const clockInTime = new Date(currentEntry.clock_in_time);
          const breakTime = currentEntry.total_break_minutes || 0;
          currentSessionDuration = Math.max(0, (now - clockInTime) / (1000 * 60) - breakTime) / 60;
          timeWorkedToday = currentSessionDuration;
        }
      }

      const weekStats = weekSummary.rows[0];
      const monthStats = monthSummary.rows[0];

      const statusData = {
        current_status: currentStatus,
        today: {
          entry: currentEntry,
          hours_worked: timeWorkedToday,
          current_session_duration: currentSessionDuration,
          status: currentStatus
        },
        this_week: {
          days_worked: parseInt(weekStats.days_worked) || 0,
          total_hours: parseFloat(weekStats.total_hours) || 0,
          avg_hours_per_day: parseFloat(weekStats.avg_hours_per_day) || 0,
          total_break_minutes: parseInt(weekStats.total_break_minutes) || 0
        },
        this_month: {
          days_worked: parseInt(monthStats.days_worked) || 0,
          total_hours: parseFloat(monthStats.total_hours) || 0
        }
      };

      console.log(`📊 Time status retrieved for ${req.user.username}: ${currentStatus}`);

      res.json({
        success: true,
        data: { time_status: statusData },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER time status with infinite precision!` :
          `📊 Time status loaded with Swiss precision!`
      });

    } catch (error) {
      console.error('❌ Get time status error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch time status',
        message: 'An error occurred while retrieving time status',
        code: 'GET_TIME_STATUS_ERROR'
      });
    }
  }
);

// Get time entries (with filtering)
router.get('/entries',
  authenticateToken,
  [
    query('start_date').optional().isISO8601(),
    query('end_date').optional().isISO8601(),
    query('user_id').optional().isUUID(),
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

      console.log(`📋 Get time entries by ${req.user.username}`);

      const {
        start_date,
        end_date,
        user_id,
        page = 1,
        limit = 20
      } = req.query;

      const offset = (page - 1) * limit;

      // Check access permissions
      const targetUserId = user_id || req.user.id;
      const canViewOthers = req.user.role === 'founder' || req.user.role === 'admin' || req.user.role === 'moderator';
      
      if (targetUserId !== req.user.id && !canViewOthers) {
        return res.status(403).json({
          error: 'Access denied',
          message: 'You can only view your own time entries',
          code: 'TIME_ENTRIES_ACCESS_DENIED'
        });
      }

      // Build WHERE conditions
      let whereConditions = ['te.user_id = $1'];
      let queryParams = [targetUserId];
      let paramCount = 1;

      if (start_date) {
        paramCount++;
        whereConditions.push(`te.date >= $${paramCount}`);
        queryParams.push(start_date);
      }

      if (end_date) {
        paramCount++;
        whereConditions.push(`te.date <= $${paramCount}`);
        queryParams.push(end_date);
      }

      const whereClause = whereConditions.join(' AND ');

      // Get time entries with user info
      const entriesResult = await secureQuery(`
        SELECT 
          te.id, te.date, te.clock_in_time, te.clock_out_time,
          te.break_start_time, te.break_end_time, te.total_break_minutes,
          te.hours_worked, te.status, te.clock_in_notes, te.clock_out_notes,
          te.project_id, te.created_at,
          u.username, u.display_name,
          p.name as project_name
        FROM time_entries te
        JOIN users u ON te.user_id = u.id
        LEFT JOIN projects p ON te.project_id = p.id
        WHERE ${whereClause}
        ORDER BY te.date DESC, te.clock_in_time DESC
        LIMIT $${paramCount + 1} OFFSET $${paramCount + 2}
      `, [...queryParams, limit, offset]);

      // Get total count
      const countResult = await secureQuery(`
        SELECT COUNT(*) as total
        FROM time_entries te
        WHERE ${whereClause}
      `, queryParams);

      const total = parseInt(countResult.rows[0].total);
      const entries = entriesResult.rows;

      // Calculate summary statistics
      const summaryResult = await secureQuery(`
        SELECT 
          COUNT(*) as total_days,
          SUM(hours_worked) as total_hours,
          AVG(hours_worked) as avg_hours_per_day,
          SUM(total_break_minutes) as total_break_minutes
        FROM time_entries te
        WHERE ${whereClause} AND hours_worked IS NOT NULL
      `, queryParams);

      const summary = summaryResult.rows[0];

      console.log(`📋 Retrieved ${entries.length} time entries (total: ${total})`);

      if (req.user.role === 'founder') {
        console.log('👑📋👑 LEGENDARY FOUNDER TIME ENTRIES ACCESS WITH INFINITE INSIGHTS! 👑📋👑');
      }

      res.json({
        success: true,
        data: {
          time_entries: entries,
          pagination: {
            current_page: page,
            per_page: limit,
            total_pages: Math.ceil(total / limit),
            total_count: total,
            has_next: (page * limit) < total,
            has_prev: page > 1
          },
          summary: {
            total_days: parseInt(summary.total_days) || 0,
            total_hours: parseFloat(summary.total_hours) || 0,
            avg_hours_per_day: parseFloat(summary.avg_hours_per_day) || 0,
            total_break_minutes: parseInt(summary.total_break_minutes) || 0
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 ${total} time entries retrieved with LEGENDARY FOUNDER insights!` :
          `📋 ${total} time entries retrieved with Swiss precision!`
      });

    } catch (error) {
      console.error('❌ Get time entries error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch time entries',
        message: 'An error occurred while retrieving time entries',
        code: 'GET_TIME_ENTRIES_ERROR'
      });
    }
  }
);

// =====================================
// 📝 TIMESHEET MANAGEMENT 📝
// =====================================

// Submit timesheet for approval
router.post('/timesheet/submit',
  authenticateToken,
  [
    body('week_start_date').isISO8601().withMessage('Valid week start date required'),
    body('entries').isArray({ min: 1, max: 7 }).withMessage('Entries array required (1-7 entries)'),
    body('entries.*.date').isISO8601(),
    body('entries.*.hours_worked').isFloat({ min: 0, max: 24 }),
    body('entries.*.project_id').optional().isUUID(),
    body('entries.*.notes').optional().isLength({ max: 500 })
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

      console.log(`📝 Submit timesheet by ${req.user.username} at 20:49:03 UTC`);

      const { week_start_date, entries } = req.body;

      // Check if timesheet already exists for this week
      const existingTimesheet = await secureQuery(`
        SELECT id, status FROM timesheets 
        WHERE user_id = $1 AND week_start_date = $2
      `, [req.user.id, week_start_date]);

      if (existingTimesheet.rows.length > 0) {
        const existing = existingTimesheet.rows[0];
        if (existing.status !== 'draft') {
          return res.status(409).json({
            error: 'Timesheet already submitted',
            message: `Timesheet for this week is already ${existing.status}`,
            code: 'TIMESHEET_ALREADY_SUBMITTED'
          });
        }
      }

      // Create or update timesheet in transaction
      const timesheet = await secureTransaction(async (client) => {
        // Create or update timesheet
        const timesheetResult = await client.query(`
          INSERT INTO timesheets (
            user_id, week_start_date, status, total_hours, submitted_at, created_at
          ) VALUES ($1, $2, 'pending', $3, NOW(), NOW())
          ON CONFLICT (user_id, week_start_date) DO UPDATE SET
            status = 'pending',
            total_hours = EXCLUDED.total_hours,
            submitted_at = NOW(),
            updated_at = NOW()
          RETURNING id, week_start_date, status, total_hours, submitted_at
        `, [
          req.user.id, 
          week_start_date, 
          entries.reduce((sum, entry) => sum + entry.hours_worked, 0)
        ]);

        const timesheet = timesheetResult.rows[0];

        // Delete existing entries for this timesheet
        await client.query(`
          DELETE FROM timesheet_entries WHERE timesheet_id = $1
        `, [timesheet.id]);

        // Insert new entries
        for (const entry of entries) {
          await client.query(`
            INSERT INTO timesheet_entries (
              timesheet_id, date, hours_worked, project_id, notes, created_at
            ) VALUES ($1, $2, $3, $4, $5, NOW())
          `, [timesheet.id, entry.date, entry.hours_worked, entry.project_id, entry.notes]);
        }

        return timesheet;
      });

      console.log(`📝 Timesheet submitted: ${req.user.username} for week ${week_start_date}`);

      if (req.user.role === 'founder') {
        console.log('👑📝👑 LEGENDARY FOUNDER TIMESHEET SUBMISSION! 👑📝👑');
      }

      res.status(201).json({
        success: true,
        data: {
          timesheet: {
            id: timesheet.id,
            week_start_date: timesheet.week_start_date,
            status: timesheet.status,
            total_hours: timesheet.total_hours,
            submitted_at: timesheet.submitted_at,
            entries_count: entries.length
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER TIMESHEET: Week ${week_start_date} submitted with infinite precision!` :
          `📝 Timesheet for week ${week_start_date} submitted successfully! Awaiting approval.`
      });

    } catch (error) {
      console.error('❌ Submit timesheet error:', error);
      res.status(500).json({ 
        error: 'Failed to submit timesheet',
        message: 'An error occurred while submitting the timesheet',
        code: 'SUBMIT_TIMESHEET_ERROR'
      });
    }
  }
);

// Approve/reject timesheet (manager/admin only)
router.patch('/timesheet/:timesheetId/approve',
  authenticateToken,
  requirePermission('users.write'),
  [
    param('timesheetId').isUUID().withMessage('Valid timesheet ID required'),
    body('action').isIn(['approve', 'reject']).withMessage('Valid action required'),
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

      console.log(`✅ ${req.body.action} timesheet ${req.params.timesheetId} by ${req.user.username}`);

      const { timesheetId } = req.params;
      const { action, notes } = req.body;

      // Get timesheet details
      const timesheetResult = await secureQuery(`
        SELECT 
          t.id, t.user_id, t.week_start_date, t.status, t.total_hours,
          u.username, u.display_name
        FROM timesheets t
        JOIN users u ON t.user_id = u.id
        WHERE t.id = $1
      `, [timesheetId]);

      if (timesheetResult.rows.length === 0) {
        return res.status(404).json({
          error: 'Timesheet not found',
          code: 'TIMESHEET_NOT_FOUND'
        });
      }

      const timesheet = timesheetResult.rows[0];

      if (timesheet.status !== 'pending') {
        return res.status(409).json({
          error: 'Invalid timesheet status',
          message: `Timesheet is ${timesheet.status}, cannot ${action}`,
          code: 'INVALID_TIMESHEET_STATUS'
        });
      }

      // Update timesheet status
      const newStatus = action === 'approve' ? 'approved' : 'rejected';
      const actionField = action === 'approve' ? 'approved_at' : 'rejected_at';

      const updatedTimesheet = await secureQuery(`
        UPDATE timesheets 
        SET 
          status = $2,
          ${actionField} = NOW(),
          ${action === 'approve' ? 'approved_by' : 'rejected_by'} = $3,
          approval_notes = $4,
          updated_at = NOW()
        WHERE id = $1
        RETURNING id, status, ${actionField}, approval_notes
      `, [timesheetId, newStatus, req.user.id, notes]);

      console.log(`✅ Timesheet ${action}d: ${timesheet.username} week ${timesheet.week_start_date}`);

      if (req.user.role === 'founder') {
        console.log(`👑✅👑 LEGENDARY FOUNDER TIMESHEET ${action.toUpperCase()}! 👑✅👑`);
      }

      res.json({
        success: true,
        data: {
          timesheet: {
            id: updatedTimesheet.rows[0].id,
            status: updatedTimesheet.rows[0].status,
            [actionField]: updatedTimesheet.rows[0][actionField],
            approval_notes: updatedTimesheet.rows[0].approval_notes,
            employee: {
              username: timesheet.username,
              display_name: timesheet.display_name
            }
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER ACTION: Timesheet ${action}d for ${timesheet.display_name} with infinite authority!` :
          `✅ Timesheet ${action}d for ${timesheet.display_name} successfully!`
      });

    } catch (error) {
      console.error('❌ Approve timesheet error:', error);
      res.status(500).json({ 
        error: 'Failed to process timesheet approval',
        message: 'An error occurred while processing the timesheet',
        code: 'APPROVE_TIMESHEET_ERROR'
      });
    }
  }
);

// =====================================
// 🏖️ LEAVE REQUEST MANAGEMENT 🏖️
// =====================================

// Submit leave request
router.post('/leave/request',
  authenticateToken,
  [
    body('leave_type').isIn(['vacation', 'sick', 'personal', 'bereavement', 'maternity', 'paternity', 'jury_duty']).withMessage('Valid leave type required'),
    body('start_date').isISO8601().withMessage('Valid start date required'),
    body('end_date').isISO8601().withMessage('Valid end date required'),
    body('reason').isLength({ min: 10, max: 1000 }).trim(),
    body('half_day').optional().isBoolean(),
    body('emergency').optional().isBoolean()
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

      console.log(`🏖️ Submit leave request by ${req.user.username} at 20:49:03 UTC`);

      const { leave_type, start_date, end_date, reason, half_day = false, emergency = false } = req.body;

      // Calculate leave days
      const startDate = new Date(start_date);
      const endDate = new Date(end_date);
      const timeDiff = endDate.getTime() - startDate.getTime();
      const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24)) + 1;
      const leaveDays = half_day ? 0.5 : daysDiff;

      if (startDate > endDate) {
        return res.status(400).json({
          error: 'Invalid date range',
          message: 'Start date must be before end date',
          code: 'INVALID_DATE_RANGE'
        });
      }

      if (startDate < new Date() && !emergency) {
        return res.status(400).json({
          error: 'Past date not allowed',
          message: 'Cannot request leave for past dates unless it\'s an emergency',
          code: 'PAST_DATE_NOT_ALLOWED'
        });
      }

      // Create leave request
      const leaveRequest = await secureQuery(`
        INSERT INTO leave_requests (
          user_id, leave_type, start_date, end_date, days_requested,
          reason, half_day, emergency, status, created_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'pending', NOW())
        RETURNING id, leave_type, start_date, end_date, days_requested, status, created_at
      `, [req.user.id, leave_type, start_date, end_date, leaveDays, reason, half_day, emergency]);

      console.log(`🏖️ Leave request created: ${req.user.username} - ${leave_type} (${leaveDays} days)`);

      if (req.user.role === 'founder') {
        console.log('👑🏖️👑 LEGENDARY FOUNDER LEAVE REQUEST! 👑🏖️👑');
      }

      res.status(201).json({
        success: true,
        data: {
          leave_request: {
            ...leaveRequest.rows[0],
            employee: {
              id: req.user.id,
              username: req.user.username,
              display_name: req.user.display_name
            }
          }
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER LEAVE: ${leave_type} request for ${leaveDays} days submitted with infinite priority!` :
          `🏖️ Leave request submitted successfully! ${leave_type} for ${leaveDays} days awaiting approval.`
      });

    } catch (error) {
      console.error('❌ Submit leave request error:', error);
      res.status(500).json({ 
        error: 'Failed to submit leave request',
        message: 'An error occurred while submitting the leave request',
        code: 'SUBMIT_LEAVE_REQUEST_ERROR'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'hr-timetrack',
    timestamp: new Date().toISOString(),
    message: '⏰ Time & attendance service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    evening_energy: '🌃 PRIME EVENING LEGENDARY TIME TRACKING AT 20:49:03! 🌃'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY TIME & ATTENDANCE SYSTEM COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Time & attendance system completed at: 2025-08-06 20:49:03 UTC`);
console.log('⏰ Time tracking: LEGENDARY PRECISION');
console.log('👑 RICKROLL187 founder time controls: MAXIMUM AUTHORITY');
console.log('📝 Timesheet management: SWISS PRECISION');
console.log('🌃 PRIME EVENING LEGENDARY TIME POWER: INFINITE AT 20:49:03!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
