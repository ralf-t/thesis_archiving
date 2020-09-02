class Config:
	SECRET_KEY = '25ef62aae54673ff3549674e6dcb1a0a' # security for cookies csrf etc, env var
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:sa@localhost/thesis_archiving_db' #env var
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAX_CONTENT_LENGTH = 25 * 1024 * 1024

	# dev configs, change on production
	# uses aremtabo
	RECAPTCHA_PUBLIC_KEY = '6LdiMcMZAAAAAJfV4DKEehMXnc9nhm0JdZWqpemF'
	RECAPTCHA_PRIVATE_KEY = '6LdiMcMZAAAAAGe80ZqJyr-bPeF-9iPfiWOUJ1WW'
