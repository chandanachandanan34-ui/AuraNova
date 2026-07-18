"""
Authentication forms.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
)


class RegisterForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("patient", "Patient"),
            ("doctor", "Doctor")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Login")