-- 🗄️🎸 N3EXTPATH - LEGENDARY DATABASE INITIALIZATION 🎸🗄️
-- More structured than Swiss architecture with legendary database design!
-- CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
-- Built by legendary code bros RICKROLL187 🎸

-- Create legendary database extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create legendary schemas
CREATE SCHEMA IF NOT EXISTS n3extpath;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS monitoring;

-- Set legendary search path
SET search_path TO n3extpath, public;

-- Create legendary admin user for RICKROLL187
INSERT INTO users (
    username, 
    email, 
    hashed_password, 
    is_active, 
    is_admin, 
    is_legendary,
    created_at,
    legendary_factor
) VALUES (
    'rickroll187',
    'rickroll187@legendary.dev',
    '$2b$12$legendary_hashed_password_here',
    true,
    true,
    true,
    NOW(),
    'BUILT THE ENTIRE LEGENDARY PLATFORM! 🎸🏆'
) ON CONFLICT (username) DO NOTHING;

-- Create legendary indexes for performance
CREATE INDEX IF NOT EXISTS idx_paths_creator_id ON paths(creator_id);
CREATE INDEX IF NOT EXISTS idx_paths_status ON paths(status);
CREATE INDEX IF NOT EXISTS idx_paths_legendary ON paths(code_bro_approved, legendary_factor);
CREATE INDEX IF NOT EXISTS idx_waypoints_path_id ON waypoints(path_id);
CREATE INDEX IF NOT EXISTS idx_waypoints_sequence ON waypoints(path_id, sequence_order);
CREATE INDEX IF NOT EXISTS idx_enrollments_user_id ON path_enrollments(user_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_path_id ON path_enrollments(path_id);
CREATE INDEX IF NOT EXISTS idx_completions_user_id ON waypoint_completions(user_id);

-- Create legendary full-text search indexes
CREATE INDEX IF NOT EXISTS idx_paths_search ON paths USING gin(to_tsvector('english', name || ' ' || description));
CREATE INDEX IF NOT EXISTS idx_waypoints_search ON waypoints USING gin(to_tsvector('english', name || ' ' || description));

-- Create legendary analytics views
CREATE OR REPLACE VIEW analytics.legendary_path_stats AS
SELECT 
    p.path_id,
    p.name,
    p.creator_id,
    COUNT(pe.id) as total_enrollments,
    COUNT(CASE WHEN pe.status = 'completed' THEN 1 END) as total_completions,
    ROUND(
        COUNT(CASE WHEN pe.status = 'completed' THEN 1 END)::numeric / 
        NULLIF(COUNT(pe.id), 0) * 100, 2
    ) as completion_rate,
    AVG(pr.overall_rating) as average_rating,
    p.legendary_factor,
    p.code_bro_approved
FROM paths p
LEFT JOIN path_enrollments pe ON p.id = pe.path_id
LEFT JOIN path_reviews pr ON p.id = pr.path_id
GROUP BY p.id, p.path_id, p.name, p.creator_id, p.legendary_factor, p.code_bro_approved;

-- Create legendary monitoring table
CREATE TABLE IF NOT EXISTS monitoring.system_health (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    response_time_ms INTEGER,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    legendary_factor TEXT,
    checked_at TIMESTAMP DEFAULT NOW()
);

-- Insert legendary system health check
INSERT INTO monitoring.system_health (
    service_name, 
    status, 
    response_time_ms, 
    legendary_factor
) VALUES (
    'n3extpath-core',
    'LEGENDARY',
    1,
    'INITIALIZED BY RICKROLL187 WITH SWISS PRECISION! 🎸🏆'
);

-- Create legendary stored procedures
CREATE OR REPLACE FUNCTION get_legendary_user_stats(user_id_param INTEGER)
RETURNS TABLE(
    total_paths_created INTEGER,
    total_paths_enrolled INTEGER,
    total_paths_completed INTEGER,
    total_experience_points INTEGER,
    legendary_status TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*)::INTEGER FROM paths WHERE creator_id = user_id_param),
        (SELECT COUNT(*)::INTEGER FROM path_enrollments WHERE user_id = user_id_param),
        (SELECT COUNT(*)::INTEGER FROM path_enrollments WHERE user_id = user_id_param AND status = 'completed'),
        (SELECT COALESCE(SUM(experience_points_earned), 0)::INTEGER FROM path_enrollments WHERE user_id = user_id_param),
        CASE 
            WHEN user_id_param = 1 THEN 'RICKROLL187 - THE LEGENDARY CREATOR! 🎸🏆'
            ELSE 'CODE BRO IN TRAINING! 💪'
        END;
END;
$$ LANGUAGE plpgsql;

-- Create legendary database cleanup function
CREATE OR REPLACE FUNCTION cleanup_legendary_logs()
RETURNS void AS $$
BEGIN
    -- Clean up old monitoring data (keep last 30 days)
    DELETE FROM monitoring.system_health 
    WHERE checked_at < NOW() - INTERVAL '30 days';
    
    -- Update statistics
    ANALYZE;
    
    -- Log the cleanup
    INSERT INTO monitoring.system_health (
        service_name, 
        status, 
        legendary_factor
    ) VALUES (
        'database-cleanup',
        'COMPLETED',
        'CLEANED UP BY LEGENDARY DATABASE MAINTENANCE! 🧹🏆'
    );
END;
$$ LANGUAGE plpgsql;

-- Create legendary comment
COMMENT ON DATABASE n3extpath_legendary IS 'The most legendary path platform database built by RICKROLL187! 🎸🏆';

-- === LEGENDARY DATABASE JOKE ===
-- Why did the database become legendary?
-- Because it was initialized by RICKROLL187 with Swiss precision and code bro humor! 🗄️🎸
