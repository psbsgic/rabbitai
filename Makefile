# Python version installed; we need 3.8 or 3.7
PYTHON=`command -v python3.8 || command -v python3.7`

.PHONY: install rabbitai venv pre-commit

install: rabbitai pre-commit

rabbitai:
	# Install external dependencies
	pip install -r requirements/local.txt

	# Install Rabbitai in editable (development) mode
	pip install -e .

	# Create an admin user in your metadata database
	rabbitai fab create-admin

	# Initialize the database
	rabbitai db upgrade

	# Create default roles and permissions
	rabbitai init

	# Load some data to play with
	rabbitai load-examples

update: update-py update-js

update-py:
	# Install external dependencies
	pip install -r requirements/local.txt

	# Install Superset in editable (development) mode
	pip install -e .

	# Initialize the database
	rabbitai db upgrade

	# Create default roles and permissions
	rabbitai init

update-js:
	# Install js packages
	cd rabbitai-frontend; npm install

venv:
	# Create a virtual environment and activate it (recommended)
	if ! [ -x "${PYTHON}" ]; then echo "You need Python 3.7 or 3.8 installed"; exit 1; fi
	test -d venv || ${PYTHON} -m venv venv # setup a python3 virtualenv
	. venv/bin/activate

pre-commit:
	# setup pre commit dependencies
	pip3 install -r requirements/integration.txt
	pre-commit install

format: py-format js-format

py-format: pre-commit
	pre-commit run black --all-files

py-lint: pre-commit
	pylint -j 0 rabbitai

js-format:
	cd rabbitai-frontend; npm run prettier
