from flask import Blueprint, flash, render_template, session, redirect, url_for, request
from utils.interestUtils import *
from utils.unitUtils import *
import pymysql

# Create a Blueprint named 'interest'
interest = Blueprint("interest", __name__)

from databaseConnection import get_db_connection


@interest.route("/postNewInterest/<int:unitRentID>", methods=["GET", "POST"])
def postNewInterest(unitRentID):
    if "username" not in session:
        flash("Please login to access this page.")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        roommateCount = request.form.get("roommateCount")
        moveInDate = request.form.get("moveInDate")
        username = session["username"]

        try:
            postNewInterestToUnit(
                cursor, username, unitRentID, roommateCount, moveInDate
            )
            conn.commit()
            flash("Your interest has been successfully posted.")

        except pymysql.Error as e:
            conn.rollback()
            flash(f"Failed to post interest: {e}", "error")

        finally:
            cursor.close()
            conn.close()

        # Redirect to the unit details page of the unit just posted interest in
        return redirect(url_for("apartment.unitDetails", unitRentID=unitRentID))

    # Handle GET request to display the form
    try:
        unitDetails = fetchUnitDetailsForInterest(cursor, unitRentID)

    except pymysql.Error as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("home.home"))

    finally:
        cursor.close()
        conn.close()

    if not unitDetails:
        flash("Apartment unit not found.")
        return redirect(url_for("home.home"))

    return render_template(
        "interestPages/postNewInterest.html", unitDetails=unitDetails
    )
