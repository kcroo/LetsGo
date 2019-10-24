#############################################################################
# Author: Kirsten Corrao
# Date: 10/1/2019
# Class: CS340
# Sources:
#   https://github.com/knightsamar/CS340_starter_flask_app
#   https://www.youtube.com/watch?v=Z1RJmh_OqeA
#   https://flask.palletsprojects.com/en/1.0.x/
#   URL converter: https://exploreflask.com/en/latest/views.html
##############################################################################

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from forms import NewTrip, AddDestination, NewUser, SwitchUser
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
@app.route('/trip/<tripName>', methods=['GET', 'POST'])
def showTrip(tripName):
    ### fill destinations with db results later
    if tripName == 'Cascade Lakes':
        destinations = ['Mt Bachelor', 'Devil\'s Lake']
    elif tripName == 'China':
        destinations = ['Beijing', 'Harbin']
    elif tripName == 'Oregon Coast':
        destinations = ['Florence', 'Newport']

    form = AddDestination()
    return render_template("mytrips.html", title="- My Trips", tripName=tripName, destinations=destinations, form=form)

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

# switch user 
@app.route('/switchuser', methods=['GET', 'POST'])
def switchUser():
    # tuple: what will be returned (i.e. userId), then what will be displayed in form (i.e. username) 
    users = [(1, 'Frodo'), (2, 'Sam'), (3, 'Merry'), (4, 'Pippin')]
    form = SwitchUser()
    form.user.choices = users
    return render_template("switchuser.html", title="- Switch User", form=form)