from typing import Any, Dict, List, Optional

from rabbitai import app
from rabbitai.models.core import Database

custom_password_store = app.config["SQLALCHEMY_CUSTOM_PASSWORD_STORE"]


def get_foreign_keys_metadata(
    database: Database, table_name: str, schema_name: Optional[str]
) -> List[Dict[str, Any]]:
    """
    获取指定数据表的外键元数据。

    :param database: 数据库对象模型
    :param table_name: 数据表名称
    :param schema_name: 模式名称
    :return:
    """
    foreign_keys = database.get_foreign_keys(table_name, schema_name)
    for fk in foreign_keys:
        fk["column_names"] = fk.pop("constrained_columns")
        fk["type"] = "fk"
    return foreign_keys


def get_indexes_metadata(
    database: Database, table_name: str, schema_name: Optional[str]
) -> List[Dict[str, Any]]:
    """
    获取指定数据表的索引元数据。

    :param database: 数据库对象模型
    :param table_name: 数据表名称
    :param schema_name: 模式名称
    :return:
    """
    indexes = database.get_indexes(table_name, schema_name)
    for idx in indexes:
        idx["type"] = "index"
    return indexes


def get_col_type(col: Dict[Any, Any]) -> str:
    """
    获取列的数据类型。

    :param col:
    :return:
    """

    try:
        dtype = f"{col['type']}"
    except Exception:  # pylint: disable=broad-except
        # sqla.types.JSON __str__ has a bug, so using __class__.
        dtype = col["type"].__class__.__name__

    return dtype


def get_table_metadata(
    database: Database, table_name: str, schema_name: Optional[str]
) -> Dict[str, Any]:
    """
    获取数据表的元数据，包括 type, pk, fks等。
    当模式未找到时，触发 SQLAlchemyError。

    包括：

    - name
    - columns
    - selectStar
    - primaryKey
    - foreignKeys
    - indexes
    - comment

    :param database: 数据库对象模型
    :param table_name: 数据表名称
    :param schema_name: 模式名称

    :return: 已准备好进行API响应的表元数据字典。

    """

    keys = []
    columns = database.get_columns(table_name, schema_name)
    primary_key = database.get_pk_constraint(table_name, schema_name)
    if primary_key and primary_key.get("constrained_columns"):
        primary_key["column_names"] = primary_key.pop("constrained_columns")
        primary_key["type"] = "pk"
        keys += [primary_key]
    foreign_keys = get_foreign_keys_metadata(database, table_name, schema_name)
    indexes = get_indexes_metadata(database, table_name, schema_name)
    keys += foreign_keys + indexes
    payload_columns: List[Dict[str, Any]] = []
    table_comment = database.get_table_comment(table_name, schema_name)
    for col in columns:
        dtype = get_col_type(col)
        payload_columns.append(
            {
                "name": col["name"],
                "type": dtype.split("(")[0] if "(" in dtype else dtype,
                "longType": dtype,
                "keys": [k for k in keys if col["name"] in k["column_names"]],
                "comment": col.get("comment"),
            }
        )

    return {
        "name": table_name,
        "columns": payload_columns,
        "selectStar": database.select_star(
            table_name,
            schema=schema_name,
            show_cols=True,
            indent=True,
            cols=columns,
            latest_partition=True,
        ),
        "primaryKey": primary_key,
        "foreignKeys": foreign_keys,
        "indexes": keys,
        "comment": table_comment,
    }
