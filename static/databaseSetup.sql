-- drop all tables
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS trip;
DROP TABLE IF EXISTS destination;

SET FOREIGN_KEY_CHECKS=1;

-- user table --
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


-- destination table --
CREATE TABLE destination (
    id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    tripId INT NOT NULL,
    arriveDate DATE,
    leaveDate DATE,
    PRIMARY KEY(id),
    FOREIGN KEY fkTrip(tripId)
        REFERENCES trip(id)
        ON DELETE CASCADE
);

INSERT INTO destination (name, tripId, arriveDate, leaveDate)
    VALUES('Mt Bachelor', 1, '2020-08-10', '2020-08-12');
INSERT INTO destination (name, tripId, arriveDate, leaveDate)
    VALUES("Devil's Lake", 1, '2020-08-12', '2020-08-15');
INSERT INTO destination (name, tripId) VALUES('Beijing', 2);
INSERT INTO destination (name, tripId) VALUES('Harbin', 2);
INSERT INTO destination (name, tripId) VALUES('Tillamook', 3);
INSERT INTO destination (name, tripId) VALUES('Oregon Dunes NRA', 3);