from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class AddressForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    desc = StringField(validators=[DataRequired()])
    work_time = StringField(validators=[DataRequired()])
    submit = SubmitField()

