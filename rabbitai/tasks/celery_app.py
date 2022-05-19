"""
This is the main entrypoint used by Celery workers. As such,
it needs to call create_app() in order to initialize things properly
"""

from typing import Any

from celery.signals import worker_process_init

# Rabbitai framework imports
from rabbitai import create_app
from rabbitai.extensions import celery_app, db

# Init the Flask app / configure everything
flask_app = create_app()

# Need to import late, as the celery_app will have been setup by "create_app()"
# pylint: disable=wrong-import-position, unused-import
from . import cache, schedules, scheduler  # isort:skip

# Export the celery app globally for Celery (as run on the cmd line) to find
app = celery_app


@worker_process_init.connect
def reset_db_connection_pool(**kwargs: Any) -> None:
    with flask_app.app_context():
        # https://docs.sqlalchemy.org/en/14/core/connections.html#engine-disposal
        db.engine.dispose()
