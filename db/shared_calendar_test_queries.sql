
-- Postcode id: 
-- 610, 611, 612

-- Household id: 
-- 620, 621, 622

-- user id: 
-- 630, 631, 632, 633, 634

-- calendar event id: 
-- 640, 641, 642

-- list id: 
-- 650, 651, 652, 653, 654, 655

-- list event id:
-- 660, 661, 662, 663, 664, 665
-- TODO: will need to setup user authentication
--  will also need to set up creation of new table
--  would be good to include test data

-- build tables
CREATE TABLE IF NOT EXISTS postcode (
    id INT AUTO_INCREMENT,
    code VARCHAR(7) NOT NULL,
    road_name VARCHAR(32),  -- road names map injectively to postcodes

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS household (
    id INT AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    password VARCHAR(512) NOT NULL,  -- hashed passwords will always be 64 characters long (256bits -> 64 chars in hex)
    max_residents INT NOT NULL,
    postcode_id INTEGER NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (postcode_id) REFERENCES postcode(id)
);

CREATE TABLE IF NOT EXISTS list (
    id INT AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    household_id INTEGER NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (household_id) REFERENCES household(id)
);

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT,
    first_name VARCHAR(64) NOT NULL,
    surname VARCHAR(64) NOT NULL,
    password VARCHAR(512) NOT NULL,
    email VARCHAR(319) NOT NULL, -- 319 is max length for email. 64 characters for local, '@', 254 for domain
    date_of_birth DATE,
    household_id INT,
    color INT,  --

    PRIMARY KEY (id),
    FOREIGN KEY (household_id) REFERENCES household(id)
);

CREATE TABLE IF NOT EXISTS list_event (
    id INT AUTO_INCREMENT,
    task VARCHAR(128) NOT NULL,
    description VARCHAR(512),
    added_by_user INT NOT NULL,
    checked_off_by_user INT,
    list INT,

    PRIMARY KEY (id),
    FOREIGN KEY (added_by_user) REFERENCES user(id),
    FOREIGN KEY (checked_off_by_user) REFERENCES user(id),
    FOREIGN KEY (list) REFERENCES list(id)
);


CREATE TABLE IF NOT EXISTS calendar_event (
    id INT AUTO_INCREMENT,
    title VARCHAR(128),
    start_time DATETIME,
    end_time DATETIME,
    notes VARCHAR(512),
    location VARCHAR(512),
    household_id INT NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (household_id) REFERENCES household(id)
);


CREATE TABLE IF NOT EXISTS user_doing_calendar_event (
    user_id INT,
    calendar_event_id INT,
    added_by_user INT,

    PRIMARY KEY (user_id, calendar_event_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (calendar_event_id) REFERENCES calendar_event(id)

);

CREATE TABLE IF NOT EXISTS pairs (
    id INT AUTO_INCREMENT,
    src INTEGER NOT NULL,
    dest INTEGER NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (src) REFERENCES user(id),
    FOREIGN KEY (dest) REFERENCES user(id)
);

CREATE TABLE transaction (
    id INT AUTO_INCREMENT,
    pair_id INT,
    amount INT,
    description VARCHAR(256),
    due_date DATE,
    paid TINYINT DEFAULT 0,

    PRIMARY KEY (id),
    FOREIGN KEY (pair_id) REFERENCES pairs(id)
);

# INSERT INTO postcode (id, code, road_name)
# VALUES (610, 1234, 'road a'),
#         (611, 2345, 'road b'),
#         (612, 3456, 'road c');
#
# INSERT INTO household (id, name, password, max_residents, postcode_id)
# VALUES (620, 'ab', 'abc123', 6, 610),
#         (621, 'bc', 'cde123', 5, 612),
#         (622, 'dc', 'def123', 6, 611);
#
# INSERT INTO user (id, first_name, surname, password, email, date_of_birth, household_id, color)
# VALUES (630, 'a', 'b', 'a1234', 'abcdefghijk1@gmail.com', '2001-01-01', 620, 112233),
#         (631, 'b', 'c', 'b1234', 'abcdefghijk2@gmail.com', '2001-01-01', 620, 112244),
#         (632, 'c', 'd', 'c1234', 'abcdefghijk3@gmail.com', '2001-01-01', 620, 112255),
#         (633, 'd', 'e', 'd1234', 'abcdefghijk4@gmail.com', '2001-01-01', 620, 112266),
#         (634, 'e', 'f', 'f1234', 'abcdefghijk5@gmail.com', '2001-01-01', 621, 112277);
#
# INSERT INTO calendar_event (id, title, start_time, end_time, notes, location, household_id)
# VALUE (640, 'event a', '2023-02-01 11:00:00', '2023-02-01 12:00:00', 'description here', 'location of event', 620),
#         (641, 'event b', '2023-07-01 11:00:00', '2023-07-01 12:00:00', 'description here', 'location of event', 620),
#         (642, 'event c', '2023-09-01 11:00:00', '2023-09-01 12:00:00', 'description here', 'location of event', 620);
#
# INSERT INTO user_doing_calendar_event (user_id, calendar_event_id, added_by_user)
# VALUE (630, 640, 630),
#         (632, 640, 630),
#         (633, 640, 630),
#         (630, 641, 632),
#         (631, 641, 632),
#         (632, 641, 632),
#         (633, 641, 632),
#         (634, 641, 632),
#         (631, 642, 633),
#         (630, 642, 633);
#
# INSERT INTO list (id, name, household_id)
# VALUE (650, 'list a', 620),
#         (651, 'list b', 620),
#         (652, 'list c', 620),
#         (653, 'list d', 621),
#         (654, 'list e', 622),
#         (655, 'list a', 622);
#
# INSERT INTO list_event (id, task, description, added_by_user, checked_off_by_user, list)
# VALUE (660, 'task a', 'description a', 630, NULL, 650),
#         (661, 'task b', 'description b', 632, NULL, 650),
#         (662, 'task c', 'description c', 633, NULL, 652),
#         (663, 'task d', 'description d', 632, NULL, 651),
#         (664, 'task e', 'description e', 631, NULL, 650),
#         (665, 'task f', 'description f', 631, NULL, 651);
