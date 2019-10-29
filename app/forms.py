from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Eingeloggt bleiben?")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email-Adresse", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Eingeloggt bleiben?")
    submit = SubmitField("Registrieren")

    def validate_username(self, username):
        u = User.query.filter(User.username.ilike("%" + username.data + "%")).first()
        if u is not None:
            raise ValidationError("Dieser Username wurde bereits verwendet.")
        if len(username.data) > User.username.type.length:
            raise ValidationError("Dieser Username ist zu lang. Max: " + str(User.email.type.length))

    def validate_email(self, email):
        e = User.query.filter_by(email=email.data).first()
        if e is not None:
            raise ValidationError("Diese Email wurde bereits verwendet.")
        if len(email.data) > User.email.type.length:
            raise ValidationError("Diese Email ist zu lang. Max: " + str(User.email.type.length))