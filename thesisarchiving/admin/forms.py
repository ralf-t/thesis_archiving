from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask import flash
from wtforms import StringField, SelectField, SubmitField, DateField, FieldList, FormField, Form, PasswordField, TextAreaField, BooleanField
from wtforms.validators import Optional, Length, DataRequired, ValidationError, EqualTo, Email
from datetime import datetime
import re, pytz, os
from thesisarchiving.models import User, Role, Thesis 

titleRegex = r"^([A-z0-9,':_%#()@&?. -]{3,250})$"
studentnumRegex = r'^([0-9]{11})$'
adminuserRegex = r'^([A-z0-9]{3})$'
pwRegex = r'^([A-z0-9 ._$*()#@!%/-]{,60})$'

class TitleAreaKeywords(Form):

	title = TextAreaField(
		'Title',
		validators=[Optional(), Length(min=3,max=250)]
		)
	area = StringField(
		'Area',
		validators=[Optional(), Length(min=3,max=60)]
		)
	keywords = StringField(
		'Keywords',
		validators=[Optional(), Length(min=3,max=609)]
		)
	
	# errors = list(self.field.errors)
	# new err = []

	# if error:
	# 	new err append(msg)

	# errors.extend(new err)
	# self.field.errors = errors

	def validate_title(self, title):
		thesis = Thesis.query.filter_by(title=title.data).first()

		if not re.fullmatch(titleRegex, title.data):
			raise ValidationError("Allowed characters: A-z 0-9 , ' : _ % # ( ) @ & ? . -")

		if thesis:
			raise ValidationError('Title is already taken.')

	def validate_keywords(self, keywords):
		keywords_list = keywords.data.split(',')

		if len(keywords_list) < 3 or len(keywords_list) > 10:
			flash("Only 3-10 keywords are allowed","danger")
			raise ValidationError("Only 3-10 keywords are allowed")

class AuthorsField(Form):
	username = StringField(validators=[Optional(), Length(min=11, max=11)])

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()

		if not re.fullmatch(studentnumRegex, username.data):
			raise ValidationError("Please enter a valid UE Student number")
		
		if not user:
			raise ValidationError('No user is found with the student number.')

class RegisterThesisForm(FlaskForm):
	yr_start = datetime.now(tz=pytz.timezone('Asia/Manila')).year - 1
	yr_end = datetime.now(tz=pytz.timezone('Asia/Manila')).year + 10

	title_area_keywords = FieldList(FormField(TitleAreaKeywords), min_entries=2, max_entries=2)
	
	program = SelectField(
		'Program',
		validators=[DataRequired()]
		)

	school_year = SelectField(
			'School Year',
			choices=[(y, f'{y}-{y+1}') for y in range(yr_start, yr_end)],
			coerce=int,
			validators=[DataRequired()]
		)
	
	semester = SelectField(
		'Semester',
		validators=[DataRequired()]
		)

	form_file = FileField(
		'Proposal form (.pdf, .doc, docx)', 
		validators=[DataRequired(), FileAllowed(['pdf', 'doc','docx'])]
		)

	adviser = StringField(
		'Adviser',
		validators=[DataRequired(), Length(min=3,max=3)]
		)
	
	authors = FieldList(FormField(AuthorsField), min_entries=5, max_entries=5)

	override_authors = BooleanField('Ignore required number of authors', validators=[Optional()])
	submit = SubmitField('Create Thesis')

	def validate_form_file(self, form_file):

		formfile = form_file.data
		formfile.seek(0, os.SEEK_END) #set cursor right at the end
		size = formfile.tell() / 1024 / 1024 #bytes -> mb

		formfile.seek(0) #set cursor again to beginning to read all the file

		if size > 15:
			raise ValidationError('File too large (max 15mb)')

	def validate_adviser(self, adviser):
		adv = User.query.filter_by(username=adviser.data).first()
		if adv not in Role.query.filter_by(name='Adviser').first().permitted:
			raise ValidationError('Adviser not found')

class RegisterUserForm(FlaskForm):
	# if superuser can add admins
	admin_role = SelectField(
		'Administrative', 
		choices=[('None', 'None'),('Superuser','Superuser'),('Admin','Admin')], 
		validators=[Optional()]
		)
	acad_role = SelectField(
		'Academic', 
		choices=[('None', 'None'),('Adviser','Adviser'),('Student','Student')], 
		validators=[DataRequired()]
		)
	
	username = StringField(
		'Username', 
		validators=[DataRequired(), Length(min=3, max=11)]
		)

	email = StringField(
		'Email', 
		validators=[DataRequired(), Email(), Length(max=120)]
		)


	password = PasswordField(
		'Password', 
		validators=[DataRequired(), Length(min=6, max=60)]
		)
	confirm_password = PasswordField(
		'Confirm Password', 
		validators=[DataRequired(), EqualTo('password')]
		)
	
	subject = SelectField(
		'Subject',
		validators=[DataRequired()]
		)

	section = SelectField(
		'Section',
		validators=[DataRequired()]
		)

	submit = SubmitField('Create User')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()

		if self.acad_role.data == 'Student':
			if not re.fullmatch(studentnumRegex, username.data):
				raise ValidationError("Please enter a valid UE Student number")
		elif self.admin_role.data != 'None' or self.acad_role.data == 'Adviser':
			if not re.fullmatch(adminuserRegex, username.data):
				raise ValidationError("Please enter 3 alphanumeric characters")
		else:
			raise ValidationError("Please select a User Permission")
		
		if user:
			raise ValidationError('Username is taken')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is taken')

	def validate_password(self, password):
		if not re.fullmatch(pwRegex, password.data):
			raise ValidationError("Allowed characters: A-z 0-9 . _ $ * ( ) # @ ! % / -")