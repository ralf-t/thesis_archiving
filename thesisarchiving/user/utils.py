from flask import current_app, flash
import random, secrets, os
from PIL import Image
from thesisarchiving.models import User

def save_image(form_picture):
	
	image_fn = ""
	_, f_ext = os.path.splitext(form_picture.filename) # underscore is throwaway var
	
	while True:	
		random_hex = secrets.token_hex(8)
		image_fn = random_hex + f_ext
		if not User.query.filter_by(image_file=image_fn).first():
			break
	
	image_path = os.path.join(current_app.root_path, 'static','images','profile pictures', image_fn)
	
	image_reso = (120,120)
	i = Image.open(form_picture)
	i.thumbnail(image_reso)
	i.save(image_path)

	i.close()

	return image_fn

def del_old_image(imagename):
	if imagename != 'all.jpg':
		image_path = os.path.join(current_app.root_path, 'static','images','profile pictures', imagename) 
		
		try:
			os.remove(image_path)
		except:
			flash('Old picture not found, updating to new profile picture', 'success')