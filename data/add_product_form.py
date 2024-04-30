from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, SelectField


class AddProductForm(FlaskForm):
    name = StringField()
    price = StringField()
    desc = TextAreaField()
    group = SelectField(choices=['Drinks', 'Food'])
    file = FileField()

