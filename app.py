import os
import sys
import freesound
import json

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, make_response, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, replace_space, synonyms, formatted, get_results

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///soundmatch.db")

# Make sure to input your freesound API_KEY in the terminal
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    """Show all the user's selected sounds"""

    rows = db.execute("SELECT * FROM sounds WHERE user_id=:id", id=session["user_id"])

    if request.method == "GET":
        if len(rows) == 0:
            return apology("Please add sounds to your list.", "You have no sounds!")
        else:

            return render_template("index.html", rows=rows)

            return apology("TODO")

    else:
        deletedSounds = request.get_json()
        print(deletedSounds)
        for sound in range(len(deletedSounds)):
            db.execute("DELETE FROM sounds WHERE user_id=:user_id AND sound_id=:sound_id",
                        user_id=session["user_id"], sound_id=deletedSounds[sound])
        return "Success"


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """search for sounds"""

    if request.method == "GET":
        return render_template("search.html")

    else:
        word = str(request.form.get("word"))

        if not word:
            return apology("Input a word or phrase.", 400)

        elif ' ' in word:
            word = word.replace(' ', '+')

        synonym_list = formatted(synonyms(word))

        # request_count is a multiple of 5 (e.g. result_count of 5 means 5 x 5 = 25 results)
        result_count = int(request.form.get("numResults"))
        id_list = get_results(synonym_list,result_count)

        # creates a session id for the generated id_list, so it can be used by other routes (namely the 'results' route)
        session['id_list'] = id_list

        # redirects user to 'results' page, plugging in the generated id_list as a query string
        return redirect(url_for('results', id_list=id_list))




@app.route("/")
def homepage():
    """display the homepage"""
    return render_template("homepage.html")


@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    """return results from search, stores selected sounds in database upon saving"""
    if request.method == "GET":
        id_list = session['id_list']
        return render_template("results.html", id_list=id_list)
    else:
        # stores json that was posted when 'save' button was clicked in a variable as a list
        selectedSounds = request.get_json()
        print(selectedSounds)

        # inserts user-selected sounds into database (sounds table)
        for sound in range(len(selectedSounds)):
            db.execute("INSERT INTO sounds (user_id, sound_id) VALUES (:user_id, :sound_id)",
                        user_id=session["user_id"], sound_id=selectedSounds[sound])
        return "Success"



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("You must provide a username.", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("You must provide a password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password.", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to homepage form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        rows = db.execute("SELECT * FROM users WHERE username=:username",
                            username=request.form.get("username"))

        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Please fill out all fields.", 403)

        elif len(rows) == 1:
            return apology("Username already exists. Please pick another.", 403)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords must match.", 403)

        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                        username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
            login()
            flash('Registration Successful!')
            return redirect("/index")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

