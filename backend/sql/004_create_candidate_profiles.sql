CREATE TABLE candidate_profiles (

    user_id UUID PRIMARY KEY,

    phone VARCHAR(20),

    current_location VARCHAR(255),

    linkedin_url TEXT,

    portfolio_url TEXT,

    resume_url TEXT,

    resume_text TEXT,

    predicted_score DECIMAL(6,2),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_candidate_profile_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);