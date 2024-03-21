# function to login verification or register check exists
def fetchUserInfo(cursor, username):
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    return cursor.fetchone()


# function to register new account
def registerNewAccount(
    cursor, username, first_name, last_name, dob, gender, email, phone, hashed_password
):
    query = """
            INSERT INTO Users (username, first_name, last_name, DOB, gender, email, Phone, passwd) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
    cursor.execute(
        query,
        (username, first_name, last_name, dob, gender, email, phone, hashed_password),
    )
