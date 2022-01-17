from flask import Flask, request, render_template, session, redirect
from functools import wraps
from flask import jsonify
import json
app = Flask(__name__)
app.secret_key = "secretkey"
books = [
    {
        "author": "Hernando de Soto",
        "country": "Peru",
        "language": "English",
        "pages": 209,
        "title": "The Mystery of Capital",
        "year": 1970,
    },
    {
        "author": "Hans Christian Andersen",
        "country": "Denmark",
        "language": "Danish",
        "pages": 784,
        "title": "Fairy tales",
        "year": 1836,
    },
    {
        "author": "Dante Alighieri",
        "country": "Italy",
        "language": "Italian",
        "pages": 928,
        "title": "The Divine Comedy",
        "year": 1315,
    },
]

# users = {"username": "testuser", "password": "testuser"}
users = [{"username": "testuser", "password": "testuser"},
        {"username": "deepak", "password": "deepak"}]



# def checkUser(username, password):
#     for user in users:
#         if username in user["username"] and password in user["password"]:
#             return True
#     return False

def sessionRequired(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        fromBrowser = session.get("username")
        for user in users:
            if user["username"] == fromBrowser:
                return fn(*args, **kwargs)
        return redirect("static/register.html")
    return decorator

#Default Route
@app.route("/", methods=["GET", "POST"])
@sessionRequired
def redirect_get():
    return render_template("index.html", username=session["username"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = {"username":request.form["username"], "password": request.form["password"]}

        if user in users:
            # set session data
            session["username"] =  request.form["username"]
            return render_template(
                "index.html", username=session["username"], title = 'books', books = books)
        else:
            return redirect("static/register.html")
    else:
        return redirect("static/register.html")


@app.route("/logout")
def logout():
    # remove the username from the session if it is there
    session.pop("username", None)
    return "Logged Out of Books"


@app.route("/books", methods=["GET", "POST"])
@sessionRequired
def book():
    username = session["username"]
    if request.method == "POST":
        # expects pure json with quotes everywheree
        new_book = request.form["book"]
        myjson = json.loads(new_book)
        books.append(myjson)
        return render_template(
            "books.html", books=books, title="books", username=session["username"]
        )
    elif request.method == "GET":
        username = session["username"]
        return render_template(
            "books.html", books=books, title="books", username=session["username"]
        )
    else:
        return 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

#Exercise:
# 1. Debug code so that it allows us to login as "testuser" and to the list of books.
# 2. Add yourself as a user so that you can login and list the books
# 3. Add the capability to add a new book to the list of books (use /books POST method) 