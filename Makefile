.PHONY: run
run:
	ENV_FILE_LOCATION=./.env.py python entry.py

.PHONY: resetdb
resetdb:
	ENV_FILE_LOCATION=./.env.py python resetdb.py