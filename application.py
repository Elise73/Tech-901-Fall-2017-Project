import time
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *

# variables
TEACHER_KEY = "testkey"

# configure application
app = Flask(__name__)

# ensure responeses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///helpdesk.db")

@app.route("/")
@login_required
def index():
    """Home Page"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    ### Custom apologies commented out for reference until decision made whether to issue generic, custom, or
    ### no apologies (as opposed to another type of error page). Generic apologies used for now, for consistency.

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # HTML form requires that users input data in both fields before the form is submitted

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :email", email=request.form.get("email"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["password"]):
            return render_template("login.html", error="Invalid username or password. Please try again.")

        # remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        if rows[0]["teacher"] == 0:
            #assign student decorator
            session["teacher"] = 0

        else:
            #assign teacher decorator
            session["teacher"] = 1

        # returns user to index
        return render_template("index.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # user trying to register
    if request.method == "POST":

        # variables
        teacher_flag = 1

        # ensure username was submitted
        if not request.form.get("email"):
            return render_template("apology.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html")

        # check that passwords are the same
        if request.form.get("password") != request.form.get("verify_password"):
            return render_template("apology.html")

        # if register as a teacher verify submited key
        if request.form.get("account_type") == "teacher" :
            teacher_flag = 0
            if request.form.get("teacher_key") != TEACHER_KEY:
                return render_template("apology.html")

        # post to database
        post = db.execute("INSERT INTO users (email, password, teacher) VALUES (:email, :uhash, :teacher)",
            email=request.form["email"],
            uhash=pwd_context.hash(request.form.get("password")),
            teacher = teacher_flag
            )

        # post failed forward to error page
        if post == None:
            return render_template("apology.html")

        # query database for username
        rows = db.execute("SELECT user_id FROM users WHERE email = :email", email=request.form.get("email"))

        # remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # redirect user to home page
        return render_template("index.html")

    # user loading page
    if request.method == "GET":
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return render_template("login.html")


@app.route("/question", methods=["GET", "POST"])
@login_required
def question():

    #make sure a question is asked
    if request.method == "GET":
        return render_template("question.html")
    if request.method == "POST":
        if not request.form.get("title"):
            return apology("must provide a title")

        # post question to database
        db.execute("INSERT INTO question (title, description, id) VALUES(:title, :description, :id)",
                    title = request.form.get("title"), description = request.form.get("description"), id=session["user_id"])
        #return to some page
    return redirect(url_for("index"))
