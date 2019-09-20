from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    portfolio_symbols = db.execute("SELECT symbol, shares FROM portfolio WHERE id = :id", id = session["user_id"])
    grand = 0
    for portfolio_symbol in portfolio_symbols:
        symbol = str(portfolio_symbol["symbol"])
        shares = int(portfolio_symbol["shares"])
        stock = lookup(symbol)
        total = shares * stock["price"]
        grand += total
        #db.execute("UPDATE portfolio SET price = :price, total = :total WHERE id = :id, symbol = :symbol", \
        #price = usd(stock["price"]), total = usd(total), id = session["user_id"], symbol = symbol)
    ucash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
    grand += ucash[0]["cash"]
    uportfolio = db.execute("SELECT * from portfolio WHERE id = :id", id = session["user_id"])

    return render_template("index.html", stocks = uportfolio, cash = usd(ucash[0]["cash"]), grand_total = usd(grand))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol!")
        try:

            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive!")
        except:
            return apology("Shares must be a positive integer!")
        money = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

        if not money or float(money[0]["cash"]) < (stock["price"] * shares):
            return apology("Not enough money!")
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol")

        # ensure proper number of shares
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive integer")
        except:
            return apology("Shares must be positive integer")

        # select user's cash
        money = db.execute("SELECT cash FROM users WHERE id = :id", \
                            id=session["user_id"])

        # check if enough money to buy
        if not money or float(money[0]["cash"]) < stock["price"] * shares:
            return apology("Not enough money")

        # update history
        db.execute("INSERT INTO histories (symbol, shares, price, id) \
                    VALUES(:symbol, :shares, :price, :id)", \
                    symbol=stock["symbol"], shares=shares, \
                    price=usd(stock["price"]), id=session["user_id"])

        # update user cash
        db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=stock["price"] * float(shares))

        # Select user shares of that symbol
        user_shares = db.execute("SELECT shares FROM portfolio \
                           WHERE id = :id AND symbol=:symbol", \
                           id=session["user_id"], symbol=stock["symbol"])

        # if user doesn't has shares of that symbol, create new stock object
        if not user_shares:
            db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) \
                        VALUES(:name, :shares, :price, :total, :symbol, :id)", \
                        name=stock["name"], shares=shares, price=usd(stock["price"]), \
                        total=usd(shares * stock["price"]), \
                        symbol=stock["symbol"], id=session["user_id"])

        # Else increment the shares count
        else:
            shares_total = user_shares[0]["shares"] + shares
            db.execute("UPDATE portfolio SET shares=:shares, total=:total \
                        WHERE id=:id AND symbol=:symbol", \
                        shares=shares_total, total = shares_total * stock["price"], id=session["user_id"], \
                        symbol=stock["symbol"])
        """else:

            price = round(float(stock["price"]),2)
            db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id", id = session["user_id"], purchase = round(float(shares * price), 2)
            db.execute("UPDATE portfolio SET shares = shares + :shares WHERE id = :id AND symbol = :symbol",
            shares = shares, id = session["user_id"], symbol = stock["symbol"])
            #user_shares = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol = :symbol", id = session["user_id"], symbol = stock["symbol"])
            #if not user_shares:
            db.execute("INSERT OR IGNORE INTO portfolio (id,symbol,shares) VALUES (:id,:symbol,:shares)",id=session["user_id"],symbol=stock["symbol"],shares=shares)
            #else:

            db.execute("INSERT INTO histories (symbol, shares, price, id, transacted) VALUES (:symbol, :shares, :price, :id, datetime('now')",
            symbol = stock["symbol"], shares = shares, price = usd(stock["price"]), id = session["user_id"])"""
        flash("Bought!")
        return redirect(url_for("index"))


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    histories = db.execute("SELECT symbol, shares, price, transacted FROM histories WHERE id = :id", id = session["user_id"])
    for history in histories:
        symbol = history["symbol"]
        shares = history["shares"]
        price = history["price"]
        transacted = history["transacted"]
    return render_template("history.html", histories = histories)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Must give symbol!")
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Stock invalid!")
        return render_template("quoted.html", stock = stock)

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username!")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Missing password!")

        elif not request.form.get("confirmation"):
            return apology("Missing confirmation!")

        if request.form.get("confirmation") != request.form.get("password"):
            return apology("password doesn't match confirmation")

        hashing = pwd_context.encrypt(request.form.get("password"))
        result = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if result == None:
            return apology("username is taken")
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username = request.form.get("username"), hash = hashing)
        session["user_id"] = result
        return redirect(url_for("index"))
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol!")
        try:

            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive!")
        except:
            return apology("Shares must be a positive integer!")

        user_shares = db.execute("SELECT shares FROM portfolio \
                                 WHERE id = :id AND symbol=:symbol", \
                                 id=session["user_id"], symbol=stock["symbol"])

        # check if enough shares to sell
        if not user_shares or int(user_shares[0]["shares"]) < shares:
            return apology("Not enough shares")

        # update history of a sell
        db.execute("INSERT INTO histories (symbol, shares, price, id) \
                    VALUES(:symbol, :shares, :price, :id)", \
                    symbol=stock["symbol"], shares=-shares, \
                    price=usd(stock["price"]), id=session["user_id"])

        # update user cash (increase)
        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=stock["price"] * float(shares))
        if shares == user_shares[0]["shares"]:
            db.execute("DELETE FROM portfolio WHERE id = :id AND symbol = :symbol", \
            id = session["user_id"], symbol = stock["symbol"])
        else:
            db.execute("UPDATE portfolio SET shares=:shares, total = :total \
                    WHERE id=:id AND symbol=:symbol", \
                    shares=user_shares[0]["shares"] - shares, total = stock["price"] * (user_shares[0]["shares"] - shares),
                    id=session["user_id"], symbol=stock["symbol"])

        flash('Sold!')
        return redirect(url_for("index"))

    # else if user reached route via GET
    else:
        return render_template("sell.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        try:
            a_cash = int(request.form.get("loan"))
            if a_cash < 0:
                return apology("Cash needs to be positive!")
            elif a_cash > 1000:
                return apology("Cash cannot be more than $1000 at once!")
        except:
            return apology("Cash needs to be a positive number!")
        db.execute("UPDATE users SET cash = cash + :loan WHERE id = :id", loan = a_cash, id = session["user_id"])
        flash("Successfully deposited cash!")
        return redirect(url_for("index"))
