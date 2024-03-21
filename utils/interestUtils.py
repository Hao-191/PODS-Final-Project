def postNewInterestToUnit(cursor, username, unitRentID, roommateCount, moveInDate):
    cursor.execute(
        """
        INSERT INTO Interests (username, UnitRentID, RoommateCnt, MoveInDate)
        VALUES (%s, %s, %s, %s)
        """,
        (username, unitRentID, roommateCount, moveInDate),
    )


def fetchUnitDetailsForInterest(cursor, unitRentID):
    cursor.execute("SELECT * FROM ApartmentUnit WHERE UnitRentID = %s", (unitRentID,))
    return cursor.fetchone()
