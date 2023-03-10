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
db = SQL("sqlite:///paocards.db")


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
                    db.execute("UPDATE custom_cards SET obj = ? WHERE user_id = ? AND std_card_id = ?", obj, user_id, i)

        else:
            for i in deck:
                person = request.form.get(f"person_{i}") or ""
                action = request.form.get(f"action_{i}") or ""
                obj = request.form.get(f"obj_{i}") or ""
                db.execute("INSERT INTO custom_cards (user_id, std_card_id, person, action, obj) VALUES (?,?,?,?,?)", user_id, i, person, action, obj)
        return redirect("/savedcards")
    else:
        user_id = session["user_id"]
        cards = db.execute("SELECT standard_cards.*, custom_cards.person, custom_cards.action, custom_cards.obj FROM standard_cards LEFT JOIN custom_cards ON standard_cards.std_card_id=custom_cards.std_card_id and custom_cards.user_id=?", user_id)
        return render_template("create.html", cards=cards)


@app.route("/play/<int:card_index>", methods=["GET", "POST"])
@login_required
def play(card_index):
    user_id = session["user_id"]
    card_images = ["AC.png", "2C.png", "3C.png", "4C.png", "5C.png", "6C.png", "7C.png", "8C.png", "9C.png", "10C.png", "JC.png", "QC.png", "KC.png", "AD.png", "2D.png", "3D.png", "4D.png", "5D.png", "6D.png", "7D.png", "8D.png", "9D.png", "10D.png", "JD.png", "QD.png", "KD.png", "AH.png", "2H.png", "3H.png", "4H.png", "5H.png", "6H.png", "7H.png", "8H.png", "9H.png", "10H.png", "JH.png", "QH.png", "KH.png", "AS.png", "2S.png", "3S.png", "4S.png", "5S.png", "6S.png", "7S.png", "8S.png", "9S.png", "10S.png", "JS.png", "QS.png", "KS.png"]
    current_card = db.execute("SELECT person, action, obj FROM custom_cards WHERE user_id = ? AND std_card_id = ?", user_id, card_index)

    #if users user_is is not in custom_cards table, redirect to create page, and prompt user to create cards
    results = db.execute("SELECT EXISTS (SELECT * FROM custom_cards WHERE user_id = ?) as exists_result", (user_id,))[0]['exists_result']
    if results == 0:
        flash("Please create your custom cards before playing.")
        return redirect("/create")
    else:
        if card_index < 52:
            print(card_index)
        else:
            flash("Congratulations, that's the end of the deck!", "alert-success")
            card_index = 0
        return render_template("play.html", card_index=card_index, card_images=card_images, current_card=current_card)


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
    session["card_index"] = 0
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Yeah, if you could provide a username that would be great", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Yeah, if you could provide a password that would be great", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            return apology("Yeah, that's an invalid username and/or password", 403)

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

    # Redirect user to login formx
    return redirect("/")



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
            return apology("Yeah, if you could provide a password that would be great", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("Yeah, I'm going to have to ask you to go ahead and confirm your password for me. If you could do that for me that would be great", 400)

        # Ensure password and password confirmation match
        elif password != request.form.get("confirmation"):
            return apology("Yeah, if you could go ahead and make sure your passwords match that would be great", 400)

        # Check if password meets complexity requirements
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            return apology("Yeah, so if your password contained at least one lowercase letter, one uppercase letter, one digit, and one special character (such as !, @, #, $, %, ^, &, *, etc), and be at least 8 characters long that would be great", 400)

        # Check if username already exists in database
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                        username=request.form.get("username"))
        if rows:
            return apology("Yeah, I'm gonna have to ask you to go ahead and pick a username that doesn't already exists", 400)

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

