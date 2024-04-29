from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from utils.userPetUtils import *
import pymysql.cursors

# Create a Blueprint named 'pet'
userPet = Blueprint("pet", __name__)

from databaseConnection import get_db_connection


# myPets route
@userPet.route("/myPets")
def myPets():
    if "username" not in session:
        flash("Please login to check this page!")
        return redirect(url_for("auth.login"))

    user = session["username"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # get current user pets info
    pets = fetchUserPets(cursor, user)

    cursor.close()
    conn.close()

    return render_template("petPages/myPets.html", username=user, pets=pets)


# addNewPet route
@userPet.route("/addNewPet", methods=["GET", "POST"])
def addNewPet():
    if "username" not in session:
        flash("Please login to check this page!")
        return redirect(url_for("auth.login"))

    user = session["username"]
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        petName = request.form.get("PetName")
        petType = request.form.get("PetType")
        petSize = request.form.get("PetSize")

        try:
            insertNewPet(cursor, petName, petType, petSize, user)
            conn.commit()
        except pymysql.Error as e:
            if 'Duplicate entry' in str(e):
                flash("You already have a {} named {}. Please choose a different type or name.".format(petType, petName))
            else:
                flash(
                    "An error occurred while adding the pet. Please try again. Error: {}".format(
                        e
                    )
                )
            return redirect(url_for("pet.addNewPet"))
        finally:
            cursor.close()
            conn.close()

        flash("Pet added successfully!")
        return redirect(url_for("pet.myPets"))

    # case for request.method == 'GET'
    try:
        petTypes = fetchAllPetTypes(cursor)
    finally:
        cursor.close()
        conn.close()

    return render_template("petPages/addNewPet.html", username=user, petTypes=petTypes)


# editPetInfo route
@userPet.route("/editPetInfo/<petName>/<petType>", methods=["GET", "POST"])
def editPetInfo(petName, petType):
    if "username" not in session:
        flash("Please login to check this page!")
        return redirect(url_for("auth.login"))

    user = session["username"]
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        newPetName = request.form["PetName"]
        newPetType = request.form["PetType"]
        newPetSize = request.form["PetSize"]

        # Check if the new pet type and name combination already exists for this user
        if checkPetExists(cursor, user, newPetType, newPetName, petType, petName):
            cursor.close()
            conn.close()
            flash("You already have a {} named {}. Please choose a different type or name.".format(newPetType, newPetName))
            return redirect(url_for("pet.editPetInfo", petName=petName, petType=petType))
        
        updatePetInfo(
            cursor, newPetName, newPetType, newPetSize, petName, petType, user
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Pet information updated successfully!")
        return redirect(url_for("pet.myPets"))

    # when get into this page, show current pet info by default
    try:
        petTypes = fetchAllPetTypes(cursor)
        petInfo = fetchCurrentEditPetInfo(cursor, petName, petType, user)
    
    finally:
        cursor.close()
        conn.close()

    if petInfo:
        return render_template(
            "petPages/editPetInfo.html", pet=petInfo, username=user, petTypes=petTypes
        )

    else:
        flash("Pet not found.")
        return redirect(url_for("pet.myPets"))
