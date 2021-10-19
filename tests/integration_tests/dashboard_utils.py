"""Utils to provide dashboards for tests"""

import json
from typing import Any, Dict, List, Optional

from pandas import DataFrame

from rabbitai import ConnectorRegistry, db
from rabbitai.connectors.sqla.models import SqlaTable
from rabbitai.models.core import Database
from rabbitai.models.dashboard import Dashboard
from rabbitai.models.slice import Slice


def create_table_for_dashboard(
    df: DataFrame,
    table_name: str,
    database: Database,
    dtype: Dict[str, Any],
    table_description: str = "",
    fetch_values_predicate: Optional[str] = None,
    schema: Optional[str] = None,
) -> SqlaTable:
    df.to_sql(
        table_name,
        database.get_sqla_engine(),
        if_exists="replace",
        chunksize=500,
        dtype=dtype,
        index=False,
        method="multi",
        schema=schema,
    )

    table_source = ConnectorRegistry.sources["table"]
    table = (
        db.session.query(table_source)
        .filter_by(database_id=database.id, schema=schema, table_name=table_name)
        .one_or_none()
    )
    if not table:
        table = table_source(schema=schema, table_name=table_name)
    if fetch_values_predicate:
        table.fetch_values_predicate = fetch_values_predicate
    table.database = database
    table.description = table_description
    db.session.merge(table)
    db.session.commit()

    return table


def create_slice(
    title: str, viz_type: str, table: SqlaTable, slices_dict: Dict[str, str]
) -> Slice:
    return Slice(
        slice_name=title,
        viz_type=viz_type,
        datasource_type="table",
        datasource_id=table.id,
        params=json.dumps(slices_dict, indent=4, sort_keys=True),
    )


def create_dashboard(
    slug: str, title: str, position: str, slices: List[Slice]
) -> Dashboard:
    dash = db.session.query(Dashboard).filter_by(slug=slug).one_or_none()

    if not dash:
        dash = Dashboard()
    dash.dashboard_title = title
    if position is not None:
        js = position
        pos = json.loads(js)
        dash.position_json = json.dumps(pos, indent=4)
    dash.slug = slug
    if slices is not None:
        dash.slices = slices
    db.session.merge(dash)
    db.session.commit()

    return dash
