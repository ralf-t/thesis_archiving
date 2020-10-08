from flask import current_app
import random, secrets, os
from thesisarchiving.models import Thesis

def save_file(form_file, file):
	
	form_fn = ""
	form_path = ""
	_, f_ext = os.path.splitext(form_file.filename) # underscore is throwaway var

	while True:	
		random_hex = secrets.token_hex(8)
		form_fn = random_hex + f_ext
		if not Thesis.query.filter_by(form_file=form_fn).first():
			break

	if file == 'form_file':
		form_path = os.path.join(current_app.root_path, 'static','thesis attachments','form file', form_fn)
	if file == 'thesis_file':
		form_path = os.path.join(current_app.root_path, 'static','thesis attachments','thesis file', form_fn)

	form_file.save(form_path)
	# form_file.close()
	
	return form_fn

def del_old_file(filename, file):
	
	file_path = ""

	if file == 'form_file':
		file_path = os.path.join(current_app.root_path, 'static','thesis attachments','form file', filename)
	if file == 'thesis_file':
		file_path = os.path.join(current_app.root_path, 'static','thesis attachments','thesis file', filename)
	
	os.remove(file_path)