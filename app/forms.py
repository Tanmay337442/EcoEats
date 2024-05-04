from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, DateField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea


forms = Blueprint('forms', __name__)

# DO ALL OF USER FORM
class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[
                                  DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo(
            'password_hash', message="Passwords must match!")])
    signup = SubmitField("Sign up")

class LoginForm(FlaskForm):
    username = StringField("Username or email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    signin = SubmitField("Sign in")

class UserUpdateForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    update = SubmitField("Save changes")

class UserUpdateForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    update = SubmitField("Save changes")

class FoodForm(FlaskForm):
    name = StringField("Food Name", validators=[DataRequired()])
    date = DateField("Expiry Date", validators=[DataRequired()])
    submit = SubmitField("Save")