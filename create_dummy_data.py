import random
import sqlite3
from string import ascii_lowercase
from werkzeug.security import generate_password_hash


db = sqlite3.connect("database.db")
db.execute("DELETE from review")
db.execute("DELETE from recipe_has_tag")
db.execute("DELETE from recipe_has_step")
db.execute("DELETE from recipe_uses_ingredient")
db.execute("DELETE from recipe")
db.execute("DELETE from user")

user_count = 10
reviewer_count = 10
recipe_count = 100
review_count = 100000

def generate_string(length):
    name = ""
    for _ in range(length):
        name+=random.choice(ascii_lowercase)
    return name

for i in range(1, user_count+1):
    pw = generate_string(10)
    pw_hash = generate_password_hash(pw)
    sql = """INSERT INTO user (username, password_hash) VALUES (?, ?)
    """
    db.execute(sql, ["user"+str(i), pw_hash])

for i in range(1, reviewer_count):
    pw = generate_string(10)
    pw_hash = generate_password_hash(pw)
    sql = """INSERT INTO user (username, password_hash) VALUES (?, ?)
    """
    db.execute(sql, ["reviewer"+str(i), pw_hash])

for i in range(1, recipe_count+1):
    user_id = random.choice(range(1, user_count+1))
    recipe_name = f"recipe{i}"
    step = "step"
    ingredient = "ingredient"
    sql = """INSERT INTO recipe (recipe_name, user_id) VALUES (?, ?)
    """
    db.execute(sql, [recipe_name, user_id])
    sql = """INSERT INTO recipe_has_step (recipe_id, step) VALUES (?, ?)"""
    db.execute(sql, [i, step])
    sql = """INSERT INTO recipe_uses_ingredient (recipe_id, ingredient_description) VALUES (?, ?)"""
    db.execute(sql, [i, ingredient])

for i in range(review_count):
    reviewer_id = random.choice(range(1, reviewer_count+1))
    recipe_id = random.choice(range(1, recipe_count+1))
    score = random.choice(range(1, 11))
    comment = f"review{i}"
    sql = """INSERT INTO review (recipe_id, user_id, score, comment) VALUES (?, ?, ?, ?)
    """
    db.execute(sql, [recipe_id, reviewer_id+user_count, score, comment])

db.commit()
db.close()