# function to search Apartments by companyName and buildingName
def searchApartmentsByCompanyAndBuilding(cursor, companyName, buildingName):
    query = """
            SELECT au.*, ab.AddrStreet, ab.AddrCity, ab.AddrState, ab.AddrZipCode
            FROM ApartmentUnit au
            JOIN ApartmentBuilding ab ON au.CompanyName = ab.CompanyName 
            AND au.BuildingName = ab.BuildingName
            WHERE au.CompanyName LIKE %s AND au.BuildingName LIKE %s
            """
    companyNameShort = "%" + companyName + "%"
    buildingNameShot = "%" + buildingName + "%"

    return cursor.execute(query, (companyNameShort, buildingNameShot))


# function to fetch user pet records
def fetchUserPets(cursor, userName):
    query = "SELECT PetName, PetType, PetSize FROM Pets WHERE username = %s"

    cursor.execute(query, (userName,))
    user_pets = cursor.fetchall()

    return user_pets


# function to handle the pet policies
def fetchAllowedPets(cursor, allowedPetsByUnit, userPets, units):
    for unit in units:
        # for each unit, check pet policies
        cursor.execute(
            """
            SELECT PetType, PetSize, isAllowed
            FROM PetPolicy
            WHERE CompanyName = %s AND BuildingName = %s
            """,
            (unit["CompanyName"], unit["BuildingName"]),
        )
        policies = cursor.fetchall()

        # List to hold names of pets allowed in this unit
        allowed_pet_names = []

        # taking the pets of the user
        for pet in userPets:
            # Check if this pet is allowed based on unit policies
            pet_allowed = any(
                policy["PetType"] == pet["PetType"]
                and policy["PetSize"] == pet["PetSize"]
                and policy["isAllowed"]
                for policy in policies
            )
            if pet_allowed:
                allowed_pet_names.append(pet["PetName"])

        # If no pets are allowed, `shows Not Allowed`
        if not allowed_pet_names:
            allowedPetsByUnit[unit["UnitRentID"]] = "Not Allowed"
        else:
            allowedPetsByUnit[unit["UnitRentID"]] = ", ".join(allowed_pet_names)

    return allowedPetsByUnit
