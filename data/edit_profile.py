from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField


class EditProfileForm(FlaskForm):
    name = StringField('Your name')
    surname = StringField('Your surname')
    email = StringField('Your email')
    phone = StringField('Your phone')
    file = FileField('Image')
    street = StringField('Street')
    apartment = StringField('Apartment')
    entrance = StringField('Entrance')
    floor = StringField('Floor')
    intercom = StringField('Intercom')
    comment = TextAreaField('Comment', render_kw={"rows": 10})
    submit = SubmitField('Save Changes')
