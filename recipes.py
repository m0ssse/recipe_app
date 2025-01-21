import db

def get_recipe(recipe_id):
    sql = """SELECT id, recipe_name
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
        sql = """INSERT INTO recipe_has_tag (recipe_id, tag)
                VALUES (?, ?)
        """
        db.execute(sql, [recipe_id, tag])