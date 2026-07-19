CREATE TABLE applications (

    application_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),


    candidate_user_id UUID NOT NULL,

    job_id UUID NOT NULL,


    application_status VARCHAR(50) NOT NULL DEFAULT 'APPLIED',


    match_score DECIMAL(6,2),


    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_application_candidate
        FOREIGN KEY (candidate_user_id)
        REFERENCES candidate_profiles(user_id)
        ON DELETE CASCADE,


    CONSTRAINT fk_application_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE,


    CONSTRAINT unique_candidate_job_application
        UNIQUE(candidate_user_id, job_id)

);