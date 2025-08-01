-- Migration: Fix RLS security issue for spatial_ref_sys table
-- Date: 2025-08-01
-- Description: Enable Row Level Security on spatial_ref_sys table and create read-only policy for authenticated users

-- Enable Row Level Security on the spatial_ref_sys table
ALTER TABLE public.spatial_ref_sys ENABLE ROW LEVEL SECURITY;

-- Create a basic read-only policy for authenticated users
-- This allows all authenticated users to read spatial reference system data
CREATE POLICY "Allow authenticated users to read spatial_ref_sys"
ON public.spatial_ref_sys
FOR SELECT
TO authenticated
USING (true);

-- Allow service role full access to spatial_ref_sys
-- This policy allows the service role to perform all operations
CREATE POLICY "Allow service role full access to spatial_ref_sys"
ON public.spatial_ref_sys
FOR ALL
TO service_role
USING (true);

-- Note: The spatial_ref_sys table is a PostGIS system table that contains
-- spatial reference system definitions. Regular users have read-only access,
-- while the service role has full access for administrative operations.
