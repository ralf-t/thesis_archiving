from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from thesisarchiving.config import Config 

'''
	create extensions object first but without an app

	and only upon create_app will the application be binded on the extension objects

	also, any queries made before app initiliazation, will raise an error 
	because there is no db in context before that

	so make your queries inside functions para maexecute only upon call.
	And by that time, sure na initialized na ang app

'''

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'light'

def create_app(config_class=Config):
	#init is initialize app
	app = Flask(__name__)
	app.config.from_object(Config)
	
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	from thesisarchiving.main.routes import main
	from thesisarchiving.user.routes import user
	from thesisarchiving.admin.routes import admin
	from thesisarchiving.errors.handlers import errors

	app.register_blueprint(main)
	app.register_blueprint(user)
	app.register_blueprint(admin)
	app.register_blueprint(errors)

	return app 