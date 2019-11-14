#############################################################################
# Author: Kirsten Corrao
# Date: 10/1/2019
# Class: CS340
# Sources:
#   https://github.com/knightsamar/CS340_starter_flask_app
#   Best Flask CRUD app tutorial: https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/
#   https://www.youtube.com/watch?v=Z1RJmh_OqeA
#   https://flask.palletsprojects.com/en/1.0.x/
#   URL converter: https://exploreflask.com/en/latest/views.html
#   changing text in submit button: https://stackoverflow.com/questions/32107545/update-text-of-submit-button-in-wtforms
#   how to print form errors: https://stackoverflow.com/questions/10722968/flask-wtf-validate-on-submit-is-never-executed
#   jinja control structures: https://jinja.palletsprojects.com/en/2.10.x/templates/
#   bootstrap modals: https://getbootstrap.com/docs/4.0/components/modal/
##############################################################################

from flask import flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from travelplanner import app, db
from .forms import NewTrip, AddDestination, AddActivity, NewUser, SwitchUser

### replace with user login later ### 
currentUserId = 1

# db test route 
@app.route('/test')
def test():
    result = db.runQuery("SELECT * from trip")
    return render_template("index.html", result=result)


# index route
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", title="") 

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        text = request.form['search']

        if text == '':
            return redirect(url_for('index')) 

        query = "SELECT name FROM trip WHERE userId = " + str(currentUserId) + " AND name LIKE '%" + text + "%'" 
        trips = db.runQuery(query)
        
        query = "SELECT d.name FROM destination d INNER JOIN trip t ON d.tripId = t.id WHERE userId = " + str(currentUserId) + " AND d.name LIKE '%" + text + "%'"
        destinations = db.runQuery(query)

        return render_template("search.html", title="Search", trips=trips, destinations=destinations) 

    return redirect(url_for('index'))

# shows all trips
@app.route('/mytrips')
def myTrips():
    query = "SELECT * FROM trip WHERE id = " + str(currentUserId)
    trips = db.runQuery(query)

    return render_template("mytrips.html", title="- My Trips", trips=trips)

# edit trip
@app.route('/mytrips/<tripId>/edit', methods=['GET', 'POST'])
def editTrip(tripId):
    form = NewTrip()

    if request.method == 'GET':
        query = "SELECT name, userId, numberOfPeople, startDate, endDate FROM trip WHERE id = " + str(tripId)
        result = db.runQuery(query)

        if result[0][1] != currentUserId:
            return redirect(url_for('index'))

        form.tripName.data = result[0][0]
        if result[0][2]:
            form.numberOfPeople.data = result[0][2]
        if result[0][3]:
            form.startDate.data = result[0][3]
        if result[0][4]:
            form.endDate.data = result[0][4]
        form.submit.label.text = 'Edit Trip'
        
        return render_template("newtrip.html", title="- Edit Trip", legend="Edit Trip", form=form)

    elif form.validate_on_submit():
        query = "UPDATE trip SET name=%s, numberOfPeople=%s, startDate=%s, endDate=%s WHERE id = " + tripId 
        params = [form.tripName.data, form.numberOfPeople.data, form.startDate.data, form.endDate.data]
        db.runQuery(query, params=params)

    return redirect(url_for('myTrips'))

# delete trip 
@app.route('/mytrips/<tripId>/delete', methods=['POST'])
def deleteTrip(tripId):
    query = "DELETE FROM trip WHERE id = " + str(tripId)
    db.runQuery(query)
    return redirect(url_for('myTrips'))

# shows individual trip --> show destination(s) for the trip
@app.route('/trip/<tripId>', methods=['GET', 'POST'])
def showTrip(tripId):
    query = "SELECT * FROM destination WHERE tripId = '" + tripId + "'"
    destinations = db.runQuery(query) 
    query = "SELECT name FROM trip WHERE id = '" + tripId + "'"
    tripName = db.runQuery(query)[0][0]

    form = AddDestination()
    return render_template("destination.html", title="- My Trips", tripId=tripId, tripName=tripName, destinations=destinations, form=form)

# shows individual destination and its activities
@app.route('/trip/<tripId>/<destId>', methods=['GET', 'POST'])
def showDestination(tripId, destId):
    query = "SELECT a.name, a.typeId, a.cost, a.notes FROM activity a INNER JOIN destinationActivity da ON da.activityId = a.id WHERE da.destinationId = " + destId
    activities = db.runQuery(query)

    query = "SELECT name FROM activityType"
    choices = db.runQuery(query)[0]

    query = "SELECT name FROM trip WHERE id = " + tripId
    tripName = db.runQuery(query)[0][0]

    query = "SELECT name FROM destination WHERE id = " + destId
    destName = db.runQuery(query)[0][0]

    form = AddActivity()
    #form.activityType.choices = choices
    
    return render_template("activity.html", title="- ", tripId=tripId, tripName=tripName, destName=destName, activities=activities, form=form)

# make new trip
@app.route('/newtrip', methods=['GET', 'POST'])
def newTrip():
    form = NewTrip()
    return render_template("newtrip.html", title="- New Trip", legend="New Trip", form=form)

# add new user 
@app.route('/newuser', methods=['GET', 'POST'])
def newUser():
    form = NewUser()

    if form.validate_on_submit():
        query = "INSERT INTO user(username) VALUES('" + form.username.data + "')"
        db.runQuery(query)
        return redirect(url_for('index'))

    return render_template("newuser.html", title=" - New User", form=form)

# switch user 
@app.route('/switchuser', methods=['GET', 'POST'])
def switchUser():
    global currentUserId
    query = "SELECT id, username FROM user WHERE NOT id = " + str(currentUserId)
    users = db.runQuery(query)
    form = SwitchUser()
    form.user.choices = users

    if form.validate_on_submit():
        currentUserId = form.user.data
        return redirect(url_for('index'))

    return render_template("switchuser.html", title="- Switch User", form=form)