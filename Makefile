#@-- help command to show usage of make commands --@#
help:
	@echo "----------------------------------------------------------------------------"
	@echo "-                     Available commands                                   -"
	@echo "----------------------------------------------------------------------------"
	@echo "---> make env              - To create virtual environment"
	@echo "---> make activate         - To activate virtual environment"
	@echo "---> make install          - To install dependencies from Pipfile.lock"
	@echo "---> make update           - To update the Pipfile.lock"
	@echo "---> make makemigrations   - To create a migration file for the changes in the models"
	@echo "---> make migrate          - To update the database with the latest migration"
	@echo "---> make lint             - To run the flake8 linter"
	@echo "---> make run              - To start the server"
	@echo " "
	@echo "----------------------->>>>>>>>>>>>><<<<<<<<<<<<<<--------------------------"
	@echo "-                     Available Docker commands                            -"
	@echo "----------------------------------------------------------------------------"
	@echo "---> make build         - To build the docker image"
	@echo "---> make start-api     - To build the docker image and start the API"
	@echo "---> make start         - To start the containers in the background"
	@echo "---> make start-verbose - To start the containers verbosely"
	@echo "---> make stop          - To stop the api containers"
	@echo "---> make clean         - To delete the application image"
	@echo "---> make help          - To show usage commands"
	@echo "----------------------------------------------------------------------------"



env:
	@ echo '<<<<<<<<<<Creating virtual environment>>>>>>>>>'
	pipenv shell --python 3.7
	@ echo ''

activate:
	@ echo '<<<<<<<<<<Activating virtual environment>>>>>>>>>'
	pipenv shell
	@ echo ''

install:
	@ echo '<<<<<<<<<<installing requirements>>>>>>>>>'
	pipenv install --dev
	@ echo ''


update:
	@ echo '<<<<<<<<<<updating Pipfile.lock>>>>>>>>>'
	pipenv update
	@ echo ''


makemigrations:
	@ echo '<<<<<<<<<<creating migrations>>>>>>>>>'
	python manage.py makemigrations
	@ echo ''

migrate:
	@ echo '<<<<<<<<<<creating migrations>>>>>>>>>'
	python manage.py migrate
	@ echo ''

test:
	@ echo '<<<<<<<<<<Run tests>>>>>>>>>'
	coverage run --source=app manage.py test --verbosity=2  && coverage report -m
	@ echo ''

run:
	@ echo '<<<<<<<<<<starting server>>>>>>>>>'
	python manage.py runserver
	@ echo ''

celery-worker:
	@ echo '<<<<<<<<<<starting celery worker>>>>>>>>>'
	celery -A app worker -l info --pool=gevent --concurrency=1000
	@ echo ''

celery-beat:
	@ echo '<<<<<<<<<<starting celery beat>>>>>>>>>'
	celery -A app beat
	@ echo ''

lint:
	@ echo '<<<<<<<<<<linting>>>>>>>>>'
	flake8 .
	@ echo ''


#@-- command to build the application--@#
build:
	@echo "<<<<<<<<<<Building application image>>>>>>>>>>>>>>"
	docker-compose build

#@-- command to start the container in the background --@#
start:
	@echo "<<<<<<<<<<Start up the api in the background after building>>>>>>>>>>>>>>"
	@echo ""
	docker-compose up -d

#@-- command to start the application --@#
start-verbose:
	@echo "<<<<<<<<<<Start up the api containers after building>>>>>>>>>>>>>>"
	@echo ""
	docker-compose up

#@-- command to start the api --@#
start-api:
	@echo "<<<<<<<<<<Build and start the API>>>>>>>>>>>>>"
	@echo ""
	docker-compose up --build

#@-- command to stop the application --@#
stop:
	@echo "<<<<<<<<<<Stop running the api containers>>>>>>>>>>>>>>"
	@echo ""
	docker-compose down

#@-- command to remove the images created --@#
clean:
	@echo "<<<<<<<<<< \033[31m  Remove application image>>>>>>>>>>>>>>"
	@echo ""
	bash cleanup.sh

#@-- help should be run by default when no command is specified --@#
default: help
