from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    name = StringField('Your name: ')
    surname = StringField('Your surname: ')
    email = StringField('Email: ')
    phone = StringField('Phone number: ')
    file = FileField('Image')
    submit = SubmitField('Save Changes')
