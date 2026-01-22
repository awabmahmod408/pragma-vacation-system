-- Employee Vacation Management System - Database Schema
-- Run this in the Supabase SQL Editor

-- 1. Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'employee')),
    total_allowance INTEGER NOT NULL DEFAULT 21,
    balance INTEGER NOT NULL DEFAULT 21,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create requests table
CREATE TABLE IF NOT EXISTS requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days_taken INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_requests_user_id ON requests(user_id);
CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status);
CREATE INDEX IF NOT EXISTS idx_requests_created_at ON requests(created_at DESC);

-- 4. Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_requests_updated_at
    BEFORE UPDATE ON requests
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 5. Insert default admin user (password: admin123)
-- Note: This is a bcrypt hash of 'admin123' - CHANGE THIS IN PRODUCTION!
INSERT INTO users (username, password_hash, role, total_allowance, balance)
VALUES (
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqL.MplI2e',
    'admin',
    0,
    0
)
ON CONFLICT (username) DO NOTHING;

-- 6. Insert sample employees for testing (password: password123)
-- Note: These use bcrypt hash of 'password123' - CHANGE OR REMOVE IN PRODUCTION!
INSERT INTO users (username, password_hash, role, total_allowance, balance)
VALUES 
    ('john.doe', '$2b$12$rQvsJ7mXHaIGyGQqKqT8f.yN/8yLPQpXuL7QFqLVBHaQW6bZqbXCe', 'employee', 21, 21),
    ('jane.smith', '$2b$12$rQvsJ7mXHaIGyGQqKqT8f.yN/8yLPQpXuL7QFqLVBHaQW6bZqbXCe', 'employee', 21, 21),
    ('bob.johnson', '$2b$12$rQvsJ7mXHaIGyGQqKqT8f.yN/8yLPQpXuL7QFqLVBHaQW6bZqbXCe', 'employee', 21, 21)
ON CONFLICT (username) DO NOTHING;

-- 7. Enable Row Level Security (RLS) for additional security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE requests ENABLE ROW LEVEL SECURITY;

-- 8. Create RLS policies
-- Policy: Users can read their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT
    USING (true); -- We'll handle authorization in the application layer

-- Policy: All authenticated users can read all requests (admin screens need this)
CREATE POLICY "Users can view requests" ON requests
    FOR SELECT
    USING (true);

-- Policy: Users can insert their own requests
CREATE POLICY "Users can create requests" ON requests
    FOR INSERT
    WITH CHECK (true);

-- Policy: Users can update requests (admin approval/rejection)
CREATE POLICY "Users can update requests" ON requests
    FOR UPDATE
    USING (true);

-- Policy: Allow updates to users table (for balance updates)
CREATE POLICY "Allow user updates" ON users
    FOR UPDATE
    USING (true);
