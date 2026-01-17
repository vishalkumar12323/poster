from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# defining RegisterForm using wtforms
class RegisterFrom(FlaskForm):
    name = StringField(label="Name", validators=[Length(min=3, max=20)])

    email = EmailField(
        label="Email", 
        validators=[DataRequired(message="Email is required"), 
        Email(message="Invalid email"), 
        Length(max=50)]
    )

    password = PasswordField(label="Password", 
        validators=[DataRequired(message="Password is required"), 
        Length(min=8, max=50, message="Password must be between 8 and 50 characters")]
    )

    confirm_password = PasswordField(
        label="Confirm Password", 
        validators=[DataRequired(message="Confirm password is required"), 
        Length(min=8, max=50, message="Password must be between 8 and 50 characters"), 
        EqualTo('password', message="Passwords must match")]
    )

    submit = SubmitField("Register")

# defining LoginForm using wtforms
class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(message="Email is required"), Email(message="Invalid email"), Length(max=50)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required"), Length(min=8, max=50, message="Password must be between 8 and 50 characters")]
    )
    submit = SubmitField("Login")
