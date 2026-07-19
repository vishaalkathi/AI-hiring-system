CREATE TABLE candidate_education (
    education_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    degree VARCHAR(100),

    field_of_study VARCHAR(150),

    institution VARCHAR(255),

    start_year INTEGER,

    graduation_year INTEGER,

    cgpa DECIMAL(3,2),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_candidate_education_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);