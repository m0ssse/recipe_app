import db

def get_all_tags():
    sql = "SELECT * from tags"

    return db.query(sql, [])
    
def get_all_recipes():
    sql = """SELECT id, recipe_name, user_id
    from recipe
    """
    return db.query(sql, [])

def recipe_count():
    sql = """SELECT COUNT(*) from recipe"""
    return db.query(sql, [])[0][0]

def get_recipes(page, page_size):
    sql = """SELECT id, recipe_name, user_id
    from recipe
    ORDER BY id ASC
    LIMIT ? OFFSET ?
    """
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_recipe(recipe_id):
    sql = """SELECT id, recipe_name, user_id
            from recipe
            WHERE recipe.id = ?
    """
    return db.query(sql, [recipe_id])

def get_ingredients(recipe_id):
    sql = """SELECT rui.ingredient_description
            FROM recipe_uses_ingredient as rui
            WHERE rui.recipe_id = ?
            """
    return db.query(sql, [recipe_id])

def get_steps(recipe_id):
    sql = """SELECT rhs.step
            FROM recipe_has_step as rhs
            WHERE rhs.recipe_id = ?
        """
    return db.query(sql, [recipe_id])

def get_tags(recipe_id):
    sql = """SELECT tags.id, tags.tag
        FROM tags, recipe_has_tag
        WHERE tags.id=recipe_has_tag.tag_id AND recipe_has_tag.recipe_id = ?
    """

    return db.query(sql, [recipe_id])

def get_recipe_tags(recipe_id):
    #this query returns a list of all tags with an additional column that has 1 if recipe with id recipe_id has that tag and 0 if not
    #this is used to display a recipe's tags as well as allow corresponding checkboxes to be pre-checked when modifying a recipe
    sql = """SELECT tags.id, tags.tag, IFNULL(0*tid+1, 0) found
    FROM
    tags
    LEFT JOIN
    (SELECT recipe_has_tag.tag_id tid FROM recipe_has_tag WHERE recipe_has_tag.recipe_id = ?)
    ON tags.id = tid
    """
    return db.query(sql, [recipe_id])

def add_recipe(recipe_name, user_id, ingredients, steps, tags):
    sql = """INSERT INTO recipe (recipe_name, user_id)
            VALUES (?, ?)
    """
    db.execute(sql, [recipe_name, user_id])
    recipe_id = db.last_insert_id()

    for ingredient in ingredients:
        sql = """INSERT INTO recipe_uses_ingredient (recipe_id, ingredient_description)
                VALUES (?, ?)
        """
        db.execute(sql, [recipe_id, ingredient])
    
    for step in steps:
        sql = """INSERT INTO recipe_has_step (recipe_id, step)
                VALUES (?, ?)
        """
        db.execute(sql, [recipe_id, step])
    
    for tag in tags:
        sql = """INSERT INTO recipe_has_tag (recipe_id, tag_id)
                VALUES (?, ?)
        """
        db.execute(sql, [recipe_id, tag])
    
    return recipe_id

def modify_recipe(recipe_id, ingredients, steps, tags):
    #if the form does not contain info for either steps or ingredients, the list passed as parameters will contain just an empty string
    #we therefore modify the relevant tables only if there is data to modify
    if ingredients[0]:
        sql = """DELETE from recipe_uses_ingredient
            where recipe_uses_ingredient.recipe_id = ?
            """
        db.execute(sql, [recipe_id])
        for ingredient in ingredients:
            sql = """INSERT INTO recipe_uses_ingredient (recipe_id, ingredient_description)
            VALUES (?, ?)
            """
            db.execute(sql, [recipe_id, ingredient])
    
    if steps[0]:
        sql = """DELETE from recipe_has_step
        where recipe_has_step.recipe_id = ?
        """
        db.execute(sql, [recipe_id])
        for step in steps:
            sql = """INSERT INTO recipe_has_step (recipe_id, step)
            VALUES (?, ?)
            """
            db.execute(sql, [recipe_id, step])
    sql = """DELETE from recipe_has_tag where recipe_has_tag.recipe_id = ?
    """
    db.execute(sql, [recipe_id])
    for tag in tags:
        sql = """INSERT INTO recipe_has_tag (recipe_id, tag_id)
        VALUES (?, ?)"""
        db.execute(sql, [recipe_id, tag])
        

def add_review(user_id, recipe_id, score, comment):
    #remove existing review for recipe from user, if it exists
    sql = """DELETE from review
    WHERE review.user_id = ? AND review.recipe_id = ?
    """
    db.execute(sql, [user_id, recipe_id])
    sql = """INSERT INTO review (user_id, recipe_id, score, comment)
            VALUES (?, ?, ?, ?)
    """
    db.execute(sql, [user_id, recipe_id, score, comment])

def get_reviews(recipe_id, page_size, page):
    sql = """SELECT review.score, review.comment, user.id AS userid, user.username AS username
        FROM review, user
        WHERE review.recipe_id = ? AND review.user_id = user.id
        ORDER BY review.id ASC
        LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [recipe_id, limit, offset])

def get_review_statistics(recipe_id):
    sql = """SELECT COUNT(*) as N, ROUND(AVG(score), 2) as ave
        FROM review
        WHERE review.recipe_id = ?"""
    return db.query(sql, [recipe_id])

def find_recipes(query):
    sql = """SELECT DISTINCT recipe.id, recipe.recipe_name
        FROM recipe, recipe_uses_ingredient, recipe_has_step
        WHERE recipe.id = recipe_uses_ingredient.recipe_id AND recipe.id = recipe_has_step.recipe_id
        AND (recipe.recipe_name LIKE ? OR recipe_uses_ingredient.ingredient_description LIKE ? OR recipe_has_step.step LIKE ?)
        ORDER BY recipe.id ASC"""

    like = "%"+query+"%"
    results = db.query(sql, [like, like, like])
    return results

def delete_recipe(recipe_id):
    tables = ["review", "recipe_uses_ingredient", "recipe_has_step", "recipe_has_tag"]
    deletion_queries = [f"""DELETE from {table} WHERE {table}.recipe_id = ?
    """ for table in tables]
    deletion_queries.append("""DELETE from recipe where recipe.id = ?
    """)
    for sql in deletion_queries:
        db.execute(sql, [recipe_id])