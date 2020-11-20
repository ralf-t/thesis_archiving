from flask import Blueprint, flash, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(401)
def error_401(error):
    return render_template('errors/401.html'), 401

@errors.app_errorhandler(403)
def error_403(error):
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
    return render_template('errors/413.html'), 413

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

