import os
import re
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Import custom modules
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter for formatting currency values
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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

    # Get transactions and sum of shares for each symbol
    transactions_db = db.execute(
        "SELECT symbol, SUM(shares) as shares, price FROM transactions WHERE user_id = ? GROUP BY symbol",
        user_id
    )

    # Get user's cash balance
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    
    return render_template("index.html", database=transactions_db, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    #Buy shares of stock.

    if request.method == "GET":
        # Render form for stock purchase
        return render_template("buy.html")
    else:
        # Process form submission
        symbol = request.form.get("symbol")
        shares_str = request.form.get("shares")

        if not symbol:
            return apology("Must Give Symbol")

        # Check if shares input is a valid number
        try:
            shares = int(shares_str)
        except ValueError:
            return apology("Shares must be a number", 400)

        if shares <= 0:
            return apology("Shares must be a positive number", 400)

        # Lookup stock information
        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol Does Not Exist")

        transaction_value = shares * stock["price"]

        user_id = session["user_id"]
        # Get user's current cash balance
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        if user_cash < transaction_value:
            return apology("Not Enough Money")

        # Calculate updated cash balance after purchase
        uptd_cash = user_cash - transaction_value

        #total = shares * price

        # Update user's cash balance in database
        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        # Get current date and time
        date = datetime.datetime.now()

        # Insert transaction into database
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
            user_id, stock["symbol"], shares, stock["price"], date
        )

        flash("Purchase complete!")

        return redirect("/")



@app.route("/history")
@login_required
def history():

    # Show history of transactions.

    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactions_db)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    #Get stock quote.
    # Process form submission
    if request.method == "POST" :
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must give a symbol")

        # Lookup stock information
        try:
            stock = lookup(symbol.upper())
        except ValueError:
            return apology("Invalid symbol")

        if stock is None:
            return apology("Symbol does not exist", 400)

        #return render_template("quoted.html", stock=stock)
        return render_template("quoted.html", name=stock["name"], symbol=stock["symbol"], price=stock["price"])
    else:
        #request.method == "GET":
        # Render form for stock quote
        return render_template("quote.html")



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




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    # Sell shares of stock.

    if request.method == "GET":
        # Render form for stock sale
        user_id = session["user_id"]
        # Get list of unique symbols from user's transactions
        symbols_db = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", user_id)
        # Extract just the symbols from the query result
        symbols = [row["symbol"] for row in symbols_db]
        return render_template("sell.html", symbols=symbols)
    else:
        # Process form submission
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("Must Give Symbol")

        # Lookup stock information
        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol Does Not Exist")

        user_id = session["user_id"]
        # Get total number of shares for the selected symbol
        symbol_db = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)
        total_shares = symbol_db[0]["total_shares"]

        if shares > total_shares:
            return apology("Not Enough Shares")

        transaction_value = shares * stock["price"]

        # Update user's cash balance
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]
        uptd_cash = user_cash + transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        # Insert transaction into database
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)", user_id, stock["symbol"], -shares, stock["price"], date)

        flash("Sold!")

        return redirect("/")
