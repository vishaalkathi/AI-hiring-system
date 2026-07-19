CREATE TABLE leetcode_profiles (

    user_id UUID PRIMARY KEY,

    leetcode_username VARCHAR(255) UNIQUE,

    -- Language features
    language_diversity INTEGER,

    language_list JSONB,

    primary_language VARCHAR(100),

    primary_language_share DECIMAL(6,5),


    -- Skill/tag features
    skill_stats JSONB,


    -- Contest features
    contest_rating INTEGER,

    contest_rank_percentile DECIMAL(6,2),

    contest_attended INTEGER,


    -- Problem solving features
    total_solved INTEGER,

    easy_solved INTEGER,

    medium_solved INTEGER,

    hard_solved INTEGER,


    -- Consistency features
    streak INTEGER,

    active_days INTEGER,


    last_synced_at TIMESTAMP,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_leetcode_profile_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);