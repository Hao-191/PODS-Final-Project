# function to fetch unit info
def fetchUnitInfo(cursor, unitRentID):
    cursor.execute(
        """
            SELECT au.*, ab.AddrStreet, ab.AddrCity, ab.AddrState, ab.AddrZipCode
            FROM ApartmentUnit au
            JOIN ApartmentBuilding ab ON au.CompanyName = ab.CompanyName AND au.BuildingName = ab.BuildingName
            WHERE au.UnitRentID = %s
        """,
        (unitRentID,),
    )

    return cursor.fetchone()


# function to fetch unit rooms
def fetchUnitRooms(cursor, unitRentID):
    cursor.execute(
        """
            SELECT * FROM Rooms WHERE UnitRentID = %s
            """,
        (unitRentID,),
    )

    return cursor.fetchall()


# function to fetch unit amenities
def fetchUnitAmenities(cursor, unitRentID):
    cursor.execute(
        """
            SELECT a.aType, a.Description FROM AmenitiesIn ai
            JOIN Amenities a ON ai.aType = a.aType
            WHERE ai.UnitRentID = %s
        """,
        (unitRentID,),
    )

    return cursor.fetchall()


# function to fetch unit interests
def fetchUnitInterests(cursor, unitRentID):
    cursor.execute(
        """
            SELECT * FROM Interests WHERE UnitRentID = %s
        """,
        (unitRentID,),
    )
    return cursor.fetchall()
