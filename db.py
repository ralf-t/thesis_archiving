from thesisarchiving import create_app
app = create_app()

with app.app_context():
	from flask_sqlalchemy import SQLAlchemy
	from thesisarchiving import db, bcrypt
	from thesisarchiving.models import Role, User, Subject, Section, Area, Keyword, Thesis, Semester, Program, Category #tinggal yung models idk why it worked lol

	# roles`/
	# user`/
	# Semester`/
	# program`/
	# categ`/
	# Subject
	# Section
	# Area
	# Keyword
	# thesis


	#################################################################

	# roles = ['Superuser','Admin','Adviser','Student']

	# for role in roles:
	# 	t = Role(name=role)
	# 	db.session.add(t)

	# db.session.commit()


	# user = User(
	# 		username='rnd',
	# 		last_name='RND',
	# 		first_name='RND',
	# 		email='aremtabo86@gmail.com',
	# 		password=bcrypt.generate_password_hash('masterkey').decode('utf-8'),
	# 		)

	# user.roles.append(Role.query.filter_by(name='Superuser').first())


	# db.session.add(user)
	# db.session.commit()

	# progs = ['BSCS' ,'BSEMC-GD', 'BSEMC-DA', 'BSIS' ,'BSIT']
	# codes = ['CS','GD','DA','IS','IT']

	# for i in range(5):
	# 	p = Program(college=progs[i],code=codes[i])
	# 	db.session.add(p)

	# categs = ['Title Proposal' ,"Approved Title", 'Suggested']
	# codes = ['TP','AP','SG']


	# for i in range(3):
	# 	c = Category(name=categs[i],code=codes[i])
	# 	db.session.add(c)

	# db.session.add(Semester(code=1))
	# db.session.add(Semester(code=2))
	
	# db.session.commit()