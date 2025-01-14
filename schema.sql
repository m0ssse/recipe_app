CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    recipe_name TEXT UNIQUE,
    instructions TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE ingredients_by_recipe (
    id INTEGER PRIMARY KEY,
    recipe INTEGER REFERENCES recipes,
    ingredient_name TEXT,
    ingredient_amount TEXT
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    tag TEXT UNIQUE
);

CREATE TABLE tags_by_recipe (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    tag_id INTEGER REFERENCES tags
);

CREATE TABLE reviews_by_recipe (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    user_id INTEGER REFERENCES users,
    score INTEGER,
    comment TEXT
)