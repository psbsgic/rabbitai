#!/bin/bash

set -ex

echo "[WARNING] this entrypoint creates an admin/admin user"
echo "[WARNING] it should only be used for lightweight testing/validation"

# Create an admin user (you will be prompted to set username, first and last name before setting a password)
rabbitai fab create-admin \
    --username admin \
    --firstname admin \
    --lastname admin \
    --email admin@admin.com \
    --password admin

# Initialize the database
rabbitai db upgrade

# Loading examples
rabbitai load_examples

# Create default roles and permissions
rabbitai init

FLASK_ENV=development FLASK_APP="rabbitai.app:create_app()" \
flask run -p 8088 --with-threads --reload --debugger --host=0.0.0.0
