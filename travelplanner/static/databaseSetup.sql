-- drop all tables
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS trip;
DROP TABLE IF EXISTS destination;
DROP TABLE IF EXISTS activityType;
DROP TABLE IF EXISTS activity;
DROP TABLE IF EXISTS destinationActivity;

SET FOREIGN_KEY_CHECKS=1;

-- user table --
CREATE TABLE user (
    id INT AUTO_INCREMENT,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    pw CHAR(60) NOT NULL,
    PRIMARY KEY(id)
);

-- these passwords stored in plain text; new users made in website will be stored using hashed bcrypt --
INSERT INTO user (username, email, pw) VALUES('Samwise', 'sam@gamgee.com', 'samwise');
INSERT INTO user (username, email, pw) VALUES('Frodo', 'frodo@baggins.com', 'frodo');


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
    VALUES('Oregon Coast', 1);


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
    VALUES("Mt Bachelor", 1, '2020-08-10', '2020-08-12');
INSERT INTO destination (name, tripId, arriveDate, leaveDate)
    VALUES("Devil's Lake", 1, '2020-08-12', '2020-08-15');
INSERT INTO destination (name, tripId) VALUES('Beijing', 2);
INSERT INTO destination (name, tripId) VALUES("Xi'An", 2);
INSERT INTO destination (name, tripId) VALUES('Tillamook', 3);
INSERT INTO destination (name, tripId) VALUES('Florence', 3);


-- activityType table -- 
CREATE TABLE activityType (
    id int AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO activityType(name) VALUES('Sightseeing');
INSERT INTO activityType(name) VALUES('Eating');
INSERT INTO activityType(name) VALUES('Nightlife');
INSERT INTO activityType(name) VALUES('Shopping');
INSERT INTO activityType(name) VALUES('Hiking');
INSERT INTO activityType(name) VALUES('Biking');
INSERT INTO activityType(name) VALUES('Backpacking');
INSERT INTO activityType(name) VALUES('Hunting');
INSERT INTO activityType(name) VALUES('Boating');
INSERT INTO activityType(name) VALUES('Fishing');
INSERT INTO activityType(name) VALUES('Kayaking');
INSERT INTO activityType(name) VALUES('Canoeing');
INSERT INTO activityType(name) VALUES('Paddleboarding');
INSERT INTO activityType(name) VALUES('Swimming');
INSERT INTO activityType(name) VALUES('Skiing');
INSERT INTO activityType(name) VALUES('Snowboarding');
INSERT INTO activityType(name) VALUES('Cross Country Skiing');
INSERT INTO activityType(name) VALUES('Snowshoeing');
INSERT INTO activityType(name) VALUES('Snowmobiling');
INSERT INTO activityType(name) VALUES('OHV');


-- activity table --
CREATE TABLE activity (
    id INT AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    typeId int,
    cost INT,
    notes VARCHAR(255),
    PRIMARY KEY(id),
    FOREIGN KEY fkType(typeId)
        REFERENCES activityType(id)
        ON DELETE SET NULL
);

INSERT INTO activity(name, typeId, cost, notes)
    VALUES("Phil's Trailhead", 6, 0, 'Tons of great MB trails.');
INSERT INTO activity(name, typeId, notes)
    VALUES("Summit South Sister", 5, 'Gains 4900 feet in 5.5 miles wow');

INSERT INTO activity(name, typeId, cost, notes)
    VALUES("Forbidden City", 1, 60, 'Additional fee for areas inside. Close to Tiananmen Square');
INSERT INTO activity(name, typeId, cost, notes)
    VALUES("Mutianyu Great Wall", 1, 60, 'Tobaggan from the great wall??');
INSERT INTO activity(name, typeId, notes)
    VALUES("Sanlitun", 3, 'TONS of bars');
INSERT INTO activity(name, typeId, cost, notes)
    VALUES("City Wall", 1, 54, 'Long walk in sun--do on cloudy day');
INSERT INTO activity(name, typeId, notes)
    VALUES("Muslim Quarter", 2, 'Culture, street food');
INSERT INTO activity(name, typeId, cost, notes)
    VALUES('Terracotta Warriors', 1, 150, 'outside city--how much is bus?');

INSERT INTO activity(name, typeId, cost, notes)
    VALUES("Tillamook Cheese Factory", 1, 0, 'Free cheese!');
INSERT INTO activity(name, typeId, cost, notes)
    VALUES("Oregon Sand Dunes National Rec Area", 18, 140, 'Price for 250cc and day fee');


-- destinationActivity -- 
CREATE TABLE destinationActivity (
    destinationId INT NOT NULL,
    activityId INT NOT NULL,
    PRIMARY KEY(destinationId, activityId),
    FOREIGN KEY fkDest(destinationId)
        REFERENCES destination(id)
        ON DELETE CASCADE,
    FOREIGN KEY fkAct(activityId)
        REFERENCES activity(id)
        ON DELETE NO ACTION
);

-- cascade lakes: share all activities 
INSERT INTO destinationActivity(destinationId, activityId) VALUES(1,1);
INSERT INTO destinationActivity(destinationId, activityId) VALUES(1,2);
INSERT INTO destinationActivity(destinationId, activityId) VALUES(2,1);
INSERT INTO destinationActivity(destinationId, activityId) VALUES(2,2);

-- beijing
INSERT INTO destinationActivity(destinationId, activityId) VALUES(3,3);
INSERT INTO destinationActivity(destinationId, activityId) VALUES(3,4);
INSERT INTO destinationActivity(destinationId, activityId) VALUES(3,5);

-- xi'an
INSERT INTO destinationActivity(destinationId, activityId) VALUES(4,6);
INSERT INTO destinationActivity(destinationId, activityId) VALUES(4,7);
INSERT INTO destinationActivity(destinationId, activityId) VALUES(4,8);

-- oregon coast 
INSERT INTO destinationActivity(destinationId, activityId) VALUES(5,9);
INSERT INTO destinationActivity(destinationId, activityId) VALUES(6,10);