import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
from werkzeug.security import generate_password_hash

import markupsafe
import secrets
import db
import config
import users
import recipes

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
PAGE_SIZE = 10
PASSWORD_LOWER_LIMIT = 8

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def page_count(n):
    return max(1, (n-1)//PAGE_SIZE+1) #same as max(1, ceil(n/page_size))

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/<int:page>")
@app.route("/")
def index(page=1):
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    recipe_count = recipes.recipe_count()
    pages = page_count(recipe_count)

    if page < 1:
        return redirect("/1")
    if page > pages:
        return redirect("/" + str(pages))
    recipes_to_display = recipes.get_recipes(page, PAGE_SIZE)
    return render_template("index.html", recipes_to_display=recipes_to_display, page=page, page_count=pages)

@app.route("/register")
def register():
    return render_template("register.html", password_lower_limit=PASSWORD_LOWER_LIMIT)

@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    if not username:
        flash("VIRHE: anna käyttäjänimi")
        return redirect("/register")
    if len(password1) < PASSWORD_LOWER_LIMIT:
        flash(f"VIRHE: salasanan tulee olla vähintään {PASSWORD_LOWER_LIMIT} merkkiä pitkä!")
        return redirect("/register")
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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")

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
    check_csrf()

    recipe_name = request.form.get("title")
    if not recipe_name or len(recipe_name)>50:
        abort(403)
    ingredients = request.form.get("ingredients").split("\n")
    if not ingredients or len(ingredients)>1000:
        abort(403)
    steps = request.form.get("steps").split("\n")
    if not steps or len(steps)>1000:
        abort(403)
    tags = request.form.getlist("tag")
    user_id = session["user_id"]
    recipe_id = recipes.add_recipe(recipe_name, user_id, ingredients, steps, tags)
    flash("Resepti lisätty!")
    return redirect("/recipe/" + str(recipe_id))

@app.route("/modify_recipe/<int:recipe_id>", methods=["POST"])
def modify_recipe(recipe_id):
    require_login()
    check_csrf()
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe[0]["user_id"]!=session["user_id"]:
        abort(403)
    ingredients = request.form.get("ingredients").split("\n")
    if len(ingredients)>1000:
        flash("Ainesosaluettelo saa olla korkeintaan 1000 merkkiä pitkä!")
        return redirect("/recipe/"+str(recipe_id))
    steps = request.form.get("steps").split("\n")
    if len(steps)>1000:
        flash("Vaiheluettelo saa olla korkeintaan 1000 merkkiä pitkä!")
        return redirect("/recipe/"+str(recipe_id))
    tags = request.form.getlist("tag")

    recipes.modify_recipe(recipe_id, ingredients=ingredients, steps=steps, tags=tags)
    flash("Reseptiä muokattu!")
    return redirect("/recipe/"+str(recipe_id))

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    recipe = recipe[0]
    steps = recipes.get_steps(recipe_id)
    ingredients = recipes.get_ingredients(recipe_id)
    review_stats = recipes.get_review_statistics(recipe_id)[0]
    recipe_tags = recipes.get_recipe_tags(recipe_id)
    return render_template("show_recipe.html", recipe=recipe, steps=steps, ingredients=ingredients, recipe_tags=recipe_tags, stats=review_stats)

@app.route("/reviews/<int:recipe_id>/<int:page>")
@app.route("/reviews/<int:recipe_id>")
def show_reviews(recipe_id, page=1):
    recipe = recipes.get_recipe(recipe_id)[0]
    review_stats = recipes.get_review_statistics(recipe_id)[0]
    review_count = review_stats["N"]
    pages = page_count(review_count)
    page = min(pages, max(page, 1))
    if page>=pages:
        page = pages
    reviews_to_display = recipes.get_reviews(recipe_id, PAGE_SIZE, page)
    return render_template("show_reviews.html", recipe=recipe, stats=review_stats, reviews=reviews_to_display, page=page, page_count=pages)

@app.route("/review_recipe/<int:recipe_id>", methods=["POST"])
def review_recipe(recipe_id):
    require_login()
    check_csrf()

    comment = request.form.get("comment")
    score = request.form.get("score")
    user_id = session["user_id"]
    recipes.add_review(user_id, recipe_id, score, comment)
    flash("Arvostelu lisätty!")
    return redirect("/recipe/" + str(recipe_id))


@app.route("/find_recipe")
def find_recipe():
    query = request.args.get("query")
    if query:
        results = recipes.find_recipes(query)
        if not results:
            results = []
    else:
        query = ""
        results = []
    return render_template("find_recipe.html", query=query, results=results)

@app.route("/delete_recipe/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    require_login()
    check_csrf()

    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe[0]["user_id"]!=session["user_id"]:
        abort(403)
    recipes.delete_recipe(recipe_id)
    flash("Resepti poistettu!")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/user/<int:user_id>/<int:page>")
@app.route("/user/<int:user_id>")
def show_user(user_id, page=1):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    recipe_count = users.recipe_count(user_id)
    pages = page_count(recipe_count)
    page = min(pages, max(page, 1))
    recipes_to_display = users.get_recipes(user_id, page, PAGE_SIZE)
    return render_template("show_user.html", user=user, recipe_count=recipe_count, recipes=recipes_to_display, page=page, page_count=pages)
