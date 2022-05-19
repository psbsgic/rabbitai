# -*- coding: utf-8 -*-

"""Loads datasets, dashboards and slices in a new rabbitai instance"""

import json
import os
import zlib
import io
from io import BytesIO
from typing import Any, Dict, List, Set
from urllib import request

from rabbitai import app, db
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.models import core as models
from rabbitai.models.slice import Slice

BASE_URL = "https://github.com/apache-superset/examples-data/blob/master/"
"""示例数据基地址

https://github.com/apache-superset/examples-data/blob/master/bart-lines.json.gz?raw=true
https://github.com/apache-superset/examples-data/blob/master/birth_names2.json.gz?raw=true
https://github.com/apache-superset/examples-data/blob/master/birth_france_data_for_country_map.csv?raw=true
https://github.com/apache-superset/examples-data/blob/master/energy.json.gz?raw=true
https://github.com/apache-superset/examples-data/blob/master/flight_data.csv.gz?raw=true
https://github.com/apache-superset/examples-data/blob/master/san_francisco.csv.gz?raw=true
https://github.com/apache-superset/examples-data/blob/master/multiformat_time_series.json.gz?raw=true
https://github.com/apache-superset/examples-data/blob/master/paris_iris.json.gz?raw=true
https://github.com/apache-superset/examples-data/blob/master/random_time_series.json.gz?raw=true
https://github.com/apache-superset/examples-data/blob/master/sf_population.json.gz?raw=true
https://github.com/apache-superset/examples-data/blob/master/countries.json.gz?raw=true

"""

DB = models.Database
"""数据库对象关系模型"""

TBL = ConnectorRegistry.sources["table"]
"""数据表类型数据源"""

config = app.config
"""应用配置对象"""

EXAMPLES_FOLDER = os.path.join(config["BASE_DIR"], "examples")
"""示例文件夹"""

misc_dash_slices: Set[str] = set()  # slices assembled in a 'Misc Chart' dashboard


def get_table_connector_registry() -> Any:
    """获取数据表类型数据源。"""
    return ConnectorRegistry.sources["table"]


def get_examples_folder() -> str:
    """获取示例文件夹。"""
    return os.path.join(app.config["BASE_DIR"], "examples")


def update_slice_ids(layout_dict: Dict[Any, Any], slices: List[Slice]) -> None:
    """
    更新图表的标识为切片的标识。

    :param layout_dict: 布局字典。
    :param slices: 切片的列表。
    :return:
    """

    charts = [
        component
        for component in layout_dict.values()
        if isinstance(component, dict) and component["type"] == "CHART"
    ]
    sorted_charts = sorted(charts, key=lambda k: k["meta"]["chartId"])
    for i, chart_component in enumerate(sorted_charts):
        if i < len(slices):
            chart_component["meta"]["chartId"] = int(slices[i].id)
            chart_component["meta"]["uuid"] = str(slices[i].uuid)


def merge_slice(slc: Slice) -> None:
    """合并切片，删除数据库中现有同标识的切片，然后将指定切片对象关系模型实例添加到数据库。"""

    # 删除数据库中现有切片
    o = db.session.query(Slice).filter_by(slice_name=slc.slice_name).first()
    if o:
        db.session.delete(o)

    # 添加给定切片刀数据库
    db.session.add(slc)
    db.session.commit()


def get_slice_json(defaults: Dict[Any, Any], **kwargs: Any) -> str:
    """将指定默认字典和关键字字典进行整合，返回序列化后的 Json 对象。"""

    defaults_copy = defaults.copy()
    defaults_copy.update(kwargs)
    return json.dumps(defaults_copy, indent=4, sort_keys=True)


def get_example_data(filepath: str, is_gzip: bool = True, make_bytes: bool = False) -> BytesIO:
    """
    获取示例数据，下载打开文件，进行解压缩。

    :param filepath: 文件路径。
    :param is_gzip: 是否压缩的。
    :param make_bytes: 是否返回字节数据内容。
    :return:
    """

    # 如果本地存在则从本地加载
    local_path = os.path.join(get_examples_folder(), "data", filepath)
    if os.path.exists(local_path):
        with io.open(local_path, "rb") as f:
            content = f.read()
    else:   # 从远程加载
        content = request.urlopen(f"{BASE_URL}{filepath}?raw=true").read()

    # 如果是压缩文件
    if is_gzip:
        content = zlib.decompress(content, zlib.MAX_WBITS | 16)

    # 创建字节内容
    if make_bytes:
        content = BytesIO(content)

    return content
