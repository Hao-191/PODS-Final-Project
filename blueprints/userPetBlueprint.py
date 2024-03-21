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

    if request.method == "POST":

        pet_name = request.form.get("PetName")
        pet_type = request.form.get("PetType")
        pet_size = request.form.get("PetSize")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            insertNewPet(cursor, pet_name, pet_type, pet_size, user)
            conn.commit()
        except pymysql.Error as e:
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
    return render_template("petPages/addNewPet.html", username=user)


# editPetInfo route
@userPet.route("/editPetInfo/<pet_name>/<pet_type>", methods=["GET", "POST"])
def editPetInfo(pet_name, pet_type):
    if "username" not in session:
        flash("Please login to check this page!")
        return redirect(url_for("auth.login"))

    user = session["username"]
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        new_pet_name = request.form["PetName"]
        new_pet_type = request.form["PetType"]
        new_pet_size = request.form["PetSize"]

        updatePetInfo(
            cursor, new_pet_name, new_pet_type, new_pet_size, pet_name, pet_type, user
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Pet information updated successfully!")
        return redirect(url_for("pet.myPets"))

    # when get into this page, show current pet info by default
    pet_info = fetchCurrentEditPetInfo(cursor, pet_name, pet_type, user)
    cursor.close()
    conn.close()

    if pet_info:
        return render_template("petPages/editPetInfo.html", pet=pet_info, username=user)

    else:
        flash("Pet not found.")
        return redirect(url_for("pet.myPets"))
