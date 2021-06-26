# type: ignore
from copy import copy

from rabbitai.config import *
from tests.rabbitai_test_custom_template_processors import CustomPrestoTemplateProcessor

AUTH_USER_REGISTRATION_ROLE = "alpha"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DATA_DIR, "unittests.db")
DEBUG = False
RABBITAI_WEBSERVER_PORT = 8081

# Allowing SQLALCHEMY_DATABASE_URI and SQLALCHEMY_EXAMPLES_URI to be defined as an env vars for
# continuous integration
if "RABBITAI__SQLALCHEMY_DATABASE_URI" in os.environ:
    SQLALCHEMY_DATABASE_URI = os.environ["RABBITAI__SQLALCHEMY_DATABASE_URI"]

SQLALCHEMY_EXAMPLES_URI = SQLALCHEMY_DATABASE_URI
if "RABBITAI__SQLALCHEMY_EXAMPLES_URI" in os.environ:
    SQLALCHEMY_EXAMPLES_URI = os.environ["RABBITAI__SQLALCHEMY_EXAMPLES_URI"]

if "UPLOAD_FOLDER" in os.environ:
    UPLOAD_FOLDER = os.environ["UPLOAD_FOLDER"]

if "sqlite" in SQLALCHEMY_DATABASE_URI:
    logger.warning(
        "SQLite Database support for metadata databases will be "
        "removed in a future version of Rabbitai."
    )

# Speeding up the tests.
PRESTO_POLL_INTERVAL = 0.1
HIVE_POLL_INTERVAL = 0.1

SQL_MAX_ROW = 10000
SQLLAB_CTAS_NO_LIMIT = True  # SQL_MAX_ROW will not take affect for the CTA queries
FEATURE_FLAGS = {
    **FEATURE_FLAGS,
    "foo": "bar",
    "KV_STORE": True,
    "SHARE_QUERIES_VIA_KV_STORE": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ENABLE_REACT_CRUD_VIEWS": os.environ.get("ENABLE_REACT_CRUD_VIEWS", False),
    "ALERT_REPORTS": True,
    "DASHBOARD_NATIVE_FILTERS": True,
}


def GET_FEATURE_FLAGS_FUNC(ff):
    ff_copy = copy(ff)
    ff_copy["super"] = "set"
    return ff_copy


TESTING = True
WTF_CSRF_ENABLED = False

FAB_ROLES = {"TestRole": [["Security", "menu_access"], ["List Users", "menu_access"]]}

AUTH_ROLE_PUBLIC = "Public"
EMAIL_NOTIFICATIONS = False
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.environ.get("REDIS_CELERY_DB", 2)
REDIS_RESULTS_DB = os.environ.get("REDIS_RESULTS_DB", 3)
REDIS_CACHE_DB = os.environ.get("REDIS_CACHE_DB", 4)

CACHE_DEFAULT_TIMEOUT = 600

CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 60,
    "CACHE_KEY_PREFIX": "rabbitai_cache",
    "CACHE_REDIS_URL": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}",
}

DATA_CACHE_CONFIG = {
    **CACHE_CONFIG,
    "CACHE_DEFAULT_TIMEOUT": 30,
    "CACHE_KEY_PREFIX": "rabbitai_data_cache",
}

GLOBAL_ASYNC_QUERIES_JWT_SECRET = "test-secret-change-me-test-secret-change-me"

ALERT_REPORTS_WORKING_TIME_OUT_KILL = True


class CeleryConfig(object):
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    CELERY_IMPORTS = ("rabbitai.sql_lab",)
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    CELERY_ANNOTATIONS = {"sql_lab.add": {"rate_limit": "10/s"}}
    CONCURRENCY = 1


CELERY_CONFIG = CeleryConfig

CUSTOM_TEMPLATE_PROCESSORS = {
    CustomPrestoTemplateProcessor.engine: CustomPrestoTemplateProcessor
}

PRESERVE_CONTEXT_ON_EXCEPTION = False
