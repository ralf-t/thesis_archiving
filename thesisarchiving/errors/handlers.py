from flask import Blueprint, flash

errors = Blueprint('errors', __name__)
# 401unathorized 404not found 403forbidden 413largeenttity 500generalerror error 405
#errorhandler(works only in current blueprint) vs app_errohandler(works for entire app)
@errors.app_errorhandler(413)
def error_413(error):
	return flash('Minimum upload size is 25 mb (413)','danger'), 413