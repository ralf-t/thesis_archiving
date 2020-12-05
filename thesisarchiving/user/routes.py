from flask import render_template, redirect, url_for, flash, abort, request, Blueprint
from thesisarchiving import db, bcrypt
from thesisarchiving.user.forms import UpdateAccountForm, UpdatePasswordForm
from thesisarchiving.user.utils import save_image, del_old_image
from thesisarchiving.models import User, Thesis
from flask_login import current_user, login_required
import random, os

user = Blueprint('user', __name__)

@user.route("/user/<string:username>", methods=['GET','POST'])
@login_required
def user_profile(username):

	user = User.query.filter_by(username=username).first_or_404()

	if user != current_user:
		abort(403)
	# if current user is user
	user_thesis = [i.id for i in user.thesis]
	query = Thesis.query.filter(Thesis.id.in_(user_thesis)).order_by(Thesis.date_register.desc()).all()

	return render_template('user/user_profile.html', query=query)

@user.route("/user/account", methods=['GET','POST'])
@login_required
def user_account():

	
	form = UpdateAccountForm()

	if form.validate_on_submit():

		if form.image_file.data:
			old_image = current_user.image_file

			current_user.image_file = save_image(form.image_file.data)
			
			del_old_image(old_image)

		current_user.email = form.email.data
		
		try:
			db.session.commit()
			flash('Account details updated', 'success')
			return redirect(url_for('user.user_account'))
		except:
			flash('An unexpected error occured','danger')

	elif request.method == 'GET':
		form.email.data = current_user.email

	return render_template('user/user_account.html', form=form)

@user.route("/user/password", methods=['GET','POST'])
@login_required
def user_password():

	form = UpdatePasswordForm()

	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

		current_user.password = hashed_pw
		try:
			db.session.commit()
			flash('Password is changed successfully', 'success')
			return redirect(url_for('user.user_password'))
		except:
			flash('An unexpected error occured','danger')

	return render_template('user/user_password.html', form=form)