# function to fetch building details by companyName, buildingName
def fetchBuildingDetails(cursor, companyName, buildingName):
    cursor.execute(
        """
                SELECT * FROM ApartmentBuilding
                WHERE CompanyName = %s AND BuildingName = %s
        """,
        (companyName, buildingName),
    )
    return cursor.fetchone()


# function to fetch building amenities by companyName, buildingName
def fetchBuildingAmenities(cursor, companyName, buildingName):
    cursor.execute(
        """
                SELECT a.aType, a.Description, p.Fee, p.waitingList FROM Provides p
                JOIN Amenities a ON p.aType = a.aType
                WHERE p.CompanyName = %s AND p.BuildingName = %s
        """,
        (companyName, buildingName),
    )
    return cursor.fetchall()


# function to fetch building available unit counts by companyName, buildingName
def fetchBuildingAvailableUnitCounts(cursor, companyName, buildingName):
    cursor.execute(
        """
                SELECT COUNT(*) AS AvailableUnits FROM ApartmentUnit
                WHERE CompanyName = %s AND BuildingName = %s AND AvailableDateForMoveIn <= CURDATE()
        """,
        (companyName, buildingName),
    )
    return cursor.fetchone()["AvailableUnits"]


# function to fetch building pet policies by companyName, buildingName
def fetchBuildingPetPolicies(cursor, companyName, buildingName):
    cursor.execute(
        """
                SELECT PetType, PetSize, isAllowed, RegistrationFee, MonthlyFee FROM PetPolicy
                WHERE CompanyName = %s AND BuildingName = %s
        """,
        (companyName, buildingName),
    )
    return cursor.fetchall()
