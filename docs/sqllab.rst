SQL Lab
=======

SQLLab 是一个现代的、功能丰富的、用 `React <https://facebook.github.io/react/>`_ 开发的 SQL IDE。

------

.. image:: _static/images/screenshots/sqllab.png

------

功能概述
----------------
- 连接到几乎任何数据库后端
- 一次处理多个查询的多选项卡环境
- 使用Rabbitai丰富的可视化功能实现查询结果可视化的平滑流程
- 浏览数据库元数据：表、列、索引、分区
- 支持长时间运行的查询

  - 使用 `Celery 分布式队列 <http://www.celeryproject.org/>`_ 向 workers 分派查询处理
  - 支持定义一个 "结果后端(results backend)" 持久化查询结果

- 用于查找已执行查询的搜索引擎
- 支持使用
  `Jinja 模板语言 <http://jinja.pocoo.org/docs/dev/>`_
  模板机制，允许在SQL代码中使用宏

附加功能
--------------
- ``alt + enter`` 作为运行查询的快捷键

使用 Jinja 模板
---------------

.. code-block:: sql

    SELECT *
    FROM some_table
    WHERE partition_key = '{{ presto.first_latest_partition('some_table') }}'

模板化在SQL代码中释放了编程语言的强大功能。

模板还可用于编写参数化的通用查询，以便轻松重用。


可用宏
''''''''''''''''

我们在Rabbitai的Jinja上下文中公开Python标准库中的某些模块：

- ``time``: ``time``
- ``datetime``: ``datetime.datetime``
- ``uuid1``: ``uuid1``
- ``uuid3``: ``uuid3``
- ``uuid4``: ``uuid4``
- ``uuid5``: ``uuid5``
- ``random``: ``random``
- ``relativedelta``: ``dateutil.relativedelta.relativedelta``

`Jinja's 在建过滤器 <http://jinja.pocoo.org/docs/dev/templates/>`_ 也可以应用到需要的地方。

.. autoclass:: rabbitai.jinja_context.ExtraCache
    :members:

.. autofunction:: rabbitai.jinja_context.filter_values

.. autoclass:: rabbitai.jinja_context.PrestoTemplateProcessor
    :members:

.. autoclass:: rabbitai.jinja_context.HiveTemplateProcessor
    :members:

扩展宏
''''''''''''''''

如 `安装 & 配置 <https://rabbitai.apache.org/installation.html#sql-lab>`__ 文档所述，
管理员可以使用配置变量 ``JINJA_CONTEXT_ADDONS`` 在其环境中公开更多的宏。
此词典中引用的所有对象将可供用户在 **SQL Lab** 中集成到其查询中。

定制模板
''''''''''''''''''''

如 `安装 & 配置 <https://rabbitai.apache.org/installation.html#sql-lab>`__ 文档所述，

管理员可以使用配置变量 ``CUSTOM_TEMPLATE_PROCESSORS`` 使用自定义模板处理器覆盖Jinja模板。
字典中引用的模板处理器将覆盖指定的数据库引擎的默认的Jinja模板处理器。

查询成本估算
'''''''''''''''''''''

有些数据库支持 ``EXPLAIN`` 查询，允许用户在执行此查询之前估计查询的成本。
目前，SQL Lab支持Presto。要启用查询成本估算，请在数据库配置的 "Extra" 字段中添加以下键：

.. code-block:: text

    {
        "version": "0.319",
        "cost_estimate_enabled": true
        ...
    }

这里，"version" 应该是您的Presto集群的版本。Presto 0.319中引入了对该功能的支持。

您还需要在 `rabbitai_config.py` 中启用功能标志，并且可以选择指定自定义格式化程序。如：

.. code-block:: python

    def presto_query_cost_formatter(cost_estimate: List[Dict[str, float]]) -> List[Dict[str, str]]:
        """
        Format cost estimate returned by Presto.

        :param cost_estimate: JSON estimate from Presto
        :return: Human readable cost estimate
        """
        # Convert cost to dollars based on CPU and network cost. These coefficients are just
        # examples, they need to be estimated based on your infrastructure.
        cpu_coefficient = 2e-12
        network_coefficient = 1e-12

        cost = 0
        for row in cost_estimate:
            cost += row.get("cpuCost", 0) * cpu_coefficient
            cost += row.get("networkCost", 0) * network_coefficient

        return [{"Cost": f"US$ {cost:.2f}"}]


    FEATURE_FLAGS = {
        "ESTIMATE_QUERY_COST": True,
        "QUERY_COST_FORMATTERS_BY_ENGINE": {"presto": presto_query_cost_formatter},
    }

.. _ref_ctas_engine_config:

Create Table As (CTAS)
''''''''''''''''''''''

您可以在SQLLab上使用 ``CREATE TABLE AS SELECT ...`` 语句。可以在数据库配置级别打开和关闭此功能。

请注意，由于 ``CREATE TABLE..`` 属于SQL DDL类别。特别是在PostgreSQL上，DDL是事务性的，
这意味着要正确使用此功能，必须在引擎参数上将 ``autocommit`` 设置为true：

.. code-block:: text

    {
        ...
        "engine_params": {"isolation_level":"AUTOCOMMIT"},
        ...
    }
