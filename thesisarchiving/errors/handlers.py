from flask import Blueprint, flash, render_template, request
from thesisarchiving import db
from thesisarchiving.models import Log
from flask_login import current_user

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(401)
def error_401(error):

	if current_user.is_anonymous:
		log = Log(description=f"Anonymous user encountered a (401)",http_error=401)
	else:
		log = Log(description=f"{current_user.roles} {current_user.username} encountered a (401)",http_error=401)
		log.user = current_user

	try:
		db.session.add(log)
		db.session.commit()
	except:
		flash("An error has occured while trying to log","danger")

	return render_template('errors/401.html'), 401

@errors.app_errorhandler(403)
def error_403(error):

	if current_user.is_anonymous:
		log = Log(description=f"Anonymous user tried accessing {request.full_path} (403)",http_error=403)
	else:
		log = Log(description=f"{current_user.roles} {current_user.username} tried accessing {request.full_path} (403)",http_error=403)
		log.user = current_user

	try:
		db.session.add(log)
		db.session.commit()
	except:
		flash("An error has occured while trying to log","danger")

	return render_template('errors/403.html'), 403

@errors.app_errorhandler(404)
def error_404(error):

	return render_template('errors/404.html'), 404

@errors.app_errorhandler(405)
def error_405(error):

	return render_template('errors/405.html'), 405

@errors.app_errorhandler(406)
def error_406(error):

	return render_template('errors/406.html'), 406

@errors.app_errorhandler(413)
def error_413(error):

	if current_user.is_anonymous:
		log = Log(description=f"Anonymous user tried uploading a large entity (413)",http_error=413)
	else:
		log = Log(description=f"{current_user.roles} {current_user.username} tried uploading a large entity (413)",http_error=413)
		log.user = current_user

	try:
		db.session.add(log)
		db.session.commit()
	except:
		flash("An error has occured while trying to log","danger")

	return render_template('errors/413.html'), 413

@errors.app_errorhandler(500)
def error_500(error):

	return render_template('errors/500.html'), 500

