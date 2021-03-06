import json
import logging
from typing import Any, Callable, Dict, List, Optional

import yaml
from flask_appbuilder import Model
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import make_transient

from rabbitai import db
from rabbitai.commands.base import BaseCommand
from rabbitai.commands.importers.exceptions import IncorrectVersionError
from rabbitai.connectors.base.models import BaseColumn, BaseDatasource, BaseMetric
from rabbitai.connectors.druid.models import (
    DruidCluster,
    DruidColumn,
    DruidDatasource,
    DruidMetric,
)
from rabbitai.connectors.sqla.models import SqlaTable, SqlMetric, TableColumn
from rabbitai.databases.commands.exceptions import DatabaseNotFoundError
from rabbitai.models.core import Database
from rabbitai.utils.dict_import_export import DATABASES_KEY, DRUID_CLUSTERS_KEY

logger = logging.getLogger(__name__)


def lookup_sqla_table(table: SqlaTable) -> Optional[SqlaTable]:
    return (
        db.session.query(SqlaTable)
        .join(Database)
        .filter(
            SqlaTable.table_name == table.table_name,
            SqlaTable.schema == table.schema,
            Database.id == table.database_id,
        )
        .first()
    )


def lookup_sqla_database(table: SqlaTable) -> Optional[Database]:
    database = (
        db.session.query(Database)
        .filter_by(database_name=table.params_dict["database_name"])
        .one_or_none()
    )
    if database is None:
        raise DatabaseNotFoundError
    return database


def lookup_druid_cluster(datasource: DruidDatasource) -> Optional[DruidCluster]:
    return db.session.query(DruidCluster).filter_by(id=datasource.cluster_id).first()


def lookup_druid_datasource(datasource: DruidDatasource) -> Optional[DruidDatasource]:
    return (
        db.session.query(DruidDatasource)
        .filter(
            DruidDatasource.datasource_name == datasource.datasource_name,
            DruidDatasource.cluster_id == datasource.cluster_id,
        )
        .first()
    )


def import_dataset(
    i_datasource: BaseDatasource,
    database_id: Optional[int] = None,
    import_time: Optional[int] = None,
) -> int:
    """Imports the datasource from the object to the database.

    Metrics and columns and datasource will be overridden if exists.
    This function can be used to import/export dashboards between multiple
    rabbitai instances. Audit metadata isn't copied over.
    """

    lookup_database: Callable[[BaseDatasource], Optional[Database]]
    lookup_datasource: Callable[[BaseDatasource], Optional[BaseDatasource]]
    if isinstance(i_datasource, SqlaTable):
        lookup_database = lookup_sqla_database
        lookup_datasource = lookup_sqla_table
    else:
        lookup_database = lookup_druid_cluster
        lookup_datasource = lookup_druid_datasource

    return import_datasource(
        db.session,
        i_datasource,
        lookup_database,
        lookup_datasource,
        import_time,
        database_id,
    )


def lookup_sqla_metric(session: Session, metric: SqlMetric) -> SqlMetric:
    return (
        session.query(SqlMetric)
        .filter(
            SqlMetric.table_id == metric.table_id,
            SqlMetric.metric_name == metric.metric_name,
        )
        .first()
    )


def lookup_druid_metric(session: Session, metric: DruidMetric) -> DruidMetric:
    return (
        session.query(DruidMetric)
        .filter(
            DruidMetric.datasource_id == metric.datasource_id,
            DruidMetric.metric_name == metric.metric_name,
        )
        .first()
    )


def import_metric(session: Session, metric: BaseMetric) -> BaseMetric:
    if isinstance(metric, SqlMetric):
        lookup_metric = lookup_sqla_metric
    else:
        lookup_metric = lookup_druid_metric
    return import_simple_obj(session, metric, lookup_metric)


def lookup_sqla_column(session: Session, column: TableColumn) -> TableColumn:
    return (
        session.query(TableColumn)
        .filter(
            TableColumn.table_id == column.table_id,
            TableColumn.column_name == column.column_name,
        )
        .first()
    )


def lookup_druid_column(session: Session, column: DruidColumn) -> DruidColumn:
    return (
        session.query(DruidColumn)
        .filter(
            DruidColumn.datasource_id == column.datasource_id,
            DruidColumn.column_name == column.column_name,
        )
        .first()
    )


def import_column(session: Session, column: BaseColumn) -> BaseColumn:
    if isinstance(column, TableColumn):
        lookup_column = lookup_sqla_column
    else:
        lookup_column = lookup_druid_column
    return import_simple_obj(session, column, lookup_column)


def import_datasource(  # pylint: disable=too-many-arguments
    session: Session,
    i_datasource: Model,
    lookup_database: Callable[[Model], Optional[Model]],
    lookup_datasource: Callable[[Model], Optional[Model]],
    import_time: Optional[int] = None,
    database_id: Optional[int] = None,
) -> int:
    """Imports the datasource from the object to the database.

    Metrics and columns and datasource will be overrided if exists.
    This function can be used to import/export datasources between multiple
    rabbitai instances. Audit metadata isn't copies over.
    """
    make_transient(i_datasource)
    logger.info("Started import of the datasource: %s", i_datasource.to_json())

    i_datasource.id = None
    i_datasource.database_id = (
        database_id
        if database_id
        else getattr(lookup_database(i_datasource), "id", None)
    )
    i_datasource.alter_params(import_time=import_time)

    # override the datasource
    datasource = lookup_datasource(i_datasource)

    if datasource:
        datasource.override(i_datasource)
        session.flush()
    else:
        datasource = i_datasource.copy()
        session.add(datasource)
        session.flush()

    for metric in i_datasource.metrics:
        new_m = metric.copy()
        new_m.table_id = datasource.id
        logger.info(
            "Importing metric %s from the datasource: %s",
            new_m.to_json(),
            i_datasource.full_name,
        )
        imported_m = import_metric(session, new_m)
        if imported_m.metric_name not in [m.metric_name for m in datasource.metrics]:
            datasource.metrics.append(imported_m)

    for column in i_datasource.columns:
        new_c = column.copy()
        new_c.table_id = datasource.id
        logger.info(
            "Importing column %s from the datasource: %s",
            new_c.to_json(),
            i_datasource.full_name,
        )
        imported_c = import_column(session, new_c)
        if imported_c.column_name not in [c.column_name for c in datasource.columns]:
            datasource.columns.append(imported_c)
    session.flush()
    return datasource.id


def import_simple_obj(
    session: Session, i_obj: Model, lookup_obj: Callable[[Session, Model], Model]
) -> Model:
    make_transient(i_obj)
    i_obj.id = None
    i_obj.table = None

    # find if the column was already imported
    existing_column = lookup_obj(session, i_obj)
    i_obj.table = None
    if existing_column:
        existing_column.override(i_obj)
        session.flush()
        return existing_column

    session.add(i_obj)
    session.flush()
    return i_obj


def import_from_dict(
    session: Session, data: Dict[str, Any], sync: Optional[List[str]] = None
) -> None:
    """Imports databases and druid clusters from dictionary"""
    if not sync:
        sync = []
    if isinstance(data, dict):
        logger.info("Importing %d %s", len(data.get(DATABASES_KEY, [])), DATABASES_KEY)
        for database in data.get(DATABASES_KEY, []):
            Database.import_from_dict(session, database, sync=sync)

        logger.info(
            "Importing %d %s", len(data.get(DRUID_CLUSTERS_KEY, [])), DRUID_CLUSTERS_KEY
        )
        for datasource in data.get(DRUID_CLUSTERS_KEY, []):
            DruidCluster.import_from_dict(session, datasource, sync=sync)
        session.commit()
    else:
        logger.info("Supplied object is not a dictionary.")


class ImportDatasetsCommand(BaseCommand):
    """
    Import datasources in YAML format.

    This is the original unversioned format used to export and import datasources
    in Rabbitai.
    """

    # pylint: disable=unused-argument
    def __init__(
        self, contents: Dict[str, str], *args: Any, **kwargs: Any,
    ):
        self.contents = contents
        self._configs: Dict[str, Any] = {}

        self.sync = []
        if kwargs.get("sync_columns"):
            self.sync.append("columns")
        if kwargs.get("sync_metrics"):
            self.sync.append("metrics")

    def run(self) -> None:
        self.validate()

        # TODO (betodealmeida): add rollback in case of error
        for file_name, config in self._configs.items():
            logger.info("Importing dataset from file %s", file_name)
            if isinstance(config, dict):
                import_from_dict(db.session, config, sync=self.sync)
            else:  # list
                for dataset in config:
                    # UI exports don't have the database metadata, so we assume
                    # the DB exists and has the same name
                    params = json.loads(dataset["params"])
                    database = (
                        db.session.query(Database)
                        .filter_by(database_name=params["database_name"])
                        .one()
                    )
                    dataset["database_id"] = database.id
                    SqlaTable.import_from_dict(db.session, dataset, sync=self.sync)

    def validate(self) -> None:
        # ensure all files are YAML
        for file_name, content in self.contents.items():
            try:
                config = yaml.safe_load(content)
            except yaml.parser.ParserError:
                logger.exception("Invalid YAML file")
                raise IncorrectVersionError(f"{file_name} is not a valid YAML file")

            # CLI export
            if isinstance(config, dict):
                # TODO (betodealmeida): validate with Marshmallow
                if DATABASES_KEY not in config and DRUID_CLUSTERS_KEY not in config:
                    raise IncorrectVersionError(f"{file_name} has no valid keys")

            # UI export
            elif isinstance(config, list):
                # TODO (betodealmeida): validate with Marshmallow
                pass

            else:
                raise IncorrectVersionError(f"{file_name} is not a valid file")

            self._configs[file_name] = config
