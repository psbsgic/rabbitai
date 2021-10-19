安装 & 配置
============================

入门
---------------

Rabbitai支持Python版本 ``>3.7`` 以利用较新的Python特性，并减少支持以前版本的负担。
我们针对 ``3.7`` 运行测试套件，另外还有一部分测试也针对 ``3.8`` 运行。

云原生!
-------------

Rabbitai的设计目的是提供高可用性。它是“云原生”的，因为它被设计成在大型分布式环境中扩展，并且在容器中运行良好。
虽然您可以轻松地在普通设置或笔记本电脑上测试Rabbitai，但扩展平台几乎没有限制。
Rabbitai也是云原生的，因为它非常灵活，允许您选择web服务器（Gunicorn、Nginx、Apache）、
元数据数据库引擎（MySQL、Postgres、MariaDB等）、消息队列（Redis、RabbitMQ、SQS等）、
结果后端（S3、Redis、Memcached等）、缓存层（Memcached、Redis等），
与NewRelic、StatsD和DataDog等服务配合良好，能够针对最流行的数据库技术运行分析工作负载。

Rabbitai在拥有数百名并发用户的大型环境中经过了战斗测试。Airbnb的生产环境在Kubernetes内部运行，
每天为600多名活跃用户提供超过10万张图表的服务。

Rabbitai web服务器和Rabbitai Celery 工作者（可选）是无状态的，因此您可以根据需要在任意多个服务器上运行来扩展。

使用Docker在本地安装和部署Rabbitai
-----------------------------------------------

要在本地尝试Rabbitai，当前支持的最佳方法是通过Docker，使用 ``docker-compose``。
Rabbitai没有对Windows的官方支持，因此我们在下面提供了一个VM解决方案。（一旦支持Windows，我们将更新此文档。）

**Step 0 - 安装 Docker 和 Docker Compose**

*Mac OSX:*

    `安装 Docker for Mac <https://docs.docker.com/docker-for-mac/install/>`__，其中包括Docker引擎和最新版本的 `docker-compose` 开箱即用。

    安装Docker for Mac后，打开Docker的首选项窗格，转到“资源”部分，将分配的内存增加到6GB。默认情况下只分配2GB的RAM，Rabbitai将无法启动。


*Linux:*

    `安装 Docker on Linux <https://docs.docker.com/engine/install/>`__ ，按照Docker的说明，选择适合您的Linux版本。

    因为 ``docker-compose`` 不是作为 Docker 安装的一部分安装的，一旦你有了一个工作的引擎，接下来按照针对Linux `docker-compose 安装说明 <https://docs.docker.com/compose/install/>`__ 进行安装


*Windows:*

    注意：Windows目前不支持Rabbitai安装环境。

    对于Windows用户来说，最好的选择是通过 `VirtualBox <https://www.virtualbox.org/>`__ 安装Ubuntu虚拟机，然后在虚拟机中继续执行Docker on Linux指令。建议为虚拟机分配至少8GB的RAM，并提供至少40GB的硬盘驱动器，以便为操作系统和所有必需的依赖项提供足够的空间。

**Step 1 - 克隆Rabbitai的Github存储库**

使用以下命令 `克隆 Rabbitai <https://github.com/psbsgic/rabbitai>`__ ：

.. code:: bash

    $ git clone https://github.com/psbsgic/rabbitai.git

一旦该命令成功完成，您应该会在当前目录中看到一个新的 ``rabbitai`` 文件夹。

**Step 2 - 通过 `docker-compose up` 启动 Rabbitai**

接下来，`cd` 到 Step 1中创建的文件夹：

.. code:: bash

    $ cd rabbitai

进入目录后，运行以下命令：

.. code:: bash

    $ docker-compose up

您应该会看到输出屏幕，上面记录了机器上启动的容器的输出。
一旦这个输出变慢时，您应该在本地机器上有一个正在运行的Rabbitai实例！

**Step 3 - 登录Rabbitai**

您的Rabbitai本地实例还包括一个用于存储数据的Postgres服务器，
并且已经预加载了Rabbitai附带的一些示例数据集。
您现在可以通过web浏览器访问Rabbitai，访问 ``http://localhost:8088``。
请注意，许多浏览器现在默认为 ``https`` -如果您的浏览器是其中之一，否则请使用``http``。

使用默认用户名和密码登录：

::

    username: admin
    password: admin

恭喜！您已成功安装Rabbitai！

OS 依赖
---------------

Rabbitai 存储数据库连接信息在元数据库中。
为此，我们使用 ``cryptography`` Python 库加密连接密码。
不幸的是，此库具有操作系统级依赖项。

您可能希望尝试下一步（“Rabbitai安装和初始化”），如果遇到错误，请返回此步骤。

以下是如何安装它们：

对于 **Debian** 和 **Ubuntu**，运行以下命令安装依赖: ::

    sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-pip libsasl2-dev libldap2-dev

**Ubuntu 20.04** 运行以下命令安装依赖: ::

    sudo apt-get install build-essential libssl-dev libffi-dev python3-dev python3-pip libsasl2-dev libldap2-dev

否则 ``cryptography`` 构建将失败。

对于 **Fedora** 和 **RHEL-derivatives**, ，运行以下命令安装依赖: ::

    sudo yum upgrade python-setuptools
    sudo yum install gcc gcc-c++ libffi-devel python-devel python-pip python-wheel openssl-devel cyrus-sasl-devel openldap-devel

**Mac OS X** ，您应该升级到最新版本的OS X，因为该版本的问题更有可能得到解决。您*可能需要*适用于您安装的OS X版本的最新版本的XCode。您还应该安装XCode命令行工具: ::

    xcode-select --install

不推荐使用系统python。自制的python也附带了pip: ::

    brew install pkg-config libffi openssl python
    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography==2.4.2

**Windows** 目前还没有官方支持，但是您可以测，
下载 `get-pip.py <https://bootstrap.pypa.io/get-pip.py>`_, 以管理员身份运行 ``python get-pip.py``。然后运行: ::

    C:\> pip install cryptography

    # You may also have to create C:\Temp
    C:\> md C:\Temp

Python virtualenv
-----------------
推荐安装 Rabbitai 到虚拟环境。Python 3 已提供 virtualenv。
但是，如果由于某种原因它没有安装在您的环境中，您可以通过针对您的操作系统的软件包安装它，否则您可以从pip安装: ::

    pip install virtualenv

您可以通过以下方式创建和激活virtualenv: ::

    # virtualenv is shipped in Python 3.6+ as venv instead of pyvenv.
    # See https://docs.python.org/3.6/library/venv.html
    python3 -m venv venv
    . venv/bin/activate

在Windows上，激活它的语法有点不同: ::

    venv\Scripts\activate

一旦你激活了你的virtualenv，你所做的一切都被限制在virtualenv内。
要退出virtualenv，只需执行命令 `deactivate`。

Python's setup tools and pip
----------------------------
通过获取最新的  ``pip`` 和 ``setuptools`` 库，您可以获得所有机会。::

    pip install --upgrade setuptools pip

Rabbitai 安装和初始化
----------------------------------------
按照以下几个简单步骤安装Rabbitai。::

    # 安装 rabbitai
    pip install rabbitai

    # 初始化数据库
    rabbitai db upgrade

    # 创建管理员用户(在设置密码之前，系统将提示您设置用户名、名字和姓氏)
    $ export FLASK_APP=rabbitai
    rabbitai fab create-admin

    # 加载示例
    rabbitai load_examples

    # 创建默认角色和权限
    rabbitai init

    # 要在端口8088上启动开发web服务器，请使用-p绑定到另一个端口
    rabbitai run -p 8088 --with-threads --reload --debugger

安装后，您应该能够将浏览器指向右侧
主机名：端口 `http://localhost:8088 <http://localhost:8088>`_，使用您在创建管理员帐户时输入的凭据登录，
导航到 `Menu -> Admin -> Refresh Metadata`。这个动作应该让Rabbitai知道你的所有数据源，
它们应该显示在 `菜单->数据源`（`Menu -> Datasources`）中，从那里你可以开始玩你的数据！

A proper WSGI HTTP Server
-------------------------

虽然您可以将Rabbitai设置为在Nginx或Apache上运行，但许多人使用Gunicorn，最好是在 **异步模式async mode** 下，
这甚至可以实现令人印象深刻的并发性，而且安装和配置都相当容易。
请参考您首选的技术文档，以在您的环境中运行良好的方式设置此WSGI应用程序。
这里有一个 **异步 async** 设置，已知它在生产中运行良好: ::

 　gunicorn \
        -w 10 \
        -k gevent \
        --timeout 120 \
        -b  0.0.0.0:6666 \
        --limit-request-line 0 \
        --limit-request-field_size 0 \
        --statsd-host localhost:8125 \
        "rabbitai.app:create_app()"

更多信息参考
`Gunicorn documentation <https://docs.gunicorn.org/en/stable/design.html>`_


Note that the development web
server (`rabbitai run` or `flask run`) is not intended for production use.

If not using gunicorn, you may want to disable the use of flask-compress
by setting `COMPRESS_REGISTER = False` in your `rabbitai_config.py`

Configuration behind a load balancer
------------------------------------

If you are running rabbitai behind a load balancer or reverse proxy (e.g. NGINX
or ELB on AWS), you may need to utilise a healthcheck endpoint so that your
load balancer knows if your rabbitai instance is running. This is provided
at ``/health`` which will return a 200 response containing "OK" if the
the webserver is running.

If the load balancer is inserting X-Forwarded-For/X-Forwarded-Proto headers, you
should set `ENABLE_PROXY_FIX = True` in the rabbitai config file to extract and use
the headers.

In case that the reverse proxy is used for providing ssl encryption,
an explicit definition of the `X-Forwarded-Proto` may be required.
For the Apache webserver this can be set as follows: ::

    RequestHeader set X-Forwarded-Proto "https"

Configuration
-------------

To configure your application, you need to create a file (module)
``rabbitai_config.py`` and make sure it is in your PYTHONPATH. Here are some
of the parameters you can copy / paste in that configuration module: ::

    #---------------------------------------------------------
    # Rabbitai specific config
    #---------------------------------------------------------
    ROW_LIMIT = 5000

    RABBITAI_WEBSERVER_PORT = 8088
    #---------------------------------------------------------

    #---------------------------------------------------------
    # Flask App Builder configuration
    #---------------------------------------------------------
    # Your App secret key
    SECRET_KEY = '\2\1thisismyscretkey\1\2\e\y\y\h'

    # The SQLAlchemy connection string to your database backend
    # This connection defines the path to the database that stores your
    # rabbitai metadata (slices, connections, tables, dashboards, ...).
    # Note that the connection information to connect to the datasources
    # you want to explore are managed directly in the web UI
    SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/rabbitai.db'

    # Flask-WTF flag for CSRF
    WTF_CSRF_ENABLED = True
    # Add endpoints that need to be exempt from CSRF protection
    WTF_CSRF_EXEMPT_LIST = []
    # A CSRF token that expires in 1 year
    WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

    # Set this API key to enable Mapbox visualizations
    MAPBOX_API_KEY = ''

All the parameters and default values defined in
https://github.com/psbsgic/rabbitai/blob/master/rabbitai/config.py
can be altered in your local ``rabbitai_config.py`` .
Administrators will want to
read through the file to understand what can be configured locally
as well as the default values in place.

Since ``rabbitai_config.py`` acts as a Flask configuration module, it
can be used to alter the settings Flask itself,
as well as Flask extensions like ``flask-wtf``, ``flask-caching``,
``flask-migrate``, and ``flask-appbuilder``. Flask App Builder, the web
framework used by Rabbitai offers many configuration settings. Please consult
the `Flask App Builder Documentation
<https://flask-appbuilder.readthedocs.org/en/latest/config.html>`_
for more information on how to configure it.

Make sure to change:

* *SQLALCHEMY_DATABASE_URI*, by default it is stored at *~/.rabbitai/rabbitai.db*
* *SECRET_KEY*, to a long random string

In case you need to exempt endpoints from CSRF, e.g. you are running a custom
auth postback endpoint, you can add them to *WTF_CSRF_EXEMPT_LIST*

     WTF_CSRF_EXEMPT_LIST = ['']


.. _ref_database_deps:

Caching
-------

Rabbitai uses `Flask-Caching <https://flask-caching.readthedocs.io/>`_ for
caching purpose. Configuring your caching backend is as easy as providing
``CACHE_CONFIG`` and ``DATA_CACHE_CONFIG`, constants in ``rabbitai_config.py``
that complies with `the Flask-Caching specifications <https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching>`_.

Flask-Caching supports multiple caching backends (Redis, Memcached,
SimpleCache (in-memory), or the local filesystem). If you are going to use
Memcached please use the `pylibmc` client library as `python-memcached` does
not handle storing binary data correctly. If you use Redis, please install
the `redis <https://pypi.python.org/pypi/redis>`_ Python package: ::

    pip install redis

For chart data, Rabbitai goes up a “timeout search path”, from a slice's configuration
to the datasource’s, the database’s, then ultimately falls back to the global default
defined in ``DATA_CACHE_CONFIG``.

.. code-block:: python

    DATA_CACHE_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24, # 1 day default (in secs)
        'CACHE_KEY_PREFIX': 'rabbitai_results',
        'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    }

It is also possible to pass a custom cache initialization function in the
config to handle additional caching use cases. The function must return an
object that is compatible with the `Flask-Caching <https://flask-caching.readthedocs.io/>`_ API.

.. code-block:: python

    from custom_caching import CustomCache

    def init_data_cache(app):
        """Takes an app instance and returns a custom cache backend"""
        config = {
            'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24, # 1 day default (in secs)
            'CACHE_KEY_PREFIX': 'rabbitai_results',
        }
        return CustomCache(app, config)

    DATA_CACHE_CONFIG = init_data_cache

Rabbitai has a Celery task that will periodically warm up the cache based on
different strategies. To use it, add the following to the `CELERYBEAT_SCHEDULE`
section in `config.py`:

.. code-block:: python

    CELERYBEAT_SCHEDULE = {
        'cache-warmup-hourly': {
            'task': 'cache-warmup',
            'schedule': crontab(minute=0, hour='*'),  # hourly
            'kwargs': {
                'strategy_name': 'top_n_dashboards',
                'top_n': 5,
                'since': '7 days ago',
            },
        },
    }

This will cache all the charts in the top 5 most popular dashboards every hour.
For other strategies, check the `rabbitai/tasks/cache.py` file.

Caching Thumbnails
------------------

This is an optional feature that can be turned on by activating its feature flag on config:

.. code-block:: python

    FEATURE_FLAGS = {
        "THUMBNAILS": True,
        "THUMBNAILS_SQLA_LISTENERS": True,
    }


For this feature you will need a cache system and celery workers. All thumbnails are stored on cache and are processed
asynchronously by the workers.

An example config where images are stored on S3 could be:

.. code-block:: python

    from flask import Flask
    from s3cache.s3cache import S3Cache

    ...

    class CeleryConfig(object):
        BROKER_URL = "redis://localhost:6379/0"
        CELERY_IMPORTS = ("rabbitai.sql_lab", "rabbitai.tasks", "rabbitai.tasks.thumbnails")
        CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
        CELERYD_PREFETCH_MULTIPLIER = 10
        CELERY_ACKS_LATE = True


    CELERY_CONFIG = CeleryConfig

    def init_thumbnail_cache(app: Flask) -> S3Cache:
        return S3Cache("bucket_name", 'thumbs_cache/')


    THUMBNAIL_CACHE_CONFIG = init_thumbnail_cache
    # Async selenium thumbnail task will use the following user
    THUMBNAIL_SELENIUM_USER = "Admin"

Using the above example cache keys for dashboards will be `rabbitai_thumb__dashboard__{ID}`

You can override the base URL for selenium using:

.. code-block:: python

    WEBDRIVER_BASEURL = "https://rabbitai.company.com"


Additional selenium web drive config can be set using `WEBDRIVER_CONFIGURATION`

You can implement a custom function to authenticate selenium, the default uses flask-login session cookie.
An example of a custom function signature:

.. code-block:: python

    def auth_driver(driver: WebDriver, user: "User") -> WebDriver:
        pass


Then on config:

.. code-block:: python

    WEBDRIVER_AUTH_FUNC = auth_driver

Database dependencies
---------------------

Rabbitai does not ship bundled with connectivity to databases, except
for Sqlite, which is part of the Python standard library.
You'll need to install the required packages for the database you
want to use as your metadata database as well as the packages needed to
connect to the databases you want to access through Rabbitai.

Here's a list of some of the recommended packages.

+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Database         | PyPI package                                                      | SQLAlchemy URI prefix                           |
+==================+===================================================================+=================================================+
| Amazon Athena    | ``"apache-rabbitai[athena]"``                                     | ``awsathena+jdbc://``                           |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Amazon Redshift  | ``"apache-rabbitai[redshift]"``                                   | ``redshift+psycopg2://``                        |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Apache Drill     | ``"apache-rabbitai[drill]"``                                      | For the REST API:``                             |
|                  |                                                                   | ``drill+sadrill://``                            |
|                  |                                                                   | For JDBC                                        |
|                  |                                                                   | ``drill+jdbc://``                               |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Apache Druid     | ``"apache-rabbitai[druid]"``                                      | ``druid://``                                    |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Apache Hive      | ``"apache-rabbitai[hive]"``                                       | ``hive://``                                     |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Apache Impala    | ``"apache-rabbitai[impala]"``                                     | ``impala://``                                   |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Apache Kylin     | ``"apache-rabbitai[kylin]"``                                      | ``kylin://``                                    |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Apache Pinot     | ``"apache-rabbitai[pinot]"``                                      | ``pinot+http://CONTROLLER:5436/``               |
|                  |                                                                   | ``query?server=http://CONTROLLER:5983/``        |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Apache Solr      | ``pip install sqlalchemy-solr``                                   | ``solr://``                                     |
+------------------+---------------------------------------+-----------------------------------------------------------------------------+
| Apache Spark SQL | ``"apache-rabbitai[hive]"``                                       | ``jdbc+hive://``                                |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| BigQuery         | ``"apache-rabbitai[bigquery]"``                                   | ``bigquery://``                                 |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| ClickHouse       | ``"apache-rabbitai[clickhouse]"``                                 |                                                 |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| CockroachDB      | ``"apache-rabbitai[cockroachdb]"``                                | ``cockroachdb://``                              |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Dremio           | ``"apache-rabbitai[dremio]"``                                     | ``dremio://``                                   |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Elasticsearch    | ``"apache-rabbitai[elasticsearch]"``                              | ``elasticsearch+http://``                       |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Exasol           | ``"apache-rabbitai[exasol]"``                                     | ``exa+pyodbc://``                               |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Google Sheets    | ``"apache-rabbitai[gsheets]"``                                    | ``gsheets://``                                  |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| IBM Db2          | ``"apache-rabbitai[db2]"``                                        | ``db2+ibm_db://``                               |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| MySQL            | ``"apache-rabbitai[mysql]"``                                      | ``mysql://``                                    |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Oracle           | ``"apache-rabbitai[oracle]"``                                     | ``oracle://``                                   |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| PostgreSQL       | ``"apache-rabbitai[postgres]"``                                   | ``postgresql+psycopg2://``                      |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Presto           | ``"apache-rabbitai[presto]"``                                     | ``presto://``                                   |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| SAP HANA         | ``"apache-rabbitai[hana]"``                                       |  ``hana://``                                    |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Snowflake        | ``"apache-rabbitai[snowflake]"``                                  | ``snowflake://``                                |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| SQLite           |                                                                   | ``sqlite://``                                   |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| SQL Server       | ``"apache-rabbitai[mssql]"``                                      | ``mssql://``                                    |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Teradata         | ``"apache-rabbitai[teradata]"``                                   | ``teradata://``                                 |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+
| Vertica          | ``"apache-rabbitai[vertical]"``                                   |  ``vertica+vertica_python://``                  |
+------------------+-------------------------------------------------------------------+-------------------------------------------------+

Note that many other databases are supported, the main criteria being the
existence of a functional SqlAlchemy dialect and Python driver. Googling
the keyword ``sqlalchemy`` in addition of a keyword that describes the
database you want to connect to should get you to the right place.

PostgreSQL
------------

The connection string for PostgreSQL looks like this ::

    postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}

Additional  may be configured via the ``extra`` field under ``engine_params``.
If you would like to enable mutual SSL here is a sample configuration:

.. code-block:: json

    {
        "metadata_params": {},
        "engine_params": {
              "connect_args":{
                    "sslmode": "require",
                    "sslrootcert": "/path/to/root_cert"
            }
         }
    }

If the key ``sslrootcert`` is present the server's certificate will be verified to be signed by the same Certificate Authority (CA).

If you would like to enable mutual SSL here is a sample configuration:

.. code-block:: json

    {
        "metadata_params": {},
        "engine_params": {
              "connect_args":{
                    "sslmode": "require",
                    "sslcert": "/path/to/client_cert",
                    "sslkey": "/path/to/client_key",
                    "sslrootcert": "/path/to/root_cert"
            }
         }
    }

See `psycopg2 SQLAlchemy <https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2>`_.

Hana
------------

The connection string for Hana looks like this ::

    hana://{username}:{password}@{host}:{port}


(AWS) Athena
------------

The connection string for Athena looks like this ::

    awsathena+jdbc://{aws_access_key_id}:{aws_secret_access_key}@athena.{region_name}.amazonaws.com/{schema_name}?s3_staging_dir={s3_staging_dir}&...

Where you need to escape/encode at least the s3_staging_dir, i.e., ::

    s3://... -> s3%3A//...

You can also use `PyAthena` library(no java required) like this ::

    awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}@athena.{region_name}.amazonaws.com/{schema_name}?s3_staging_dir={s3_staging_dir}&...

See `PyAthena <https://github.com/laughingman7743/PyAthena#sqlalchemy>`_.

(Google) BigQuery
-----------------

The connection string for BigQuery looks like this ::

    bigquery://{project_id}

Additionally, you will need to configure authentication via a
Service Account. Create your Service Account via the Google
Cloud Platform control panel, provide it access to the appropriate
BigQuery datasets, and download the JSON configuration file
for the service account. In Rabbitai, Add a JSON blob to
the "Secure Extra" field in the database configuration page
with the following format ::

    {
        "credentials_info": <contents of credentials JSON file>
    }

The resulting file should have this structure ::

    {
        "credentials_info": {
            "type": "service_account",
            "project_id": "...",
            "private_key_id": "...",
            "private_key": "...",
            "client_email": "...",
            "client_id": "...",
            "auth_uri": "...",
            "token_uri": "...",
            "auth_provider_x509_cert_url": "...",
            "client_x509_cert_url": "...",
        }
    }

You should then be able to connect to your BigQuery datasets.

To be able to upload data, e.g. sample data, the python library `pandas_gbq` is required.


Apache Solr
------------

The connection string for Apache Solr looks like this ::

    solr://{username}:{password}@{host}:{port}/{server_path}/{collection}[/?use_ssl=true|false]

Elasticsearch
-------------

The connection string for Elasticsearch looks like this ::

    elasticsearch+http://{user}:{password}@{host}:9200/

Using HTTPS ::

    elasticsearch+https://{user}:{password}@{host}:9200/


Elasticsearch as a default limit of 10000 rows, so you can increase this limit on your cluster
or set Rabbitai's row limit on config ::

    ROW_LIMIT = 10000

You can query multiple indices on SQLLab for example ::

    select timestamp, agent from "logstash-*"

But, to use visualizations for multiple indices you need to create an alias index on your cluster ::

    POST /_aliases
    {
        "actions" : [
            { "add" : { "index" : "logstash-**", "alias" : "logstash_all" } }
        ]
    }

Then register your table with the ``alias`` name ``logstasg_all``

Snowflake
---------

The connection string for Snowflake looks like this ::

    snowflake://{user}:{password}@{account}.{region}/{database}?role={role}&warehouse={warehouse}

The schema is not necessary in the connection string, as it is defined per table/query.
The role and warehouse can be omitted if defaults are defined for the user, i.e.

    snowflake://{user}:{password}@{account}.{region}/{database}

Make sure the user has privileges to access and use all required
databases/schemas/tables/views/warehouses, as the Snowflake SQLAlchemy engine does
not test for user/role rights during engine creation by default. However, when
pressing the "Test Connection" button in the Create or Edit Database dialog,
user/role credentials are validated by passing `"validate_default_parameters": True`
to the `connect()` method during engine creation. If the user/role is not authorized
to access the database, an error is recorded in the Rabbitai logs.

See `Snowflake SQLAlchemy <https://github.com/snowflakedb/snowflake-sqlalchemy>`_.

Teradata
---------

The connection string for Teradata looks like this ::

    teradata://{user}:{password}@{host}

*Note*: Its required to have Teradata ODBC drivers installed and environment variables configured for proper work of sqlalchemy dialect. Teradata ODBC Drivers available here: https://downloads.teradata.com/download/connectivity/odbc-driver/linux

Required environment variables: ::

    export ODBCINI=/.../teradata/client/ODBC_64/odbc.ini
    export ODBCINST=/.../teradata/client/ODBC_64/odbcinst.ini

See `Teradata SQLAlchemy <https://github.com/Teradata/sqlalchemy-teradata>`_.

Apache Drill
------------
At the time of writing, the SQLAlchemy Dialect is not available on pypi and must be downloaded here:
`SQLAlchemy Drill <https://github.com/JohnOmernik/sqlalchemy-drill>`_

Alternatively, you can install it completely from the command line as follows: ::

    git clone https://github.com/JohnOmernik/sqlalchemy-drill
    cd sqlalchemy-drill
    python3 setup.py install

Once that is done, you can connect to Drill in two ways, either via the REST interface or by JDBC.  If you are connecting via JDBC, you must have the
Drill JDBC Driver installed.

The basic connection string for Drill looks like this ::

    drill+sadrill://{username}:{password}@{host}:{port}/{storage_plugin}?use_ssl=True

If you are using JDBC to connect to Drill, the connection string looks like this: ::

    drill+jdbc://{username}:{password}@{host}:{port}/{storage_plugin}

For a complete tutorial about how to use Apache Drill with Rabbitai, see this tutorial:
`Visualize Anything with Rabbitai and Drill <http://thedataist.com/visualize-anything-with-rabbitai-and-drill/>`_

Deeper SQLAlchemy integration
-----------------------------

It is possible to tweak the database connection information using the
parameters exposed by SQLAlchemy. In the ``Database`` edit view, you will
find an ``extra`` field as a ``JSON`` blob.

.. image:: _static/images/tutorial/add_db.png
   :scale: 30 %

This JSON string contains extra configuration elements. The ``engine_params``
object gets unpacked into the
`sqlalchemy.create_engine <https://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine>`_ call,
while the ``metadata_params`` get unpacked into the
`sqlalchemy.MetaData <https://docs.sqlalchemy.org/en/rel_1_2/core/metadata.html#sqlalchemy.schema.MetaData>`_ call. Refer to the SQLAlchemy docs for more information.

.. note:: If your using CTAS on SQLLab and PostgreSQL
    take a look at :ref:`ref_ctas_engine_config` for specific ``engine_params``.


Schemas (Postgres & Redshift)
-----------------------------

Postgres and Redshift, as well as other databases,
use the concept of **schema** as a logical entity
on top of the **database**. For Rabbitai to connect to a specific schema,
there's a **schema** parameter you can set in the table form.


External Password store for SQLAlchemy connections
--------------------------------------------------
It is possible to use an external store for you database passwords. This is
useful if you are running a custom secret distribution framework and do not wish
to store secrets in Rabbitai's meta database.

Example:
Write a function that takes a single argument of type ``sqla.engine.url`` and returns
the password for the given connection string. Then set ``SQLALCHEMY_CUSTOM_PASSWORD_STORE``
in your config file to point to that function. ::

    def example_lookup_password(url):
        secret = <<get password from external framework>>
        return 'secret'

    SQLALCHEMY_CUSTOM_PASSWORD_STORE = example_lookup_password

A common pattern is to use environment variables to make secrets available.
``SQLALCHEMY_CUSTOM_PASSWORD_STORE`` can also be used for that purpose. ::

    def example_password_as_env_var(url):
        # assuming the uri looks like
        # mysql://localhost?rabbitai_user:{RABBITAI_PASSWORD}
        return url.password.format(os.environ)

    SQLALCHEMY_CUSTOM_PASSWORD_STORE = example_password_as_env_var


SSL Access to databases
-----------------------
This example worked with a MySQL database that requires SSL. The configuration
may differ with other backends. This is what was put in the ``extra``
parameter ::

    {
        "metadata_params": {},
        "engine_params": {
              "connect_args":{
                  "sslmode":"require",
                  "sslrootcert": "/path/to/my/pem"
            }
         }
    }


Druid
-----

The native Druid connector (behind the ``DRUID_IS_ACTIVE`` feature flag)
is slowly getting deprecated in favor of the SQLAlchemy/DBAPI connector made
available in the ``pydruid`` library.

To use a custom SSL certificate to validate HTTPS requests, the certificate
contents can be entered in the ``Root Certificate`` field in the Database
dialog. When using a custom certificate, ``pydruid`` will automatically use
``https`` scheme. To disable SSL verification add the following to extras:
``engine_params": {"connect_args": {"scheme": "https", "ssl_verify_cert": false}}``

Dremio
------

Install the following dependencies to connect to Dremio:

* Dremio SQLAlchemy: ``pip install sqlalchemy_dremio``

  * If you receive any errors during the installation of ``sqlalchemy_dremio``, make sure to install the prerequisites for PyODBC properly by following the instructions for your OS here: https://github.com/narendrans/sqlalchemy_dremio#installation
* Dremio's ODBC driver: https://www.dremio.com/drivers/

Example SQLAlchemy URI: ``dremio://dremio:dremio123@localhost:31010/dremio``

Presto
------

By default Rabbitai assumes the most recent version of Presto is being used when
querying the datasource. If you're using an older version of presto, you can configure
it in the ``extra`` parameter::

    {
        "version": "0.123"
    }


Exasol
---------

The connection string for Exasol looks like this ::

    exa+pyodbc://{user}:{password}@{host}

*Note*: It's required to have Exasol ODBC drivers installed for the sqlalchemy dialect to work properly. Exasol ODBC Drivers available are here: https://www.exasol.com/portal/display/DOWNLOAD/Exasol+Download+Section

Example config (odbcinst.ini can be left empty) ::

    $ cat $/.../path/to/odbc.ini
    [EXAODBC]
    DRIVER = /.../path/to/driver/EXASOL_driver.so
    EXAHOST = host:8563
    EXASCHEMA = main

See `SQLAlchemy for Exasol <https://github.com/blue-yonder/sqlalchemy_exasol>`_.

CORS
----

The extra CORS Dependency must be installed:

.. code-block:: text

    pip install apache-rabbitai[cors]

The following keys in `rabbitai_config.py` can be specified to configure CORS:


* ``ENABLE_CORS``: Must be set to True in order to enable CORS
* ``CORS_OPTIONS``: options passed to Flask-CORS (`documentation <https://flask-cors.corydolphin.com/en/latest/api.html#extension>`)


Domain Sharding
---------------

Chrome allows up to 6 open connections per domain at a time. When there are more
than 6 slices in dashboard, a lot of time fetch requests are queued up and wait for
next available socket. `PR 5039 <https://github.com/apache/rabbitai/pull/5039>`_ adds domain sharding to Rabbitai,
and this feature will be enabled by configuration only (by default Rabbitai
doesn't allow cross-domain request).

* ``RABBITAI_WEBSERVER_DOMAINS``: list of allowed hostnames for domain sharding feature. default `None`


Middleware
----------

Rabbitai allows you to add your own middleware. To add your own middleware, update the ``ADDITIONAL_MIDDLEWARE`` key in
your `rabbitai_config.py`. ``ADDITIONAL_MIDDLEWARE`` should be a list of your additional middleware classes.

For example, to use AUTH_REMOTE_USER from behind a proxy server like nginx, you have to add a simple middleware class to
add the value of ``HTTP_X_PROXY_REMOTE_USER`` (or any other custom header from the proxy) to Gunicorn's ``REMOTE_USER``
environment variable: ::

    class RemoteUserMiddleware(object):
        def __init__(self, app):
            self.app = app
        def __call__(self, environ, start_response):
            user = environ.pop('HTTP_X_PROXY_REMOTE_USER', None)
            environ['REMOTE_USER'] = user
            return self.app(environ, start_response)

    ADDITIONAL_MIDDLEWARE = [RemoteUserMiddleware, ]

*Adapted from http://flask.pocoo.org/snippets/69/*

Event Logging
-------------

Rabbitai by default logs special action event on its database. These logs can be accessed on the UI navigating to
"Security" -> "Action Log". You can freely customize these logs by implementing your own event log class.

Example of a simple JSON to Stdout class::

    class JSONStdOutEventLogger(AbstractEventLogger):

        def log(self, user_id, action, *args, **kwargs):
            records = kwargs.get('records', list())
            dashboard_id = kwargs.get('dashboard_id')
            slice_id = kwargs.get('slice_id')
            duration_ms = kwargs.get('duration_ms')
            referrer = kwargs.get('referrer')

            for record in records:
                log = dict(
                    action=action,
                    json=record,
                    dashboard_id=dashboard_id,
                    slice_id=slice_id,
                    duration_ms=duration_ms,
                    referrer=referrer,
                    user_id=user_id
                )
                print(json.dumps(log))


Then on Rabbitai's config pass an instance of the logger type you want to use.

    EVENT_LOGGER = JSONStdOutEventLogger()


Upgrading
---------

Upgrading should be as straightforward as running::

    pip install apache-rabbitai --upgrade
    rabbitai db upgrade
    rabbitai init

We recommend to follow standard best practices when upgrading Rabbitai, such
as taking a database backup prior to the upgrade, upgrading a staging
environment prior to upgrading production, and upgrading production while less
users are active on the platform.

.. note ::
   Some upgrades may contain backward-incompatible changes, or require
   scheduling downtime, when that is the case, contributors attach notes in
   ``UPDATING.md`` in the repository. It's recommended to review this
   file prior to running an upgrade.


Celery Tasks
------------

On large analytic databases, it's common to run queries that
execute for minutes or hours.
To enable support for long running queries that
execute beyond the typical web request's timeout (30-60 seconds), it is
necessary to configure an asynchronous backend for Rabbitai which consists of:

* one or many Rabbitai workers (which is implemented as a Celery worker), and
  can be started with the ``celery worker`` command, run
  ``celery worker --help`` to view the related options.
* a celery broker (message queue) for which we recommend using Redis
  or RabbitMQ
* a results backend that defines where the worker will persist the query
  results

Configuring Celery requires defining a ``CELERY_CONFIG`` in your
``rabbitai_config.py``. Both the worker and web server processes should
have the same configuration.

.. code-block:: python

    class CeleryConfig(object):
        BROKER_URL = 'redis://localhost:6379/0'
        CELERY_IMPORTS = (
            'rabbitai.sql_lab',
            'rabbitai.tasks',
        )
        CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
        CELERYD_LOG_LEVEL = 'DEBUG'
        CELERYD_PREFETCH_MULTIPLIER = 10
        CELERY_ACKS_LATE = True
        CELERY_ANNOTATIONS = {
            'sql_lab.get_sql_results': {
                'rate_limit': '100/s',
            },
            'email_reports.send': {
                'rate_limit': '1/s',
                'time_limit': 120,
                'soft_time_limit': 150,
                'ignore_result': True,
            },
        }
        CELERYBEAT_SCHEDULE = {
            'email_reports.schedule_hourly': {
                'task': 'email_reports.schedule_hourly',
                'schedule': crontab(minute=1, hour='*'),
            },
        }

    CELERY_CONFIG = CeleryConfig

* To start a Celery worker to leverage the configuration run: ::

    celery --app=rabbitai.tasks.celery_app:app worker --pool=prefork -O fair -c 4

* To start a job which schedules periodic background jobs, run ::

    celery --app=rabbitai.tasks.celery_app:app beat

To setup a result backend, you need to pass an instance of a derivative
of ``from cachelib.base.BaseCache`` to the ``RESULTS_BACKEND``
configuration key in your ``rabbitai_config.py``. It's possible to use
Memcached, Redis, S3 (https://pypi.python.org/pypi/s3werkzeugcache),
memory or the file system (in a single server-type setup or for testing),
or to write your own caching interface. Your ``rabbitai_config.py`` may
look something like:

.. code-block:: python

    # On S3
    from s3cache.s3cache import S3Cache
    S3_CACHE_BUCKET = 'foobar-rabbitai'
    S3_CACHE_KEY_PREFIX = 'sql_lab_result'
    RESULTS_BACKEND = S3Cache(S3_CACHE_BUCKET, S3_CACHE_KEY_PREFIX)

    # On Redis
    from cachelib.redis import RedisCache
    RESULTS_BACKEND = RedisCache(
        host='localhost', port=6379, key_prefix='rabbitai_results')

For performance gains, `MessagePack <https://github.com/msgpack/msgpack-python>`_
and `PyArrow <https://arrow.apache.org/docs/python/>`_ are now used for results
serialization. This can be disabled by setting ``RESULTS_BACKEND_USE_MSGPACK = False``
in your configuration, should any issues arise. Please clear your existing results
cache store when upgrading an existing environment.

**Async queries for dashboards and Explore**

It's also possible to configure database queries for charts to operate in `async` mode.
This is especially useful for dashboards with many charts that may otherwise be affected
by browser connection limits. To enable async queries for dashboards and Explore, the
following dependencies are required:

- Redis 5.0+ (the feature utilizes `Redis Streams <https://redis.io/topics/streams-intro>`_)
- Cache backends enabled via the ``CACHE_CONFIG`` and ``DATA_CACHE_CONFIG`` config settings
- Celery workers configured and running to process async tasks

The following configuration settings are available for async queries (see config.py for default values)

- ``GLOBAL_ASYNC_QUERIES`` (feature flag) - enable or disable async query operation
- ``GLOBAL_ASYNC_QUERIES_REDIS_CONFIG`` - Redis connection info
- ``GLOBAL_ASYNC_QUERIES_REDIS_STREAM_PREFIX`` - the prefix used with Redis Streams
- ``GLOBAL_ASYNC_QUERIES_REDIS_STREAM_LIMIT`` - the maximum number of events for each user-specific event stream (FIFO eviction)
- ``GLOBAL_ASYNC_QUERIES_REDIS_STREAM_LIMIT_FIREHOSE`` - the maximum number of events for all users (FIFO eviction)
- ``GLOBAL_ASYNC_QUERIES_JWT_COOKIE_NAME`` - the async query feature uses a `JWT <https://tools.ietf.org/html/rfc7519>`_ cookie for authentication, this setting is the cookie's name
- ``GLOBAL_ASYNC_QUERIES_JWT_COOKIE_SECURE`` - JWT cookie secure option
- ``GLOBAL_ASYNC_QUERIES_JWT_COOKIE_DOMAIN`` - JWT cookie domain option (`see docs for set_cookie <https://tedboy.github.io/flask/interface_api.response_object.html#flask.Response.set_cookie>`
- ``GLOBAL_ASYNC_QUERIES_JWT_SECRET`` - JWT's use a secret key to sign and validate the contents. This value should be at least 32 bytes and have sufficient randomness for proper security
- ``GLOBAL_ASYNC_QUERIES_TRANSPORT`` - available options: "polling" (HTTP, default), "ws" (WebSocket, requires running rabbitai-websocket server)
- ``GLOBAL_ASYNC_QUERIES_POLLING_DELAY`` - the time (in ms) between polling requests

More information on the async query feature can be found in `SIP-39 <https://github.com/apache/rabbitai/issues/9190>`_.

**Important notes**

* It is important that all the worker nodes and web servers in
  the Rabbitai cluster share a common metadata database.
  This means that SQLite will not work in this context since it has
  limited support for concurrency and
  typically lives on the local file system.

* There should only be one instance of ``celery beat`` running in your
  entire setup. If not, background jobs can get scheduled multiple times
  resulting in weird behaviors like duplicate delivery of reports,
  higher than expected load / traffic etc.

* SQL Lab will only run your queries asynchronously if you enable
  "Asynchronous Query Execution" in your database settings.


Email Reports
-------------
Email reports allow users to schedule email reports for

* chart and dashboard visualization (Attachment or inline)
* chart data (CSV attachment on inline table)

**Setup**

Make sure you enable email reports in your configuration file

.. code-block:: python

    ENABLE_SCHEDULED_EMAIL_REPORTS = True

This flag enables some permissions that are stored in your database, so you'll want to run `rabbitai init` again if you are running this in a dev environment.
Now you will find two new items in the navigation bar that allow you to schedule email
reports

* Manage -> Dashboard Emails
* Manage -> Chart Email Schedules

Schedules are defined in crontab format and each schedule
can have a list of recipients (all of them can receive a single mail,
or separate mails). For audit purposes, all outgoing mails can have a
mandatory bcc.

In order get picked up you need to configure a celery worker and a celery beat
(see section above "Celery Tasks"). Your celery configuration also
needs an entry ``email_reports.schedule_hourly`` for ``CELERYBEAT_SCHEDULE``.

To send emails you need to configure SMTP settings in your configuration file. e.g.

.. code-block:: python

    EMAIL_NOTIFICATIONS = True

    SMTP_HOST = "email-smtp.eu-west-1.amazonaws.com"
    SMTP_STARTTLS = True
    SMTP_SSL = False
    SMTP_USER = "smtp_username"
    SMTP_PORT = 25
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
    SMTP_MAIL_FROM = "insights@komoot.com"


To render dashboards you need to install a local browser on your rabbitai instance

  * `geckodriver <https://github.com/mozilla/geckodriver>`_ and Firefox is preferred
  * `chromedriver <http://chromedriver.chromium.org/>`_ is a good option too

You need to adjust the ``WEBDRIVER_TYPE`` accordingly in your configuration.

You also need to specify on behalf of which username to render the dashboards. In general
dashboards and charts are not accessible to unauthorized requests, that is why the
worker needs to take over credentials of an existing user to take a snapshot. ::

    EMAIL_REPORTS_USER = 'username_with_permission_to_access_dashboards'


**Important notes**

* Be mindful of the concurrency setting for celery (using ``-c 4``).
  Selenium/webdriver instances can consume a lot of CPU / memory on your servers.

* In some cases, if you notice a lot of leaked ``geckodriver`` processes, try running
  your celery processes with ::

    celery worker --pool=prefork --max-tasks-per-child=128 ...

* It is recommended to run separate workers for ``sql_lab`` and
  ``email_reports`` tasks. Can be done by using ``queue`` field in ``CELERY_ANNOTATIONS``

* Adjust ``WEBDRIVER_BASEURL`` in your config if celery workers can't access rabbitai via its
  default value ``http://0.0.0.0:8080/`` (notice the port number 8080, many other setups use
  port 8088).

SQL Lab
-------
SQL Lab is a powerful SQL IDE that works with all SQLAlchemy compatible
databases. By default, queries are executed in the scope of a web
request so they may eventually timeout as queries exceed the maximum duration of a web
request in your environment, whether it'd be a reverse proxy or the Rabbitai
server itself. In such cases, it is preferred to use ``celery`` to run the queries
in the background. Please follow the examples/notes mentioned above to get your
celery setup working.

Also note that SQL Lab supports Jinja templating in queries and that it's
possible to overload
the default Jinja context in your environment by defining the
``JINJA_CONTEXT_ADDONS`` in your rabbitai configuration. Objects referenced
in this dictionary are made available for users to use in their SQL.

.. code-block:: python

    JINJA_CONTEXT_ADDONS = {
        'my_crazy_macro': lambda x: x*2,
    }

Default values for jinja templates can be specified via ``Parameters`` menu in the SQL Lab user interface.
In the UI you can assign a set of parameters as JSON

.. code-block:: JSON
    {
        "my_table": "foo"
    }

The parameters become available in your SQL (example:SELECT * FROM {{ my_table }} ) by using Jinja templating syntax.
SQL Lab template parameters are stored with the dataset as TEMPLATE PARAMETERS.

There is a special ``_filters`` parameter which can be used to test filters used in the jinja template.

.. code-block:: JSON
    {
        "_filters": [ {
            "col": "action_type",
            "op": "IN",
            "val": ["sell", "buy"]
            } ]
    }

.. code-block:: python
    SELECT action, count(*) as times
            FROM logs
            WHERE
                action in ({{ "'" + "','".join(filter_values('action_type')) + "'" }})
            GROUP BY action

Note ``_filters`` is not stored with the dataset. It's only used within the SQL Lab UI.


Besides default Jinja templating, SQL lab also supports self-defined template
processor by setting the ``CUSTOM_TEMPLATE_PROCESSORS`` in your rabbitai configuration.
The values in this dictionary overwrite the default Jinja template processors of the
specified database engine.
The example below configures a custom presto template processor which implements
its own logic of processing macro template with regex parsing. It uses ``$`` style
macro instead of ``{{ }}`` style in Jinja templating. By configuring it with
``CUSTOM_TEMPLATE_PROCESSORS``, sql template on presto database is processed
by the custom one rather than the default one.

.. code-block:: python

    def DATE(
        ts: datetime, day_offset: SupportsInt = 0, hour_offset: SupportsInt = 0
    ) -> str:
        """Current day as a string."""
        day_offset, hour_offset = int(day_offset), int(hour_offset)
        offset_day = (ts + timedelta(days=day_offset, hours=hour_offset)).date()
        return str(offset_day)

    class CustomPrestoTemplateProcessor(PrestoTemplateProcessor):
        """A custom presto template processor."""

        engine = "presto"

        def process_template(self, sql: str, **kwargs) -> str:
            """Processes a sql template with $ style macro using regex."""
            # Add custom macros functions.
            macros = {
                "DATE": partial(DATE, datetime.utcnow())
            }  # type: Dict[str, Any]
            # Update with macros defined in context and kwargs.
            macros.update(self.context)
            macros.update(kwargs)

            def replacer(match):
                """Expand $ style macros with corresponding function calls."""
                macro_name, args_str = match.groups()
                args = [a.strip() for a in args_str.split(",")]
                if args == [""]:
                    args = []
                f = macros[macro_name[1:]]
                return f(*args)

            macro_names = ["$" + name for name in macros.keys()]
            pattern = r"(%s)\s*\(([^()]*)\)" % "|".join(map(re.escape, macro_names))
            return re.sub(pattern, replacer, sql)

    CUSTOM_TEMPLATE_PROCESSORS = {
        CustomPrestoTemplateProcessor.engine: CustomPrestoTemplateProcessor
    }


SQL Lab also includes a live query validation feature with pluggable backends.
You can configure which validation implementation is used with which database
engine by adding a block like the following to your config.py:

.. code-block:: python

     FEATURE_FLAGS = {
         'SQL_VALIDATORS_BY_ENGINE': {
             'presto': 'PrestoDBSQLValidator',
         }
     }

The available validators and names can be found in `sql_validators/`.

**Scheduling queries**

You can optionally allow your users to schedule queries directly in SQL Lab.
This is done by adding extra metadata to saved queries, which are then picked
up by an external scheduled (like [Apache Airflow](https://airflow.apache.org/)).

To allow scheduled queries, add the following to your `config.py`:

.. code-block:: python

    FEATURE_FLAGS = {
        # Configuration for scheduling queries from SQL Lab. This information is
        # collected when the user clicks "Schedule query", and saved into the `extra`
        # field of saved queries.
        # See: https://github.com/mozilla-services/react-jsonschema-form
        'SCHEDULED_QUERIES': {
            'JSONSCHEMA': {
                'title': 'Schedule',
                'description': (
                    'In order to schedule a query, you need to specify when it '
                    'should start running, when it should stop running, and how '
                    'often it should run. You can also optionally specify '
                    'dependencies that should be met before the query is '
                    'executed. Please read the documentation for best practices '
                    'and more information on how to specify dependencies.'
                ),
                'type': 'object',
                'properties': {
                    'output_table': {
                        'type': 'string',
                        'title': 'Output table name',
                    },
                    'start_date': {
                        'type': 'string',
                        'title': 'Start date',
                        # date-time is parsed using the chrono library, see
                        # https://www.npmjs.com/package/chrono-node#usage
                        'format': 'date-time',
                        'default': 'tomorrow at 9am',
                    },
                    'end_date': {
                        'type': 'string',
                        'title': 'End date',
                        # date-time is parsed using the chrono library, see
                        # https://www.npmjs.com/package/chrono-node#usage
                        'format': 'date-time',
                        'default': '9am in 30 days',
                    },
                    'schedule_interval': {
                        'type': 'string',
                        'title': 'Schedule interval',
                    },
                    'dependencies': {
                        'type': 'array',
                        'title': 'Dependencies',
                        'items': {
                            'type': 'string',
                        },
                    },
                },
            },
            'UISCHEMA': {
                'schedule_interval': {
                    'ui:placeholder': '@daily, @weekly, etc.',
                },
                'dependencies': {
                    'ui:help': (
                        'Check the documentation for the correct format when '
                        'defining dependencies.'
                    ),
                },
            },
            'VALIDATION': [
                # ensure that start_date <= end_date
                {
                    'name': 'less_equal',
                    'arguments': ['start_date', 'end_date'],
                    'message': 'End date cannot be before start date',
                    # this is where the error message is shown
                    'container': 'end_date',
                },
            ],
            # link to the scheduler; this example links to an Airflow pipeline
            # that uses the query id and the output table as its name
            'linkback': (
                'https://airflow.example.com/admin/airflow/tree?'
                'dag_id=query_${id}_${extra_json.schedule_info.output_table}'
            ),
        },
    }

This feature flag is based on [react-jsonschema-form](https://github.com/mozilla-services/react-jsonschema-form),
and will add a button called "Schedule Query" to SQL Lab. When the button is
clicked, a modal will show up where the user can add the metadata required for
scheduling the query.

This information can then be retrieved from the endpoint `/savedqueryviewapi/api/read`
and used to schedule the queries that have `scheduled_queries` in their JSON
metadata. For schedulers other than Airflow, additional fields can be easily
added to the configuration file above.

Celery Flower
-------------
Flower is a web based tool for monitoring the Celery cluster which you can
install from pip: ::

    pip install flower

and run via: ::

    celery flower --app=rabbitai.tasks.celery_app:app

Building from source
---------------------

More advanced users may want to build Rabbitai from sources. That
would be the case if you fork the project to add features specific to
your environment. See `CONTRIBUTING.md#setup-local-environment-for-development <https://github.com/apache/rabbitai/blob/master/CONTRIBUTING.md#setup-local-environment-for-development>`_.

Blueprints
----------

`Blueprints are Flask's reusable apps <https://flask.palletsprojects.com/en/1.0.x/tutorial/views/>`_.
Rabbitai allows you to specify an array of Blueprints
in your ``rabbitai_config`` module. Here's
an example of how this can work with a simple Blueprint. By doing
so, you can expect Rabbitai to serve a page that says "OK"
at the ``/simple_page`` url. This can allow you to run other things such
as custom data visualization applications alongside Rabbitai, on the
same server.

.. code-block:: python

    from flask import Blueprint
    simple_page = Blueprint('simple_page', __name__,
                                    template_folder='templates')
    @simple_page.route('/', defaults={'page': 'index'})
    @simple_page.route('/<page>')
    def show(page):
        return "Ok"

    BLUEPRINTS = [simple_page]

StatsD logging
--------------

Rabbitai is instrumented to log events to StatsD if desired. Most endpoints hit
are logged as well as key events like query start and end in SQL Lab.

To setup StatsD logging, it's a matter of configuring the logger in your
``rabbitai_config.py``.

.. code-block:: python

    from rabbitai.stats_logger import StatsdStatsLogger
    STATS_LOGGER = StatsdStatsLogger(host='localhost', port=8125, prefix='rabbitai')

Note that it's also possible to implement you own logger by deriving
``rabbitai.stats_logger.BaseStatsLogger``.


Install Rabbitai with helm in Kubernetes
----------------------------------------

You can install Rabbitai into Kubernetes with Helm <https://helm.sh/>. The chart is
located in the ``helm`` directory.

To install Rabbitai in your Kubernetes cluster with Helm 3, run:

.. code-block:: bash

    helm dep install ./helm/rabbitai
    helm upgrade --install rabbitai ./helm/rabbitai

Note that the above command will install Rabbitai into ``default`` namespace of your Kubernetes cluster.

Custom OAuth2 configuration
---------------------------

Beyond FAB supported providers (github, twitter, linkedin, google, azure), its easy to connect Rabbitai with other OAuth2 Authorization Server implementations that support "code" authorization.

The first step: Configure authorization in Rabbitai ``rabbitai_config.py``.

.. code-block:: python

    AUTH_TYPE = AUTH_OAUTH
    OAUTH_PROVIDERS = [
        {   'name':'egaSSO',
            'token_key':'access_token', # Name of the token in the response of access_token_url
            'icon':'fa-address-card',   # Icon for the provider
            'remote_app': {
                'client_id':'myClientId',  # Client Id (Identify Rabbitai application)
                'client_secret':'MySecret', # Secret for this Client Id (Identify Rabbitai application)
                'client_kwargs':{
                    'scope': 'read'               # Scope for the Authorization
                },
                'access_token_params':{        # Additional parameters for calls to access_token_url
                    'client_id':'myClientId'
                },
                'api_base_url':'https://myAuthorizationServer/oauth2AuthorizationServer/',
                'access_token_url':'https://myAuthorizationServer/oauth2AuthorizationServer/token',
                'authorize_url':'https://myAuthorizationServer/oauth2AuthorizationServer/authorize'
            }
        }
    ]

    # Will allow user self registration, allowing to create Flask users from Authorized User
    AUTH_USER_REGISTRATION = True

    # The default user self registration role
    AUTH_USER_REGISTRATION_ROLE = "Public"

Second step: Create a `CustomSsoSecurityManager` that extends `RabbitaiSecurityManager` and overrides `oauth_user_info`:

.. code-block:: python

    import logging
    from rabbitai.security import RabbitaiSecurityManager

    class CustomSsoSecurityManager(RabbitaiSecurityManager):

        def oauth_user_info(self, provider, response=None):
            logging.debug("Oauth2 provider: {0}.".format(provider))
            if provider == 'egaSSO':
                # As example, this line request a GET to base_url + '/' + userDetails with Bearer  Authentication,
        # and expects that authorization server checks the token, and response with user details
                me = self.appbuilder.sm.oauth_remotes[provider].get('userDetails').data
                logging.debug("user_data: {0}".format(me))
                return { 'name' : me['name'], 'email' : me['email'], 'id' : me['user_name'], 'username' : me['user_name'], 'first_name':'', 'last_name':''}
        ...

This file must be located at the same directory than ``rabbitai_config.py`` with the name ``custom_sso_security_manager.py``.

Then we can add this two lines to ``rabbitai_config.py``:

.. code-block:: python

  from custom_sso_security_manager import CustomSsoSecurityManager
  CUSTOM_SECURITY_MANAGER = CustomSsoSecurityManager

Feature Flags
-------------

Because of a wide variety of users, Rabbitai has some features that are not enabled by default. For example, some users have stronger security restrictions, while some others may not. So Rabbitai allow users to enable or disable some features by config. For feature owners, you can add optional functionalities in Rabbitai, but will be only affected by a subset of users.

You can enable or disable features with flag from ``rabbitai_config.py``:

.. code-block:: python

     FEATURE_FLAGS = {
         'CLIENT_CACHE': False,
         'ENABLE_EXPLORE_JSON_CSRF_PROTECTION': False,
         'PRESTO_EXPAND_DATA': False,
     }

A current list of feature flags can be found in `RESOURCES/FEATURE_FLAGS.md`


SIP-15
------

`SIP-15 <https://github.com/apache/rabbitai/issues/6360>`_ aims to ensure that time intervals are handled in a consistent and transparent manner for both the Druid and SQLAlchemy connectors.

Prior to SIP-15 SQLAlchemy used inclusive endpoints however these may behave like exclusive for string columns (due to lexicographical ordering) if no formatting was defined and the column formatting did not conform to an ISO 8601 date-time (refer to the SIP for details).

To remedy this rather than having to define the date/time format for every non-IS0 8601 date-time column, once can define a default column mapping on a per database level via the ``extra`` parameter ::

    {
        "python_date_format_by_column_name": {
            "ds": "%Y-%m-%d"
        }
    }

**New deployments**

All new Rabbitai deployments should enable SIP-15 via,

.. code-block:: python

    SIP_15_ENABLED = True

**Existing deployments**

Given that it is not apparent whether the chart creator was aware of the time range inconsistencies (and adjusted the endpoints accordingly) changing the behavior of all charts is overly aggressive. Instead SIP-15 proivides a soft transistion allowing producers (chart owners) to see the impact of the proposed change and adjust their charts accordingly.

Prior to enabling SIP-15 existing deployments should communicate to their users the impact of the change and define a grace period end date (exclusive of course) after which all charts will conform to the [start, end) interval, i.e.,

.. code-block:: python

    from dateime import date

    SIP_15_ENABLED = True
    SIP_15_GRACE_PERIOD_END = date(<YYYY>, <MM>, <DD>)

To aid with transparency the current endpoint behavior is explicitly called out in the chart time range (post SIP-15 this will be [start, end) for all connectors and databases). One can override the defaults on a per database level via the ``extra``
parameter ::

    {
        "time_range_endpoints": ["inclusive", "inclusive"]
    }


Note in a future release the interim SIP-15 logic will be removed (including the ``time_grain_endpoints`` form-data field) via a code change and Alembic migration.
