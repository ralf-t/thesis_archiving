from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import Optional, Length, DataRequired, ValidationError, Email
from datetime import datetime
import re, pytz
from thesisarchiving.models import User

pwRegex = r'^([A-z0-9 ._$*()#@!%/-]{,60})$'
usernameRegex = r'^([A-z0-9]{3})$|^([0-9]{11})$'

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password ', validators=[DataRequired()])
	recaptcha = RecaptchaField()
	submit = SubmitField('Login')

	def validate_username(self, username):

		if not re.fullmatch(usernameRegex, username.data):
			raise ValidationError('Username is invalid')

	def validate_password(self, password):
		if not re.fullmatch(pwRegex, password.data):
			raise ValidationError("Password is invalid")

class RequestResetForm(FlaskForm):
	email = StringField(
		'Email', 
		validators=[DataRequired(), Email(), Length(max=120)]
		)

	submit = SubmitField('Send Reset Link')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()

		if not user:
			raise ValidationError('No user is registered with the e-mail')

class BasicSearchForm(FlaskForm):
	title = StringField(
		'Title',
		validators=[Optional(), Length(max=250)]
		)
	search = SubmitField('Search')
	
class AdvancedSearchForm(FlaskForm):

	yr_start = datetime.now(tz=pytz.timezone('Asia/Manila')).year - 1
	yr_end = datetime.now(tz=pytz.timezone('Asia/Manila')).year + 10

	title = StringField(
		'Title',
		validators=[Optional(), Length(max=250)]
		)
	
	area = StringField(
		'Area',
		validators=[Optional(), Length(max=60)]
		)
	
	keywords = StringField(
		'Keywords',
		validators=[Optional(), Length(max=609)]
		)
	
	program = SelectField(
		'Program', 
		validators=[DataRequired()]
		)

	semester = SelectField(
		'Semester',
		validators=[DataRequired()]
		)


	search = SubmitField('Search')