#!/usr/bin/env bash

set -eo pipefail

REQUIREMENTS_LOCAL="/app/docker/requirements-local.txt"
# 如果 Cypress 运行 – 重写管理员密码，导出环境变量
if [ "$CYPRESS_CONFIG" == "true" ]; then
    export RABBITAI_CONFIG=tests.integration_tests.rabbitai_test_config
    export RABBITAI_TESTENV=true
    export ENABLE_REACT_CRUD_VIEWS=true
    export RABBITAI__SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://rabbitai:rabbitai@db:5432/rabbitaidb
fi

#
# 确保我们已经安装了开发人员依赖软件包
#
if [ -f "${REQUIREMENTS_LOCAL}" ]; then
  echo "Installing local overrides at ${REQUIREMENTS_LOCAL}"
  pip install -r "${REQUIREMENTS_LOCAL}"
else
  echo "Skipping local overrides"
fi

if [[ "${1}" == "worker" ]]; then
  echo "Starting Celery worker..."
  celery --app=rabbitai.tasks.celery_app:app worker -Ofair -l INFO
elif [[ "${1}" == "beat" ]]; then
  echo "Starting Celery beat..."
  celery --app=rabbitai.tasks.celery_app:app beat --pidfile /tmp/celerybeat.pid -l INFO -s "${RABBITAI_HOME}"/celerybeat-schedule
elif [[ "${1}" == "app" ]]; then
  echo "Starting web app..."
  flask run -p 8088 --with-threads --reload --debugger --host=0.0.0.0
elif [[ "${1}" == "app-gunicorn" ]]; then
  echo "Starting web app..."
  /app/docker/docker-entrypoint.sh
fi
