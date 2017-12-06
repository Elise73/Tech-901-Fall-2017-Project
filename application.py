import time
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
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

@app.route("/")
#@login_required
def index():
    """Home Page"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # user trying to login
    if request.method == "POST":
        #TODO
        #VERIFY USER HERE
        return render_template("apology.html")

    # user loading page
    if request.method == "GET":
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # user trying to register
    if request.method == "POST":

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
            if request.form.get("teacher_key") != TEACHER_KEY:
                return render_template("apology.html")

        # Post database
        #post = db.execute("INSERT INTO users (username, hash) VALUES (:username, :uhash)",
        #    username=request.form["username"], uhash=pwd_context.hash(request.form.get("password")))

        # Post failed forward to error page
        #if post == None:
        #    return render_template("apology.html")

        # query database for username
        #rows = db.execute("SELECT id FROM users WHERE username = :username", username=request.form.get("username"))

        # remember which user has logged in
        #session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return render_template("index.html")

    # user loading page
    if request.method == "GET":
        return render_template("register.html")

