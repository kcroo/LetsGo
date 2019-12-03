# sources 
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# https://www.youtube.com/watch?v=UIJKdCIEXUQ&t
# DateField: https://stackoverflow.com/questions/26057710/datepickerwidget-with-flask-flask-admin-and-wtforms
# Default values: https://stackoverflow.com/questions/21314068/wtforms-field-defaults-suddenly-dont-work
# coerce-int: https://stackoverflow.com/questions/13964152/not-a-valid-choice-for-dynamic-select-field-wtforms
# select field needs list of tuples: https://stackoverflow.com/questions/6417935/wtforms-too-many-values-to-unpack-with-selectfield
#       http://wtforms.simplecodes.com/docs/0.6/fields.html#wtforms.fields.SelectField

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms.widgets.html5 import NumberInput
from wtforms.widgets import HiddenInput
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, AnyOf, Optional, Email
from datetime import date, timedelta

from travelplanner import db

class NewTrip(FlaskForm):
    startDefault = date.today() + timedelta(days=30)
    endDefault = startDefault + timedelta(weeks=2)

    tripName = StringField('Trip Name', validators=[DataRequired(), Length(min=1, max=255)], render_kw={"Placeholder": "e.g. California Roadtrip or Backpacking Europe"})
    numberOfPeople = IntegerField('Number of People', default=1, widget=NumberInput(), validators=[NumberRange(min=1, max=100), Optional()])
    startDate = DateField('Start Date', default=startDefault, validators=[Optional()])
    endDate = DateField('End Date', default=endDefault, validators=[Optional()])
    submit = SubmitField('Create Trip')

    def validate_endDate(self, endDate):
        if endDate.data < self.startDate.data:
            raise ValidationError('End Date cannot be before Start Date.')

class AddDestination(FlaskForm):
    tripId = HiddenField()
    tripStart = DateField(widget=HiddenInput())
    tripEnd = DateField(widget=HiddenInput())

    destinationName = StringField('Destination Name', validators=[DataRequired(), Length(min=1, max=255)], render_kw={"Placeholder": "e.g. Yosemite National Park or Paris"})
    arriveDate = DateField('Arrive Date', validators=[Optional()])
    leaveDate = DateField('Leave Date', validators=[Optional()])
    submit = SubmitField('Add Destination')

    # makes sure destination dates are between trip dates; and that arrival date is before leave date
    def validate_arriveDate(self, arriveDate):
        if self.arriveDate.data:
            if self.tripStart.data and self.tripStart.data > self.arriveDate.data:
                raise ValidationError(f'Error: cannot arrive to destination before trip start date ({self.tripStart.data}).')
            if self.leaveDate.data and self.arriveDate.data > self.leaveDate.data:
                raise ValidationError('Error: arrive date cannot be after leave date.')

    def validate_leaveDate(self, leaveDate):
        if self.leaveDate.data and self.tripEnd.data:
            if self.tripEnd.data < self.leaveDate.data:
                raise ValidationError(f'Error: cannot leave destination after trip end date ({self.tripEnd.data}).')

class AddActivity(FlaskForm):
    activityName = StringField('Activity Name', validators=[DataRequired(), Length(min=1, max=100)], render_kw={"Placeholder": "e.g. Half Dome Trail or Eiffel Tower"})
    activityCost = IntegerField('Cost', widget=NumberInput(), validators=[NumberRange(min=0), Optional()])
    activityType = SelectField('Activity Type', coerce=int, choices=[], validators=[Optional()])
    activityNote = StringField('Notes', validators=[Optional()])
    submit = SubmitField('Add Activity')

    # make sure cost is not negative
    def validate_activityCost(self, activityCost):
        if activityCost and activityCost.data < 0:
            raise ValidationError('Cost cannot be negative.')

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