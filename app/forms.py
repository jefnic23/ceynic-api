from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, IntegerField, SelectField, MultipleFileField
from wtforms.validators import InputRequired


class ProductForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(message="Enter a title")], render_kw={'autofocus': True})
    price = IntegerField('Price', validators=[InputRequired(message="Enter the price")])
    medium = SelectField('Medium', choices=[('painting', 'PAINTING'), ('print', 'PRINT')])
    height = IntegerField('Height', validators=[InputRequired(message="Enter painting height")])
    width = IntegerField('Height', validators=[InputRequired(message="Enter painting width")])
    description = TextAreaField('Description', validators=[InputRequired(message="Enter painting description")])
    slideshow = BooleanField('Slideshow')
    images = MultipleFileField('Upload image(s)', validators=[InputRequired(message="Upload at least one image")])
