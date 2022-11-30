-- SQLite DDL

create table postcode
(
    id   INTEGER
        primary key autoincrement,
    name TEXT not null
);

create table road
(
    id   INTEGER
        primary key autoincrement,
    name TEXT not null
);

create table household
(
    id           INTEGER
        primary key autoincrement,
    name         TEXT    not null,
    password     TEXT    not null,
    max_usrs     INTEGER not null,
    house_number INTEGER not null,
    road         INTEGER not null
        references road,
    postcode     INTEGER not null
        references postcode
);

create table list
(
    id   INTEGER
        primary key autoincrement,
    name TEXT    not null,
    gid  INTEGER not null
        references household
);

create table users
(
    id            INTEGER
        primary key autoincrement,
    name          TEXT    not null,
    surname       TEXT    not null,
    password      TEXT    not null,
    email         TEXT    not null,
    date_of_birth TEXT    not null,
    gid           INTEGER not null
        references household
);

create table list_event
(
    id          INTEGER
        primary key autoincrement,
    task        TEXT    not null,
    description TEXT,
    added_by    INTEGER not null
        references users,
    checked_off INTEGER
        references users
);

create table notifications
(
    id        INTEGER
        primary key autoincrement,
    usr_email TEXT not null
        references users (email)
);

create table calendar_event
(
    id                 INTEGER
        primary key autoincrement,
    title              TEXT    not null,
    start_time         TEXT    not null,
    end_time           TEXT    not null,
    start_date         TEXT    not null,
    end_date           TEXT    not null,
    notes              TEXT    not null,
    location           TEXT    not null,
    email_notification INTEGER not null
        references notifications,
    gid                INTEGER not null
        references household
);

create table pairs
(
    id   INTEGER
        primary key autoincrement,
    src  INTEGER not null
        references users,
    dest INTEGER
        references users
);

create table transactions
(
    id          INTEGER
        primary key autoincrement,
    pair_id     INTEGER not null
        references pairs,
    house_id    INTEGER not null
        references household,
    amount      INTEGER not null,
    reference   TEXT    not null,
    description TEXT,
    due_date    TEXT    not null
);

