ALTER TABLE candidate_profiles
ADD COLUMN parsed_role TEXT,
ADD COLUMN parsed_skills JSONB,
ADD COLUMN parsed_experience DECIMAL(4,1),
ADD COLUMN resume_parsed_at TIMESTAMP;