from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    name = StringField()
    price = StringField()
    desc = TextAreaField()
    group = SelectField(choices=['Drinks', 'Food'])
    file = FileField()

