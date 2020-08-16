from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, DataRequired, ValidationError, EqualTo, Email
from thesisarchiving import bcrypt
from thesisarchiving.models import User
import os

class UpdateAccountForm(FlaskForm):

	image_file = FileField(
		'Profile picture', 
		validators=[FileAllowed(['jpg', 'png'])]
		)

	email = StringField(
		'Email', 
		validators=[DataRequired(), Email(), Length(max=120)]
		)


	submit = SubmitField('Update account')

	def validate_image_file(self, image_file):
		image = image_file.data
		image.seek(0, os.SEEK_END)
		size = image.tell() / 1024 / 1024 #bytes -> mb
		
		if size > 5:
			raise ValidationError('Image too large (max 5mb)')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one.')


class UpdatePasswordForm(FlaskForm):

	password = PasswordField(
		'Password', 
		validators=[DataRequired(), Length(min=6, max=60)]
		)

	new_password = PasswordField(
		'New password', 
		validators=[DataRequired(), Length(min=6, max=60)]
		)

	confirm_new_password = PasswordField(
		'Confirm Password', 
		validators=[DataRequired(), EqualTo('new_password')]
		)

	submit = SubmitField('Update password')

	def validate_password(self, password):
		if not bcrypt.check_password_hash(current_user.password, password.data):
			raise ValidationError('Password is incorrect')

	def validate_new_password(self, password):
		if bcrypt.check_password_hash(current_user.password, password.data):
			raise ValidationError('Please enter a different password')