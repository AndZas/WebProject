from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    desc = StringField(validators=[DataRequired()])
    price = StringField(validators=[DataRequired()])
    img = FileField(validators=[DataRequired()])

    submit = SubmitField()
