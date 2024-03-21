# function to fetch user's pets
def fetchUserPets(cursor, user):
    cursor.execute(
        "SELECT PetName, PetType, PetSize FROM Pets WHERE username = %s", (user,)
    )
    return cursor.fetchall()

# function to register a new pet
def insertNewPet(cursor, pet_name, pet_type, pet_size, user):
    cursor.execute(
        "INSERT INTO Pets (PetName, PetType, PetSize, username) VALUES (%s, %s, %s, %s)",
        (pet_name, pet_type, pet_size, user),
    )

# function to update current pet info
def updatePetInfo(
    cursor, new_pet_name, new_pet_type, new_pet_size, pet_name, pet_type, user
):

    cursor.execute(
        """
            UPDATE Pets
            SET PetName = %s, PetType = %s, PetSize = %s
            WHERE PetName = %s AND PetType = %s AND username = %s
        """,
        (new_pet_name, new_pet_type, new_pet_size, pet_name, pet_type, user),
    )

# function to fetch current edit page pet info
def fetchCurrentEditPetInfo(cursor, pet_name, pet_type, user):
    query = "SELECT * FROM Pets WHERE PetName = %s AND PetType = %s AND username = %s"
    cursor.execute(query, (pet_name, pet_type, user))
    return cursor.fetchone()
