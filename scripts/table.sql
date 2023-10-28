DROP TABLE IF EXISTS raw.users;
DROP TABLE IF EXISTS raw.locations;
DROP TABLE IF EXISTS raw.additional;

create table if not exists raw.users(
id UUID primary key not null,
gender varchar,
name varchar,
first varchar,
last varchar,
date_of_birth date,
created_at timestamp default now()
);

CREATE TABLE if not exists raw.locations(
    id UUID PRIMARY KEY NOT NULL,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    postcode VARCHAR,
    country_code VARCHAR,
    user_id UUID REFERENCES raw.users(id),
    created_at timestamp default now()
);

create table if not exists raw.additional(
    id UUID PRIMARY KEY NOT NULL,
    phone VARCHAR,
    email VARCHAR,
    picture_large VARCHAR,
    user_id UUID REFERENCES raw.users(id),
    created_at timestamp default now()
); 
