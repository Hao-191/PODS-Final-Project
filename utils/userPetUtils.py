# function to fetch user's pets
def fetchUserPets(cursor, user):
    cursor.execute(
        "SELECT PetName, PetType, PetSize FROM Pets WHERE username = %s", (user,)
    )
    return cursor.fetchall()


# function to register a new pet
def insertNewPet(cursor, petName, petType, petSize, user):
    cursor.execute(
        "INSERT INTO Pets (PetName, PetType, PetSize, username) VALUES (%s, %s, %s, %s)",
        (petName, petType, petSize, user),
    )


# function to update current pet info
def updatePetInfo(
    cursor, newPetName, newPetType, newPetSize, petName, petType, user
):

    cursor.execute(
        """
            UPDATE Pets
            SET PetName = %s, PetType = %s, PetSize = %s
            WHERE PetName = %s AND PetType = %s AND username = %s
        """,
        (newPetName, newPetType, newPetSize, petName, petType, user),
    )


# function to fetch current edit page pet info
def fetchCurrentEditPetInfo(cursor, petName, petType, user):
    cursor.execute(
        "SELECT * FROM Pets WHERE PetName = %s AND PetType = %s AND username = %s",
        (petName, petType, user),
    )
    return cursor.fetchone()


# function to fetch all existing pet types
def fetchAllPetTypes(cursor):
    cursor.execute("SELECT DISTINCT PetType FROM Pets")
    return cursor.fetchall()


# fuction to check if there exists a (petName, petType) pair for a certain user
def checkPetExists(cursor, user, newPetType, newPetName, petType, petName):
    cursor.execute("SELECT * FROM Pets WHERE userName=%s AND petType=%s AND petName=%s AND NOT (petType=%s AND petName=%s)", 
                       (user, newPetType, newPetName, petType, petName))
    return cursor.fetchone()