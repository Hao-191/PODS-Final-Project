from flask import Flask
from blueprints.userAuthBlueprint import userAuth
from blueprints.userHomeBlueprint import userHome
from blueprints.userPetBlueprint import userPet
from blueprints.apartmentBlueprint import apartment
from blueprints.interestBlueprint import interest

app = Flask(__name__)
app.secret_key = "secret key"
app.register_blueprint(userAuth)
app.register_blueprint(userHome)
app.register_blueprint(userPet)
app.register_blueprint(apartment)
app.register_blueprint(interest)