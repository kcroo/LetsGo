# sources 
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# https://www.youtube.com/watch?v=UIJKdCIEXUQ&t
# DateField: https://stackoverflow.com/questions/26057710/datepickerwidget-with-flask-flask-admin-and-wtforms
# Default values: https://stackoverflow.com/questions/21314068/wtforms-field-defaults-suddenly-dont-work
# coerce-int: https://stackoverflow.com/questions/13964152/not-a-valid-choice-for-dynamic-select-field-wtforms
# select field needs list of tuples: https://stackoverflow.com/questions/6417935/wtforms-too-many-values-to-unpack-with-selectfield
#       http://wtforms.simplecodes.com/docs/0.6/fields.html#wtforms.fields.SelectField

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.widgets.html5 import NumberInput
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, AnyOf, Optional, Email
from datetime import date, timedelta

from travelplanner import db

class NewTrip(FlaskForm):
    tomorrow = date.today() + timedelta(days=1)
    nextWeek = tomorrow + timedelta(weeks=1)

    tripName = StringField('Trip Name', validators=[DataRequired(), Length(min=1, max=255)])
    numberOfPeople = IntegerField('Number of People', default=1, widget=NumberInput(), validators=[NumberRange(min=1, max=100), Optional()])
    startDate = DateField('Start Date', default=tomorrow, validators=[Optional()])
    endDate = DateField('End Date', default=nextWeek, validators=[Optional()])
    submit = SubmitField('Create Trip')

class AddDestination(FlaskForm):
    tomorrow = date.today() + timedelta(days=1)
    nextWeek = tomorrow + timedelta(weeks=1)

    destinationName = StringField('Destination Name', validators=[DataRequired(), Length(min=1, max=255)])
    arriveDate = DateField('Arrive Date', default=tomorrow, validators=[Optional()])
    leaveDate = DateField('Leave Date', default=nextWeek, validators=[Optional()])
    submit = SubmitField('Add Destination')

class AddActivity(FlaskForm):
    activityName = StringField('Activity Name', validators=[DataRequired(), Length(min=1, max=100)])
    activityCost = IntegerField('Cost', widget=NumberInput(), validators=[NumberRange(min=0), Optional()])
    activityType = SelectField('Activity Type', coerce=int, choices=[], validators=[Optional()])
    activityNote = StringField('Notes', validators=[Optional()])
    submit = SubmitField('Add Activity')

class AddActivityType(FlaskForm):
    activityType = StringField('Activity Type', validators=[DataRequired(), Length(min=1, max=100)], render_kw={"Placeholder": "e.g. Rock Climbing or Scuba Diving"})
    submit = SubmitField('Add Activity Type')

    # validate that activity type doesn't already exist
    def validate_activityType(self, activityType):
        query = 'SELECT name FROM activityType WHERE name = %s'
        params = (activityType.data,)
        result = db.runQuery(query, params)
        print(activityType.data)
        print(result)
        if result:
            print('raising error')
            raise ValidationError('Activity Type already exists. Please enter another.')

class NewUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField('Create New User')

    # validation functions MUST begin with validate_ to run 
    def validate_username(self, username):
        query = "SELECT id FROM user WHERE username = '" + username.data + "'" 
        result = db.runQuery(query)
        if result:
            raise ValidationError('Username already exists. Please choose another.')

    def validate_email(self, email):
        query = "SELECT email FROM user WHERE email = %s"
        params = (email,)
        result = db.runQuery(query, params)
        if result:
            raise ValidationError('Email is taken. Please choose another.')

class SwitchUser(FlaskForm):
    user = SelectField('Users', choices=[], validators=[DataRequired()], coerce=int)
    submit = SubmitField('Switch User')

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField('Login')