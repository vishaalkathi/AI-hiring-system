CREATE TABLE jobs (

    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    employer_user_id UUID NOT NULL,


    -- Job information

    title VARCHAR(255) NOT NULL,

    description TEXT NOT NULL,

    location VARCHAR(255),

    employment_type VARCHAR(50),

    experience_required VARCHAR(100),


    -- AI matching features

    required_skills JSONB,

    preferred_skills JSONB,


    -- Job lifecycle

    status VARCHAR(50) NOT NULL DEFAULT 'OPEN',


    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_job_employer
        FOREIGN KEY (employer_user_id)
        REFERENCES employer_profiles(user_id)
        ON DELETE CASCADE

);