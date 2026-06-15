CREATE TABLE sessions (
    session_pk INTEGER PRIMARY KEY,
    date TEXT,
    bucket TEXT,
    hours REAL,
    project TEXT,
    notes TEXT
);

CREATE TABLE targets(
    week TEXT,
    bucket TEXT,
    target REAL,
    PRIMARY KEY (week, bucket)
);