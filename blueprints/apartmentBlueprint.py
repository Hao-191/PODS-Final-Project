from flask import Blueprint, flash, render_template, session, redirect, url_for
from utils.buildingUtils import *
from utils.unitUtils import *
import pymysql

# Create a Blueprint named 'apartment'
apartment = Blueprint("apartment", __name__)

from databaseConnection import get_db_connection


@apartment.route("/unitDetails/<int:unitRentID>")
def unitDetails(unitRentID):
    if "username" not in session:
        flash("Please login to check this page!")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch unit details
        unitDetails = fetchUnitInfo(cursor, unitRentID)
        # Fetch room details for this unit
        roomDetails = fetchUnitRooms(cursor, unitRentID)
        # Fetch amenities for this unit
        amenities = fetchUnitAmenities(cursor, unitRentID)
        # Fetch interests for this unit
        interests = fetchUnitInterests(cursor, unitRentID)

    except pymysql.Error as e:
        flash(f"Database error: {e}")
        return redirect(url_for("home.home"))

    finally:
        cursor.close()
        conn.close()

    if not unitDetails:
        flash("Apartment unit not found.")
        return redirect(url_for("home.home"))

    return render_template(
        "apartmentPages/unitDetails.html",
        unit=unitDetails,
        rooms=roomDetails,
        amenities=amenities,
        interests=interests,
    )


@apartment.route("/buildingDetails/<companyName>/<buildingName>")
def buildingDetails(companyName, buildingName):
    if "username" not in session:
        flash("Please login to check this page!")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch basic building details
        buildingDetails = fetchBuildingDetails(cursor, companyName, buildingName)
        # Fetch amenities provided by the building
        amenities = fetchBuildingAmenities(cursor, companyName, buildingName)
        # Count available units for rent
        availableUnits = fetchBuildingAvailableUnitCounts(
            cursor, companyName, buildingName
        )
        # Fetch pet policies for the building
        petPolicies = fetchBuildingPetPolicies(cursor, companyName, buildingName)

    except pymysql.Error as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("home.home"))

    finally:
        cursor.close()
        conn.close()

    if not buildingDetails:
        flash("Building not found.", "error")
        return redirect(url_for("home.home"))

    return render_template(
        "apartmentPages/buildingDetails.html",
        building=buildingDetails,
        amenities=amenities,
        availableUnits=availableUnits,
        petPolicies=petPolicies,
    )
