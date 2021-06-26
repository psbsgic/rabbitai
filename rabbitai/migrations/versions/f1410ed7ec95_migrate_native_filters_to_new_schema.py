"""migrate native filters to new schema

Revision ID: f1410ed7ec95
Revises: d416d0d715cc
Create Date: 2021-04-29 15:32:21.939018

"""

# revision identifiers, used by Alembic.
revision = "f1410ed7ec95"
down_revision = "d416d0d715cc"

import json
from typing import Any, Dict, Iterable, Tuple

from alembic import op
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

from rabbitai import db

Base = declarative_base()


class Dashboard(Base):
    """Declarative class to do query in upgrade"""

    __tablename__ = "dashboards"
    id = Column(Integer, primary_key=True)
    json_metadata = Column(Text)


def upgrade_filters(native_filters: Iterable[Dict[str, Any]]) -> int:
    """
    Move `defaultValue` into `defaultDataMask.filterState`
    """
    changed_filters = 0
    for native_filter in native_filters:
        default_value = native_filter.pop("defaultValue", None)
        if default_value is not None:
            changed_filters += 1
            default_data_mask = {}
            default_data_mask["filterState"] = {"value": default_value}
            native_filter["defaultDataMask"] = default_data_mask
    return changed_filters


def downgrade_filters(native_filters: Iterable[Dict[str, Any]]) -> int:
    """
    Move `defaultDataMask.filterState` into `defaultValue`
    """
    changed_filters = 0
    for native_filter in native_filters:
        default_data_mask = native_filter.pop("defaultDataMask", {})
        filter_state = default_data_mask.get("filterState")
        if filter_state is not None:
            changed_filters += 1
            value = filter_state["value"]
            native_filter["defaultValue"] = value
    return changed_filters


def upgrade_dashboard(dashboard: Dict[str, Any]) -> Tuple[int, int]:
    changed_filters, changed_filter_sets = 0, 0
    # upgrade native select filter metadata
    # upgrade native select filter metadata
    native_filters = dashboard.get("native_filter_configuration")
    if native_filters:
        changed_filters += upgrade_filters(native_filters)

    # upgrade filter sets
    filter_sets = dashboard.get("filter_sets_configuration", [])
    for filter_set in filter_sets:
        if upgrade_filters(filter_set.get("nativeFilters", {}).values()):
            changed_filter_sets += 1
    return changed_filters, changed_filter_sets


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)

    dashboards = (
        session.query(Dashboard)
        .filter(Dashboard.json_metadata.like('%"native_filter_configuration"%'))
        .all()
    )
    changed_filters, changed_filter_sets = 0, 0
    for dashboard in dashboards:
        try:
            json_metadata = json.loads(dashboard.json_metadata)
            dashboard.json_metadata = json.dumps(json_metadata, sort_keys=True)

            upgrades = upgrade_dashboard(json_metadata)
            changed_filters += upgrades[0]
            changed_filter_sets += upgrades[1]
            dashboard.json_metadata = json.dumps(json_metadata, sort_keys=True)
        except Exception as e:
            print(f"Parsing json_metadata for dashboard {dashboard.id} failed.")
            raise e

    session.commit()
    session.close()
    print(f"Upgraded {changed_filters} filters and {changed_filter_sets} filter sets.")


def downgrade_dashboard(dashboard: Dict[str, Any]) -> Tuple[int, int]:
    changed_filters, changed_filter_sets = 0, 0
    # upgrade native select filter metadata
    native_filters = dashboard.get("native_filter_configuration")
    if native_filters:
        changed_filters += downgrade_filters(native_filters)

    # upgrade filter sets
    filter_sets = dashboard.get("filter_sets_configuration", [])
    for filter_set in filter_sets:
        if downgrade_filters(filter_set.get("nativeFilters", {}).values()):
            changed_filter_sets += 1
    return changed_filters, changed_filter_sets


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)

    dashboards = (
        session.query(Dashboard)
        .filter(Dashboard.json_metadata.like('%"native_filter_configuration"%'))
        .all()
    )
    changed_filters, changed_filter_sets = 0, 0
    for dashboard in dashboards:
        try:
            json_metadata = json.loads(dashboard.json_metadata)
            downgrades = downgrade_dashboard(json_metadata)
            changed_filters += downgrades[0]
            changed_filter_sets += downgrades[1]
            dashboard.json_metadata = json.dumps(json_metadata, sort_keys=True)
        except Exception as e:
            print(f"Parsing json_metadata for dashboard {dashboard.id} failed.")
            raise e

    session.commit()
    session.close()
    print(
        f"Downgraded {changed_filters} filters and {changed_filter_sets} filter sets."
    )
