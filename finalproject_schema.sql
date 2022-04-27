-- DROP DATABASE IF EXISTS cinemaholics_db;
CREATE DATABASE IF NOT EXISTS cinemaholics_db;
USE cinemaholics_db;

CREATE TABLE IF NOT EXISTS users (
    user_id   INT           AUTO_INCREMENT,
    username  VARCHAR(255)  NOT NULL,
    email     VARCHAR(255)  NOT NULL,
    passkey   VARCHAR(255)  NOT NULL,
    pfp       VARCHAR(255)  NOT NULL,
    about     TEXT(65535)   NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS posts (
    post_id    INT           AUTO_INCREMENT,
    user_id    INT           NOT NULL,
    title      VARCHAR(255)  NOT NULL,
    body       TEXT(65535)   NOT NULL,
    post_time  VARCHAR(255)  NOT NULL,
    likes      INT           NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS replies (
	reply_id   INT            AUTO_INCREMENT,
    post_id    INT            NOT NULL,
    user_id    INT            NOT NULL,
    body       TEXT(65535)    NOT NULL,
    post_time  VARCHAR(255)   NOT NULL,
    likes      INT            NOT NULL,
    PRIMARY KEY (reply_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE IF NOT EXISTS movie (
	movie_id     INT,
	poster_url   VARCHAR(500),
    PRIMARY KEY (movie_id)
);

CREATE TABLE IF NOT EXISTS user_ratings (
    user_id      INT,
    movie_id     INT,
    user_rating  FLOAT,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
);

CREATE TABLE IF NOT EXISTS edits (
    edit_id    INT AUTO_INCREMENT,
    user_id       INT NOT NULL,
    post_id     INT,
	reply_id     INT,
    reason  VARCHAR(255)   NOT NULL,
    time  VARCHAR(255)   NOT NULL,
    PRIMARY KEY (edit_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (reply_id) REFERENCES replies(reply_id)
    
);

CREATE TABLE IF NOT EXISTS watchlist (
    user_id    INT,
    movie_id       INT,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
);