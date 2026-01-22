-- Audit Log System - Database Schema
-- Run this in Supabase SQL Editor to create the audit log table

-- Create audit_logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    username TEXT NOT NULL,
    action_type TEXT NOT NULL,  -- 'LOGIN', 'LOGOUT', 'REQUEST_CREATE', 'REQUEST_APPROVE', 'REQUEST_REJECT', 'USER_CREATE', 'USER_UPDATE', 'USER_DELETE'
    action_details TEXT,  -- JSON or text description of the action
    ip_address TEXT,  -- Optional: for security tracking
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action_type ON audit_logs(action_type);

-- Add RLS policy to allow all operations (we handle authorization in app)
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all operations on audit_logs" ON audit_logs
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Add comment
COMMENT ON TABLE audit_logs IS 'System audit log for tracking all user activities and admin operations';
