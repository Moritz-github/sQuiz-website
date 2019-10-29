from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email-Adresse", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Eingeloggt bleiben?")
    submit = SubmitField("Registrieren")

    def validate_username(self, username):
        u = User.query.filter_by(username=username)
        if u is not None:
            return true