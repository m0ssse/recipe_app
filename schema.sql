CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipe (
    id INTEGER PRIMARY KEY,
    recipe_name TEXT UNIQUE,
    user_id INTEGER REFERENCES user
);

CREATE TABLE recipe_uses_ingredient (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipe,
    ingredient_description TEXT
);

CREATE TABLE recipe_has_step (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipe,
    step TEXT
);

CREATE TABLE recipe_has_tag (
    id INTEGER PRIMARY KEY,
    tag TEXT
);

CREATE TABLE review (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipe,
    user_id INTEGER REFERENCES user,
    score INTEGER,
    comment TEXT
)