from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message="Please enter your name")], render_kw={'autofocus': True})
    email = StringField('Email', validators=[InputRequired(message="Please enter your email"), Email(message="Please enter a valid email")])
    msg = TextAreaField('Message', validators=[InputRequired(message='Please enter a message')])
    recaptcha = RecaptchaField()
    send = SubmitField("Send")
