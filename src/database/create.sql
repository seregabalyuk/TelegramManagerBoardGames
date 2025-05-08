CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    game_name VARCHAR(100) NOT NULL,
    min_players INT,
    max_players INT,
    playing_time INT,
    complexity INT
);

CREATE TABLE group_users (
    id SERIAL PRIMARY KEY,
    telegram_group_id BIGINT UNIQUE,
    title VARCHAR(100) NOT NULL
);

CREATE TABLE shops(
    id SERIAL PRIMARY KEY,
    shop_name VARCHAR(100) NOT NULL,
    website VARCHAR(2048) NOT NULL
);

CREATE TABLE group_member (
    group_id INT REFERENCES group_users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
--    title VARCHAR(100) NOT NULL,
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE gameboards (
    user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    game_id INT REFERENCES games(id) ON DELETE CASCADE ON UPDATE CASCADE,
    if_bought BOOLEAN DEFAULT false,
    if_free BOOLEAN DEFAULT false,
    owner_user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (user_id, game_id)
);

CREATE TABLE product (
    game_id INT REFERENCES games(id) ON DELETE CASCADE ON UPDATE CASCADE,
    shop_id INT REFERENCES shops(id) ON DELETE CASCADE ON UPDATE CASCADE,
    Price FLOAT,
    PRIMARY KEY (game_id, shop_id)
);