#!/usr/bin/env bash

set -e

#
# Always install local overrides first
#
/app/docker/docker-bootstrap.sh

STEP_CNT=4

echo_step() {
cat <<EOF

######################################################################


Init Step ${1}/${STEP_CNT} [${2}] -- ${3}


######################################################################

EOF
}
ADMIN_PASSWORD="admin"
# If Cypress run – overwrite the password for admin and export env variables
if [ "$CYPRESS_CONFIG" == "true" ]; then
    ADMIN_PASSWORD="general"
    export RABBITAI_CONFIG=tests.rabbitai_test_config
    export RABBITAI_TESTENV=true
    export ENABLE_REACT_CRUD_VIEWS=true
    export RABBITAI__SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://rabbitai:rabbitai@db:5432/rabbitai_db
fi
# Initialize the database
echo_step "1" "Starting" "Applying DB migrations"
rabbitai db upgrade
echo_step "1" "Complete" "Applying DB migrations"

# Create an admin user
echo_step "2" "Starting" "Setting up admin user ( admin / $ADMIN_PASSWORD )"
rabbitai fab create-admin \
              --username admin \
              --firstname Peng \
              --lastname Songbo \
              --email pengsongbo@hotmail.com \
              --password $ADMIN_PASSWORD
echo_step "2" "Complete" "Setting up admin user"
# Create default roles and permissions
echo_step "3" "Starting" "Setting up roles and perms"
rabbitai init
echo_step "3" "Complete" "Setting up roles and perms"

if [ "$RABBITAI_LOAD_EXAMPLES" = "yes" ]; then
    # Load some data to play with
    echo_step "4" "Starting" "Loading examples"
    # If Cypress run which consumes rabbitai_test_config – load required data for tests
    if [ "$CYPRESS_CONFIG" == "true" ]; then
        rabbitai load_test_users
        rabbitai load_examples --load-test-data
    else
        rabbitai load_examples
    fi
    echo_step "4" "Complete" "Loading examples"
fi
