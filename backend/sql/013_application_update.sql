ALTER TABLE applications
ADD COLUMN resume_url_snapshot TEXT,
ADD COLUMN resume_text_snapshot TEXT,
ADD COLUMN parsed_role_snapshot TEXT,
ADD COLUMN parsed_skills_snapshot JSONB,
ADD COLUMN parsed_experience_snapshot DECIMAL(4,1);