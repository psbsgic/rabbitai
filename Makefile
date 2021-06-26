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

	# Install Rabbitai in editable (development) mode
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
	python3 -m venv venv # setup a python3 virtualenv
	source venv/bin/activate

pre-commit:
	# setup pre commit dependencies
	pip3 install -r requirements/integration.txt
	pre-commit install

format: py-format js-format

py-format: pre-commit
	pre-commit run black --all-files

js-format:
	cd rabbitai-frontend; npm run prettier
