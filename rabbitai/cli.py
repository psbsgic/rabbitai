#!/usr/bin/env python

import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from subprocess import Popen
from typing import Any, Dict, List, Optional, Type, Union
from zipfile import is_zipfile, ZipFile

import click
import yaml
from celery.utils.abstract import CallableTask
from colorama import Fore, Style
from flask import current_app, g
from flask.cli import FlaskGroup, with_appcontext
from flask_appbuilder import Model

from rabbitai import app, appbuilder, config, security_manager
from rabbitai.app import create_app
from rabbitai.extensions import celery_app, db
from rabbitai.utils import core as utils
from rabbitai.utils.celery import session_scope
from rabbitai.utils.urls import get_url_path

logger = logging.getLogger(__name__)

# region feature_flags

feature_flags = config.DEFAULT_FEATURE_FLAGS.copy()
feature_flags.update(config.FEATURE_FLAGS)
feature_flags_func = config.GET_FEATURE_FLAGS_FUNC
if feature_flags_func:
    # pylint: disable=not-callable
    try:
        feature_flags = feature_flags_func(feature_flags)
    except Exception:  # pylint: disable=broad-except
        # bypass any feature flags that depend on context
        # that's not available
        pass

# endregion


def normalize_token(token_name: str) -> str:
    """
    从 click >=7 开始，函数名中的下划线将替换为破折号。
    为了避免重命名所有cli函数（例如，将 load_examples 重命名为 load-examples），
    此函数用于将下划线替换为破折号。

    :param token_name: 名称可能包含破折号。
    :return: 用下划线替换为破折号的名称
    """

    return token_name.replace("_", "-")


@click.group(
    cls=FlaskGroup,
    create_app=create_app,
    context_settings={"token_normalize_func": normalize_token},
)
@with_appcontext
def rabbitai() -> None:
    """构建 RabbitAI 应用命令行环境，管理在应用上下文和外壳上下文（提供应用对象和数据库对象）执行脚本。"""

    @app.shell_context_processor
    def make_shell_context() -> Dict[str, Any]:
        return dict(app=app, db=db)


@rabbitai.command()
@with_appcontext
def init() -> None:
    """初始化 RabbitAI 应用，添加权限到应用构建者，同步安全管理器角色定义。"""

    appbuilder.add_permissions(update_perms=True)
    security_manager.sync_role_definitions()


@rabbitai.command()
@with_appcontext
@click.option("--verbose", "-v", is_flag=True, help="该命令的帮助信息")
def version(verbose: bool) -> None:
    """打印输出当前版本信息。"""

    print(Fore.BLUE + "-=" * 15)
    print(
        Fore.YELLOW
        + "RabbitAI "
        + Fore.CYAN
        + "{version}".format(version=app.config["VERSION_STRING"])
    )
    print(Fore.BLUE + "-=" * 15)
    if verbose:
        print("[DB] : " + "{}".format(db.engine))
    print(Style.RESET_ALL)


def load_examples_run(
    load_test_data: bool = False,
    load_big_data: bool = False,
    only_metadata: bool = False,
    force: bool = False,
) -> None:
    """
    加载示例及其数据到数据库。

    :param load_test_data: 是否加载测试数据。
    :param load_big_data: 是否加载大数据。
    :param only_metadata: 是否仅加载元数据。
    :param force: 是否强制。
    :return:
    """

    if only_metadata:
        print("Loading examples metadata")
    else:
        examples_db = utils.get_example_database()
        print(f"Loading examples metadata and related data into {examples_db}")

    from rabbitai import examples

    examples.load_css_templates()

    if load_test_data:
        print("Loading energy related dataset")
        examples.load_energy(only_metadata, force)

    print("Loading [World Bank's Health Nutrition and Population Stats]")
    examples.load_world_bank_health_n_pop(only_metadata, force)

    print("Loading [Birth names]")
    examples.load_birth_names(only_metadata, force)

    if load_test_data:
        print("Loading [Tabbed dashboard]")
        examples.load_tabbed_dashboard(only_metadata)

    if not load_test_data:
        print("Loading [Random long/lat data]")
        examples.load_long_lat_data(only_metadata, force)

        print("Loading [Country Map data]")
        examples.load_country_map_data(only_metadata, force)

        print("Loading [San Francisco population polygons]")
        examples.load_sf_population_polygons(only_metadata, force)

        print("Loading [Flights data]")
        examples.load_flights(only_metadata, force)

        print("Loading [BART lines]")
        examples.load_bart_lines(only_metadata, force)

        print("Loading [Multi Line]")
        examples.load_multi_line(only_metadata)

        print("Loading [Misc Charts] dashboard")
        examples.load_misc_dashboard()

        print("Loading DECK.gl demo")
        examples.load_deck_dash()

    if load_big_data:
        print("Loading big synthetic data for tests")
        examples.load_big_data()

    # 加载以 YAML 配置文件格式存储的示例
    examples.load_from_configs(force, load_test_data)


@with_appcontext
@rabbitai.command()
@click.option("--load-test-data", "-t", is_flag=True, help="是否加载附加的测试数据")
@click.option("--load-big-data", "-b", is_flag=True, help="是否加载附加大数据")
@click.option("--only-metadata", "-m", is_flag=True, help="仅加载元数据，跳过实际数据")
@click.option("--force", "-f", is_flag=True, help="即使数据表存在也要强制加载数据到示例数据库")
def load_examples(
    load_test_data: bool,
    load_big_data: bool,
    only_metadata: bool = False,
    force: bool = False,
) -> None:
    """
    加载一组切片、仪表板和支持数据集。

    :param load_test_data: 是否加载测试数据。
    :param load_big_data: 是否加载大表数据。
    :param only_metadata: 是否仅加载元数据，默认False。
    :param force: 是否强制，默认False。
    :return:
    """
    load_examples_run(load_test_data, load_big_data, only_metadata, force)


@with_appcontext
@rabbitai.command()
@click.option("--database_name", "-d", help="要更改的数据库名称")
@click.option("--uri", "-u", help="要更改的数据库地址")
@click.option(
    "--skip_create",
    "-s",
    is_flag=True,
    default=False,
    help="如果数据库不存在是否创建",
)
def set_database_uri(database_name: str, uri: str, skip_create: bool) -> None:
    """
    更新数据库连接URI。

    :param database_name: 数据库名称。
    :param uri: 地址字符串。
    :param skip_create: 是否跳过创建操作。
    :return:
    """

    utils.get_or_create_db(database_name, uri, not skip_create)


@rabbitai.command()
@with_appcontext
@click.option(
    "--datasource",
    "-d",
    help="指定要加载数据源的名称，如果省略则刷新所有数据源",
)
@click.option(
    "--merge",
    "-m",
    is_flag=True,
    default=False,
    help="指定在操作时使用的 'merge' 属性，默认为 False。",
)
def refresh_druid(datasource: str, merge: bool) -> None:
    """
    刷新druid数据源。

    :param datasource: 数据源名称。
    :param merge: 是否合并。
    :return:
    """

    session = db.session()
    from rabbitai.connectors.druid.models import DruidCluster

    for cluster in session.query(DruidCluster).all():
        try:
            cluster.refresh_datasources(datasource_name=datasource, merge_flag=merge)
        except Exception as ex:  # pylint: disable=broad-except
            print("Error while processing cluster '{}'\n{}".format(cluster, str(ex)))
            logger.exception(ex)
        cluster.metadata_last_refreshed = datetime.now()
        print("Refreshed metadata from cluster " "[" + cluster.cluster_name + "]")

    session.commit()


if feature_flags.get("VERSIONED_EXPORT"):

    @rabbitai.command()
    @with_appcontext
    @click.option(
        "--dashboard-file", "-f", help="指定存储导出结果的文件",
    )
    def export_dashboards(dashboard_file: Optional[str] = None) -> None:
        """
        导出仪表盘到 ZIP 文件。

        :param dashboard_file: ZIP 文件。
        :return:
        """

        from rabbitai.dashboards.commands.export import ExportDashboardsCommand
        from rabbitai.models.dashboard import Dashboard

        g.user = security_manager.find_user(username="admin")

        dashboard_ids = [id_ for (id_,) in db.session.query(Dashboard.id).all()]
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        root = f"dashboard_export_{timestamp}"
        dashboard_file = dashboard_file or f"{root}.zip"

        try:
            with ZipFile(dashboard_file, "w") as bundle:
                for file_name, file_content in ExportDashboardsCommand(
                    dashboard_ids
                ).run():
                    with bundle.open(f"{root}/{file_name}", "w") as fp:
                        fp.write(file_content.encode())
        except Exception:  # pylint: disable=broad-except
            logger.exception(
                "There was an error when exporting the dashboards, please check "
                "the exception traceback in the log"
            )

    # pylint: disable=too-many-locals
    @rabbitai.command()
    @with_appcontext
    @click.option(
        "--datasource-file", "-f", help="指定存储导出结果的文件",
    )
    def export_datasources(datasource_file: Optional[str] = None) -> None:
        """
        导出数据源到 ZIP 文件。

        :param datasource_file:
        :return:
        """

        from rabbitai.connectors.sqla.models import SqlaTable
        from rabbitai.datasets.commands.export import ExportDatasetsCommand

        g.user = security_manager.find_user(username="admin")

        dataset_ids = [id_ for (id_,) in db.session.query(SqlaTable.id).all()]
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        root = f"dataset_export_{timestamp}"
        datasource_file = datasource_file or f"{root}.zip"

        try:
            with ZipFile(datasource_file, "w") as bundle:
                for file_name, file_content in ExportDatasetsCommand(dataset_ids).run():
                    with bundle.open(f"{root}/{file_name}", "w") as fp:
                        fp.write(file_content.encode())
        except Exception:
            logger.exception(
                "There was an error when exporting the datasets, please check "
                "the exception traceback in the log"
            )

    @rabbitai.command()
    @with_appcontext
    @click.option(
        "--path", "-p", help="ZIP 文件路径",
    )
    @click.option(
        "--username",
        "-u",
        default=None,
        help="指定该仪表盘要分配给那个用户",
    )
    def import_dashboards(path: str, username: Optional[str]) -> None:
        """
        从ZIP文件导入仪表盘。

        :param path:
        :param username:
        :return:
        """

        from rabbitai.commands.importers.v1.utils import get_contents_from_bundle
        from rabbitai.dashboards.commands.importers.dispatcher import (
            ImportDashboardsCommand,
        )

        if username is not None:
            g.user = security_manager.find_user(username=username)
        if is_zipfile(path):
            with ZipFile(path) as bundle:
                contents = get_contents_from_bundle(bundle)
        else:
            contents = {path: open(path).read()}
        try:
            ImportDashboardsCommand(contents, overwrite=True).run()
        except Exception:  # pylint: disable=broad-except
            logger.exception(
                "There was an error when importing the dashboards(s), please check "
                "the exception traceback in the log"
            )

    @rabbitai.command()
    @with_appcontext
    @click.option(
        "--path", "-p", help="ZIP 文件路径",
    )
    def import_datasources(path: str) -> None:
        """
        从 ZIP 文件导入数据源。

        :param path: 文件路径。
        :return:
        """

        from rabbitai.commands.importers.v1.utils import get_contents_from_bundle
        from rabbitai.datasets.commands.importers.dispatcher import (
            ImportDatasetsCommand,
        )

        if is_zipfile(path):
            with ZipFile(path) as bundle:
                contents = get_contents_from_bundle(bundle)
        else:
            contents = {path: open(path).read()}
        try:
            ImportDatasetsCommand(contents, overwrite=True).run()
        except Exception:
            logger.exception(
                "There was an error when importing the dataset(s), please check the "
                "exception traceback in the log"
            )


else:

    @rabbitai.command()
    @with_appcontext
    @click.option(
        "--dashboard-file", "-f", default=None, help="指定存储导出结果的文件"
    )
    @click.option(
        "--print_stdout",
        "-p",
        is_flag=True,
        default=False,
        help="Print JSON to stdout",
    )
    def export_dashboards(
        dashboard_file: Optional[str], print_stdout: bool = False
    ) -> None:
        """
        导出所有仪表盘为 JSON 文件。

        :param dashboard_file: 仪表盘文件。
        :param print_stdout: 是否输出到标准输出，默认False。
        :return:
        """

        from rabbitai.utils import dashboard_import_export

        data = dashboard_import_export.export_dashboards(db.session)
        if print_stdout or not dashboard_file:
            print(data)
        if dashboard_file:
            logger.info("Exporting dashboards to %s", dashboard_file)
            with open(dashboard_file, "w") as data_stream:
                data_stream.write(data)

    # pylint: disable=too-many-locals
    @rabbitai.command()
    @with_appcontext
    @click.option(
        "--datasource-file",
        "-f",
        default=None,
        help="指定存储导出结果的文件",
    )
    @click.option(
        "--print_stdout",
        "-p",
        is_flag=True,
        default=False,
        help="Print YAML to stdout",
    )
    @click.option(
        "--back-references",
        "-b",
        is_flag=True,
        default=False,
        help="Include parent back references",
    )
    @click.option(
        "--include-defaults",
        "-d",
        is_flag=True,
        default=False,
        help="Include fields containing defaults",
    )
    def export_datasources(
        datasource_file: Optional[str],
        print_stdout: bool = False,
        back_references: bool = False,
        include_defaults: bool = False,
    ) -> None:
        """
        导出数据源为 YAML 文件。

        :param datasource_file: YAML 文件。
        :param print_stdout:
        :param back_references:
        :param include_defaults:
        :return:
        """

        from rabbitai.utils import dict_import_export

        data = dict_import_export.export_to_dict(
            session=db.session,
            recursive=True,
            back_references=back_references,
            include_defaults=include_defaults,
        )
        if print_stdout or not datasource_file:
            yaml.safe_dump(data, sys.stdout, default_flow_style=False)
        if datasource_file:
            logger.info("Exporting datasources to %s", datasource_file)
            with open(datasource_file, "w") as data_stream:
                yaml.safe_dump(data, data_stream, default_flow_style=False)

    @rabbitai.command()
    @with_appcontext
    @click.option(
        "--path",
        "-p",
        help="Path to a single JSON file or path containing multiple JSON "
        "files to import (*.json)",
    )
    @click.option(
        "--recursive",
        "-r",
        is_flag=True,
        default=False,
        help="recursively search the path for json files",
    )
    @click.option(
        "--username",
        "-u",
        default=None,
        help="Specify the user name to assign dashboards to",
    )
    def import_dashboards(path: str, recursive: bool, username: str) -> None:
        """
        从指定 JSON 文件导入仪表盘。

        :param path:
        :param recursive:
        :param username:
        :return:
        """

        from rabbitai.dashboards.commands.importers.v0 import ImportDashboardsCommand

        path_object = Path(path)
        files: List[Path] = []
        if path_object.is_file():
            files.append(path_object)
        elif path_object.exists() and not recursive:
            files.extend(path_object.glob("*.json"))
        elif path_object.exists() and recursive:
            files.extend(path_object.rglob("*.json"))
        if username is not None:
            g.user = security_manager.find_user(username=username)
        contents = {path.name: open(path).read() for path in files}
        try:
            ImportDashboardsCommand(contents).run()
        except Exception:  # pylint: disable=broad-except
            logger.exception("Error when importing dashboard")

    @rabbitai.command()
    @with_appcontext
    @click.option(
        "--path",
        "-p",
        help="Path to a single YAML file or path containing multiple YAML "
        "files to import (*.yaml or *.yml)",
    )
    @click.option(
        "--sync",
        "-s",
        "sync",
        default="",
        help="comma seperated list of element types to synchronize "
        'e.g. "metrics,columns" deletes metrics and columns in the DB '
        "that are not specified in the YAML file",
    )
    @click.option(
        "--recursive",
        "-r",
        is_flag=True,
        default=False,
        help="recursively search the path for yaml files",
    )
    def import_datasources(path: str, sync: str, recursive: bool) -> None:
        """
        从指定路径下的 YAML 文件导入数据源。

        :param path: 路径。
        :param sync: 同步，columns，metrics
        :param recursive: 是否迭代。
        :return:
        """

        from rabbitai.datasets.commands.importers.v0 import ImportDatasetsCommand

        sync_array = sync.split(",")
        sync_columns = "columns" in sync_array
        sync_metrics = "metrics" in sync_array

        path_object = Path(path)
        files: List[Path] = []
        if path_object.is_file():
            files.append(path_object)
        elif path_object.exists() and not recursive:
            files.extend(path_object.glob("*.yaml"))
            files.extend(path_object.glob("*.yml"))
        elif path_object.exists() and recursive:
            files.extend(path_object.rglob("*.yaml"))
            files.extend(path_object.rglob("*.yml"))
        contents = {path.name: open(path).read() for path in files}
        try:
            ImportDatasetsCommand(contents, sync_columns, sync_metrics).run()
        except Exception:  # pylint: disable=broad-except
            logger.exception("Error when importing dataset")

    @rabbitai.command()
    @with_appcontext
    @click.option(
        "--back-references",
        "-b",
        is_flag=True,
        default=False,
        help="Include parent back references",
    )
    def export_datasource_schema(back_references: bool) -> None:
        """
        Export datasource YAML schema to stdout

        :param back_references:
        :return:
        """
        from rabbitai.utils import dict_import_export

        data = dict_import_export.export_schema_to_dict(back_references=back_references)
        yaml.safe_dump(data, sys.stdout, default_flow_style=False)


@rabbitai.command()
@with_appcontext
def update_datasources_cache() -> None:
    """Refresh sqllab datasources cache"""

    from rabbitai.models.core import Database

    for database in db.session.query(Database).all():
        if database.allow_multi_schema_metadata_fetch:
            print("Fetching {} datasources ...".format(database.name))
            try:
                database.get_all_table_names_in_database(
                    force=True, cache=True, cache_timeout=24 * 60 * 60
                )
                database.get_all_view_names_in_database(
                    force=True, cache=True, cache_timeout=24 * 60 * 60
                )
            except Exception as ex:  # pylint: disable=broad-except
                print("{}".format(str(ex)))


@rabbitai.command()
@with_appcontext
@click.option(
    "--workers", "-w", type=int, help="Number of celery server workers to fire up"
)
def worker(workers: int) -> None:
    """Starts a RabbitAI worker for async SQL query execution."""
    logger.info(
        "The 'rabbitai worker' command is deprecated. Please use the 'celery "
        "worker' command instead."
    )
    if workers:
        celery_app.conf.update(CELERYD_CONCURRENCY=workers)
    elif app.config["RABBITAI_CELERY_WORKERS"]:
        celery_app.conf.update(
            CELERYD_CONCURRENCY=app.config["RABBITAI_CELERY_WORKERS"]
        )

    local_worker = celery_app.Worker(optimization="fair")
    local_worker.start()


@rabbitai.command()
@with_appcontext
@click.option(
    "-p", "--port", default="5555", help="Port on which to start the Flower process"
)
@click.option(
    "-a", "--address", default="localhost", help="Address on which to run the service"
)
def flower(port: int, address: str) -> None:
    """
    Runs a Celery Flower web server

    Celery Flower is a UI to monitor the Celery operation on a given broker
    """

    broker_url = celery_app.conf.BROKER_URL
    cmd = (
        "celery flower "
        f"--broker={broker_url} "
        f"--port={port} "
        f"--address={address} "
    )
    logger.info(
        "The 'rabbitai flower' command is deprecated. Please use the 'celery "
        "flower' command instead."
    )
    print(Fore.GREEN + "Starting a Celery Flower instance")
    print(Fore.BLUE + "-=" * 40)
    print(Fore.YELLOW + cmd)
    print(Fore.BLUE + "-=" * 40)
    Popen(cmd, shell=True).wait()


@rabbitai.command()
@with_appcontext
@click.option(
    "--asynchronous",
    "-a",
    is_flag=True,
    default=False,
    help="Trigger commands to run remotely on a worker",
)
@click.option(
    "--dashboards_only",
    "-d",
    is_flag=True,
    default=False,
    help="Only process dashboards",
)
@click.option(
    "--charts_only", "-c", is_flag=True, default=False, help="Only process charts"
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Force refresh, even if previously cached",
)
@click.option("--model_id", "-i", multiple=True)
def compute_thumbnails(
    asynchronous: bool,
    dashboards_only: bool,
    charts_only: bool,
    force: bool,
    model_id: int,
) -> None:
    """
    计算缩略图。

    :param asynchronous:
    :param dashboards_only:
    :param charts_only:
    :param force:
    :param model_id:
    :return:
    """

    from rabbitai.models.dashboard import Dashboard
    from rabbitai.models.slice import Slice
    from rabbitai.tasks.thumbnails import (
        cache_chart_thumbnail,
        cache_dashboard_thumbnail,
    )

    def compute_generic_thumbnail(
        friendly_type: str,
        model_cls: Union[Type[Dashboard], Type[Slice]],
        model_id: int,
        compute_func: CallableTask,
    ) -> None:
        query = db.session.query(model_cls)
        if model_id:
            query = query.filter(model_cls.id.in_(model_id))
        dashboards = query.all()
        count = len(dashboards)
        for i, model in enumerate(dashboards):
            if asynchronous:
                func = compute_func.delay
                action = "Triggering"
            else:
                func = compute_func
                action = "Processing"

            msg = f'{action} {friendly_type} "{model}" ({i+1}/{count})'
            click.secho(msg, fg="green")
            if friendly_type == "chart":
                url = get_url_path(
                    "Rabbitai.slice", slice_id=model.id, standalone="true"
                )
            else:
                url = get_url_path("Rabbitai.dashboard", dashboard_id_or_slug=model.id)

            func(url, model.digest, force=force)

    if not charts_only:
        compute_generic_thumbnail("dashboard", Dashboard, model_id, cache_dashboard_thumbnail)
    if not dashboards_only:
        compute_generic_thumbnail("chart", Slice, model_id, cache_chart_thumbnail)


@rabbitai.command()
@with_appcontext
def load_test_users() -> None:
    """
    Loads admin, alpha, and gamma user for testing purposes

    Syncs permissions for those users/roles
    """
    print(Fore.GREEN + "Loading a set of users for unit tests")
    load_test_users_run()


def load_test_users_run() -> None:
    """
    Loads admin, alpha, and gamma user for testing purposes

    Syncs permissions for those users/roles
    """
    if app.config["TESTING"]:

        sm = security_manager

        examples_db = utils.get_example_database()

        examples_pv = sm.add_permission_view_menu("database_access", examples_db.perm)

        sm.sync_role_definitions()
        gamma_sqllab_role = sm.add_role("gamma_sqllab")
        sm.add_permission_role(gamma_sqllab_role, examples_pv)

        gamma_no_csv_role = sm.add_role("gamma_no_csv")
        sm.add_permission_role(gamma_no_csv_role, examples_pv)

        for role in ["Gamma", "sql_lab"]:
            for perm in sm.find_role(role).permissions:
                sm.add_permission_role(gamma_sqllab_role, perm)

                if str(perm) != "can csv on Rabbitai":
                    sm.add_permission_role(gamma_no_csv_role, perm)

        users = (
            ("admin", "Admin"),
            ("gamma", "Gamma"),
            ("gamma2", "Gamma"),
            ("gamma_sqllab", "gamma_sqllab"),
            ("alpha", "Alpha"),
            ("gamma_no_csv", "gamma_no_csv"),
        )
        for username, role in users:
            user = sm.find_user(username)
            if not user:
                sm.add_user(
                    username,
                    username,
                    "user",
                    username + "@fab.org",
                    sm.find_role(role),
                    password="general",
                )
        sm.get_session.commit()


@rabbitai.command()
@with_appcontext
def sync_tags() -> None:
    """Rebuilds special tags (owner, type, favorited by)."""
    # pylint: disable=no-member
    metadata = Model.metadata

    from rabbitai.common.tags import add_favorites, add_owners, add_types

    add_types(db.engine, metadata)
    add_owners(db.engine, metadata)
    add_favorites(db.engine, metadata)


@rabbitai.command()
@with_appcontext
def alert() -> None:
    """Run the alert scheduler loop"""

    # this command is just for testing purposes
    from rabbitai.models.schedules import ScheduleType
    from rabbitai.tasks.schedules import schedule_window

    click.secho("Processing one alert loop", fg="green")
    with session_scope(nullpool=True) as session:
        schedule_window(
            report_type=ScheduleType.alert,
            start_at=datetime.now() - timedelta(1000),
            stop_at=datetime.now(),
            resolution=6000,
            session=session,
        )


@rabbitai.command()
@with_appcontext
def update_api_docs() -> None:
    """Regenerate the openapi.json file in docs"""

    from apispec import APISpec
    from apispec.ext.marshmallow import MarshmallowPlugin
    from flask_appbuilder.api import BaseApi
    from os import path

    rabbitai_dir = path.abspath(path.dirname(__file__))
    openapi_json = path.join(
        rabbitai_dir, "..", "docs", "src", "resources", "openapi.json"
    )
    api_version = "v1"

    version_found = False
    api_spec = APISpec(
        title=current_app.appbuilder.app_name,
        version=api_version,
        openapi_version="3.0.2",
        info=dict(description=current_app.appbuilder.app_name),
        plugins=[MarshmallowPlugin()],
        servers=[{"url": "/api/{}".format(api_version)}],
    )
    for base_api in current_app.appbuilder.baseviews:
        if isinstance(base_api, BaseApi) and base_api.version == api_version:
            base_api.add_api_spec(api_spec)
            version_found = True
    if version_found:
        click.secho("Generating openapi.json", fg="green")
        with open(openapi_json, "w", encoding="utf-8") as outfile:
            json.dump(api_spec.to_dict(), outfile, sort_keys=True, indent=2)
    else:
        click.secho("API version not found", err=True)
