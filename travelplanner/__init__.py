from flask import Flask
from flask_bcrypt import Bcrypt
from .config import Config 
from .database import Database

# start flask app
app = Flask(__name__)

# set up database info and secret key 
app.config.from_object(Config)
db = Database(app)

# set up bcrypt to encrypt passwords
bcrypt = Bcrypt(app)

from travelplanner import routes