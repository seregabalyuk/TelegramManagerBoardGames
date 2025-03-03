CREATE TABLE users (
    users_id SERIAL PRIMARY KEY,
    telegram_id INT,
    username VARCHAR(100) NOT NULL
);

CREATE TABLE games (
    games_id SERIAL PRIMARY KEY,
    games_name VARCHAR(100) NOT NULL,
    min_players INT,
    max_players INT,
    playing_time INT,
    complexity INT
);

CREATE TABLE group_users (
    group_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE shops(
    shops_id SERIAL PRIMARY KEY,
    shops_name VARCHAR(100) NOT NULL,
    website VARCHAR(2048) NOT NULL
);

CREATE TABLE group_member (
    group_id INT REFERENCES group_users(group_id),
    users_id INT REFERENCES users(users_id),
    title VARCHAR(100) NOT NULL,
    PRIMARY KEY (group_id, users_id)
);

CREATE TABLE gameboards (
    users_id INT REFERENCES users(users_id),
    games_id INT REFERENCES games(games_id),
    if_bought BOOLEAN,
    if_free BOOLEAN,
    PRIMARY KEY (users_id, games_id)
);

CREATE TABLE product (
    games_id INT REFERENCES games(games_id),
    shops_id INT REFERENCES shops(shops_id),
    Price FLOAT,
    PRIMARY KEY (games_id, shops_id)
);