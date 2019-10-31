-- user table --
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INT AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO user (username) VALUES('Samwise');
INSERT INTO user (username) VALUES('Frodo');
INSERT INTO user (username) VALUES('Meriadoc');
INSERT INTO user (username) VALUES('Pippin');

-- trip table --
DROP TABLE IF EXISTS trip;

CREATE TABLE trip (
    id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    userId INT NOT NULL,
    numberOfPeople INT,
    startDate DATE,
    endDate DATE,
    PRIMARY KEY(id),
    FOREIGN KEY fkUser(userId)
        REFERENCES user(id)
        ON DELETE CASCADE
);

INSERT INTO trip (name, userId, numberOfPeople, startDate, endDate) 
    VALUES('Cascade Lakes', 1, 2, '2020-08-10', '2020-08-15');
INSERT INTO trip (name, userId, numberOfPeople) 
    VALUES('China', 2, 1);
INSERT INTO trip (name, userId) 
    VALUES('Oregon Coast', 3);