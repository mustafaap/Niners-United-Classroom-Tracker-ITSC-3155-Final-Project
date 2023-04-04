CREATE TABLE IF NOT EXISTS rating(
    rating_id SERIAL PRIMARY KEY,
    restroom_name VARCHAR(255) NOT NULL,
    cleanliness INT NOT NULL,
    accessibility VARCHAR(255) NOT NULL,
    functionality BOOLEAN NOT NULL,
    overall INT NOT NULL,
    comments VARCHAR(255) NOT NULL
)