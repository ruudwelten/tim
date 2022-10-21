-- Initialization of the database
CREATE TABLE IF NOT EXISTS timestamps (
    timestamp timestamp default (strftime('%s', 'now')) PRIMARY KEY,
    title text
);
