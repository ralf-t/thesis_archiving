from thesisarchiving import create_app
import os

# modify
dev = True

if dev:
	app = create_app()
else:
	app = create_app(os.path.join('/thesisarchiving/static')) #godaddy static folder issue fix
	#static_url_path = relative path to static folder from root
	#static_folder = yung absolute path to the static
	

if __name__ == '__main__':
	app.run(debug=True if dev else False)