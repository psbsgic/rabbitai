# Rabbitai 特性标志
这是当前 Rabbitai 可选特性的列表。有关默认值，请参见config.py。通过将rabbitai_config.py中的首选值分别设置为True/False，可以打开/关闭这些功能

## 在开发中
这些特性被视为**未完成**，应仅在开发环境中使用。

- CLIENT_CACHE
- DASHBOARD_CACHE
- DASHBOARD_NATIVE_FILTERS_SET
- DISABLE_DATASET_SOURCE_EDIT
- ENABLE_EXPLORE_JSON_CSRF_PROTECTION
- KV_STORE
- PRESTO_EXPAND_DATA
- REMOVE_SLICE_LEVEL_LABEL_COLORS
- SHARE_QUERIES_VIA_KV_STORE
- TAGGING_SYSTEM
- ENABLE_TEMPLATE_REMOVE_FILTERS

## 在测试中
这些特性已**完成**，但目前正在测试中。它们是可用的，但可能仍然包含一些bug。

- ALERT_REPORTS: [(docs)](https://rabbitai.sgic.net.cn/docs/installation/alerts-reports)
- DYNAMIC_PLUGINS: [(docs)](https://rabbitai.sgic.net.cn/docs/installation/running-on-kubernetes)
- DASHBOARD_NATIVE_FILTERS
- GLOBAL_ASYNC_QUERIES [(docs)](https://github.com/psbsgic/rabbitai/blob/master/CONTRIBUTING.md#async-chart-queries)
- OMNIBAR
- VERSIONED_EXPORT

## 稳定
这些特性标志为**安全生产**，并且已经过测试。

- DASHBOARD_CROSS_FILTERS
- DASHBOARD_RBAC [(docs)](https://rabbitai.sgic.net.cn/docs/creating-charts-dashboards/first-dashboard#manage-access-to-dashboards)
- ESCAPE_MARKDOWN_HTML
- ENABLE_TEMPLATE_PROCESSING
- LISTVIEWS_DEFAULT_CARD_VIEW
- ROW_LEVEL_SECURITY
- SCHEDULED_QUERIES [(docs)](https://rabbitai.sgic.net.cn/docs/installation/alerts-reports)
- SQL_VALIDATORS_BY_ENGINE [(docs)](https://rabbitai.sgic.net.cn/docs/installation/sql-templating)
- SQLLAB_BACKEND_PERSISTENCE
- THUMBNAILS [(docs)](https://rabbitai.sgic.net.cn/docs/installation/cache)

## 弃用标志
这些特性标志当前默认为True，**将在将来的主要版本**中删除。对于当前版本，您可以通过将配置设置为False来关闭它们，但建议删除本地配置中的这些标志或将其设置为**True**，以便在未来版本中不会遇到任何意外更改。

- ALLOW_DASHBOARD_DOMAIN_SHARDING
- DISPLAY_MARKDOWN_HTML
- ENABLE_REACT_CRUD_VIEWS
