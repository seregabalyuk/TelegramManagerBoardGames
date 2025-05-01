CREATE TABLE users (
    users_id SERIAL PRIMARY KEY,
    telegram_id VARCHAR(32) UNIQUE,--INT VERCHAR()fwf
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
    telegram_group_id VARCHAR(32) UNIQUE,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE shops(
    shops_id SERIAL PRIMARY KEY,
    shops_name VARCHAR(100) NOT NULL,
    website VARCHAR(2048) NOT NULL
);

CREATE TABLE group_member (
    group_id INT REFERENCES group_users(group_id) ON DELETE CASCADE ON UPDATE CASCADE,
    users_id INT REFERENCES users(users_id) ON DELETE CASCADE ON UPDATE CASCADE,
    title VARCHAR(100) NOT NULL,
    PRIMARY KEY (group_id, users_id)
);

CREATE TABLE gameboards (
    users_id INT REFERENCES users(users_id) ON DELETE CASCADE ON UPDATE CASCADE,
    games_id INT REFERENCES games(games_id) ON DELETE CASCADE ON UPDATE CASCADE,
    if_bought BOOLEAN DEFAULT false,
    if_free BOOLEAN DEFAULT false,
    owner_user_id INT REFERENCES users(users_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (users_id, games_id)
);

CREATE TABLE product (
    games_id INT REFERENCES games(games_id) ON DELETE CASCADE ON UPDATE CASCADE,
    shops_id INT REFERENCES shops(shops_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Price FLOAT,
    PRIMARY KEY (games_id, shops_id)
);