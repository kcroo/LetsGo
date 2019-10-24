# sources 
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# https://www.youtube.com/watch?v=UIJKdCIEXUQ&t

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length

class NewTrip(FlaskForm):
    tripName = StringField('Trip Name', validators=[DataRequired(), Length(min=1, max=255)])
    numberOfPeople = IntegerField('Number of People')
    startDate = DateField('Start Date')
    endDate = DateField('End Date')
    submit = SubmitField('Create Trip')