from flask import flash, Blueprint, render_template, session, request, redirect, url_for
from utils.userHomeUtils import *
import pymysql

# Create a Blueprint named 'home'
userHome = Blueprint("home", __name__)

from databaseConnection import get_db_connection


# home route
@userHome.route("/home")
def home():
    """
    This page is a little bit complex
    It intergrates a lot of functionalities
    User can do search / advanced search here
    User can check the allowed pets for each unit (based on user's pets)
    """
    if "username" not in session:
        flash("Please login to check this page!")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    user = session["username"]
    cursor = conn.cursor()

    try:
        # Check if search parameters are provided
        companyName = request.args.get("companyName")
        buildingName = request.args.get("buildingName")

        # Advanced search parameters
        maxRent = request.args.get("maxRent")
        minSquareFootage = request.args.get("minSquareFootage")
        amenity = request.args.get("amenities")

        # Get ApartmentUnits info
        if companyName and buildingName:
            # Basic search using companyName and building name
            searchApartmentsByCompanyAndBuilding(cursor, companyName, buildingName)
        elif maxRent or minSquareFootage or amenity:
            # Advanced search based on the parameters
            advancedSearch(cursor, maxRent, minSquareFootage, amenity)
        else:
            # No search parameters provided, display first 10 units
            cursor.execute("SELECT * FROM ApartmentUnit ORDER BY UnitRentID LIMIT 10")

        apartmentUnits = cursor.fetchall()

        # Then we check the pet policies and the amenities that the unit/building provides
        userPets = fetchUserPets(cursor, user)
        allowedPetsByUnit = fetchAllowedPets(cursor, userPets, apartmentUnits)
        amenitiesByUnit = fetchAmenitiesByUnits(cursor, apartmentUnits)

        # Get all amenities for the select field
        allAmenities = fetchAllAmenities(cursor)

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
        amenitiesByUnit=amenitiesByUnit,
        allAmenities=allAmenities,
    )
