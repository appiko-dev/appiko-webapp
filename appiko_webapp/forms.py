from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from appiko_webapp.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=17)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=4)])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):  # validate  to insure no duplicates
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is taken.")

    def validate_email(self, email):  # validate email to insure no duplicates
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("This email is taken.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign in")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=17)])
    submit = SubmitField("Update Account")

    def validate_username(self, username):
        if username.data is not current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is taken.")
