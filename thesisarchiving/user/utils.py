from flask import current_app, flash
import random, secrets, os
from PIL import Image

def save_image(form_picture):
	
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename) # underscore is throwaway var
	image_fn = random_hex + f_ext
	image_path = os.path.join(current_app.root_path, 'static/images/profile pictures', image_fn)
	
	image_reso = (120,120)
	i = Image.open(form_picture)
	i.thumbnail(image_reso)
	i.save(image_path)

	i.close()


	return image_fn

def del_old_image(imagename):
	if imagename != 'all.jpg':
		image_path = os.path.join(current_app.root_path, 'static/images/profile pictures', imagename)

		try:
			os.remove(image_path)
		except:
			flash('Old picture not found, updating to new profile picture', 'success')