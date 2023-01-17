import os
import re
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash


# Import custom modules
from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///xfinal.db")


@app.after_request
def after_request(response):

    # Ensure responses aren't cached.

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    # Show portfolio of stocks.
    user_id = session["user_id"]

    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        for card_id in request.form:
            person = request.form.get(card_id + "-person")
            action = request.form.get(card_id + "-action")
            object = request.form.get(card_id + "-object")
            db.execute("INSERT INTO custom_cards (standard_card_id, user_id, person, action, object) VALUES (?,?,?,?,?)",
    card_id, user_id, request.form.get(card_id + "-person") or '', request.form.get(card_id + "-action") or '', request.form.get(card_id + "-object") or ''
,
                       card_id, session["user_id"], person, action, object)

        flash("Custom card parameters saved!")
        return redirect("/savedcards")
    else:
        cards = db.execute("SELECT * FROM standard_cards")
        return render_template("create.html", cards=cards)






@app.route("/savedcards")
@login_required
def savedcards():
    user_id = session["user_id"]
    custom_cards = db.execute("SELECT custom_cards.id, standard_cards.rank, standard_cards.suit, custom_cards.person, custom_cards.action, custom_cards.object FROM custom_cards JOIN standard_cards ON custom_cards.standard_card_id = standard_cards.id WHERE custom_cards.user_id = ?", user_id)
    return render_template("savedcards.html", custom_cards=custom_cards)



@app.route("/login", methods=["GET", "POST"])
def login():

    # Handle user login.

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Log user out.

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


"""
@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    #Test user for each card.
    # Process form submission
    if request.method == "POST" :
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must give a symbol")

        # Lookup stock information



        if card is None:
            return apology("Symbol does not exist", 400)

    else:
        #request.method == "GET":
        # Render form for stock quote
        return render_template("index.html")
"""



@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and password confirmation match
        elif password != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Check if password meets complexity requirements
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            return apology("password must contain at least one lowercase letter, one uppercase letter, one digit, and one symbol, and be at least 8 characters long", 400)

        # Check if username already exists in database
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                        username=request.form.get("username"))
        if rows:
            return apology("username already exists", 400)

        # Hash password
        hash = generate_password_hash(password)

        # Insert new user into database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=hash)

        # Query database for newly registered user
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                        username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


