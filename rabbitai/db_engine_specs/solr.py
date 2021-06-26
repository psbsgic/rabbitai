from rabbitai.db_engine_specs.base import BaseEngineSpec


class SolrEngineSpec(BaseEngineSpec):  # pylint: disable=abstract-method
    """Engine spec for Apache Solr"""

    engine = "solr"
    engine_name = "Apache Solr"

    time_groupby_inline = False
    time_secondary_columns = False
    allows_joins = False
    allows_subqueries = False

    _time_grain_expressions = {
        None: "{col}",
    }
