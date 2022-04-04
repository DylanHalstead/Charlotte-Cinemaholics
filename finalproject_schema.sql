DROP DATABASE IF EXISTS cinemaholics_db;
CREATE DATABASE cinemaholics_db;
USE cinemaholics_db;

CREATE TABLE IF NOT EXISTS users (
    users_id   INT           AUTO_INCREMENT,
    username  VARCHAR(255)  NOT NULL,
    email     VARCHAR(255)  NOT NULL,
    passkey   VARCHAR(255)  NOT NULL,
    pfp       VARCHAR(255)  NOT NULL,
    about     TEXT(65535)   NULL,
    PRIMARY KEY (user_id)    
);

CREATE TABLE IF NOT EXISTS posts (
    post_id    INT           AUTO_INCREMENT,
    users_id   INT           NOT NULL,
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
    users_id   INT            NOT NULL,
    body       TEXT(65535)    NOT NULL,
    post_time  VARCHAR(255)   NOT NULL,
    likes      INT            NOT NULL,
    PRIMARY KEY (reply_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE IF NOT EXISTS users_playlist  (
	users_id     INT,
	playlist_id  INT,
    PRIMARY KEY (users_id, playlist_id),
    FOREIGN KEY (users_id) REFERENCES users(users_id),
    FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id)
);

CREATE TABLE IF NOT EXISTS playlist  (
	playlist_id     INT             AUTO_INCREMENT,
    playlist_name   VARCHAR(255),
    PRIMARY KEY (playlist_id)
);

CREATE TABLE IF NOT EXISTS playlist_movie (
    playlist_id    INT,
    movie_id       INT,
    PRIMARY KEY (playlist_id, movie_id),
    FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
);

CREATE TABLE IF NOT EXISTS movie  (
	-- poster_URL, title, IMDB_rating, genre, etc... will all come from the movie_id (used to find IMDB page)
	movie_id     INT,
    UNCC_rating  DECIMAL,
    PRIMARY KEY (movie_id)
);