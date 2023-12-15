.PHONY: backend-install
backend-install:
	cd backend && pipenv install

.PHONY: backend-run
backend-run: backend-install
	cd backend && pipenv run python3 manage.py runserver

.PHONY: backend-createsuperuser
backend-createsuperuser: backend-install
	cd backend && pipenv run python3 manage.py createsuperuser

.PHONY: backend-migrate
backend-migrate: backend-install
	cd backend && pipenv run python3 manage.py migrate

.PHONY: backend-makemigrations
backend-makemigrations: backend-install
	cd backend && pipenv run python3 manage.py makemigrations

.PHONY: backend-tests
backend-tests: backend-install
	cd backend && pipenv run python3 manage.py test

.PHONY: lambda-install
lambda-install:
	cd lambda && pipenv install

.PHONY: lambda-run
lambda-run:
	cd lambda && pipenv run flask --app views run


.PHONY: lambda-tests
lambda-tests: backend-install
	cd lambda && pipenv run python3 -m pytest tests.py
