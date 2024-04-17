from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    name = StringField('Your name')
    surname = StringField('Your surname')
    email = StringField('Email')
    phone = StringField('Phone number')
    file = FileField('Image')
    street = StringField('Street')
    apartment = StringField('Apartment')
    entrance = StringField('Entrance')
    floor = StringField('Floor')
    intercom = StringField('Intercom')
    comment = TextAreaField('Comment for courier', render_kw={"rows": 10})
    submit = SubmitField('Save Changes')
