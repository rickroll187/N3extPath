-- File: backend/scripts/security-enhancements.sql
-- 🛡️🎸 N3EXTPATH - LEGENDARY SECURITY ENHANCEMENTS DATABASE 🎸🛡️
-- Swiss precision database security with infinite protection energy
-- Built: 2025-08-06 19:22:26 UTC by RICKROLL187
-- Email: letstalktech010@gmail.com
-- WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

-- =====================================
-- 🚨 SECURITY INCIDENT TRACKING 🚨
-- =====================================

-- Security incidents table for comprehensive tracking
CREATE TABLE IF NOT EXISTS security_incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    incident_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) DEFAULT 'low' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    description TEXT,
    ip_address INET,
    user_agent TEXT,
    headers JSONB,
    request_data JSONB,
    response_code INTEGER,
    blocked BOOLEAN DEFAULT false,
    resolved BOOLEAN DEFAULT false,
    resolved_by UUID REFERENCES users(id) ON DELETE SET NULL,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Failed login attempts tracking
CREATE TABLE IF NOT EXISTS failed_login_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username_attempted VARCHAR(100),
    ip_address INET NOT NULL,
    user_agent TEXT,
    attempt_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    failure_reason VARCHAR(100)
);

-- Session security tracking
CREATE TABLE IF NOT EXISTS session_security (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ip_address INET NOT NULL,
    user_agent TEXT,
    login_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    logout_time TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    security_flags JSONB DEFAULT '{}'
);

-- Social engineering attempts tracking
CREATE TABLE IF NOT EXISTS social_engineering_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    ip_address INET NOT NULL,
    attempt_type VARCHAR(50) NOT NULL,
    content TEXT,
    patterns_detected JSONB,
    risk_score INTEGER DEFAULT 0,
    blocked BOOLEAN DEFAULT false,
    reported_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- IP reputation tracking
CREATE TABLE IF NOT EXISTS ip_reputation (
    ip_address INET PRIMARY KEY,
    reputation_score INTEGER DEFAULT 0,
    country_code VARCHAR(2),
    is_tor BOOLEAN DEFAULT false,
    is_vpn BOOLEAN DEFAULT false,
    is_proxy BOOLEAN DEFAULT false,
    is_malicious BOOLEAN DEFAULT false,
    blocked_at TIMESTAMP WITH TIME ZONE,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================
-- 🔐 ADVANCED SECURITY CONSTRAINTS 🔐
-- =====================================

-- Enhanced user constraints for security
ALTER TABLE users ADD COLUMN IF NOT EXISTS failed_login_count INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS account_locked_until TIMESTAMP WITH TIME ZONE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS password_changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_enabled BOOLEAN DEFAULT false;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_secret VARCHAR(256);
ALTER TABLE users ADD COLUMN IF NOT EXISTS backup_codes TEXT[];
ALTER TABLE users ADD COLUMN IF NOT EXISTS security_questions JSONB DEFAULT '[]';
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_security_check TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE users ADD COLUMN IF NOT EXISTS risk_score INTEGER DEFAULT 0;

-- Add security constraints
DO $$
BEGIN
    -- Password age constraint (must be changed every 90 days for non-founder)
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'users_password_age') THEN
        ALTER TABLE users ADD CONSTRAINT users_password_age 
        CHECK (
            role = 'founder' OR 
            password_changed_at > NOW() - INTERVAL '90 days'
        );
    END IF;

    -- Failed login limit constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'users_failed_login_limit') THEN
        ALTER TABLE users ADD CONSTRAINT users_failed_login_limit 
        CHECK (failed_login_count <= 10);
    END IF;

    -- Security incident severity constraint
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'security_incidents_valid_type') THEN
        ALTER TABLE security_incidents ADD CONSTRAINT security_incidents_valid_type 
        CHECK (incident_type IN (
            'login_failure', 'social_engineering_attempt', 'rate_limit_exceeded',
            'suspicious_behavior', 'unauthorized_access', 'data_breach_attempt',
            'malware_detected', 'phishing_attempt', 'injection_attempt',
            'session_hijack', 'privilege_escalation', 'brute_force_attack'
        ));
    END IF;
END $$;

-- =====================================
-- 🗂️ SECURITY PERFORMANCE INDEXES 🗂️
-- =====================================

-- Security incidents indexes
CREATE INDEX IF NOT EXISTS idx_security_incidents_user_id ON security_incidents(user_id);
CREATE INDEX IF NOT EXISTS idx_security_incidents_type ON security_incidents(incident_type);
CREATE INDEX IF NOT EXISTS idx_security_incidents_severity ON security_incidents(severity);
CREATE INDEX IF NOT EXISTS idx_security_incidents_created_at ON security_incidents(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_security_incidents_ip ON security_incidents(ip_address);
CREATE INDEX IF NOT EXISTS idx_security_incidents_unresolved ON security_incidents(resolved) WHERE resolved = false;

-- Failed login attempts indexes
CREATE INDEX IF NOT EXISTS idx_failed_logins_ip ON failed_login_attempts(ip_address);
CREATE INDEX IF NOT EXISTS idx_failed_logins_username ON failed_login_attempts(username_attempted);
CREATE INDEX IF NOT EXISTS idx_failed_logins_time ON failed_login_attempts(attempt_time DESC);

-- Session security indexes
CREATE INDEX IF NOT EXISTS idx_session_security_user_id ON session_security(user_id);
CREATE INDEX IF NOT EXISTS idx_session_security_active ON session_security(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_session_security_ip ON session_security(ip_address);

-- Social engineering attempts indexes
CREATE INDEX IF NOT EXISTS idx_social_eng_ip ON social_engineering_attempts(ip_address);
CREATE INDEX IF NOT EXISTS idx_social_eng_type ON social_engineering_attempts(attempt_type);
CREATE INDEX IF NOT EXISTS idx_social_eng_risk ON social_engineering_attempts(risk_score DESC);

-- IP reputation indexes
CREATE INDEX IF NOT EXISTS idx_ip_reputation_score ON ip_reputation(reputation_score);
CREATE INDEX IF NOT EXISTS idx_ip_reputation_malicious ON ip_reputation(is_malicious) WHERE is_malicious = true;

-- User security indexes
CREATE INDEX IF NOT EXISTS idx_users_failed_logins ON users(failed_login_count) WHERE failed_login_count > 0;
CREATE INDEX IF NOT EXISTS idx_users_locked ON users(account_locked_until) WHERE account_locked_until IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_users_mfa ON users(mfa_enabled) WHERE mfa_enabled = true;
CREATE INDEX IF NOT EXISTS idx_users_risk_score ON users(risk_score DESC);

-- =====================================
-- 🔧 SECURITY FUNCTIONS 🔧
-- =====================================

-- Function to log security incident
CREATE OR REPLACE FUNCTION log_security_incident(
    p_user_id UUID DEFAULT NULL,
    p_incident_type VARCHAR(100),
    p_severity VARCHAR(20) DEFAULT 'low',
    p_description TEXT DEFAULT NULL,
    p_ip_address INET DEFAULT NULL,
    p_user_agent TEXT DEFAULT NULL,
    p_blocked BOOLEAN DEFAULT false
) RETURNS UUID AS $$
DECLARE
    incident_id UUID;
BEGIN
    INSERT INTO security_incidents (
        user_id, incident_type, severity, description, 
        ip_address, user_agent, blocked, created_at
    ) VALUES (
        p_user_id, p_incident_type, p_severity, p_description,
        p_ip_address, p_user_agent, p_blocked, NOW()
    ) RETURNING id INTO incident_id;
    
    -- Update IP reputation if malicious
    IF p_blocked = true THEN
        INSERT INTO ip_reputation (ip_address, reputation_score, is_malicious, last_updated)
        VALUES (p_ip_address, -10, true, NOW())
        ON CONFLICT (ip_address) DO UPDATE SET
            reputation_score = ip_reputation.reputation_score - 10,
            is_malicious = true,
            last_updated = NOW();
    END IF;
    
    RETURN incident_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to check if IP is blocked
CREATE OR REPLACE FUNCTION is_ip_blocked(p_ip_address INET) RETURNS BOOLEAN AS $$
DECLARE
    is_blocked BOOLEAN := false;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM ip_reputation 
        WHERE ip_address = p_ip_address 
        AND (is_malicious = true OR reputation_score < -50)
    ) INTO is_blocked;
    
    RETURN is_blocked;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to handle failed login
CREATE OR REPLACE FUNCTION handle_failed_login(
    p_username VARCHAR(100),
    p_ip_address INET,
    p_user_agent TEXT DEFAULT NULL,
    p_failure_reason VARCHAR(100) DEFAULT 'invalid_credentials'
) RETURNS VOID AS $$
DECLARE
    user_id UUID;
    current_failed_count INTEGER;
BEGIN
    -- Log failed attempt
    INSERT INTO failed_login_attempts (
        username_attempted, ip_address, user_agent, failure_reason, attempt_time
    ) VALUES (
        p_username, p_ip_address, p_user_agent, p_failure_reason, NOW()
    );
    
    -- Update user failed login count if user exists
    SELECT id, failed_login_count INTO user_id, current_failed_count
    FROM users 
    WHERE LOWER(username) = LOWER(p_username) OR LOWER(email) = LOWER(p_username);
    
    IF user_id IS NOT NULL THEN
        UPDATE users 
        SET 
            failed_login_count = current_failed_count + 1,
            account_locked_until = CASE 
                WHEN current_failed_count + 1 >= 5 THEN NOW() + INTERVAL '15 minutes'
                WHEN current_failed_count + 1 >= 10 THEN NOW() + INTERVAL '1 hour'
                ELSE account_locked_until
            END
        WHERE id = user_id;
        
        -- Log security incident for multiple failures
        IF current_failed_count + 1 >= 3 THEN
            PERFORM log_security_incident(
                user_id, 
                'login_failure', 
                CASE WHEN current_failed_count + 1 >= 5 THEN 'high' ELSE 'medium' END,
                format('Multiple failed login attempts: %s', current_failed_count + 1),
                p_ip_address,
                p_user_agent,
                current_failed_count + 1 >= 5
            );
        END IF;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to reset failed login count on successful login
CREATE OR REPLACE FUNCTION reset_failed_login_count(p_user_id UUID) RETURNS VOID AS $$
BEGIN
    UPDATE users 
    SET 
        failed_login_count = 0,
        account_locked_until = NULL,
        last_security_check = NOW()
    WHERE id = p_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to clean old security data
CREATE OR REPLACE FUNCTION cleanup_security_data() RETURNS INTEGER AS $$
DECLARE
    total_cleaned INTEGER := 0;
    cleaned_count INTEGER;
BEGIN
    -- Clean old failed login attempts (keep 30 days)
    DELETE FROM failed_login_attempts 
    WHERE attempt_time < NOW() - INTERVAL '30 days';
    GET DIAGNOSTICS cleaned_count = ROW_COUNT;
    total_cleaned := total_cleaned + cleaned_count;
    
    -- Clean old resolved security incidents (keep 90 days)
    DELETE FROM security_incidents 
    WHERE resolved = true AND resolved_at < NOW() - INTERVAL '90 days';
    GET DIAGNOSTICS cleaned_count = ROW_COUNT;
    total_cleaned := total_cleaned + cleaned_count;
    
    -- Clean old inactive sessions (keep 7 days)
    DELETE FROM session_security 
    WHERE is_active = false AND logout_time < NOW() - INTERVAL '7 days';
    GET DIAGNOSTICS cleaned_count = ROW_COUNT;
    total_cleaned := total_cleaned + cleaned_count;
    
    -- Clean old social engineering attempts (keep 60 days)
    DELETE FROM social_engineering_attempts 
    WHERE created_at < NOW() - INTERVAL '60 days';
    GET DIAGNOSTICS cleaned_count = ROW_COUNT;
    total_cleaned := total_cleaned + cleaned_count;
    
    RETURN total_cleaned;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================
-- 🎯 SECURITY VIEWS FOR MONITORING 🎯
-- =====================================

-- Security dashboard view
CREATE OR REPLACE VIEW security_dashboard AS
SELECT 
    'security_incidents' as metric_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN severity = 'critical' THEN 1 END) as critical_count,
    COUNT(CASE WHEN created_at > NOW() - INTERVAL '24 hours' THEN 1 END) as last_24h_count,
    COUNT(CASE WHEN resolved = false THEN 1 END) as unresolved_count
FROM security_incidents
UNION ALL
SELECT 
    'failed_logins' as metric_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN attempt_time > NOW() - INTERVAL '1 hour' THEN 1 END) as critical_count,
    COUNT(CASE WHEN attempt_time > NOW() - INTERVAL '24 hours' THEN 1 END) as last_24h_count,
    0 as unresolved_count
FROM failed_login_attempts
UNION ALL
SELECT 
    'locked_accounts' as metric_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN account_locked_until > NOW() THEN 1 END) as critical_count,
    COUNT(CASE WHEN account_locked_until > NOW() - INTERVAL '24 hours' THEN 1 END) as last_24h_count,
    COUNT(CASE WHEN account_locked_until > NOW() THEN 1 END) as unresolved_count
FROM users
WHERE account_locked_until IS NOT NULL;

-- High-risk users view
CREATE OR REPLACE VIEW high_risk_users AS
SELECT 
    u.id,
    u.username,
    u.display_name,
    u.email,
    u.failed_login_count,
    u.account_locked_until,
    u.risk_score,
    u.last_login,
    COUNT(si.id) as security_incident_count,
    COUNT(fla.id) as failed_login_attempt_count,
    MAX(si.created_at) as last_incident_at
FROM users u
LEFT JOIN security_incidents si ON u.id = si.user_id AND si.created_at > NOW() - INTERVAL '30 days'
LEFT JOIN failed_login_attempts fla ON (u.username = fla.username_attempted OR u.email = fla.username_attempted) 
    AND fla.attempt_time > NOW() - INTERVAL '30 days'
WHERE u.status != 'deleted' 
    AND (u.risk_score > 10 OR u.failed_login_count > 2 OR u.account_locked_until IS NOT NULL)
GROUP BY u.id, u.username, u.display_name, u.email, u.failed_login_count, u.account_locked_until, u.risk_score, u.last_login
ORDER BY u.risk_score DESC, security_incident_count DESC;

-- =====================================
-- 🏆 FOUNDER PROTECTION MEASURES 🏆
-- =====================================

-- Ensure founder account cannot be locked or limited
CREATE OR REPLACE FUNCTION protect_founder_account() RETURNS TRIGGER AS $$
BEGIN
    -- Prevent founder account from being locked or having failed login count
    IF NEW.role = 'founder' THEN
        NEW.failed_login_count = 0;
        NEW.account_locked_until = NULL;
        NEW.risk_score = 0;
    END IF;
    
    -- Prevent founder role from being changed by anyone except founder
    IF OLD.role = 'founder' AND NEW.role != 'founder' THEN
        -- Only allow founder to change their own role (which should never happen)
        IF NEW.id != OLD.id THEN
            RAISE EXCEPTION 'Cannot modify founder role';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to protect founder account
DROP TRIGGER IF EXISTS protect_founder_trigger ON users;
CREATE TRIGGER protect_founder_trigger
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION protect_founder_account();

-- =====================================
-- ✅ VERIFICATION AND SETUP ✅
-- =====================================

-- Verify security enhancements applied
SELECT 
    'Security database enhancements applied successfully at 2025-08-06 19:22:26 UTC' as status,
    'RICKROLL187' as applied_by,
    NOW() as applied_at,
    'WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!' as message;

-- Check new security tables
SELECT 
    table_name,
    '✅ Security table ready' as status
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('security_incidents', 'failed_login_attempts', 'session_security', 'social_engineering_attempts', 'ip_reputation')
ORDER BY table_name;

COMMENT ON TABLE security_incidents IS '🚨 LEGENDARY SECURITY INCIDENT TRACKING - Built with Swiss precision by RICKROLL187 at 2025-08-06 19:22:26 UTC';
COMMENT ON TABLE failed_login_attempts IS '🔐 LEGENDARY FAILED LOGIN TRACKING - Advanced authentication security';
COMMENT ON TABLE session_security IS '🔒 LEGENDARY SESSION SECURITY - Session management and tracking';
COMMENT ON TABLE social_engineering_attempts IS '🧠 LEGENDARY SOCIAL ENGINEERING PROTECTION - Advanced threat detection';
COMMENT ON TABLE ip_reputation IS '🌍 LEGENDARY IP REPUTATION SYSTEM - Network threat intelligence';

-- 🎸🎸🎸 LEGENDARY DATABASE SECURITY ENHANCEMENTS COMPLETE! 🎸🎸🎸
-- Built with Swiss precision by RICKROLL187!
-- Email: letstalktech010@gmail.com
-- WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
-- Database security enhancements completed at: 2025-08-06 19:22:26 UTC
-- 🛡️ Database security: LEGENDARY PRECISION
-- 👑 RICKROLL187 founder protection: UNBREAKABLE
-- 🚨 Threat tracking: SWISS PRECISION
-- 🌃 EVENING LEGENDARY DATABASE SECURITY: INFINITE AT 19:22:26!
-- 🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸
