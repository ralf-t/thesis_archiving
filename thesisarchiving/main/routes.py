from flask import render_template, redirect, url_for, request, Blueprint, flash
from thesisarchiving import bcrypt
from thesisarchiving.utils import advanced_search, fuzz_tags
from thesisarchiving.main.forms import LoginForm, BasicSearchForm, AdvancedSearchForm, ResetRequestForm, ResetPasswordForm
from thesisarchiving.models import Role, User, Program, Thesis, Semester
from flask_login import login_user, current_user, logout_user, login_required
from urllib import parse
import random, uuid

main = Blueprint('main', __name__)

@main.route("/thesis_archiving/login", methods=['GET','POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form = LoginForm()

	if form.validate_on_submit():
		msg = 'User is either not registered or has invalid details'
		user = User.query.filter_by(username=form.username.data).first()
		
		if user and bcrypt.check_password_hash(user.password, form.password.data): #converts hash to string to compare to input string
			login_user(user)
			next_page = request.args.get('next') # returns url/route if exists else none
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			form.username.errors.append(msg)

	return render_template('main/login.html', form=form)

@main.route("/thesis_archiving/logout")
@login_required
def logout():

	logout_user()
	return redirect(url_for('main.login'))

@main.route("/thesis_archiving/", methods=['GET','POST'])
@main.route("/thesis_archiving/home", methods=['GET','POST'])
@main.route("/thesis_archiving/home/<string:college_name>", methods=['GET','POST'])
@login_required
def home(college_name=None):
	'''
	everytime 'home' is opened, query string will always be grabbed

	if accessing from advanced_searching route, 'All' will be placed in the url for placeholder

	when clicking college filters, it preserves the query string and overwrites program arg if present
	
	query strings will only come from advanced_searching,college filters, and title search 
	'''
	query_str = parse.urlencode(request.args)

	college = Program.query.filter_by(college=college_name).first() #gets from navbar filter
	prog_id = str(college) if college else None #turns __repr__ to string

	#set only value if argument is present and not str'None'
	title = request.args.get('title') if request.args.get('title') and request.args.get('title') != 'None' else None
	area = request.args.get('area') if request.args.get('area') and request.args.get('area') != 'None' else None
	keywords = request.args.get('keywords').split(',') if request.args.get('keywords') and request.args.get('keywords') != 'None' else None
	program = request.args.get('program') if request.args.get('program') and request.args.get('program') != 'None' else None
	semester = request.args.get('semester') if request.args.get('semester') and request.args.get('semester') != 'None' else None
	
	basic_search = BasicSearchForm()
	
	if basic_search.validate_on_submit():
		title = basic_search.title.data
		return redirect(url_for('main.home', college_name=college_name, title=title))

	query = advanced_search(title=title, area=area, keywords=keywords, program=prog_id if prog_id else program, semester=semester)

	return render_template('main/home.html', basic_search=basic_search, query=query, query_str=query_str, programs=Program.query.all())

@main.route("/thesis_archiving/advanced_search", methods=['GET','POST'])
@login_required
def advanced_searching():
	
	form = AdvancedSearchForm()

	form.program.choices = [(str(program.id), program.college) for program in Program.query.all()]
	form.program.choices.insert(0, ('None', 'None'))
	
	form.semester.choices = choices=[(str(sem.id), sem.code) for sem in Semester.query.order_by(Semester.code).all() ]
	form.semester.choices.insert(0, ('None', 'None'))

	query_dict = {
		'title':None, 
		'area':None, 
		'keywords':None, 
		'program':None,
		'semester':None
		}

	if form.validate_on_submit():
		query_dict['title'] = form.title.data.strip() if form.title.data.strip() else None
		query_dict['area'] = form.area.data.strip() if form.area.data.strip() else None
		query_dict['keywords'] = form.keywords.data.strip() if form.keywords.data.strip() else None
		query_dict['program'] = form.program.data if form.program.data != 'None' else None
		query_dict['semester'] = form.semester.data if form.semester.data != 'None' else None
		
		
		query_str = parse.urlencode(query_dict)

		return redirect(url_for('main.home', college_name='All') + '?' + query_str)

	return render_template('main/advanced_searching.html', form=form)

@main.route("/thesis_archiving/thesis/<string:thesis_title>", methods=['GET','POST'])
@login_required
def thesis_profile(thesis_title):

	thesis = Thesis.query.filter_by(title=thesis_title).first_or_404()
	adviser = Role.query.filter_by(name='Adviser').first().permitted
	student = Role.query.filter_by(name='Student').first().permitted

	contributor = current_user in thesis.contributors

		# return redirect(url_for('home'))

	return render_template('main/thesis_profile.html', thesis=thesis, adviser=adviser, student=student, contributor=contributor)

@main.route("/thesis_archiving/reset_password/<token>", methods=['GET','POST'])
def reset_password(token):
	
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	
	user = User.verify_reset_token(token)

	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('main.reset_request'))
		
	form = ResetPasswordForm()
	
	if form.validate_on_submit():
		pass

	return render_template('main/reset_password.html', title='Reset Password', form=form)

@main.route("/thesis_archiving/reset_request", methods=['GET','POST'])
def reset_request():
	
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	
	form = ResetRequestForm()
	
	if form.validate_on_submit():
		flash('Email sent. Please check your inbox or spam folder.', 'success')
		return redirect(url_for('main.reset_request'))

	return render_template('main/reset_request.html', title='Reset Request', form=form)
###################AJAX

@main.route("/thesis_archiving/admin/register/thesis/fuzz_tags", methods=['POST'])
def tags():
	tags = fuzz_tags(request.form['val'], request.form['name'])	

	return render_template('main/tags.html', tags=tags, name=request.form['name'])
