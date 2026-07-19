CREATE INDEX idx_jobs_employer
ON jobs(employer_user_id);

CREATE INDEX idx_jobs_status
ON jobs(status);

CREATE INDEX idx_applications_candidate
ON applications(candidate_user_id);

CREATE INDEX idx_applications_job
ON applications(job_id);