DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS rating(
    rating_id SERIAL PRIMARY KEY,
    restroom_name VARCHAR(255),
    rating_body TEXT,
    cleanliness DECIMAL(2,1),
    accessibility VARCHAR(255),
    functionality BOOLEAN,
    overall DECIMAL(2,1),
    map_tag VARCHAR(255),
    votes INTEGER,
    rater_id INTEGER,
    FOREIGN KEY (rater_id) REFERENCES users(user_id)
    --When votes table is created, add FK
);

CREATE TABLE IF NOT EXISTS users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    favorite VARCHAR(255),
    picture VARCHAR(255)
);