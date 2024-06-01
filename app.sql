CREATE DATABASE music_recommender;

USE music_recommender;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    favorite_genres VARCHAR(255),
    favorite_artists VARCHAR(255),
    preferred_moods VARCHAR(255)
);

CREATE TABLE songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    artist VARCHAR(100),
    genre VARCHAR(50),
    mood VARCHAR(50)
);

CREATE TABLE user_likes (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    song_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id)
);

