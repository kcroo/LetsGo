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
from forms import NewTrip, AddDestination, AddActivity, NewUser, SwitchUser
from config import Config 
from database import Database

# start flask app
app = Flask(__name__)

# set up database info and secret key 
app.config.from_object(Config)
db = Database(app)


# db test route 
@app.route('/test')
def test():
    result = db.runQuery("SELECT * from trip")
    return render_template("index.html", result=result)


# index route
@app.route('/')
def index():
    return render_template("index.html", title="")

# shows all trips
@app.route('/mytrips')
def myTrips():
    trips = db.runQuery("SELECT * FROM trip")

    return render_template("mytrips.html", title="- My Trips", trips=trips)

# shows individual trip
@app.route('/trip/<tripName>', methods=['GET', 'POST'])
def showTrip(tripName):
    query = "SELECT * FROM destination WHERE name = '" + tripName + "'"
    destinations = db.runQuery(query) 

    form = AddDestination()
    return render_template("mytrips.html", title="- My Trips", tripName=tripName, destinations=destinations, form=form)

# shows individual destination and its activities
@app.route('/trip/<tripName>/<destName>', methods=['GET', 'POST'])
def showDestination(tripName, destName):
    ### fill with db results later
    activities = None 
    for a in allActivities:
        for key, values in a.items(): 
            if key == destName: 
                    activities = values 

    choices = [(0, ''), (1, 'Sightseeing'), (2, 'Dining'), (3, 'Hiking'), (4, 'Backpacking'), (5, 'Cycling'), (6, 'Mountain Biking')]
    form = AddActivity()
    form.activityType.choices = choices
    
    return render_template("destination.html", title="- ", tripName=tripName, destName=destName, activities=activities, form=form)

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