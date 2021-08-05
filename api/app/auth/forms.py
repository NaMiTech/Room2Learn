from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    repeatPassword = PasswordField('Repeat password', validators=[DataRequired()])
    privacy = BooleanField('I Accept The Privacy Policy',validators=[DataRequired()])
    commercial = BooleanField('Receive Commercial Information')
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Create account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
	phone = StringField('Phone', validators=[DataRequired(), Length(max=64)])
	EIN = StringField('EIN', validators=[DataRequired(), Length(max=64)])
	address = StringField('Address', validators=[DataRequired(), Length(max=64)])
	address2 = StringField('Address2', validators=[DataRequired(), Length(max=64)])
	country = StringField('Country', validators=[DataRequired(), Length(max=64)])
	city = StringField('City', validators=[DataRequired(), Length(max=64)])
	state = StringField('State', validators=[DataRequired(), Length(max=64)])
	zipcode = StringField('Zipcode', validators=[DataRequired(), Length(max=64)])
	contact_name = StringField('Contact name', validators=[DataRequired(), Length(max=64)])
	contact_phone = StringField('Contact phone', validators=[Length(max=64)])
	contact_phone2 = StringField('Contact phone2', validators=[Length(max=64)])
	contact_email = StringField('Contact email', validators=[Email()])
	submit = SubmitField('Send')

class PasswordForm(FlaskForm):
	oldPassword = PasswordField('Old Password', validators=[DataRequired()])
	password = PasswordField('New Password', validators=[DataRequired()])
	submit = SubmitField('Send')