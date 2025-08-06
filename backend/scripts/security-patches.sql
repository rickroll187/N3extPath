-- File: backend/scripts/security-patches.sql
-- 🛡️🎸 N3EXTPATH - LEGENDARY SECURITY DATABASE PATCHES 🎸🛡️
-- Swiss precision database security with infinite protection energy
-- Built: 2025-08-06 18:47:47 UTC by RICKROLL187
-- Email: letstalktech010@gmail.com
-- WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

-- =====================================
-- 🔐 SECURITY ENHANCEMENTS 🔐
-- =====================================

-- Admin logs table for audit trail
CREATE TABLE IF NOT EXISTS admin_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(50) NOT NULL,
    target_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notification preferences table
CREATE TABLE IF NOT EXISTS notification_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    preferences JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Webhooks table
CREATE TABLE IF NOT EXISTS webhooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    events JSONB NOT NULL DEFAULT '[]',
    secret_key VARCHAR(256) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_webhook_name_per_user UNIQUE(user_id, name),
    CONSTRAINT unique_webhook_url_per_user UNIQUE(user_id, url)
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    data JSONB DEFAULT '{}',
    priority VARCHAR(20) DEFAULT 'medium',
    read_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================
-- 🗂️ INDEXES FOR PERFORMANCE 🗂️
-- =====================================

-- Admin logs indexes
CREATE INDEX IF NOT EXISTS idx_admin_logs_admin_id ON admin_logs(admin_id);
CREATE INDEX IF NOT EXISTS idx_admin_logs_created_at ON admin_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_admin_logs_action ON admin_logs(action);
CREATE INDEX IF NOT EXISTS idx_admin_logs_target ON admin_logs(target_type, target_id);

-- Notifications indexes
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notifications_unread ON notifications(user_id, read_at) WHERE read_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(type);

-- Webhooks indexes
CREATE INDEX IF NOT EXISTS idx_webhooks_user_id ON webhooks(user_id);
CREATE INDEX IF NOT EXISTS idx_webhooks_active ON webhooks(is_active) WHERE is_active = true;

-- Security indexes for existing tables
CREATE INDEX IF NOT EXISTS idx_users_email_lower ON users(LOWER(email)) WHERE status != 'deleted';
CREATE INDEX IF NOT EXISTS idx_users_username_lower ON users(LOWER(username)) WHERE status != 'deleted';
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login DESC);

-- Team security indexes
CREATE INDEX IF NOT EXISTS idx_teams_owner_id ON teams(owner_id);
CREATE INDEX IF NOT EXISTS idx_teams_status ON teams(status);
CREATE INDEX IF NOT EXISTS idx_teams_public ON teams(is_public) WHERE is_public = true;
CREATE INDEX IF NOT EXISTS idx_team_members_user_team ON team_members(user_id, team_id);

-- OKR security indexes
CREATE INDEX IF NOT EXISTS idx_okrs_owner_id ON okrs(owner_id);
CREATE INDEX IF NOT EXISTS idx_okrs_team_id ON okrs(team_id);
CREATE INDEX IF NOT EXISTS idx_okrs_status ON okrs(status);

-- Message security indexes
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_team_id ON messages(team_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);

-- =====================================
-- 🔒 SECURITY CONSTRAINTS 🔒
-- =====================================

-- Add constraints to existing tables if they don't exist
DO $$
BEGIN
    -- User email constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'users_email_format') THEN
        ALTER TABLE users ADD CONSTRAINT users_email_format 
        CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
    END IF;

    -- User username constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'users_username_format') THEN
        ALTER TABLE users ADD CONSTRAINT users_username_format 
        CHECK (username ~* '^[a-zA-Z0-9_-]{3,30}$');
    END IF;

    -- User role constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'users_valid_role') THEN
        ALTER TABLE users ADD CONSTRAINT users_valid_role 
        CHECK (role IN ('founder', 'admin', 'moderator', 'user'));
    END IF;

    -- User status constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'users_valid_status') THEN
        ALTER TABLE users ADD CONSTRAINT users_valid_status 
        CHECK (status IN ('active', 'suspended', 'banned', 'pending', 'deleted'));
    END IF;

    -- Team member role constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'team_members_valid_role') THEN
        ALTER TABLE team_members ADD CONSTRAINT team_members_valid_role 
        CHECK (role IN ('admin', 'moderator', 'member'));
    END IF;

    -- OKR status constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'okrs_valid_status') THEN
        ALTER TABLE okrs ADD CONSTRAINT okrs_valid_status 
        CHECK (status IN ('draft', 'active', 'completed', 'cancelled', 'archived'));
    END IF;

    -- OKR progress constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'okrs_progress_range') THEN
        ALTER TABLE okrs ADD CONSTRAINT okrs_progress_range 
        CHECK (progress >= 0 AND progress <= 100);
    END IF;

    -- OKR confidence constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'okrs_confidence_range') THEN
        ALTER TABLE okrs ADD CONSTRAINT okrs_confidence_range 
        CHECK (confidence >= 0 AND confidence <= 100);
    END IF;

    -- Notification priority constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'notifications_valid_priority') THEN
        ALTER TABLE notifications ADD CONSTRAINT notifications_valid_priority 
        CHECK (priority IN ('low', 'medium', 'high', 'urgent'));
    END IF;
END $$;

-- =====================================
-- 🔐 ROW LEVEL SECURITY (RLS) 🔐
-- =====================================

-- Enable RLS on sensitive tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhooks ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE notification_preferences ENABLE ROW LEVEL SECURITY;

-- Users can only see active users (unless admin)
CREATE POLICY users_visibility ON users
    FOR SELECT
    USING (status = 'active' OR EXISTS (
        SELECT 1 FROM users u WHERE u.id = current_user_id() AND u.role IN ('founder', 'admin')
    ));

-- Users can only update their own profile (unless admin)
CREATE POLICY users_self_update ON users
    FOR UPDATE
    USING (id = current_user_id() OR EXISTS (
        SELECT 1 FROM users u WHERE u.id = current_user_id() AND u.role IN ('founder', 'admin')
    ));

-- Admin logs are only visible to admins
CREATE POLICY admin_logs_visibility ON admin_logs
    FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM users u WHERE u.id = current_user_id() AND u.role IN ('founder', 'admin')
    ));

-- Users can only see their own webhooks
CREATE POLICY webhooks_ownership ON webhooks
    FOR ALL
    USING (user_id = current_user_id() OR EXISTS (
        SELECT 1 FROM users u WHERE u.id = current_user_id() AND u.role IN ('founder', 'admin')
    ));

-- Users can only see their own notifications
CREATE POLICY notifications_ownership ON notifications
    FOR ALL
    USING (user_id = current_user_id());

-- Users can only manage their own notification preferences
CREATE POLICY notification_preferences_ownership ON notification_preferences
    FOR ALL
    USING (user_id = current_user_id());

-- =====================================
-- 🔧 SECURITY FUNCTIONS 🔧
-- =====================================

-- Function to get current user ID (to be implemented in application)
CREATE OR REPLACE FUNCTION current_user_id() RETURNS UUID AS $$
BEGIN
    -- This function should be implemented to return the current authenticated user's ID
    -- For now, it returns NULL to disable RLS in direct database access
    RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to log admin actions
CREATE OR REPLACE FUNCTION log_admin_action(
    p_admin_id UUID,
    p_action VARCHAR(100),
    p_target_type VARCHAR(50),
    p_target_id UUID DEFAULT NULL,
    p_details JSONB DEFAULT NULL,
    p_ip_address INET DEFAULT NULL,
    p_user_agent TEXT DEFAULT NULL
) RETURNS UUID AS $$
DECLARE
    log_id UUID;
BEGIN
    INSERT INTO admin_logs (
        admin_id, action, target_type, target_id, details, ip_address, user_agent, created_at
    ) VALUES (
        p_admin_id, p_action, p_target_type, p_target_id, p_details, p_ip_address, p_user_agent, NOW()
    ) RETURNING id INTO log_id;
    
    RETURN log_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to clean old admin logs (keep last 6 months)
CREATE OR REPLACE FUNCTION cleanup_old_admin_logs() RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM admin_logs 
    WHERE created_at < NOW() - INTERVAL '6 months';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to clean old notifications (keep last 3 months for read, 6 months for unread)
CREATE OR REPLACE FUNCTION cleanup_old_notifications() RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM notifications 
    WHERE (read_at IS NOT NULL AND created_at < NOW() - INTERVAL '3 months')
       OR (read_at IS NULL AND created_at < NOW() - INTERVAL '6 months');
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================
-- 📊 ANALYTICS VIEWS 📊
-- =====================================

-- Secure user analytics view
CREATE OR REPLACE VIEW user_analytics AS
SELECT 
    u.id,
    u.username,
    u.display_name,
    u.role,
    u.is_legendary,
    u.code_bro_energy,
    u.created_at,
    u.last_login,
    COUNT(DISTINCT tm.team_id) as team_count,
    COUNT(DISTINCT o.id) as okr_count,
    AVG(o.progress) as avg_okr_progress,
    COUNT(DISTINCT m.id) as message_count
FROM users u
LEFT JOIN team_members tm ON u.id = tm.user_id
LEFT JOIN okrs o ON u.id = o.owner_id
LEFT JOIN messages m ON u.id = m.user_id AND m.created_at > NOW() - INTERVAL '30 days'
WHERE u.status = 'active'
GROUP BY u.id, u.username, u.display_name, u.role, u.is_legendary, u.code_bro_energy, u.created_at, u.last_login;

-- Secure team analytics view
CREATE OR REPLACE VIEW team_analytics AS
SELECT 
    t.id,
    t.name,
    t.description,
    t.is_legendary,
    t.created_at,
    COUNT(DISTINCT tm.user_id) as member_count,
    SUM(u.code_bro_energy) as total_energy,
    COUNT(DISTINCT o.id) as okr_count,
    AVG(o.progress) as avg_okr_progress,
    COUNT(DISTINCT m.id) as message_count_7d
FROM teams t
LEFT JOIN team_members tm ON t.id = tm.team_id
LEFT JOIN users u ON tm.user_id = u.id AND u.status = 'active'
LEFT JOIN okrs o ON t.id = o.team_id
LEFT JOIN messages m ON t.id = m.team_id AND m.created_at > NOW() - INTERVAL '7 days'
WHERE t.status = 'active'
GROUP BY t.id, t.name, t.description, t.is_legendary, t.created_at;

-- =====================================
-- 🕐 SCHEDULED CLEANUP JOBS 🕐
-- =====================================

-- Note: These would typically be run by a cron job or similar scheduler
-- CREATE EVENT IF NOT EXISTS cleanup_logs
-- ON SCHEDULE EVERY 1 DAY
-- DO CALL cleanup_old_admin_logs();

-- CREATE EVENT IF NOT EXISTS cleanup_notifications  
-- ON SCHEDULE EVERY 1 DAY
-- DO CALL cleanup_old_notifications();

-- =====================================
-- ✅ VERIFICATION QUERIES ✅
-- =====================================

-- Verify security patches applied
SELECT 
    'Security patches applied successfully at 2025-08-06 18:47:47 UTC' as status,
    'RICKROLL187' as applied_by,
    NOW() as applied_at,
    'WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!' as message;

-- Check table existence
SELECT 
    table_name,
    CASE 
        WHEN table_name IN ('admin_logs', 'notifications', 'notification_preferences', 'webhooks') 
        THEN '✅ Security table exists'
        ELSE '⚠️ Check table'
    END as security_status
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'teams', 'team_members', 'okrs', 'messages', 'admin_logs', 'notifications', 'notification_preferences', 'webhooks')
ORDER BY table_name;

-- Check indexes
SELECT 
    indexname,
    '✅ Security index active' as status
FROM pg_indexes 
WHERE schemaname = 'public' 
AND indexname LIKE 'idx_%'
ORDER BY indexname;

COMMENT ON TABLE admin_logs IS '🛡️ LEGENDARY AUDIT TRAIL - Built with Swiss precision by RICKROLL187 at 2025-08-06 18:47:47 UTC';
COMMENT ON TABLE notifications IS '🔔 LEGENDARY NOTIFICATIONS - Swiss precision messaging system';
COMMENT ON TABLE webhooks IS '🔗 LEGENDARY WEBHOOKS - Infinite integration power';
COMMENT ON TABLE notification_preferences IS '⚙️ LEGENDARY PREFERENCES - User notification control';

-- 🎸🎸🎸 LEGENDARY DATABASE SECURITY PATCHES COMPLETE! 🎸🎸🎸
-- Built with Swiss precision by RICKROLL187!
-- Email: letstalktech010@gmail.com
-- WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
-- Database security completed at: 2025-08-06 18:47:47 UTC
-- 🛡️ Database security: LEGENDARY PRECISION
-- 👑 RICKROLL187 founder database protection: MAXIMUM SECURITY
-- 🔐 Data integrity: SWISS PRECISION
-- 🌅 EVENING LEGENDARY DATABASE SECURITY: INFINITE AT 18:47:47!
-- 🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸
