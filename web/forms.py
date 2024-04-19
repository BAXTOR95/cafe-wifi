from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, URL


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    location_input = StringField('Address', validators=[DataRequired()])
    address2_input = StringField('Apt, Suite, etc (optional)')
    locality_input = StringField('City', validators=[DataRequired()])
    administrative_area_level_1_input = StringField('State/Province', validators=[DataRequired()])
    postal_code_input = StringField('Zip/Postal code', validators=[DataRequired()])
    country_input = StringField('Country', validators=[DataRequired()])
    has_sockets = BooleanField('Has Sockets')
    has_toilet = BooleanField('Has Toilet')
    has_wifi = BooleanField('Has Wifi')
    can_take_calls = BooleanField('Can Take Calls')
    seats = StringField('Number of Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Add Cafe')
