# Rabbitai 功能
这是当前Rabbitai可选功能的列表。有关默认值，请参见config.py。通过将rabbitai_config.py中的首选值分别设置为True/False，可以打开/关闭这些功能。

## 开发中
这些特性被认为是**未完成的**，只能在开发环境中使用。

- CLIENT_CACHE
- DASHBOARD_CACHE
- DASHBOARD_NATIVE_FILTERS_SET
- DASHBOARD_RBAC
- DISABLE_DATASET_SOURCE_EDIT
- ENABLE_EXPLORE_JSON_CSRF_PROTECTION
- KV_STORE
- PRESTO_EXPAND_DATA
- REMOVE_SLICE_LEVEL_LABEL_COLORS
- SHARE_QUERIES_VIA_KV_STORE
- TAGGING_SYSTEM
- ENABLE_TEMPLATE_REMOVE_FILTERS

## 测试中
这些功能已**完成**，但目前正在测试中。它们是可用的，但仍可能包含一些bug。

- ALERT_REPORTS: [(docs)](https://github.com/pengsongbo2016/rabbitai/docs/installation/alerts-reports)
- DYNAMIC_PLUGINS: [(docs)](https://github.com/pengsongbo2016/rabbitai/docs/installation/running-on-kubernetes)
- DASHBOARD_NATIVE_FILTERS
- GLOBAL_ASYNC_QUERIES [(docs)](https://github.com/pengsongbo2016/rabbitai/blob/master/CONTRIBUTING.md#async-chart-queries)
- OMNIBAR
- VERSIONED_EXPORT

## 稳定
这些功能标志是**安全文档的**，并且已经过测试。

- DASHBOARD_CROSS_FILTERS
- ESCAPE_MARKDOWN_HTML
- ENABLE_TEMPLATE_PROCESSING
- LISTVIEWS_DEFAULT_CARD_VIEW
- ROW_LEVEL_SECURITY
- SCHEDULED_QUERIES [(docs)](https://github.com/pengsongbo2016/rabbitai/docs/installation/alerts-reports)
- SQL_VALIDATORS_BY_ENGINE [(docs)](https://github.com/pengsongbo2016/rabbitai/docs/installation/sql-templating)
- SQLLAB_BACKEND_PERSISTENCE
- THUMBNAILS [(docs)](https://github.com/pengsongbo2016/rabbitai/docs/installation/cache)
