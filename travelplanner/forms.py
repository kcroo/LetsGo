# sources 
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# https://www.youtube.com/watch?v=UIJKdCIEXUQ&t
# DateField: https://stackoverflow.com/questions/26057710/datepickerwidget-with-flask-flask-admin-and-wtforms
# Default values: https://stackoverflow.com/questions/21314068/wtforms-field-defaults-suddenly-dont-work

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.widgets.html5 import NumberInput
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from datetime import date, timedelta

from travelplanner import db

class NewTrip(FlaskForm):
    tomorrow = date.today() + timedelta(days=1)
    nextWeek = tomorrow + timedelta(weeks=1)

    tripName = StringField('Trip Name', validators=[DataRequired(), Length(min=1, max=255)])
    numberOfPeople = IntegerField('Number of People', default=1, widget=NumberInput(), validators=[NumberRange(min=1, max=100)])
    startDate = DateField('Start Date', default=tomorrow)
    endDate = DateField('End Date', default=nextWeek)
    submit = SubmitField('Create Trip')

class AddDestination(FlaskForm):
    destinationName = StringField('Destination Name', validators=[DataRequired(), Length(min=1, max=255)])
    arriveDate = DateField('Arrive Date')
    leaveDate = DateField('Leave Date')
    submit = SubmitField('Add Destination')

class AddActivity(FlaskForm):
    activityName = StringField('Activity Name', validators=[DataRequired(), Length(min=1, max=100)])
    activityCost = IntegerField('Cost', widget=NumberInput(), validators=[NumberRange(min=0)])
    activityType = SelectField('Activity Type', choices=[])
    submit = SubmitField('Add Activity')
 
class NewUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    submit = SubmitField('Create New User')

    # validation functions MUST begin with validate_ to run 
    def validate_username(self, username):
        query = "SELECT id FROM user WHERE username = '" + username.data + "'" 
        result = db.runQuery(query)
        if result:
            raise ValidationError('Username already exists. Please choose another.')

class SwitchUser(FlaskForm):
    user = SelectField('Users', choices=[], validators=[DataRequired()])
    submit = SubmitField('Switch User')