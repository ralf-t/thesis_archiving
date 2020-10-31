from flask import render_template, redirect, url_for, flash, jsonify, request, abort, Blueprint
from thesisarchiving import db, bcrypt
from thesisarchiving.utils import has_roles, advanced_search, send_reset_email
from thesisarchiving.admin.forms import RegisterUserForm, RegisterThesisForm, GeneralCreateForm, UpdateSubjectForm, UpdateSectionForm, UpdateUserForm
from thesisarchiving.admin.utils import save_file, del_old_file
from thesisarchiving.models import Role, User, Subject, Section, Area, Keyword, Thesis, Semester, Program, Category #tinggal yung models idk why it worked lol
from flask_login import login_user, current_user, logout_user, login_required
import random, string, uuid
from psycopg2.extras import NumericRange

admin = Blueprint('admin', __name__)


@admin.route("/thesis_archiving/admin")
@login_required
@has_roles('Admin')
def admin_view():
	s_user = Role.query.filter_by(name='Superuser').first().permitted
	
	thesis = Thesis.query.count()
	advisers = Role.query.filter_by(name='Adviser').first().permitted.count()
	students = Role.query.filter_by(name='Student').first().permitted.count()
	admins = Role.query.filter_by(name='Admin').first().permitted.count()

	return render_template('admin/admin.html', s_user=s_user, thesis=thesis, advisers=advisers, students=students, admins=admins)

@admin.route("/thesis_archiving/admin/register/user", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def register_user():
	s_user = Role.query.filter_by(name='Superuser').first().permitted

	form = RegisterUserForm()

	form.subject.choices = [(str(r.id), r.name) for r in Subject.query.all()] if Subject.query.all() else [('None', 'None')]
	form.subject.choices.insert(0,('None', 'None'))
	form.section.choices = [(str(r.id), r.code) for r in Section.query.all()] if Section.query.all() else [('None', 'None')]
	form.section.choices.insert(0,('None', 'None'))

	if form.validate_on_submit():
		adminrole = Role.query.filter_by(name=form.admin_role.data).first()
		acadrole = Role.query.filter_by(name=form.acad_role.data).first()
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

		user = User(
			username=form.username.data,
			last_name=form.last_name.data if form.last_name.data.strip() else None,
			first_name=form.first_name.data if form.first_name.data.strip() else None,
			middle_initial=form.middle_initial.data if form.middle_initial.data.strip() else None,
			email=form.email.data,
			password=hashed_pw,
			subject_id=uuid.UUID(form.subject.data) if form.subject.data != 'None' else None,
			section_id=uuid.UUID(form.section.data) if form.section.data != 'None' else None
			)

		if adminrole:
			user.roles.append(adminrole)
		if acadrole:
			user.roles.append(acadrole)
		
		try:
			db.session.add(user)
			db.session.commit()

			user = User.query.filter_by(username=form.username.data).first()
			send_reset_email(user) #pass in user object

			flash(f'Account emailed to {form.username.data}', 'success')
		except Exception as e:
			print(e)
			flash('An unexpected error has occured', 'danger')
		return redirect(url_for('admin.register_user'))

	return render_template('admin/register_user.html', form=form, s_user=s_user)


@admin.route("/thesis_archiving/admin/register/thesis", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def register_thesis():

	form = RegisterThesisForm()

	form.program.choices = [(str(program.id), program.college) for program in Program.query.all()]
	
	form.semester.choices = [(str(sem.id), sem.code) for sem in Semester.query.order_by(Semester.code).all() ]

	form.adviser.choices = [(str(adv.id), f"{adv.last_name}, {adv.first_name}, {adv.middle_initial}") for adv in Role.query.filter_by(name="Adviser").first().permitted ]

	if form.validate_on_submit():

		custom_errors = 0

		author_entries = 0
		author_inputs = []

		title_entries = 0
		area_entries = 0
		keywords_entries = 0

		file_name_error = []

		for field in form.title_area_keywords.entries:
			if field.title.data.strip():
				title_entries += 1
				if field.area.data.strip():
					area_entries += 1
				if field.keywords.data.strip():
					keywords_entries += 1

		if not title_entries:
			for field in form.title_area_keywords.entries:
				field.title.errors.append('Provide atleast 1 title')
				custom_errors += 1

		if title_entries != area_entries:
			for field in form.title_area_keywords.entries:
				field.area.errors.append('Specify thesis area')
				custom_errors += 1

		if title_entries != keywords_entries:
			for field in form.title_area_keywords.entries:
				field.keywords.errors.append('Specify thesis keywords')
				flash('Keyword fields are empty','danger')
				custom_errors += 1

		for field in form.authors.entries:
			if field.username.data.strip():
				author_entries += 1
				author_inputs.append(field.username.data)
		
		#override option
		if form.override_authors.data:
			if author_entries < 1:
				for field in form.authors.entries:
					field.username.errors.append('Atleast 1 author is required.')
					custom_errors += 1
		else:
			if author_entries < 4:
				for field in form.authors.entries:
					field.username.errors.append('Atleast 4 authors are required.')
					custom_errors += 1

		if len(author_inputs) > len(set(author_inputs)):
			for field in form.authors.entries:
				if field.username.data:
					field.username.errors.append('Authors must be unique from one another.')
					custom_errors += 1
		
		if custom_errors:
			return render_template('admin/register_thesis.html', form=form)

		added = 0
		try:
			c_num_int = 1
			program = Program.query.get(uuid.UUID(form.program.data))
			school_year = form.school_year.data #int coerced
			semester = Semester.query.get(uuid.UUID(form.semester.data))
			
			for field in form.title_area_keywords.entries:
				
				title = field.title.data.strip()
				area = field.area.data.strip()
				keywords = field.keywords.data.strip().split(',')
				category = Category.query.filter_by(code='TP').first()
				adviser = form.adviser.data
				latest_thesis = Thesis.query.order_by(Thesis.date_register.desc()).first()

				if title and area and keywords:
					if latest_thesis:
						c_num_int = int(latest_thesis.call_number.split('-')[-1]) + 1

					thesis_c_num = '{}-{}-{}{}-{}'.format(
										school_year, 
										semester.code, 
										category.code, 
										program.code, 
										c_num_int
									)

					thesis = Thesis(
						call_number=thesis_c_num,
						title=title,
						program_id=program.id,
						category_id=category.id,
						school_year=NumericRange(school_year, school_year + 1,'[]'),
						semester_id=semester.id,
						form_file=save_file(form.form_file.data, 'form_file')
						)

					if Area.query.filter_by(name=area).first():
						thesis.area = Area.query.filter_by(name=area).first()
					else:
						thesis.area = Area(name=area)

					for keyword in keywords:
						if Keyword.query.filter_by(name=keyword).first():
							thesis.research_keywords.append(Keyword.query.filter_by(name=keyword).first())
						else:
							thesis.research_keywords.append(Keyword(name=keyword))
					
					thesis.contributors.append(User.query.get(uuid.UUID(adviser)))
					
					for author_field in form.authors.entries:
						if author_field.username.data:
							contributor = author_field.username.data
							thesis.contributors.append(User.query.filter_by(username=contributor).first())
					
					file_name_error.append(thesis.form_file)
					db.session.add(thesis)
					db.session.commit()
					added += 1

		except:
			del_old_file(file_name_error[added], 'form_file') #on call ng save_file(), nasasave agad
			db.session.rollback()
			flash(f'An error occured while registering entry-{added}','danger')
			return redirect(url_for('admin.register_thesis'))

		else:
			flash('Theses successfully registered','success')
			return redirect(url_for('admin.register_thesis'))

	return render_template('admin/register_thesis.html', form=form)

@admin.route("/thesis_archiving/admin/register/general", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def register_general():
	
	form = GeneralCreateForm()

	form.select_data.choices.extend([('Subject','Subject'),('Section','Section')])

	if form.validate_on_submit():
		flash("test good","success")
		return redirect(url_for('admin.register_general'))
		
	return render_template('admin/register_general.html', form=form)


@admin.route("/thesis_archiving/admin/theses", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def theses():

	page = request.args.get("page", 1, type=int)
	theses = Thesis.query.order_by(Thesis.call_number.asc()).paginate(page=page, per_page=10)

	return render_template('admin/theses.html', theses=theses)

@admin.route("/thesis_archiving/admin/update/thesis/<string:thesis_title>", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def update_thesis(thesis_title):

	thesis = Thesis.query.filter_by(title=thesis_title).first_or_404()

	return render_template('admin/update_thesis.html')
	
@admin.route("/thesis_archiving/admin/users", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def users():

	page = request.args.get("page", 1, type=int)
	users = User.query.order_by(User.username.asc()).paginate(page=page, per_page=10)

	return render_template('admin/users.html', users=users)


@admin.route("/thesis_archiving/admin/update/user/<string:user_username>", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def update_user(user_username):

	user = User.query.filter_by(username=user_username).first_or_404()

	s_user = Role.query.filter_by(name='Superuser').first().permitted

	form = UpdateUserForm(user)

	form.subject.choices = [(str(r.name), r.name) for r in Subject.query.all()] if Subject.query.all() else [('None', 'None')]
	form.subject.choices.insert(0,('None', 'None'))
	form.section.choices = [(str(r.code), r.code) for r in Section.query.all()] if Section.query.all() else [('None', 'None')]
	form.section.choices.insert(0,('None', 'None'))

	if form.validate_on_submit():
		roles = [i for i in user.roles] # get all user's role
		acad_role = Role.query.filter_by(name=form.acad_role.data).first()
		admin_role = Role.query.filter_by(name=form.admin_role.data).first()

		for i in roles: #remove all user's roles
			user.roles.remove(i)

		if acad_role or admin_role: #append all selected roles
			if acad_role:
				user.roles.append(acad_role)
			if admin_role:
				user.roles.append(admin_role)

		user.last_name = form.last_name.data
		user.first_name = form.first_name.data
		user.middle_initial = form.middle_initial.data
		user.email = form.email.data
		user.subject_id = Subject.query.filter_by(name=form.subject.data).first().id if form.subject.data != 'None' else None
		user.section_id = Section.query.filter_by(code=form.section.data).first().id if form.section.data != 'None' else None

		db.session.commit()
		flash('User update success','success')
		return redirect(url_for('admin.update_user',user_username=user_username))

	elif request.method == 'GET':
		form.admin_role.default = 'None'
		form.acad_role.default = 'None'

		for i in ['Superuser','Admin']:
			if Role.query.filter_by(name=i).first() in user.roles:
				form.admin_role.default = i
				break 

		for i in ['Adviser','Student']:
			if Role.query.filter_by(name=i).first() in user.roles:
				form.acad_role.default = i
				break

		form.subject.default = user.subject.name if user.subject else 'None'
		form.section.default = user.section.code if user.section else 'None'
		form.process()
		
		form.last_name.data = user.last_name
		form.first_name.data = user.first_name
		form.middle_initial.data = user.middle_initial
		form.email.data = user.email

	return render_template('admin/update_user.html', form=form, s_user=s_user, user=user)

@admin.route("/thesis_archiving/admin/delete/user/<string:user_username>", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def delete_user(user_username):

	user = User.query.filter_by(username=user_username).first_or_404()

	db.session.delete(user)
	db.session.commit()

	flash("User has been deleted from the server","success")

	return redirect(url_for('admin.users'))

@admin.route("/thesis_archiving/admin/subjects", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def subjects():

	page = request.args.get("page", 1, type=int)
	subjects = Subject.query.order_by(Subject.name.asc()).paginate(page=page, per_page=10)

	return render_template('admin/subjects.html', subjects=subjects)

@admin.route("/thesis_archiving/admin/sections", methods=['GET','POST'])
@login_required
@has_roles('Admin')
def sections():

	page = request.args.get("page", 1, type=int)
	sections = Section.query.order_by(Section.code.asc()).paginate(page=page, per_page=10)

	return render_template('admin/sections.html', sections=sections)


########################################## AJAX
@admin.route('/thesis_archiving/admin/register/user/generated_user', methods=['POST'])
def generate_username():
	role = request.form['role']
	generated_user = ''

	if role != 'Student':
		while True:
			generated_user = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
			if (User.query.filter_by(username=generated_user).first() == None):
				break	

	return jsonify(generated_user)

@admin.route("/thesis_archiving/admin/register/thesis/advanced_search", methods=['POST'])
def similar_thesis():
	data = request.get_json(force=True)
	
	title = data['title'] 
	area = data['area'] 
	keywords = data['keywords']

	query = advanced_search(title=title,area=area,keywords=keywords) if title or area or keywords else None
	#returns a dict w/ keys of 'query','count'
	
	return render_template('main/theses_query.html', query=query)

##################################################################################################################################################
# @admin.route("/thesis_archiving/admin/subjects")
# @login_required
# @has_roles('Admin')
# def subjects_read():

# 	subjects = Subject.query.all()

# 	return render_template('admin/subjects.html', subjects=subjects)

# @admin.route("/thesis_archiving/admin/subjects/create")
# @login_required
# @has_roles('Admin')
# def subjects_create():



# 	return render_template('admin/subjects.html', subjects=subjects)

# @admin.route("/thesis_archiving/admin/subjects/update/<uuid:subject_id>")
# @login_required
# @has_roles('Admin')
# def subjects_update(subject_id):

# 	subject = Subject.query.get_or_404(subject_id)
# 	code = subject.code

# 	form = SubjectUpdateForm()

# 	if form.validate_on_submit():
# 		subject.name = form.name.data
# 		subject.code = form.code.data

# 		try:
# 			db.session.commit()
# 			flash('Successfully updated {}'.format(code),'success')
# 		except:
# 			flash('An unexpected error has occured','danger')

# 	return render_template('admin/subjects_update.html', subject=subject)

# @admin.route("/thesis_archiving/admin/subjects/delete/<uuid:subject_id>")
# @login_required
# @has_roles('Admin')
# def subjects_delete(subject_id):

# 	subject = Subject.query.get_or_404(subject_id)
# 	code = subject.code

# 	try:
# 		db.session.delete(subject)
# 		db.session.commit()
# 		flash('Successfully deleted {}'.format(code),'success')
# 	except:
# 		flash('An unexpected error has occured','danger')

# 	return redirect(url_for('admin.subjects_read'))

