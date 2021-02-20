from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import pytz
from thesisarchiving import db, login_manager
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import YEAR, BIGINT, LONGTEXT, SMALLINT

# CASACADE LAHAT NG MGA RELATIONSHIP


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

#okay lang mag delete ng sa many to many, di naapektuha yung child like okay lang idelete yung Roles, magiging empty lagn yung role ng User table
class Subject(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	name = db.Column(db.String(120), unique=True, nullable=False)
	code = db.Column(db.String(10), unique=True, nullable=False)
	users = db.relationship('User', backref='subject', lazy=True) #ang backref maaccess yung entire object (in this case, ang program_obj naacess yung 
																													#buong Program class niya)
	def __repr__(self):
		return f"{self.name}"

class Section(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	code = db.Column(db.String(10), unique=True, nullable=False)
	users = db.relationship('User', backref='section', lazy=True) 

	def __repr__(self):
		return f"{self.code}"

class Role(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)

	def __repr__(self):
		return f"{self.name}"

class User(db.Model, UserMixin):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	username = db.Column(db.String(11), unique=True, nullable=False) #studnum 11, adviser 3an, admin3an, 
	last_name = db.Column(db.String(60), nullable=False)
	first_name = db.Column(db.String(60), nullable=False)
	middle_initial = db.Column(db.String(5), nullable=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	roles = db.relationship('Role', secondary='user_role', backref=db.backref('permitted', lazy='dynamic'))
	thesis = db.relationship('Thesis', secondary='thesis_contributors', backref=db.backref('contributors', lazy=True))
	subject_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('subject.id'), nullable=True)#test cascade
	section_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('section.id'), nullable=True)#ondelete='CASCADE'
	image_file =  db.Column(db.String(20), nullable=False, default='all.jpg') 
	date_register = db.Column(db.DateTime, nullable=False, default=lambda:datetime.now(tz=pytz.timezone('Asia/Manila')))
	logs = db.relationship('Log', backref='user', lazy='dynamic')

	def get_reset_token(self, expires_sec=86400): #1 week expiration
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'username': self.username}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		
		try:
			user_username = s.loads(token)['username']
		except:
			return None

		return User.query.filter_by(username=user_username).first()

	def __repr__(self):
		return f"{self.username} - {self.roles}"

user_role = db.Table('user_role',
	db.Column('user_id', BIGINT(unsigned=True), db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('role_id', BIGINT(unsigned=True), db.ForeignKey('role.id', ondelete='CASCADE'))
	)

#######################################################################################################################################################
class Program(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	college = db.Column(db.String(30), unique=True, nullable=False)
	code = db.Column(db.String(5), unique=True, nullable=False)
	theses = db.relationship('Thesis', backref='program', lazy='dynamic') 

	def __repr__(self):
		return f"{self.id}"

class Category(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	code = db.Column(db.String(5), unique=True, nullable=False)
	theses = db.relationship('Thesis', backref='category', lazy='dynamic')

	def __repr__(self):
		return f"{self.name}"

class Semester(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	code = db.Column(BIGINT(unsigned=True), unique=True, nullable=False)
	theses = db.relationship('Thesis', backref='semester', lazy='dynamic')

	def __repr__(self):
		return f"{self.code}"

class Area(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	name = db.Column(db.String(60), unique=True, nullable=False)
	theses = db.relationship('Thesis', backref='area', lazy='dynamic')

	def __repr__(self):
		return f"{self.name}"

class Keyword(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	name = db.Column(db.String(60), unique=True, nullable=False)

	def __repr__(self):
		return f"{self.name}"

class Thesis(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	call_number = db.Column(db.String(20), unique=True, nullable=False)
	title = db.Column(db.String(250), unique=True, nullable=False)
	overview = db.Column(LONGTEXT,nullable=True)
	program_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('program.id'), nullable=False)
	category_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('category.id'), nullable=False)
	#useful --> count,append/remove, filterby chaining
	sy_start = db.Column(YEAR, nullable=False)
	sy_end = db.Column(YEAR, nullable=False)
	semester_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('semester.id'), nullable=False)
	research_area_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('area.id'), nullable=False)
	research_keywords = db.relationship('Keyword', secondary='thesis_keywords', backref=db.backref('theses', lazy='dynamic'))
	form_file = db.Column(db.String(30), unique=True, nullable=True) 
	thesis_file = db.Column(db.String(30), unique=True, nullable=True) 
	date_deploy = db.Column(db.DateTime, nullable=True)
	date_register = db.Column(db.DateTime, nullable=False, default=lambda:datetime.now(tz=pytz.timezone('Asia/Manila')))

	def __repr__(self):
		return f"([{self.id}], {self.category_id}, {self.call_number}, {self.title})"

thesis_contributors = db.Table('thesis_contributors',
	db.Column('user_id', BIGINT(unsigned=True), db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('thesis_id', BIGINT(unsigned=True), db.ForeignKey('thesis.id', ondelete='CASCADE'))
	)

thesis_keywords = db.Table('thesis_keywords',
	db.Column('thesis_id', BIGINT(unsigned=True), db.ForeignKey('thesis.id', ondelete='CASCADE')),
	db.Column('keyword_id', BIGINT(unsigned=True), db.ForeignKey('keyword.id', ondelete='CASCADE'))
	)


###############

class Log(db.Model):
	id = db.Column(BIGINT(unsigned=True), primary_key=True)
	user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), nullable=True)
	description = db.Column(db.String(250), nullable=False)
	http_error = db.Column(SMALLINT, nullable=True)
	date_time = db.Column(db.DateTime, nullable=False, default=lambda:datetime.now(tz=pytz.timezone('Asia/Manila')))

	def __repr__(self):
		return f"({self.id},{self.date_time})"

