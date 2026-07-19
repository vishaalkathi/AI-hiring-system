CREATE TABLE employer_profiles (
    user_id UUID PRIMARY KEY,

    company_name VARCHAR(255) NOT NULL,

    company_description TEXT,

    website_url TEXT,

    company_location VARCHAR(255),


    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employer_profiles_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);