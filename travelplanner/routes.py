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
#
#   sql wildcards and LIKE: https://stackoverflow.com/questions/3134691/python-string-formats-with-sql-wildcards-and-like
#
#   last_insert_id() in mysql: https://dev.mysql.com/doc/refman/8.0/en/information-functions.html#function_last-insert-id
#   make tuple of tuples returned from db into a list: https://stackoverflow.com/questions/3204245/how-do-i-convert-a-tuple-of-tuples-to-a-one-dimensional-list-using-list-comprehe/3204267#3204267

##############################################################################

from flask import flash, render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flask_mysqldb import MySQL
from travelplanner import app, db, bcrypt
from .forms import NewTrip, AddDestination, AddActivity, Login, NewUser, SwitchUser
from .login import User, loadUser

# index route
@app.route('/', methods=['GET'])
def index():
    username = ""
    if current_user.is_authenticated:
        username = current_user.username.capitalize()

    return render_template("index.html", title="", username=username) 

@app.route('/search', methods=['POST'])
@login_required
def search():
    if request.method == 'POST':
        text = request.form['search']

        # search for each word in text (separated by space)
        words = text.split()

        trips = []
        destinations = []
        activities = []

        for word in words:
            likeText = '%' + word + '%'

            # get matching trips
            query = "SELECT id, name FROM trip WHERE userId = %s AND name LIKE %s"
            params = (current_user.id, likeText)
            result = db.runQuery(query, params=params)

            for r in result:
                trips.append(r)
            
            # get matching destinations
            query = "SELECT t.id, d.id, d.name FROM destination d INNER JOIN trip t ON d.tripId = t.id WHERE userId = %s AND d.name LIKE %s"
            params = (current_user.id, likeText)
            result = db.runQuery(query, params=params)

            for r in result:
                destinations.append(r)

            # get matching activities
            query = """SELECT t.id, d.id, d.name, a.name FROM activity a 
                        INNER JOIN activityType at ON a.typeId = at.id
                        INNER JOIN destinationActivity da ON a.id = da.activityId
                        INNER JOIN destination d ON da.destinationId = d.id 
                        INNER JOIN trip t ON d.tripId = t.id
                        WHERE t.userId = %s AND (a.name LIKE %s OR a.notes LIKE %s OR at.name LIKE %s)
                        """
            params = (current_user.id, likeText, likeText, likeText)
            result = db.runQuery(query, params=params)

            for r in result:
                activities.append(r)

        return render_template("search.html", title="Search", trips=trips, destinations=destinations, activities=activities, username=current_user.username.capitalize()) 

    return redirect(url_for('index'))

# shows all trips
@app.route('/mytrips')
@login_required
def myTrips():
    query = "SELECT * FROM trip WHERE userId = %s"
    params = (str(current_user.id))
    trips = db.runQuery(query, params) 
    print(current_user.username)

    return render_template("mytrips.html", title="- My Trips", trips=trips, username=current_user.username.capitalize())

# edit trip
@app.route('/mytrips/<tripId>/editT', methods=['GET', 'POST'])
@login_required
def editTrip(tripId):
    form = NewTrip()

    if request.method == 'GET':
        query = "SELECT name, userId, numberOfPeople, startDate, endDate FROM trip WHERE id = " + str(tripId)
        result = db.runQuery(query)

        form.tripName.data = result[0][0]
        if result[0][2]:
            form.numberOfPeople.data = result[0][2]
        if result[0][3]:
            form.startDate.data = result[0][3]
        if result[0][4]:
            form.endDate.data = result[0][4]
        form.submit.label.text = 'Edit Trip'
        
        return render_template("editTrip.html", title="- Edit Trip", legend="Edit Trip", form=form, username=current_user.username.capitalize())

    elif form.validate_on_submit():
        query = "UPDATE trip SET name=%s, numberOfPeople=%s, startDate=%s, endDate=%s WHERE id = " + tripId 
        params = [form.tripName.data, form.numberOfPeople.data, form.startDate.data, form.endDate.data]
        db.runQuery(query, params=params)

    return redirect(url_for('myTrips'))

# delete trip 
@app.route('/mytrips/<tripId>/delete', methods=['POST'])
@login_required
def deleteTrip(tripId):
    query = "DELETE FROM trip WHERE id = " + str(tripId)
    db.runQuery(query)
    return redirect(url_for('myTrips'))

# shows individual trip --> show destination(s) for the trip
@app.route('/trip/<tripId>', methods=['GET', 'POST'])
@login_required
def showTrip(tripId):
    query = "SELECT * FROM destination WHERE tripId = '" + tripId + "'"
    destinations = db.runQuery(query) 
    query = "SELECT name FROM trip WHERE id = '" + tripId + "'"
    tripName = db.runQuery(query)[0][0]

    form = AddDestination()
    return render_template("destination.html", title="- My Trips", tripId=tripId, tripName=tripName, destinations=destinations, form=form, username=current_user.username.capitalize())

# edit destination
@app.route('/trip/<tripId>/<destId>/editD', methods=['GET', 'POST'])
@login_required
def editDestination(tripId,destId):
    form = AddDestination()

    if request.method == 'GET':
        query = "SELECT name, tripId, arriveDate, leaveDate FROM destination WHERE id = %s"
        params = (destId,)
        result = db.runQuery(query, params)

        query = "SELECT name FROM trip WHERE id = %s"
        params = (tripId,)
        tripName = db.runQuery(query, params)[0][0]

        form.destinationName.data = result[0][0]
        if result[0][2]:
            form.arriveDate.data = result[0][2]
        if result[0][3]:
            form.leaveDate.data = result[0][3]
        form.submit.label.text = 'Edit Destination'
        
        return render_template("editDestination.html", title="- Edit Destination", legend="Edit Destination", tripId=tripId, tripName=tripName, destId=destId, form=form,  username=current_user.username.capitalize())

    elif form.validate_on_submit():
        query = "UPDATE destination SET name=%s, arriveDate=%s, leaveDate=%s WHERE id = " + destId 
        params = [form.destinationName.data, form.arriveDate.data, form.leaveDate.data]
        db.runQuery(query, params=params)

    return redirect(url_for('showTrip', tripId=tripId))

# delete destination 
@app.route('/mytrips/<tripId>/<destId>/delete', methods=['POST'])
def deleteDestination(tripId, destId):
    # select all activities associated with this destination (may need to delete these activities)
    query = "SELECT a.id FROM activity a INNER JOIN destinationActivity da ON da.activityId = a.id WHERE da.destinationId = %s"
    params = (destId,)
    activities = db.runQuery(query, params)

    # delete destination (also deletes associated destinationActivity)
    query = "DELETE FROM destination WHERE id = %s"
    params = (destId,)
    db.runQuery(query, params)

    # if associated activity isn't used by any other destination: delete it also 
    for a in activities:
        query = "SELECT activityId FROM destinationActivity WHERE activityId = %s"
        params = (a,)
        result = db.runQuery(query, params)
        if not result:
            query = "DELETE FROM activity WHERE id = %s"
            db.runQuery(query, params)
    

    return redirect(url_for('showTrip', tripId=tripId))

# show activity --> shows individual destination and its activities
@app.route('/trip/<tripId>/<destId>', methods=['GET', 'POST'])
@login_required
def showDestination(tripId, destId):
    query = "SELECT a.id, a.name, a.typeId, a.cost, a.notes FROM activity a INNER JOIN destinationActivity da ON da.activityId = a.id WHERE da.destinationId = " + destId
    activities = db.runQuery(query)

    query = "SELECT name FROM activityType"
    choices = db.runQuery(query)[0]

    query = "SELECT name FROM trip WHERE id = " + tripId
    tripName = db.runQuery(query)[0][0]

    query = "SELECT name FROM destination WHERE id = " + destId
    destName = db.runQuery(query)[0][0]

    form = AddActivity()
    #form.activityType.choices = choices
    
    return render_template("activity.html", title="- ", tripId=tripId, destId=destId, tripName=tripName, destName=destName, activities=activities, form=form, username=current_user.username.capitalize())

# edit activity
@app.route('/trip/<tripId>/<destId>/<actId>/editA', methods=['GET', 'POST'])
@login_required
def editActivity(tripId,destId,actId):
    form = AddActivity()

    if request.method == 'GET':
        query = "SELECT a.id, a.name, a.typeId, a.cost, a.notes FROM activity a INNER JOIN destinationActivity da ON da.activityId = a.id WHERE da.activityId = " + str(actId)
        result = db.runQuery(query)

        query = "SELECT name FROM trip WHERE id = " + str(tripId)
        tripName = db.runQuery(query)[0][0]

        query = "SELECT name FROM destination WHERE id = " + str(destId)
        destName = db.runQuery(query)[0][0]

        form.activityName.data = result[0][1]
        if result[0][2]:
            form.activityType.data = result[0][2]
        if result[0][3]:
            form.activityCost.data = result[0][3]
        if result[0][4]:
            form.activityNote.data = result[0][4]
        form.submit.label.text = 'Edit Activity'
        
        return render_template("editActivity.html", title="- Edit Activity", legend="Edit Activity", tripId=tripId, tripName=tripName, destId=destId, destName=destName, actId=actId, activities=result, form=form, username=current_user.username.capitalize())

    elif form.validate_on_submit():
        query = "UPDATE activity SET name=%s, cost=%s, typeId=%s, notes=%s WHERE id = %s"

        if form.activityType.data == 'None':
            form.activityType.data = None

        print(form.activityName.data, form.activityCost.data, form.activityType.data, form.activityNote.data, actId)
        params = [form.activityName.data, form.activityCost.data, form.activityType.data, form.activityNote.data, actId]
        db.runQuery(query, params=params)

    return redirect(url_for('showDestination', tripId=tripId, destId=destId))

# delete activity 
@app.route('/mytrips/<tripId>/<destId>/<actId>/delete', methods=['POST'])
def deleteActivity(tripId, destId, actId):
    # delete instance in destinationActivity
    query = "DELETE FROM destinationActivity WHERE destinationId = %s AND activityId = %s"
    params = (destId, actId)
    db.runQuery(query, params)

    # if activity is NOT shared by another destination, also delete activity
    query = "SELECT destinationId FROM destinationActivity WHERE activityId = %s"
    params = (actId,)
    otherDestinations = db.runQuery(query, params)

    if not otherDestinations:
        query = "DELETE FROM activity WHERE id = %s"
        params = (actId,)
        db.runQuery(query, params)

    return redirect(url_for('showDestination', tripId=tripId, destId=destId))

# make new trip
@app.route('/newtrip', methods=['GET', 'POST'])
@login_required
def newTrip():
    form = NewTrip()

    if request.method == 'GET':
        return render_template("newtrip.html", title="- New Trip", legend="New Trip", form=form, username=current_user.username.capitalize())

    elif request.method == 'POST' and form.validate_on_submit():
        query = "INSERT INTO trip (name, userId, numberOfPeople, startDate, endDate) VALUES (%s, %s, %s, %s, %s)"
        params = (form.tripName.data, current_user.id, form.numberOfPeople.data, form.startDate.data, form.endDate.data)
        db.runQuery(query, params=params)

        query = "SELECT LAST_INSERT_ID()"
        id = db.runQuery(query)[0][0]

        return redirect(url_for('myTrips', tripId=id))

    else:
        return redirect(url_for('myTrips'))

# make new destination
@app.route('/newDestination', methods=['GET', 'POST'])
@login_required
def newDestination():
    form = AddDestination()

    if request.method == 'GET':
        return render_template("newDestination.html", title="- Add Destination", legend="Add Destination", form=form, username=current_user.username.capitalize())

    elif request.method == 'POST' and form.validate_on_submit():
        query = "INSERT INTO trip (name, userId, numberOfPeople, startDate, endDate) VALUES (%s, %s, %s, %s, %s)"
        params = (form.tripName.data, current_user.id, form.numberOfPeople.data, form.startDate.data, form.endDate.data)
        db.runQuery(query, params=params)

        query = "SELECT LAST_INSERT_ID()"
        id = db.runQuery(query)[0][0]

        return redirect(url_for('showTrip', tripId=id))

    else:
        return redirect(url_for('showTrip'))

# make new activity
@app.route('/newActivity', methods=['GET', 'POST'])
@login_required
def newActivity():
    form = AddActivity()

    if request.method == 'GET':
        return render_template("newActivity.html", title="- Add Activity", legend="Add Activity", form=form, username=current_user.username.capitalize())

    elif request.method == 'POST' and form.validate_on_submit():
        query = "INSERT INTO trip (name, userId, numberOfPeople, startDate, endDate) VALUES (%s, %s, %s, %s, %s)"
        params = (form.tripName.data, current_user.id, form.numberOfPeople.data, form.startDate.data, form.endDate.data)
        db.runQuery(query, params=params)

        query = "SELECT LAST_INSERT_ID()"
        id = db.runQuery(query)[0][0]

        return redirect(url_for('showDestination', tripId=id))

    else:
        return redirect(url_for('showDestination'))

# add new user 
@app.route('/newuser', methods=['GET', 'POST'])
def newUser():
    form = NewUser()

    if form.validate_on_submit():
        # generate hashed password: decode converts it from bytes literal to string 
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        query = "INSERT INTO user(username, email, pw) VALUES(%s, %s, %s)"
        params = (form.username.data.lower(), form.email.data, hashedPassword)
        db.runQuery(query, params)
        return redirect(url_for('index'))

    return render_template("newuser.html", title=" - New User", form=form)

# log in 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = Login()

    if request.method == 'POST':
        username = form.username.data.lower()
        query = 'SELECT id, pw FROM user WHERE username = %s'
        params = (username,)
        result = db.runQuery(query, params)

        if result and bcrypt.check_password_hash(result[0][1], form.password.data):
            login_user(User(id=result[0][0], username=username))
            flash('You are now logged in.', 'success')
            return redirect(url_for('index'))
        else:
            print("invalid password")
            flash('Login failed. Please check username and password.', 'danger')

    return render_template("login.html", title="- Login", form=form)

# log out 
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You are now logged out.', 'success')
    return redirect(url_for('index'))

# reset database 
@app.route('/reset', methods=['GET'])
def resetDB():
    # drop all tables
    query = []

    query.append("SET FOREIGN_KEY_CHECKS=0;")
    query.append("DROP TABLE IF EXISTS user;")
    query.append("DROP TABLE IF EXISTS trip;")
    query.append("DROP TABLE IF EXISTS destination;")
    query.append("DROP TABLE IF EXISTS activityType;")
    query.append("DROP TABLE IF EXISTS activity;")
    query.append("DROP TABLE IF EXISTS destinationActivity;")
    query.append("SET FOREIGN_KEY_CHECKS=1;")

    db.runMultipleQueries(query)

    # make all tables
    query.append("CREATE TABLE user (id INT AUTO_INCREMENT, username VARCHAR(20) UNIQUE NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, pw CHAR(60) NOT NULL, PRIMARY KEY(id));")
    query.append("CREATE TABLE trip (id INT AUTO_INCREMENT, name VARCHAR(255) NOT NULL, userId INT NOT NULL, numberOfPeople INT, startDate DATE, endDate DATE, PRIMARY KEY(id), FOREIGN KEY fkUser(userId) REFERENCES user(id) ON DELETE CASCADE);")
    query.append("CREATE TABLE destination (id INT AUTO_INCREMENT, name VARCHAR(255) NOT NULL, tripId INT NOT NULL, arriveDate DATE, leaveDate DATE, PRIMARY KEY(id), FOREIGN KEY fkTrip(tripId) REFERENCES trip(id) ON DELETE CASCADE);")
    query.append("CREATE TABLE activityType (id int AUTO_INCREMENT, name VARCHAR(100) NOT NULL, PRIMARY KEY(id));")
    query.append("CREATE TABLE activity (id INT AUTO_INCREMENT, name VARCHAR(100) NOT NULL, typeId int NULL, cost INT, notes VARCHAR(255), PRIMARY KEY(id), FOREIGN KEY fkType(typeId) REFERENCES activityType(id) ON DELETE SET NULL);")
    query.append("CREATE TABLE destinationActivity (destinationId INT NOT NULL, activityId INT NOT NULL, PRIMARY KEY(destinationId, activityId), FOREIGN KEY fkDest(destinationId) REFERENCES destination(id) ON DELETE CASCADE, FOREIGN KEY fkAct(activityId) REFERENCES activity(id) ON DELETE CASCADE);")

    db.runMultipleQueries(query)

    # users
    hashedPassword = bcrypt.generate_password_hash('samwise').decode('utf-8')
    query = "INSERT INTO user (username, email, pw) VALUES(%s, %s, %s)"
    params = ('samwise', 'sam@gamgee.com', hashedPassword)
    db.runQuery(query, params=params)

    hashedPassword = bcrypt.generate_password_hash('frodo').decode('utf-8')
    query = "INSERT INTO user (username, email, pw) VALUES(%s, %s, %s)"
    params = ('frodo', 'frodo@baggins.com', hashedPassword)
    db.runQuery(query, params=params)
    
    query = []

    # trips 
    query.append("INSERT INTO trip (name, userId, numberOfPeople, startDate, endDate) VALUES('Cascade Lakes', 1, 2, '2020-08-10', '2020-08-15')")
    query.append("INSERT INTO trip (name, userId, numberOfPeople) VALUES('China', 2, 1)")
    query.append("INSERT INTO trip (name, userId) VALUES('Oregon Coast', 1)")

    # destinations
    query.append("INSERT INTO destination (name, tripId, arriveDate, leaveDate) VALUES('Mt Bachelor', 1, '2020-08-10', '2020-08-12')")
    query.append("INSERT INTO destination (name, tripId, arriveDate, leaveDate) VALUES('Devil''s Lake', 1, '2020-08-12', '2020-08-15')")
    query.append("INSERT INTO destination (name, tripId) VALUES('Beijing', 2)")
    query.append("INSERT INTO destination (name, tripId) VALUES('Xi''An', 2)")
    query.append("INSERT INTO destination (name, tripId) VALUES('Tillamook', 3)")
    query.append("INSERT INTO destination (name, tripId) VALUES('Florence', 3)")

    # activity types 
    query.append("INSERT INTO activityType(name) VALUES('Eating')")
    query.append("INSERT INTO activityType(name) VALUES('Sightseeing')")
    query.append("INSERT INTO activityType(name) VALUES('Nightlife')")
    query.append("INSERT INTO activityType(name) VALUES('Shopping')")
    query.append("INSERT INTO activityType(name) VALUES('Hiking')")
    query.append("INSERT INTO activityType(name) VALUES('Biking')")
    query.append("INSERT INTO activityType(name) VALUES('Backpacking')")
    query.append("INSERT INTO activityType(name) VALUES('Hunting')")
    query.append("INSERT INTO activityType(name) VALUES('Boating')")
    query.append("INSERT INTO activityType(name) VALUES('Fishing')")
    query.append("INSERT INTO activityType(name) VALUES('Kayaking')")
    query.append("INSERT INTO activityType(name) VALUES('Canoeing')")
    query.append("INSERT INTO activityType(name) VALUES('Paddleboarding')")
    query.append("INSERT INTO activityType(name) VALUES('Swimming')")
    query.append("INSERT INTO activityType(name) VALUES('Skiing')")
    query.append("INSERT INTO activityType(name) VALUES('Snowboarding')")
    query.append("INSERT INTO activityType(name) VALUES('Cross Country Skiing')")
    query.append("INSERT INTO activityType(name) VALUES('Snowshoeing')")
    query.append("INSERT INTO activityType(name) VALUES('Snowmobiling')")
    query.append("INSERT INTO activityType(name) VALUES('OHV')")

    # activities
    query.append("INSERT INTO activity(name, typeId, cost, notes) VALUES('Phil''s Trailhead', 6, 0, 'Tons of great MB trails.');")
    query.append("INSERT INTO activity(name, typeId, notes) VALUES('Summit South Sister', 5, 'Gains 4900 feet in 5.5 miles wow');")

    query.append("INSERT INTO activity(name, typeId, cost, notes) VALUES('Forbidden City', 1, 60, 'Additional fee for areas inside. Close to Tiananmen Square');")
    query.append("INSERT INTO activity(name, typeId, cost, notes) VALUES('Mutianyu Great Wall', 1, 60, 'Tobaggan from the great wall??');")
    query.append("INSERT INTO activity(name, typeId, notes) VALUES('Sanlitun', 3, 'TONS of bars');")
    query.append("INSERT INTO activity(name, typeId, cost, notes) VALUES('City Wall', 1, 54, 'Long walk in sun--do on cloudy day');")
    query.append("INSERT INTO activity(name, typeId, notes) VALUES('Muslim Quarter', 2, 'Culture, street food');")
    query.append("INSERT INTO activity(name, typeId, cost, notes) VALUES('Terracotta Warriors', 1, 150, 'outside city--how much is bus?');")

    query.append("INSERT INTO activity(name, typeId, cost, notes) VALUES('Tillamook Cheese Factory', 1, 0, 'Free cheese!');")
    query.append("INSERT INTO activity(name, typeId, cost, notes) VALUES('Oregon Sand Dunes National Rec Area', 18, 140, 'Price for 250cc and day fee');")

    # link destination and activity
    # cascade lakes: share all activities 
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(1,1);")
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(1,2);")
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(2,1);")
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(2,2);")

    # beijing
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(3,3);")
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(3,4);")
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(3,5);")

    # xi'an
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(4,6);")
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(4,7);")
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(4,8);")

    # oregon coast 
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(5,9);")
    query.append("INSERT INTO destinationActivity(destinationId, activityId) VALUES(6,10);")

    db.runMultipleQueries(query)

    return render_template("index.html", title="") 
