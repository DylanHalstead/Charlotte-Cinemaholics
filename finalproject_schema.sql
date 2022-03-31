-- Re/create DB
DROP DATABASE IF EXISTS final;
CREATE DATABASE final;
USE final;


CREATE TABLE users (
    user_id INT AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    user_pfp VARCHAR(255) NOT NULL,
    user_about TEXT(65535),
    PRIMARY KEY (user_id)    
);

CREATE TABLE posts (
    post_id INT AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(255) NOT NULL,
    body    TEXT(65535) NOT NULL,
    post_time VARCHAR(255) NOT NULL,
    likes   INT NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE replies (
	reply_id INT AUTO_INCREMENT,
    post_id INT,
    user_id INT,
    body TEXT(65535) NOT NULL,
    post_time VARCHAR(255) NOT NULL,
    likes INT NOT NULL,
    PRIMARY KEY (reply_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);




