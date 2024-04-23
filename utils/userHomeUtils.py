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

    cursor.execute(query, (companyNameShort, buildingNameShot))


# function to fetch user pet records
def fetchUserPets(cursor, userName):
    query = "SELECT PetName, PetType, PetSize FROM Pets WHERE username = %s"

    cursor.execute(query, (userName,))
    user_pets = cursor.fetchall()

    return user_pets


# function to handle the pet policies
def fetchAllowedPets(cursor, userPets, units):
    allowedPetsByUnit = {}

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


# function to fetch all amenities that this unit provides
def fetchAmenitiesByUnits(cursor, apartmentUnits):
    amenitiesByUnit = {}

    for unit in apartmentUnits:
        unitId = unit["UnitRentID"]
        companyName = unit["CompanyName"]
        buildingName = unit["BuildingName"]

        # Fetch amenities specific to the unit
        cursor.execute(
            """
            SELECT aType FROM AmenitiesIn WHERE UnitRentID = %s
        """,
            (unitId,),
        )
        unitAmenities = [amenity["aType"] for amenity in cursor.fetchall()]

        # Fetch amenities provided by the building
        cursor.execute(
            """
            SELECT aType FROM Provides WHERE CompanyName = %s AND BuildingName = %s
        """,
            (companyName, buildingName),
        )
        buildingAmenities = [amenity["aType"] for amenity in cursor.fetchall()]

        # Combine and remove duplicates
        combinedAmenities = ", ".join(set(unitAmenities + buildingAmenities))
        amenitiesByUnit[unitId] = combinedAmenities

    return amenitiesByUnit


# function to handle the advanced search
def advancedSearch(cursor, maxRent, minSquareFootage, amenity):
    # Correct the variable name here to match
    parameters = []

    # Base query that fetches unit details along with unit and building amenities
    query = """
    SELECT au.UnitRentID, au.CompanyName, au.BuildingName, au.unitNumber, au.MonthlyRent, au.squareFootage, au.AvailableDateForMoveIn,
           GROUP_CONCAT(DISTINCT ai.aType ORDER BY ai.aType SEPARATOR ', ') AS UnitAmenities,
           GROUP_CONCAT(DISTINCT p.aType ORDER BY p.aType SEPARATOR ', ') AS BuildingAmenities
    FROM ApartmentUnit au
    LEFT JOIN AmenitiesIn ai ON au.UnitRentID = ai.UnitRentID
    LEFT JOIN Provides p ON au.CompanyName = p.CompanyName AND au.BuildingName = p.BuildingName
    WHERE 1=1
    """

    # Adding conditions based on provided search criteria
    if maxRent:
        query += " AND au.MonthlyRent <= %s"
        parameters.append(maxRent)

    if minSquareFootage:
        query += " AND au.squareFootage >= %s"
        parameters.append(minSquareFootage)

    if amenity:
        query += " AND (ai.aType = %s OR p.aType = %s)"
        # Use 'parameters' consistently
        parameters += [amenity, amenity]  # Correctly adding the amenity parameter twice

    query += " GROUP BY au.UnitRentID"

    # Pass 'parameters' to the execute method
    cursor.execute(query, parameters)


# function to fetch all amenities for select field
def fetchAllAmenities(cursor):
    cursor.execute("SELECT aType FROM Amenities ORDER BY aType")
    return cursor.fetchall()