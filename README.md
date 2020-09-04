# After cloning/pulling, if `config.py` is not present inside `thesisarchiving/` folder, create one
# then paste the following code.


	class Config:
		SECRET_KEY = '25ef62aae54673ff3549674e6dcb1a0a' # security for cookies csrf etc, env var
		SQLALCHEMY_DATABASE_URI = 'postgresql://POSTGRESUSERNAME:POSTGRESPASSWORD@localhost/thesis_archiving_db' #env var
		SQLALCHEMY_TRACK_MODIFICATIONS = False
		MAX_CONTENT_LENGTH = 25 * 1024 * 1024

		# dev configs, change on production
		# uses aremtabo
		RECAPTCHA_PUBLIC_KEY = '6Ldg27oZAAAAAAKw1nQ66BFuhuoj2y9IOmsFmNtq'
		RECAPTCHA_PRIVATE_KEY = '6Ldg27oZAAAAAD1nQmaSfcQbfR-8lu6DQ4xW2mVQ'

