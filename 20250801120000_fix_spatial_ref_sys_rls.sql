-- Fix RLS security issue for spatial_ref_sys table
ALTER TABLE public.spatial_ref_sys ENABLE ROW LEVEL SECURITY;

-- Create a basic read-only policy for authenticated users
CREATE POLICY "Allow authenticated users to read spatial_ref_sys"
ON public.spatial_ref_sys
FOR SELECT
TO authenticated
USING (true);

-- Allow service role full access to spatial_ref_sys
CREATE POLICY "Allow service role full access to spatial_ref_sys"
ON public.spatial_ref_sys
FOR ALL
TO service_role
USING (true);
