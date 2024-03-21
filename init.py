# Import Flask Library
from flask import render_template

from app import app

from databaseConnection import get_db_connection

# Configure MySQL
conn = get_db_connection()


# Define a route to hello function
@app.route("/")
def hello():
    return render_template("userAuthPages/login.html")


app.secret_key = "some key that you will never guess"
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
