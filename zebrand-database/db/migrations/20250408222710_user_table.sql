-- migrate:up
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    role VARCHAR(10) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

INSERT INTO users (name, role, email, password, created_at, updated_at, deleted_at)
VALUES (
    'string',
    'admin',
    'string@gmail.com',
    '$argon2id$v=19$m=65536,t=3,p=4$6XdAjxvZbBBR0Rq2F1mTqQ$719IiYlnPMB4aVWMK2o2vLuJoYmm18S6/46RgG4iYO0',
    '2025-04-09 21:52:01.44675+00',
    NULL,
    NULL
);

-- migrate:down
DROP TABLE IF EXISTS users;
