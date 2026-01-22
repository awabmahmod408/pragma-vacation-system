-- Add unbillable_days column to requests table
-- Run this in Supabase SQL Editor

ALTER TABLE requests ADD COLUMN IF NOT EXISTS unbillable_days INTEGER DEFAULT 0;

-- Add comment
COMMENT ON COLUMN requests.unbillable_days IS 'Number of vacation days that exceed the user available balance at the time of request';
