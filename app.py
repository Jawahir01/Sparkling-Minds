import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_courses")
def get_courses():
    courses = list(mongo.db.courses.find())
    return render_template("courses.html", courses=courses)


@app.route("/get_sports")
def get_sports():
    sports = list(mongo.db.sports.find())
    return render_template("sports.html", sports=sports)


# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("This username has been already taken")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "first-name": request.form.get("first-name").lower(),
            "last-name": request.form.get("last-name").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "phone-number": request.form.get("phone-number")
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("You have been Successful! Registered")
        return redirect(url_for("profile", username=session["user"]))
   
    return render_template("register.html")


# User signin route
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # check if username exists in db

        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:

            # ensure hashed password matches user input
            if check_password_hash(
            existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("signin"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("signin"))

    return render_template("signin.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        children = list(mongo.db.kids.find({'username': username}))
        return render_template("profile.html", username=username, children=children)


@app.route("/add_child", methods=["GET", "POST"])
def add_child():
    # insert a child to DB based on user's session
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    # Add new child to the user's list
    if request.method == "POST":
        child = {
            "username": session["user"],
            "childfname": request.form.get("childfname"),
            "childlname": request.form.get("childlname"),
            "date_of_birth": request.form.get("date_of_birth"),
            "school_name": request.form.get("school_name"),
            "school_year": request.form.get("school_year"),
            "child_med_conditions": request.form.get("child_med_conditions")
        }
        mongo.db.kids.insert_one(child)
        flash("Your Child hass been added successfully!")

    children = list(mongo.db.kids.find({'username': username}))
    return render_template("profile.html", children=children)


@app.route("/signout")
def signout():
    # remove user from session cookie
    flash("You have been signed out")
    session.pop("user")
    return redirect(url_for("signin"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
