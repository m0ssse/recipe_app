import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import users
import recipes

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_recipes = recipes.get_all_recipes()
    return render_template("index.html", all_recipes=all_recipes)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO user (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            #session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/new_recipe")
def new_recipe():
    require_login()
    tags = recipes.get_all_tags()
    return render_template("new_recipe.html", tags=tags)

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    require_login()
    recipe_name = request.form.get("title")
    ingredients = request.form.get("ingredients").split("\n")
    steps = request.form.get("steps").split("\n")
    tags = request.form.getlist("tag")
    user_id = session["user_id"]
    recipe_id = recipes.add_recipe(recipe_name, user_id, ingredients, steps, tags)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/modify_recipe/<int:recipe_id>", methods=["POST"])
def modify_recipe(recipe_id):
    require_login()
    ingredients = request.form.get("ingredients").split("\n")
    steps = request.form.get("steps").split("\n")
    tags = request.form.getlist("tag")
    print(tags)
    user_id = session["user_id"]

    recipes.modify_recipe(recipe_id, ingredients=ingredients, steps=steps, tags=tags)
    return redirect("/recipe/"+str(recipe_id))

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)[0]
    steps = recipes.get_steps(recipe_id)
    ingredients = recipes.get_ingredients(recipe_id)
    review_stats = recipes.get_review_statistics(recipe_id)
    recipe_tags = recipes.get_recipe_tags(recipe_id)
    return render_template("show_recipe.html", recipe=recipe, steps=steps, ingredients=ingredients, recipe_tags=recipe_tags, stats=review_stats)

@app.route("/reviews/<int:recipe_id>")
def show_reviews(recipe_id):
    recipe = recipes.get_recipe(recipe_id)[0]
    review_stats = recipes.get_review_statistics(recipe_id)[0]
    reviews = recipes.get_reviews(recipe_id)
    return render_template("show_reviews.html", recipe=recipe, stats=review_stats, reviews=reviews)

@app.route("/review_recipe/<int:recipe_id>", methods=["POST"])
def review_recipe(recipe_id):
    require_login()

    comment = request.form.get("comment")
    score = request.form.get("score")
    user_id = session["user_id"]
    recipes.add_review(user_id, recipe_id, score, comment)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/find_recipe")
def find_recipe():
    query = request.args.get("query")
    if query:
        results = recipes.find_recipes(query)
        print(results)
        if not results:
            results = []
    else:
        query = ""
        results = []
    return render_template("find_recipe.html", query=query, results=results)

@app.route("/delete_recipe/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    require_login()
    recipes.delete_recipe(recipe_id)
    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(403)
    recipes = users.get_recipes(user_id)
    return render_template("show_user.html", user=user, recipes=recipes)