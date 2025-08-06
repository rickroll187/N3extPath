// File: backend/routes/notifications.js
/**
 * 🔔🎸 N3EXTPATH - LEGENDARY NOTIFICATIONS & WEBHOOKS API 🎸🔔
 * Swiss precision notifications with infinite code bro energy
 * Built: 2025-08-06 18:00:31 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const express = require('express');
const { Pool } = require('pg');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const { body, query, validationResult } = require('express-validator');
const crypto = require('crypto');
const axios = require('axios');

const router = express.Router();
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

console.log('🔔🎸🔔 LEGENDARY NOTIFICATIONS & WEBHOOKS LOADING! 🔔🎸🔔');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Notifications routes loaded at: 2025-08-06 18:00:31 UTC`);
console.log('🌅 EVENING LEGENDARY NOTIFICATIONS ENERGY AT 18:00:31!');

// =====================================
// 🛡️ MIDDLEWARE & RATE LIMITING 🛡️
// =====================================

// Notifications rate limiter
const notificationsLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 200, // limit each IP to 200 requests per windowMs
  message: {
    error: 'Too many notification requests from this IP, please try again later.',
    retryAfter: '15 minutes'
  }
});

// Webhook rate limiter (more restrictive)
const webhookLimiter = rateLimit({
  windowMs: 5 * 60 * 1000, // 5 minutes
  max: 50, // limit each IP to 50 webhook requests per windowMs
  message: {
    error: 'Too many webhook requests from this IP, please try again later.',
    retryAfter: '5 minutes'
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
      console.log('👑🔔👑 RICKROLL187 FOUNDER NOTIFICATIONS ACCESS! 👑🔔👑');
      console.log('🚀 LEGENDARY FOUNDER NOTIFICATIONS WITH INFINITE CODE BRO ENERGY!');
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
// 🔔 NOTIFICATION FUNCTIONS 🔔
// =====================================

// Create notification function
async function createNotification(userId, type, title, message, data = {}, priority = 'medium') {
  try {
    const result = await pool.query(`
      INSERT INTO notifications (
        user_id, type, title, message, data, priority, created_at
      ) VALUES ($1, $2, $3, $4, $5, $6, NOW())
      RETURNING id, created_at
    `, [userId, type, title, message, JSON.stringify(data), priority]);
    
    console.log(`🔔 Notification created: ${type} for user ${userId}`);
    return result.rows[0];
  } catch (error) {
    console.error('❌ Error creating notification:', error);
    throw error;
  }
}

// Send webhook function
async function sendWebhook(webhookUrl, event, data, signature = null) {
  try {
    const payload = {
      event,
      data,
      timestamp: new Date().toISOString(),
      platform: 'N3EXTPATH',
      version: '1.0.0'
    };

    const headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'N3EXTPATH-Webhook/1.0'
    };

    if (signature) {
      headers['X-N3EXTPATH-Signature'] = signature;
    }

    const response = await axios.post(webhookUrl, payload, {
      headers,
      timeout: 10000, // 10 second timeout
      maxRedirects: 0
    });

    console.log(`🔗 Webhook sent successfully: ${event} to ${webhookUrl}`);
    return { success: true, status: response.status, data: response.data };
  } catch (error) {
    console.error(`❌ Webhook failed: ${event} to ${webhookUrl}:`, error.message);
    return { success: false, error: error.message };
  }
}

// =====================================
// 🔔 NOTIFICATION ROUTES 🔔
// =====================================

// Get user notifications
router.get('/notifications',
  notificationsLimiter,
  authenticateToken,
  [
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt(),
    query('offset').optional().isInt({ min: 0 }).toInt(),
    query('unread_only').optional().isBoolean(),
    query('type').optional().isIn(['okr_update', 'team_invite', 'message', 'system', 'achievement', 'reminder', 'security'])
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

      console.log(`🔔 Notifications request by ${req.user.username} at 18:00:31 UTC`);

      const { limit = 20, offset = 0, unread_only = false, type } = req.query;
      
      let whereConditions = ['user_id = $1'];
      let queryParams = [req.user.id];
      let paramCount = 1;

      if (unread_only) {
        whereConditions.push('read_at IS NULL');
      }

      if (type) {
        paramCount++;
        whereConditions.push(`type = $${paramCount}`);
        queryParams.push(type);
      }

      const whereClause = whereConditions.join(' AND ');

      // Get notifications
      const notifications = await pool.query(`
        SELECT 
          id, type, title, message, data, priority, 
          read_at, created_at,
          CASE WHEN read_at IS NULL THEN true ELSE false END as unread
        FROM notifications 
        WHERE ${whereClause}
        ORDER BY created_at DESC, priority DESC
        LIMIT $${paramCount + 1} OFFSET $${paramCount + 2}
      `, [...queryParams, limit, offset]);

      // Get unread count
      const unreadCount = await pool.query(`
        SELECT COUNT(*) as unread_count 
        FROM notifications 
        WHERE user_id = $1 AND read_at IS NULL
      `, [req.user.id]);

      console.log('🔔 Notifications retrieved successfully!');
      res.json({
        success: true,
        data: {
          notifications: notifications.rows.map(row => ({
            ...row,
            data: typeof row.data === 'string' ? JSON.parse(row.data) : row.data
          })),
          pagination: {
            limit,
            offset,
            total: notifications.rows.length,
            has_more: notifications.rows.length === limit
          },
          unread_count: parseInt(unreadCount.rows[0].unread_count)
        },
        message: req.user.role === 'founder' ? 
          '👑 Legendary founder notifications with infinite updates!' : 
          '🔔 Notifications retrieved with Swiss precision!'
      });

    } catch (error) {
      console.error('❌ Notifications error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch notifications',
        message: 'An error occurred while retrieving notifications'
      });
    }
  }
);

// Mark notifications as read
router.patch('/notifications/read',
  notificationsLimiter,
  authenticateToken,
  [
    body('notification_ids').optional().isArray(),
    body('notification_ids.*').isUUID(),
    body('mark_all').optional().isBoolean()
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

      console.log(`📖 Mark notifications as read by ${req.user.username}`);

      const { notification_ids, mark_all = false } = req.body;

      let updateQuery;
      let queryParams;

      if (mark_all) {
        updateQuery = `
          UPDATE notifications 
          SET read_at = NOW() 
          WHERE user_id = $1 AND read_at IS NULL
          RETURNING id
        `;
        queryParams = [req.user.id];
      } else if (notification_ids && notification_ids.length > 0) {
        const placeholders = notification_ids.map((_, index) => `$${index + 2}`).join(',');
        updateQuery = `
          UPDATE notifications 
          SET read_at = NOW() 
          WHERE user_id = $1 AND id IN (${placeholders}) AND read_at IS NULL
          RETURNING id
        `;
        queryParams = [req.user.id, ...notification_ids];
      } else {
        return res.status(400).json({
          error: 'Invalid request',
          message: 'Either provide notification_ids or set mark_all to true'
        });
      }

      const result = await pool.query(updateQuery, queryParams);

      console.log(`📖 ${result.rows.length} notifications marked as read!`);
      res.json({
        success: true,
        data: {
          marked_count: result.rows.length,
          notification_ids: result.rows.map(row => row.id)
        },
        message: `${result.rows.length} notifications marked as read!`
      });

    } catch (error) {
      console.error('❌ Mark notifications read error:', error);
      res.status(500).json({ 
        error: 'Failed to mark notifications as read',
        message: 'An error occurred while updating notifications'
      });
    }
  }
);

// Delete notifications
router.delete('/notifications',
  notificationsLimiter,
  authenticateToken,
  [
    body('notification_ids').isArray().notEmpty(),
    body('notification_ids.*').isUUID()
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

      console.log(`🗑️ Delete notifications by ${req.user.username}`);

      const { notification_ids } = req.body;
      const placeholders = notification_ids.map((_, index) => `$${index + 2}`).join(',');

      const result = await pool.query(`
        DELETE FROM notifications 
        WHERE user_id = $1 AND id IN (${placeholders})
        RETURNING id
      `, [req.user.id, ...notification_ids]);

      console.log(`🗑️ ${result.rows.length} notifications deleted!`);
      res.json({
        success: true,
        data: {
          deleted_count: result.rows.length,
          notification_ids: result.rows.map(row => row.id)
        },
        message: `${result.rows.length} notifications deleted successfully!`
      });

    } catch (error) {
      console.error('❌ Delete notifications error:', error);
      res.status(500).json({ 
        error: 'Failed to delete notifications',
        message: 'An error occurred while deleting notifications'
      });
    }
  }
);

// Send notification (admin only)
router.post('/notifications/send',
  notificationsLimiter,
  authenticateToken,
  requireAdmin,
  [
    body('user_ids').optional().isArray(),
    body('user_ids.*').isUUID(),
    body('broadcast').optional().isBoolean(),
    body('type').isIn(['okr_update', 'team_invite', 'message', 'system', 'achievement', 'reminder', 'security']),
    body('title').isLength({ min: 1, max: 200 }),
    body('message').isLength({ min: 1, max: 1000 }),
    body('data').optional().isObject(),
    body('priority').optional().isIn(['low', 'medium', 'high', 'urgent'])
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

      console.log(`📢 Send notifications by ${req.user.username}`);
      
      if (req.user.role === 'founder') {
        console.log('👑 FOUNDER BROADCAST SYSTEM ACTIVATED WITH INFINITE REACH! 👑');
      }

      const { user_ids, broadcast = false, type, title, message, data = {}, priority = 'medium' } = req.body;

      let targetUsers = [];

      if (broadcast) {
        // Send to all users
        const allUsers = await pool.query('SELECT id FROM users WHERE id != $1', [req.user.id]);
        targetUsers = allUsers.rows.map(row => row.id);
        console.log(`📢 Broadcasting to ${targetUsers.length} users!`);
      } else if (user_ids && user_ids.length > 0) {
        targetUsers = user_ids;
      } else {
        return res.status(400).json({
          error: 'Invalid request',
          message: 'Either provide user_ids or set broadcast to true'
        });
      }

      // Create notifications for all target users
      const createdNotifications = [];
      for (const userId of targetUsers) {
        try {
          const notification = await createNotification(userId, type, title, message, data, priority);
          createdNotifications.push(notification);
        } catch (error) {
          console.error(`❌ Failed to create notification for user ${userId}:`, error);
        }
      }

      console.log(`📢 ${createdNotifications.length} notifications sent successfully!`);
      res.json({
        success: true,
        data: {
          sent_count: createdNotifications.length,
          target_count: targetUsers.length,
          type,
          priority,
          broadcast
        },
        message: req.user.role === 'founder' ? 
          `👑 LEGENDARY FOUNDER BROADCAST: ${createdNotifications.length} notifications sent with infinite power!` :
          `📢 ${createdNotifications.length} notifications sent successfully!`
      });

    } catch (error) {
      console.error('❌ Send notifications error:', error);
      res.status(500).json({ 
        error: 'Failed to send notifications',
        message: 'An error occurred while sending notifications'
      });
    }
  }
);

// =====================================
// 🔗 WEBHOOK ROUTES 🔗
// =====================================

// Get webhooks
router.get('/webhooks',
  webhookLimiter,
  authenticateToken,
  async (req, res) => {
    try {
      console.log(`🔗 Webhooks request by ${req.user.username}`);

      const webhooks = await pool.query(`
        SELECT 
          id, name, url, events, is_active, secret_key, 
          created_at, updated_at, last_triggered_at,
          success_count, failure_count
        FROM webhooks 
        WHERE user_id = $1 OR $2 = ANY(ARRAY['founder', 'admin'])
        ORDER BY created_at DESC
      `, [req.user.id, req.user.role]);

      console.log('🔗 Webhooks retrieved successfully!');
      res.json({
        success: true,
        data: {
          webhooks: webhooks.rows.map(row => ({
            ...row,
            events: Array.isArray(row.events) ? row.events : JSON.parse(row.events || '[]'),
            // Don't expose secret key in response
            secret_key: row.secret_key ? '***HIDDEN***' : null
          }))
        },
        message: 'Webhooks retrieved with Swiss precision!'
      });

    } catch (error) {
      console.error('❌ Get webhooks error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch webhooks',
        message: 'An error occurred while retrieving webhooks'
      });
    }
  }
);

// Create webhook
router.post('/webhooks',
  webhookLimiter,
  authenticateToken,
  [
    body('name').isLength({ min: 1, max: 100 }),
    body('url').isURL(),
    body('events').isArray().notEmpty(),
    body('events.*').isIn([
      'okr.created', 'okr.updated', 'okr.completed', 'okr.deleted',
      'team.created', 'team.updated', 'team.member_added', 'team.member_removed',
      'user.created', 'user.updated', 'user.login',
      'message.created', 'message.updated', 'message.deleted',
      'notification.sent', 'system.alert'
    ]),
    body('secret_key').optional().isLength({ min: 16, max: 256 })
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

      console.log(`🔗 Create webhook by ${req.user.username}`);

      const { name, url, events, secret_key } = req.body;

      // Generate secret key if not provided
      const finalSecretKey = secret_key || crypto.randomBytes(32).toString('hex');

      const result = await pool.query(`
        INSERT INTO webhooks (
          user_id, name, url, events, secret_key, is_active, created_at
        ) VALUES ($1, $2, $3, $4, $5, true, NOW())
        RETURNING id, name, url, events, is_active, created_at
      `, [req.user.id, name, url, JSON.stringify(events), finalSecretKey]);

      console.log('🔗 Webhook created successfully!');
      res.status(201).json({
        success: true,
        data: {
          webhook: {
            ...result.rows[0],
            events: JSON.parse(result.rows[0].events),
            secret_key: finalSecretKey // Show once during creation
          }
        },
        message: 'Webhook created successfully! Save your secret key - it won\'t be shown again.'
      });

    } catch (error) {
      console.error('❌ Create webhook error:', error);
      
      if (error.code === '23505') { // Unique constraint violation
        res.status(409).json({
          error: 'Webhook already exists',
          message: 'A webhook with this name or URL already exists'
        });
      } else {
        res.status(500).json({ 
          error: 'Failed to create webhook',
          message: 'An error occurred while creating the webhook'
        });
      }
    }
  }
);

// Update webhook
router.patch('/webhooks/:webhookId',
  webhookLimiter,
  authenticateToken,
  [
    body('name').optional().isLength({ min: 1, max: 100 }),
    body('url').optional().isURL(),
    body('events').optional().isArray().notEmpty(),
    body('events.*').optional().isIn([
      'okr.created', 'okr.updated', 'okr.completed', 'okr.deleted',
      'team.created', 'team.updated', 'team.member_added', 'team.member_removed',
      'user.created', 'user.updated', 'user.login',
      'message.created', 'message.updated', 'message.deleted',
      'notification.sent', 'system.alert'
    ]),
    body('is_active').optional().isBoolean()
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

      console.log(`🔗 Update webhook ${req.params.webhookId} by ${req.user.username}`);

      const { webhookId } = req.params;
      const updates = req.body;

      // Check ownership
      const ownership = await pool.query(`
        SELECT id FROM webhooks 
        WHERE id = $1 AND (user_id = $2 OR $3 = ANY(ARRAY['founder', 'admin']))
      `, [webhookId, req.user.id, req.user.role]);

      if (ownership.rows.length === 0) {
        return res.status(404).json({
          error: 'Webhook not found',
          message: 'Webhook not found or you don\'t have permission to modify it'
        });
      }

      // Build update query
      const updateFields = [];
      const queryParams = [];
      let paramCount = 0;

      for (const [key, value] of Object.entries(updates)) {
        if (value !== undefined) {
          paramCount++;
          updateFields.push(`${key} = $${paramCount}`);
          queryParams.push(key === 'events' ? JSON.stringify(value) : value);
        }
      }

      if (updateFields.length === 0) {
        return res.status(400).json({
          error: 'No updates provided',
          message: 'At least one field must be updated'
        });
      }

      queryParams.push(webhookId);
      const result = await pool.query(`
        UPDATE webhooks 
        SET ${updateFields.join(', ')}, updated_at = NOW()
        WHERE id = $${paramCount + 1}
        RETURNING id, name, url, events, is_active, updated_at
      `, queryParams);

      console.log('🔗 Webhook updated successfully!');
      res.json({
        success: true,
        data: {
          webhook: {
            ...result.rows[0],
            events: JSON.parse(result.rows[0].events)
          }
        },
        message: 'Webhook updated successfully!'
      });

    } catch (error) {
      console.error('❌ Update webhook error:', error);
      res.status(500).json({ 
        error: 'Failed to update webhook',
        message: 'An error occurred while updating the webhook'
      });
    }
  }
);

// Delete webhook
router.delete('/webhooks/:webhookId',
  webhookLimiter,
  authenticateToken,
  async (req, res) => {
    try {
      console.log(`🗑️ Delete webhook ${req.params.webhookId} by ${req.user.username}`);

      const { webhookId } = req.params;

      const result = await pool.query(`
        DELETE FROM webhooks 
        WHERE id = $1 AND (user_id = $2 OR $3 = ANY(ARRAY['founder', 'admin']))
        RETURNING id, name
      `, [webhookId, req.user.id, req.user.role]);

      if (result.rows.length === 0) {
        return res.status(404).json({
          error: 'Webhook not found',
          message: 'Webhook not found or you don\'t have permission to delete it'
        });
      }

      console.log('🗑️ Webhook deleted successfully!');
      res.json({
        success: true,
        data: {
          deleted_webhook: result.rows[0]
        },
        message: 'Webhook deleted successfully!'
      });

    } catch (error) {
      console.error('❌ Delete webhook error:', error);
      res.status(500).json({ 
        error: 'Failed to delete webhook',
        message: 'An error occurred while deleting the webhook'
      });
    }
  }
);

// Test webhook
router.post('/webhooks/:webhookId/test',
  webhookLimiter,
  authenticateToken,
  async (req, res) => {
    try {
      console.log(`🧪 Test webhook ${req.params.webhookId} by ${req.user.username}`);

      const { webhookId } = req.params;

      // Get webhook details
      const webhook = await pool.query(`
        SELECT id, name, url, secret_key FROM webhooks 
        WHERE id = $1 AND (user_id = $2 OR $3 = ANY(ARRAY['founder', 'admin']))
      `, [webhookId, req.user.id, req.user.role]);

      if (webhook.rows.length === 0) {
        return res.status(404).json({
          error: 'Webhook not found',
          message: 'Webhook not found or you don\'t have permission to test it'
        });
      }

      const webhookData = webhook.rows[0];

      // Create test payload
      const testData = {
        event: 'webhook.test',
        webhook_id: webhookId,
        webhook_name: webhookData.name,
        test_timestamp: new Date().toISOString(),
        triggered_by: {
          id: req.user.id,
          username: req.user.username,
          role: req.user.role
        },
        message: req.user.role === 'founder' ? 
          '👑 LEGENDARY FOUNDER WEBHOOK TEST with infinite power!' :
          '🧪 Webhook test from N3EXTPATH with Swiss precision!'
      };

      // Generate signature
      const signature = crypto
        .createHmac('sha256', webhookData.secret_key)
        .update(JSON.stringify(testData))
        .digest('hex');

      // Send test webhook
      const result = await sendWebhook(webhookData.url, 'webhook.test', testData, `sha256=${signature}`);

      // Update webhook stats
      if (result.success) {
        await pool.query(`
          UPDATE webhooks 
          SET success_count = success_count + 1, last_triggered_at = NOW()
          WHERE id = $1
        `, [webhookId]);
      } else {
        await pool.query(`
          UPDATE webhooks 
          SET failure_count = failure_count + 1
          WHERE id = $1
        `, [webhookId]);
      }

      console.log('🧪 Webhook test completed!');
      res.json({
        success: true,
        data: {
          webhook_id: webhookId,
          test_result: result,
          test_data: testData
        },
        message: result.success ? 
          'Webhook test successful! Check your endpoint for the test payload.' :
          `Webhook test failed: ${result.error}`
      });

    } catch (error) {
      console.error('❌ Test webhook error:', error);
      res.status(500).json({ 
        error: 'Failed to test webhook',
        message: 'An error occurred while testing the webhook'
      });
    }
  }
);

// Get notification preferences
router.get('/preferences',
  notificationsLimiter,
  authenticateToken,
  async (req, res) => {
    try {
      console.log(`⚙️ Get notification preferences for ${req.user.username}`);

      const preferences = await pool.query(`
        SELECT * FROM notification_preferences 
        WHERE user_id = $1
      `, [req.user.id]);

      // Default preferences if none exist
      const defaultPrefs = {
        okr_updates: true,
        team_invites: true,
        messages: true,
        system_notifications: true,
        achievements: true,
        reminders: true,
        security_alerts: true,
        email_notifications: false,
        push_notifications: true,
        digest_frequency: 'daily'
      };

      const userPrefs = preferences.rows.length > 0 ? 
        { ...defaultPrefs, ...preferences.rows[0].preferences } : 
        defaultPrefs;

      res.json({
        success: true,
        data: {
          preferences: userPrefs
        },
        message: 'Notification preferences retrieved successfully!'
      });

    } catch (error) {
      console.error('❌ Get preferences error:', error);
      res.status(500).json({ 
        error: 'Failed to fetch preferences',
        message: 'An error occurred while retrieving notification preferences'
      });
    }
  }
);

// Update notification preferences
router.patch('/preferences',
  notificationsLimiter,
  authenticateToken,
  [
    body('preferences').isObject(),
    body('preferences.okr_updates').optional().isBoolean(),
    body('preferences.team_invites').optional().isBoolean(),
    body('preferences.messages').optional().isBoolean(),
    body('preferences.system_notifications').optional().isBoolean(),
    body('preferences.achievements').optional().isBoolean(),
    body('preferences.reminders').optional().isBoolean(),
    body('preferences.security_alerts').optional().isBoolean(),
    body('preferences.email_notifications').optional().isBoolean(),
    body('preferences.push_notifications').optional().isBoolean(),
    body('preferences.digest_frequency').optional().isIn(['never', 'daily', 'weekly', 'monthly'])
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

      console.log(`⚙️ Update notification preferences for ${req.user.username}`);

      const { preferences } = req.body;

      // Upsert preferences
      const result = await pool.query(`
        INSERT INTO notification_preferences (user_id, preferences, updated_at)
        VALUES ($1, $2, NOW())
        ON CONFLICT (user_id) DO UPDATE SET
          preferences = excluded.preferences,
          updated_at = excluded.updated_at
        RETURNING preferences
      `, [req.user.id, JSON.stringify(preferences)]);

      console.log('⚙️ Notification preferences updated successfully!');
      res.json({
        success: true,
        data: {
          preferences: result.rows[0].preferences
        },
        message: 'Notification preferences updated successfully!'
      });

    } catch (error) {
      console.error('❌ Update preferences error:', error);
      res.status(500).json({ 
        error: 'Failed to update preferences',
        message: 'An error occurred while updating notification preferences'
      });
    }
  }
);

// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'notifications',
    timestamp: new Date().toISOString(),
    message: '🔔 Notifications service operational with Swiss precision!',
    version: '1.0.0',
    uptime: process.uptime(),
    features: ['notifications', 'webhooks', 'preferences'],
    evening_energy: '🌅 EVENING LEGENDARY NOTIFICATIONS POWER AT 18:00:31! 🌅'
  });
});

module.exports = router;

console.log('🎸🎸🎸 LEGENDARY NOTIFICATIONS & WEBHOOKS ROUTES COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Notifications routes completed at: 2025-08-06 18:00:31 UTC`);
console.log('🔔 Notifications API: SWISS PRECISION');
console.log('👑 RICKROLL187 founder notifications: LEGENDARY');
console.log('🔗 Webhooks system: MAXIMUM INTEGRATION');
console.log('🌅 EVENING LEGENDARY NOTIFICATIONS ENERGY: INFINITE AT 18:00:31!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
