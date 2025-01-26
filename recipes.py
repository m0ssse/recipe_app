import db

def get_all_recipes():
    sql = """SELECT id, recipe_name, user_id
    from recipe
    """
    return db.query(sql, [])

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

def modify_recipe(recipe_id, ingredients, steps):
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