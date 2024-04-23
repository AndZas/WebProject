from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, FileField, MultipleFileField
from wtforms.validators import DataRequired



class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    phone = StringField('Phone number', validators=[DataRequired()])
    submit = SubmitField('Login')
