-- Initialization of the database
CREATE TABLE IF NOT EXISTS timestamps (
    timestamp timestamp default (strftime('%s', 'now')) PRIMARY KEY,
    title text,
    tally integer default 1,
    created timestamp default (strftime('%s', 'now'))
);

CREATE TABLE IF NOT EXISTS projects (
    code text PRIMARY KEY,
    name text,
    color integer default 40,
    start timestamp default (strftime('%s', 'now')),
    end timestamp default (strftime('%s', 'now', '+90 days'))
);
