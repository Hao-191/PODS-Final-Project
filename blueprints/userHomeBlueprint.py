from flask import flash, Blueprint, render_template, session, request, redirect, url_for
from utils.userHomeUtils import *
import pymysql

# Create a Blueprint named 'home'
userHome = Blueprint("home", __name__)

from databaseConnection import get_db_connection


# home route
@userHome.route("/home")
def home():
    if "username" not in session:
        flash("Please login to check this page!")
        return redirect(url_for("auth.login"))

    try:
        conn = get_db_connection()
        user = session["username"]
        cursor = conn.cursor()

        # Check if search parameters are provided
        companyName = request.args.get("companyName")
        buildingName = request.args.get("buildingName")

        # Get ApartmentUnits info
        if companyName and buildingName:
            searchApartmentsByCompanyAndBuilding(cursor, companyName, buildingName)
        else:
            # No search parameters provided, display first 50 units
            cursor.execute("SELECT * FROM ApartmentUnit ORDER BY UnitRentID LIMIT 50")
            
        apartmentUnits = cursor.fetchall()

        # Then we check the pet policies
        userPets = fetchUserPets(cursor, user)
        allowedPetsByUnit = {}
        allowedPetsByUnit = fetchAllowedPets(
            cursor, allowedPetsByUnit, userPets, apartmentUnits
        )

        cursor.close()
        conn.close()

    except pymysql.Error as e:
        flash(f"Database error: {e}", "error")
        return render_template("home.html")

    return render_template(
        "home.html",
        username=user,
        apartmentUnits=apartmentUnits,
        allowedPetsByUnit=allowedPetsByUnit,
    )
