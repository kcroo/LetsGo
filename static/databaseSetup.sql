-- users table --
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO users (username) VALUES('Frodo');
INSERT INTO users (username) VALUES('Samwise');
INSERT INTO users (username) VALUES('Meriadoc');
INSERT INTO users (username) VALUES('Pippin');