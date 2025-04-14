-- migrate:up
INSERT INTO users (name, role, email, password, created_at, updated_at, deleted_at)
VALUES (
    'string',
    'admin',
    'string@gmail.com',
    '$argon2id$v=19$m=65536,t=3,p=4$e3ySTacZNvWYycldUVjeTw$SgORFB4piQPpbl0qIJQZrwztK0YdgIj5yAXM3hIcIPo',
    '2025-04-09 21:52:01.44675+00',
    NULL,
    NULL
);

-- migrate:down
DELETE FROM users
WHERE
    name = 'string' AND
    role = 'admin' AND
    email = 'string@gmail.com' AND
    password = '$argon2id$v=19$m=65536,t=3,p=4$e3ySTacZNvWYycldUVjeTw$SgORFB4piQPpbl0qIJQZrwztK0YdgIj5yAXM3hIcIPo' AND
    created_at = '2025-04-09 21:52:01.44675+00';
