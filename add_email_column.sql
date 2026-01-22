-- Update Users Table to include Email
-- Run this in Supabase SQL Editor

ALTER TABLE users ADD COLUMN IF NOT EXISTS email TEXT;

-- Update existing sample users with placeholder emails
UPDATE users SET email = 'admin@example.com' WHERE username = 'admin';
UPDATE users SET email = 'john.doe@example.com' WHERE username = 'john.doe';
UPDATE users SET email = 'jane.smith@example.com' WHERE username = 'jane.smith';
UPDATE users SET email = 'bob.johnson@example.com' WHERE username = 'bob.johnson';

-- Add comment
COMMENT ON COLUMN users.email IS 'Email address for sending vacation request status updates';
