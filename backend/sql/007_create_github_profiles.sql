CREATE TABLE github_profiles (

    user_id UUID PRIMARY KEY,

    github_username VARCHAR(255) UNIQUE,

    public_repos INTEGER,

    followers INTEGER,

    total_stars INTEGER,

    languages JSONB,

    active_repos INTEGER,

    last_synced_at TIMESTAMP,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_github_profile_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);