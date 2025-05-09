CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    name VARCHAR(100) NOT NULL -- Зачем?
);

CREATE TABLE types_boardgames (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    min_players INT,
    max_players INT,
    playing_time INT,
    complexity INT
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    name VARCHAR(100) NOT NULL,
    password INT
);

CREATE TABLE shops (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    website VARCHAR(2048) NOT NULL
);

CREATE TABLE groups_members (
    group_id INT REFERENCES groups(id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE boardgames (
    id SERIAL PRIMARY KEY,
    owner_user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    type_boardgame_id INT REFERENCES types_boardgames(id) ON DELETE CASCADE ON UPDATE CASCADE,

    took_user_id INT NULL DEFAULT NULL REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    is_bought BOOLEAN DEFAULT false
);

CREATE TABLE product (
    type_boardgame_id INT REFERENCES types_boardgames(id) ON DELETE CASCADE ON UPDATE CASCADE,
    shop_id INT REFERENCES shops(id) ON DELETE CASCADE ON UPDATE CASCADE,
    Price FLOAT,
    PRIMARY KEY (type_boardgame_id, shop_id)
);