#############################################################################
# Author: Kirsten Corrao
# Date: 10/1/2019
# Class: CS340
# Sources:
#   https://github.com/knightsamar/CS340_starter_flask_app
#   https://www.youtube.com/watch?v=Z1RJmh_OqeA
#   https://flask.palletsprojects.com/en/1.0.x/
##############################################################################

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from forms import NewTrip, NewUser
from config import Config 

# start flask app
app = Flask(__name__)

# set up database info and secret key 
app.config.from_object(Config)
db = MySQL(app)

# index route
@app.route('/')
def index():
    return render_template("index.html", title="", result="Amazing trip planner!!")

# shows all trips
@app.route('/mytrips')
def myTrips():
    trips = ['Cascade Lakes', 'China', 'Oregon Coast']
    return render_template("mytrips.html", title="- My Trips", trips=trips)

# shows individual trip
@app.route('/trip/<tripName>')
def showTrip(tripName):
    return render_template("mytrips.html", title="- My Trips", tripName=tripName)

# make new trip
@app.route('/newtrip', methods=['GET', 'POST'])
def newTrip():
    form = NewTrip()
    return render_template("newtrip.html", title="- New Trip", form=form)

# add new user 
@app.route('/newuser', methods=['GET', 'POST'])
def newUser():
    form = NewUser()
    return render_template("newuser.html", title=" - New User", form=form)