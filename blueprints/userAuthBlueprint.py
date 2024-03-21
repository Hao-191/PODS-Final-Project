from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from utils.userAuthUtils import *

# Create a Blueprint named 'auth'
userAuth = Blueprint("auth", __name__)

from databaseConnection import get_db_connection


# login route
@userAuth.route("/login")
def login():
    return render_template("userAuthPages/login.html")


# register route
@userAuth.route("/register")
def register():
    return render_template("userAuthPages/register.html")


# Authenticates the login
@userAuth.route("/loginAuth", methods=["GET", "POST"])
def loginAuth():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the user by username and check if exists
    user_record = fetchUserInfo(cursor, username)
    cursor.close()
    conn.close()

    if user_record and check_password_hash(user_record["passwd"], password):
        # Password matches, proceed to login
        session["username"] = username
        return redirect(url_for("home.home"))
    else:
        # Login failed
        return render_template(
            "userAuthPages/login.html",
            error="Invalid login or username, please check your credential.",
        )


# Authenticates the register
@userAuth.route("/registerAuth", methods=["GET", "POST"])
def registerAuth():

    # Collecting all form data
    username = request.form["username"]
    password = request.form["password"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    dob = request.form["DOB"]
    gender = request.form["gender"]
    email = request.form.get("email", "")
    phone = request.form.get("Phone", "")

    # Hash the password
    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username already exists
    if fetchUserInfo(cursor, username):
        cursor.close()
        return render_template(
            "userAuthPages/register.html",
            error="This user already exists, please login or register a new user.",
        )
    
    registerNewAccount(
        cursor,
        username,
        first_name,
        last_name,
        dob,
        gender,
        email,
        phone,
        hashed_password,
    )

    conn.commit()
    flash("Successfully registered! Please login into your account.")

    cursor.close()
    conn.close()

    return redirect(url_for("auth.login"))


@userAuth.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")

