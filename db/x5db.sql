-- TODO: will need to setup user authentication
--  will also need to set up creation of new table
--  would be good to include test data

-- build tables
CREATE TABLE postcode (
    id INT AUTO_INCREMENT,
    code VARCHAR(7) NOT NULL,
    road_name VARCHAR(32),  -- road names map injectively to postcodes

    PRIMARY KEY (id)
);

CREATE TABLE household (
    id INT AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL,  -- hashed passwords will always be 64 characters long (256bits -> 64 chars in hex)
    max_residents INT NOT NULL,
    postcode_id INTEGER NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (postcode_id) REFERENCES postcode(id)
);

CREATE TABLE list (
    id INT AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    household_id INTEGER NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (household_id) REFERENCES household(id)
);

CREATE TABLE user (
    id INT AUTO_INCREMENT,
    first_name VARCHAR(64) NOT NULL,
    surname VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL,
    email VARCHAR(319) NOT NULL, -- 319 is max length for email. 64 characters for local, '@', 254 for domain
    date_of_birth DATE,
    household_id INT,
    color INT,  --

    PRIMARY KEY (id),
    FOREIGN KEY (household_id) REFERENCES household(id)
);

CREATE TABLE list_event (
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


CREATE TABLE calendar_event (
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


CREATE TABLE user_doing_calendar_event (
    user_id INT,
    calendar_event_id INT,
    added_by_user INT,

    PRIMARY KEY (user_id, calendar_event_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (calendar_event_id) REFERENCES calendar_event(id)

);


CREATE TABLE pairs (
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