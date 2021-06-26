import os

# region Babel config for translations

# Setup default language
BABEL_DEFAULT_LOCALE = "zh"
# Your application default translation path
BABEL_DEFAULT_FOLDER = "rabbitai/translations"
# The allowed translation for you app
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "es": {"flag": "es", "name": "Spanish"},
    "it": {"flag": "it", "name": "Italian"},
    "fr": {"flag": "fr", "name": "French"},
    "zh": {"flag": "cn", "name": "Chinese"},
    "ja": {"flag": "jp", "name": "Japanese"},
    "de": {"flag": "de", "name": "German"},
    "pt": {"flag": "pt", "name": "Portuguese"},
    "pt_BR": {"flag": "br", "name": "Brazilian Portuguese"},
    "ru": {"flag": "ru", "name": "Russian"},
    "ko": {"flag": "kr", "name": "Korean"},
}

# endregion

# SQLAlchemy 数据库连接字符串
# SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'

# 连接到 postgresql 数据库
# 用户名:密码@localhost:端口（5432）/数据库名（superset）
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:psb123456@localhost:5432/superset'

# 默认缓存配置
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
"""项目的根目录，即配置文件所在目录。"""

# 存储数据的目录
if "SUPERSET_HOME" in os.environ:
    DATA_DIR = os.environ["SUPERSET_HOME"]
    """数据目录，SUPERSET_HOME系统环境变量定义的目录"""
else:
    DATA_DIR = os.path.join(os.path.expanduser("~"), ".superset")
    """数据目录，用户目录下的.superset目录"""

# CACHE_CONFIG: CacheConfig = {"CACHE_TYPE": "null"}
CACHE_CONFIG = {
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": DATA_DIR
}

# 数据源和查询结果缓存，默认使用默认缓存配置
DATA_CACHE_CONFIG = CACHE_CONFIG
