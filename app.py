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

    # Show main page.
    user_id = session["user_id"]

    return render_template("index.html")



@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        user_id = session["user_id"]
        deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]

        #check if user has already user_id in custom_cards table
        results = db.execute("SELECT EXISTS (SELECT * FROM custom_cards WHERE user_id = ?) as exists_result", (user_id,))[0]['exists_result']

        if results == 1:
            for i in deck:
                person = request.form.get(f"person_{i}") or ""
                action = request.form.get(f"action_{i}") or ""
                obj = request.form.get(f"obj_{i}") or ""
                '''db.execute("UPDATE custom_cards SET person = ?, action = ?, obj = ? WHERE user_id = ? AND std_card_id = ?", person, action, obj, user_id, i);'''
                if person:
                    db.execute("UPDATE custom_cards SET person = ? WHERE user_id = ? AND std_card_id = ?", person, user_id, i)
                if action:
                    db.execute("UPDATE custom_cards SET action = ? WHERE user_id = ? AND std_card_id = ?", action, user_id, i)
                if obj:
                    db.execute("UPDATE custom_cards SET obj = ? WHERE user_id = ? AND std_card_id = ?", obj, user_id, i);

        else:
            for i in deck:
                person = request.form.get(f"person_{i}") or ""
                action = request.form.get(f"action_{i}") or ""
                obj = request.form.get(f"obj_{i}") or ""
                db.execute("INSERT INTO custom_cards (user_id, std_card_id, person, action, obj) VALUES (?,?,?,?,?)", user_id, i, person, action, obj);
        return redirect("/savedcards")
    else:
        user_id = session["user_id"]
        #cards = db.execute("SELECT * FROM standard_cards")
        cards = db.execute("SELECT standard_cards.*, custom_cards.person, custom_cards.action, custom_cards.obj FROM standard_cards LEFT JOIN custom_cards ON standard_cards.std_card_id=custom_cards.std_card_id and custom_cards.user_id=?", user_id)
        return render_template("create.html", cards=cards)




@app.route("/savedcards")
@login_required
def savedcards():
    user_id = session["user_id"]
    custom_cards = db.execute("SELECT custom_cards.cust_card_id, standard_cards.rank, standard_cards.suit, custom_cards.person, custom_cards.action, custom_cards.obj FROM custom_cards JOIN standard_cards ON custom_cards.std_card_id = standard_cards.std_card_id WHERE custom_cards.user_id = ?", user_id)
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
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

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


@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "GET":
        user_id = session["user_id"]
        cards = db.execute("SELECT * FROM custom_cards WHERE user_id = ? ORDER BY std_card_id", user_id)
        return render_template("play.html", cards=cards)
    elif card is None:
            return apology("No saved cards please go to the Create Cards Page", 400)
    elif request.method == "POST":
        if "Flip" in request.form:
            # Handle logic for flipping the card to show custom attributes
        elif "Next" in request.form:
            # Handle logic for displaying the next card

    else:
        #request.method == "GET":
        # Render form for stock quote
        return render_template("index.html")



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
        result = db.execute("INSERT INTO users (username, password_hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=hash)

        # Query database for newly registered user
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                        username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


