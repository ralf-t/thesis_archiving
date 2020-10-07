from flask import current_app
import random, secrets, os
from thesisarchiving.models import Thesis

def save_file(form_file, file):
	
	form_fn = ""
	path = ""
	_, f_ext = os.path.splitext(form_file.filename) # underscore is throwaway var

	if file == 'form_file':
		path = 'static/thesis attachments/form file'

	if file == 'thesis_file':
		path = 'static/thesis attachments/thesis file'

	while True:
		random_hex = secrets.token_hex(8)
		form_fn = random_hex + f_ext
		if not Thesis.query.filter_by(form_file=form_fn).first():
			break

	form_path = os.path.join(current_app.root_path, path, form_fn)
	
	form_file.save(form_path)
	# form_file.close()
	
	return form_fn

def del_old_file(filename, file):
	
	path = ""

	if file == 'form_file':
		path = 'static/thesis attachments/form file'

	if file == 'thesis_file':
		path = 'static/thesis attachments/thesis file'

	file_path = os.path.join(current_app.root_path, path, filename)
	# may produce future errors on using /../..
		# possible alternative os.path.join(current_app.root_path, 'path','to','folder', filename) 
	os.remove(file_path)