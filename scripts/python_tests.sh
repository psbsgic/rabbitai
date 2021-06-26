#!/usr/bin/env bash


set -e

export RABBITAI_CONFIG=${RABBITAI_CONFIG:-tests.rabbitai_test_config}
export RABBITAI_TESTENV=true
echo "Rabbitai config module: $RABBITAI_CONFIG"

rabbitai db upgrade
rabbitai init

echo "Running tests"
pytest --maxfail=1 --cov=rabbitai $@
