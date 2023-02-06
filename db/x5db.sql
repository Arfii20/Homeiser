-- TODO: will need to setup user authentication
--  will also need to set up creation of new table
--  would be good to include test data

-- build tables
CREATE TABLE postcode (
    id INT
        PRIMARY KEY AUTO_INCREMENT,
    road_name VARCHAR(7) NOT NULL
);

CREATE TABLE household (
    id INT
        PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL,  -- hashed passwords will always be 64 characters long (256bits -> 64 chars in hex)
    max_residents INT NOT NULL,
    road_name VARCHAR(100) NOT NULL
        REFERENCES postcode,
    postcode INTEGER NOT NULL,
);
