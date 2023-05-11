DROP TABLE IF EXISTS comment_votes;
DROP TABLE IF EXISTS rating_votes;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    favorite VARCHAR(255),
    picture VARCHAR(255),
    commented_on INTEGER[] DEFAULT '{}',
    rupvoted_on INTEGER[] DEFAULT '{}',
    rdownvoted_on INTEGER[] DEFAULT '{}',
    cupvoted_on INTEGER[] DEFAULT '{}',
    cdownvoted_on INTEGER[] DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS rating(
    rating_id SERIAL PRIMARY KEY,
    restroom_name VARCHAR(255),
    rating_body TEXT,
    cleanliness DECIMAL(2,1),
    accessibility VARCHAR[] DEFAULT '{}',
    functionality BOOLEAN,
    overall DECIMAL(2,1),
    map_tag VARCHAR(255),
    votes INTEGER DEFAULT 0,
    rater_id INTEGER,
    comments INTEGER[] DEFAULT '{}',
    FOREIGN KEY (rater_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments(
    comment_id SERIAL PRIMARY KEY,
    comment_body TEXT,
    user_id INT,
    rating_id INT,
    total_votes INT DEFAULT 0,
    comment_id_vote INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (rating_id) REFERENCES rating(rating_id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id_vote) REFERENCES comments(comment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rating_votes(
    vote_id INT PRIMARY KEY, --New primary key
    rating_id INT,
    upvotes INT, --Add default = 0
    downvotes INT, --Add default = 0
    user_id INT,
    rating_id_vote INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (rating_id_vote) REFERENCES rating(rating_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comment_votes(
    comment_id INT PRIMARY KEY,
    upvotes INT,
    downvotes INT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE
);