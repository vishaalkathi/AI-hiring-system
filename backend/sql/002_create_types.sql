CREATE TYPE user_role AS ENUM (
    'CANDIDATE',
    'EMPLOYER',
    'ADMIN'
);

CREATE TYPE job_status AS ENUM (
    'OPEN',
    'CLOSED',
    'DRAFT'
);

CREATE TYPE application_status AS ENUM (
    'PENDING',
    'SHORTLISTED',
    'REJECTED',
    'HIRED'
);