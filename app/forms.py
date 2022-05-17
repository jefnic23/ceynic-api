from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, IntegerField, SelectField, MultipleFileField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message="Please enter your name")], render_kw={'autofocus': True})
    email = StringField('Email', validators=[InputRequired(message="Please enter your email"), Email(message="Please enter a valid email")])
    msg = TextAreaField('Message', validators=[InputRequired(message='Please enter a message')])
    recaptcha = RecaptchaField()
    send = SubmitField("Send")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message="Please enter your email"), Email(message="Please enter a valid email")], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[InputRequired(message="Password required")])
    remember_me = BooleanField('Remember me')
    submit_button = SubmitField('Login')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Enter your email", validators=[InputRequired(message="Please enter your email"), Email(message="Please enter a valid email")], render_kw={'autofocus': True})
    submit_button = SubmitField("Request Password Reset")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New password',
        validators=[InputRequired(message="Password required"), 
        Length(min=8, message="Password must be at least 8 characters")], 
        render_kw={'autofocus': True})
    confirm_pswd = PasswordField('Confirm new password',
        validators=[InputRequired(message="Password required"), 
        EqualTo("password", message="Passwords must match")])
    submit_button = SubmitField("Submit new password")

class ProductForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(message="Enter a title")], render_kw={'autofocus': True})
    price = IntegerField('Price', validators=[InputRequired(message="Enter the price")])
    medium = SelectField('Medium', choices=[('painting', 'PAINTING'), ('print', 'PRINT')])
    height = IntegerField('Height', validators=[InputRequired(message="Enter painting height")])
    width = IntegerField('Height', validators=[InputRequired(message="Enter painting width")])
    description = TextAreaField('Description', validators=[InputRequired(message="Enter painting description")])
    images = MultipleFileField('Upload image(s)', validators=[InputRequired(message="Upload at least one image")])
