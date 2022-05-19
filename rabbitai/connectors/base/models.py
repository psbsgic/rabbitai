# -*- coding: utf-8 -*-

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Hashable, List, Optional, Set, Type, Union

from flask_appbuilder.security.sqla.models import User
from sqlalchemy import and_, Boolean, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import foreign, Query, relationship, RelationshipProperty, Session

from rabbitai import is_feature_enabled, security_manager
from rabbitai.constants import NULL_STRING
from rabbitai.models.helpers import AuditMixinNullable, ImportExportMixin, QueryResult
from rabbitai.models.slice import Slice
from rabbitai.typing import FilterValue, FilterValues, QueryObjectDict
from rabbitai.utils import core as utils
from rabbitai.utils.core import GenericDataType

METRIC_FORM_DATA_PARAMS = [
    "metric",
    "metric_2",
    "metrics",
    "metrics_b",
    "percent_metrics",
    "secondary_metric",
    "size",
    "timeseries_limit_metric",
    "x",
    "y",
]
"""指标表单数据参数列表"""

COLUMN_FORM_DATA_PARAMS = [
    "all_columns",
    "all_columns_x",
    "columns",
    "entity",
    "groupby",
    "order_by_cols",
    "series",
]
"""列表单数据参数列表"""


class DatasourceKind(str, Enum):
    """数据源种类枚举，VIRTUAL、PHYSICAL。"""

    VIRTUAL = "virtual"
    PHYSICAL = "physical"


class BaseDatasource(AuditMixinNullable, ImportExportMixin):
    """
    基础数据源数据模型，一个面向可查询对象（数据表、数据文件等数据源）的通用接口。
    由 columns、metrics、slices 组成。支持审计和导入导出功能。

    包括以下列（字段）：

    - id：唯一标识，主键
    - description：描述
    - default_endpoint：默认终结点
    - is_featured：是否特征
    - filter_select_enabled：是否启用过滤选择
    - offset：偏移
    - cache_timeout：缓存超时
    - params：查询参数
    - perm：权限
    - schema_perm：架构权限
    - slices：切片数据模型列表，关系。
    """

    # region 类属性

    __tablename__: Optional[str] = None
    """数据表名称，{connector_name}_datasource"""

    baselink: Optional[str] = None
    """基连接，指向模型视图终结点的基地址"""

    owner_class: Optional[User] = None
    """拥有者类类型，User"""

    query_language: Optional[str] = None
    """查询语言，用于在UI中显示查询时突出显示代码"""

    is_rls_supported: bool = False
    """是否支持行级安全性，只有一些数据源支持行级安全性"""

    sql: Optional[str] = None
    """SQL语句字符串"""

    owners: List[User]
    """用户对象列表"""

    update_from_object_fields: List[str]
    """可以更新对象的字段名称列表"""

    columns: List["BaseColumn"] = []
    """列对象的列表"""

    metrics: List["BaseMetric"] = []
    """指标（计算）对象的列表"""

    # endregion

    # region Columns

    id = Column(Integer, primary_key=True)
    """唯一标识，主键"""
    description = Column(Text)
    """描述"""
    default_endpoint = Column(Text)
    """默认终结点"""
    is_featured = Column(Boolean, default=False)
    """是否特征"""
    filter_select_enabled = Column(Boolean, default=is_feature_enabled("UX_BETA"))
    """启用过滤选择"""
    offset = Column(Integer, default=0)
    """偏移"""
    cache_timeout = Column(Integer)
    """缓存超时"""
    params = Column(String(1000))
    """查询参数"""
    perm = Column(String(1000))
    """权限"""
    schema_perm = Column(String(1000))
    """架构权限"""

    @declared_attr
    def slices(self) -> RelationshipProperty:
        """切片关系属性。"""

        return relationship(
            "Slice",
            primaryjoin=lambda: and_(
                foreign(Slice.datasource_id) == self.id,
                foreign(Slice.datasource_type) == self.type,
            ),
        )

    # endregion

    # region property

    @property
    def name(self) -> str:
        """名称，可以是列或指向列的属性"""
        raise NotImplementedError()

    @property
    def column_class(self) -> Type["BaseColumn"]:
        """获取列对象的类类型，BaseColumn及其派生类型。"""

        raise NotImplementedError()

    @property
    def metric_class(self) -> Type["BaseMetric"]:
        """获取指标类类型，BaseMetric及其派生类型。"""

        raise NotImplementedError()

    @property
    def kind(self) -> DatasourceKind:
        """数据源种类，即虚拟的还是物理的。"""
        return DatasourceKind.VIRTUAL if self.sql else DatasourceKind.PHYSICAL

    @property
    def is_virtual(self) -> bool:
        """种类是否虚拟的，"""
        return self.kind == DatasourceKind.VIRTUAL

    @property
    def type(self) -> str:
        """数据源类型（字符串）。"""
        raise NotImplementedError()

    @property
    def uid(self) -> str:
        """跨数据源类型的唯一标识：{id}__{type}"""

        return f"{self.id}__{self.type}"

    @property
    def column_names(self) -> List[str]:
        """列名称的列表。"""
        return sorted([c.column_name for c in self.columns], key=lambda x: x or "")

    @property
    def columns_types(self) -> Dict[str, str]:
        """列名称及其类型的字典。"""
        return {c.column_name: c.type for c in self.columns}

    @property
    def main_dttm_col(self) -> str:
        """主时间列名称，默认：timestamp"""
        return "timestamp"

    @property
    def datasource_name(self) -> str:
        """数据源名称。"""
        raise NotImplementedError()

    @property
    def connection(self) -> Optional[str]:
        """表示数据源上下文的字符串"""
        return None

    @property
    def schema(self) -> Optional[str]:
        """表示数据源模式的字符串（如果适用）"""
        return None

    @property
    def filterable_column_names(self) -> List[str]:
        """获取可过滤的列名称的排序列表。"""
        return sorted([c.column_name for c in self.columns if c.filterable])

    @property
    def dttm_cols(self) -> List[str]:
        """获取时间列名称的列表。"""
        return []

    @property
    def url(self) -> str:
        """获取编辑地址：/{baselink}/edit/{id}。"""
        return "/{}/edit/{}".format(self.baselink, self.id)

    @property
    def explore_url(self) -> str:
        """获取浏览地址：default_endpoint 或 /rabbitai/explore/{type}/{id}/。"""

        if self.default_endpoint:
            return self.default_endpoint
        return f"/rabbitai/explore/{self.type}/{self.id}/"

    @property
    def column_formats(self) -> Dict[str, Optional[str]]:
        """获取列名称及其格式对象（d3format）的字典。"""
        return {m.metric_name: m.d3format for m in self.metrics if m.d3format}

    @property
    def short_data(self) -> Dict[str, Any]:
        """
        获取简单（基本）数据，
        即要发送到前端的数据源的数据（id、uid、edit_url、name、type、schema、connection、creator）。
        """

        return {
            "edit_url": self.url,
            "id": self.id,
            "uid": self.uid,
            "schema": self.schema,
            "name": self.name,
            "type": self.type,
            "connection": self.connection,
            "creator": str(self.created_by),
        }

    @property
    def select_star(self) -> Optional[str]:
        """获取 SELECT * 语句。"""
        pass

    @property
    def data(self) -> Dict[str, Any]:
        """获取要发送到前端的数据。"""

        order_by_choices = []
        # self.column_names return sorted column_names
        for column_name in self.column_names:
            column_name = str(column_name or "")
            order_by_choices.append(
                (json.dumps([column_name, True]), column_name + " [asc]")
            )
            order_by_choices.append(
                (json.dumps([column_name, False]), column_name + " [desc]")
            )

        verbose_map = {"__timestamp": "时间"}
        verbose_map.update(
            {o.metric_name: o.verbose_name or o.metric_name for o in self.metrics}
        )
        verbose_map.update(
            {o.column_name: o.verbose_name or o.column_name for o in self.columns}
        )

        return {
            # simple fields
            "id": self.id,
            "uid": self.uid,
            "column_formats": self.column_formats,
            "description": self.description,
            "database": self.database.data,  # pylint: disable=no-member
            "default_endpoint": self.default_endpoint,
            "filter_select": self.filter_select_enabled,
            "filter_select_enabled": self.filter_select_enabled,
            "name": self.name,
            "datasource_name": self.datasource_name,
            "table_name": self.datasource_name,
            "type": self.type,
            "schema": self.schema,
            "offset": self.offset,
            "cache_timeout": self.cache_timeout,
            "params": self.params,
            "perm": self.perm,
            "edit_url": self.url,
            # sqla-specific
            "sql": self.sql,
            # one to many
            "columns": [o.data for o in self.columns],
            "metrics": [o.data for o in self.metrics],
            # TODO deprecate, move logic to JS
            "order_by_choices": order_by_choices,
            "owners": [owner.id for owner in self.owners],
            "verbose_map": verbose_map,
            "select_star": self.select_star,
        }

    # endregion

    def add_missing_metrics(self, metrics: List["BaseMetric"]) -> None:
        """
        添加指定指标列表到该实例当前指标列表中，不重复添加。

        :param metrics: 要添加的指标列表。
        :return:
        """

        existing_metrics = {m.metric_name for m in self.metrics}
        for metric in metrics:
            if metric.metric_name not in existing_metrics:
                metric.table_id = self.id
                self.metrics.append(metric)

    def data_for_slices(self, slices: List[Slice]) -> Dict[str, Any]:
        """
        数据源的表示形式，仅包含呈现切片所需的数据。

        用于在加载仪表板时减少有效负载。
        """

        data = self.data
        metric_names = set()
        column_names = set()
        for slc in slices:
            form_data = slc.form_data
            # 从 form_data 中取出所有必需的指标
            for metric_param in METRIC_FORM_DATA_PARAMS:
                for metric in utils.get_iterable(form_data.get(metric_param) or []):
                    metric_names.add(utils.get_metric_name(metric))
                    if utils.is_adhoc_metric(metric):
                        column_names.add(
                            (metric.get("column") or {}).get("column_name")
                        )

            # 查询过滤器中使用的列
            column_names.update(
                filter_["subject"]
                for filter_ in form_data.get("adhoc_filters") or []
                if filter_.get("clause") == "WHERE" and filter_.get("subject")
            )

            # 过滤器框使用的列
            column_names.update(
                filter_config["column"]
                for filter_config in form_data.get("filter_configs") or []
                if "column" in filter_config
            )

            column_names.update(
                column
                for column_param in COLUMN_FORM_DATA_PARAMS
                for column in utils.get_iterable(form_data.get(column_param) or [])
            )

        filtered_metrics = [
            metric
            for metric in data["metrics"]
            if metric["metric_name"] in metric_names
        ]

        filtered_columns: List[Column] = []
        column_types: Set[GenericDataType] = set()
        for column in data["columns"]:
            generic_type = column.get("type_generic")
            if generic_type is not None:
                column_types.add(generic_type)
            if column["column_name"] in column_names:
                filtered_columns.append(column)

        data["column_types"] = list(column_types)
        del data["description"]
        data.update({"metrics": filtered_metrics})
        data.update({"columns": filtered_columns})
        verbose_map = {"__timestamp": "时间"}
        verbose_map.update(
            {
                metric["metric_name"]: metric["verbose_name"] or metric["metric_name"]
                for metric in filtered_metrics
            }
        )
        verbose_map.update(
            {
                column["column_name"]: column["verbose_name"] or column["column_name"]
                for column in filtered_columns
            }
        )
        data["verbose_map"] = verbose_map

        return data

    @staticmethod
    def filter_values_handler(
        values: Optional[FilterValues],
        target_column_type: utils.GenericDataType,
        is_list_target: bool = False,
    ) -> Optional[FilterValues]:
        """
        处理过滤值为 Python 类型值。

        :param values: 过滤值。
        :param target_column_type: 目标列类型。
        :param is_list_target: 目标是否列表，默认False。
        :return:
        """

        if values is None:
            return None

        def handle_single_value(value: Optional[FilterValue]) -> Optional[FilterValue]:
            """
            处理单个过滤值为Python数据类型值。

            :param value:
            :return:
            """

            # backward compatibility with previous <select> components
            if (
                isinstance(value, (float, int))
                and target_column_type == utils.GenericDataType.TEMPORAL
            ):
                return datetime.utcfromtimestamp(value / 1000)
            if isinstance(value, str):
                value = value.strip("\t\n'\"")

                if target_column_type == utils.GenericDataType.NUMERIC:
                    # For backwards compatibility and edge cases
                    # where a column data type might have changed
                    return utils.cast_to_num(value)
                if value == NULL_STRING:
                    return None
                if value == "<empty string>":
                    return ""
            if target_column_type == utils.GenericDataType.BOOLEAN:
                return utils.cast_to_boolean(value)
            return value

        if isinstance(values, (list, tuple)):
            values = [handle_single_value(v) for v in values]  # type: ignore
        else:
            values = handle_single_value(values)

        if is_list_target and not isinstance(values, (tuple, list)):
            values = [values]  # type: ignore
        elif not is_list_target and isinstance(values, (tuple, list)):
            values = values[0] if values else None

        return values

    def external_metadata(self) -> List[Dict[str, str]]:
        """从外部系统返回列信息"""
        raise NotImplementedError()

    def get_query_str(self, query_obj: QueryObjectDict) -> str:
        """返回指定查询对象字典的字符串形式。

        这用于向用户显示，以便用户能够理解幕后发生的事情
        """
        raise NotImplementedError()

    def query(self, query_obj: QueryObjectDict) -> QueryResult:
        """执行查询并返回查询结果 QueryResult。"""
        raise NotImplementedError()

    def values_for_column(self, column_name: str, limit: int = 10000) -> List[Any]:
        """
        给定一列，返回不同值的迭代器。

        这用于填充下拉列表，该下拉列表显示“浏览”视图中过滤器中的值列表
        """
        raise NotImplementedError()

    @staticmethod
    def default_query(qry: Query) -> Query:
        """获取默认查询。"""
        return qry

    def get_column(self, column_name: Optional[str]) -> Optional["BaseColumn"]:
        """
        获取具有指定名称的列对象。

        :param column_name: 列名称。
        :return:
        """

        if not column_name:
            return None
        for col in self.columns:
            if col.column_name == column_name:
                return col
        return None

    @staticmethod
    def get_fk_many_from_list(
        object_list: List[Any],
        fkmany: List[Column],
        fkmany_class: Type[Union["BaseColumn", "BaseMetric"]],
        key_attr: str,
    ) -> List[Column]:
        """
        从对象列表更新ORM一对多列表

        用于使用相同代码同步指标和列

        :param object_list: 对象列表。
        :param fkmany: 外键的列对象的列表。
        :param fkmany_class: 外键列或指标的类型。
        :param key_attr: 外键键属性名称。
        :return: 外键的列对象的列表。
        """

        # 从各对象中获取外键属性值及其对象的字典
        object_dict = {o.get(key_attr): o for o in object_list}

        # 删除移除的外键
        fkmany = [o for o in fkmany if getattr(o, key_attr) in object_dict]

        # 同步存在的外键
        for fk in fkmany:
            obj = object_dict.get(getattr(fk, key_attr))
            if obj:
                for attr in fkmany_class.update_from_object_fields:
                    setattr(fk, attr, obj.get(attr))

        # 创建新的外键
        new_fks = []
        orm_keys = [getattr(o, key_attr) for o in fkmany]
        for obj in object_list:
            key = obj.get(key_attr)
            if key not in orm_keys:
                del obj["id"]
                orm_kwargs = {}
                for k in obj:
                    if k in fkmany_class.update_from_object_fields and k in obj:
                        orm_kwargs[k] = obj[k]
                new_obj = fkmany_class(**orm_kwargs)
                new_fks.append(new_obj)

        fkmany += new_fks

        return fkmany

    def update_from_object(self, obj: Dict[str, Any]) -> None:
        """
        依据指定对象（字典）更新该数据源对象实例。

        UI的表编辑器创建了一个复杂的数据结构，其中包含数据源的大多数属性以及指标和列对象数组。
        此方法从UI接收对象并同步数据源以匹配它。由于不同连接器的字段不同，
        因此实现使用 ``update_from_object_fields``，可以为每个连接器定义该字段，并定义应同步的字段。

        :param obj: 对象（字典）。
        :return:
        """

        # 设置字段值
        for attr in self.update_from_object_fields:
            setattr(self, attr, obj.get(attr))

        self.owners = obj.get("owners", [])

        # 同步指标对象集合
        metrics = (
            self.get_fk_many_from_list(
                obj["metrics"], self.metrics, self.metric_class, "metric_name"
            )
            if self.metric_class and "metrics" in obj
            else []
        )
        self.metrics = metrics

        # 同步列对象集合
        self.columns = (
            self.get_fk_many_from_list(
                obj["columns"], self.columns, self.column_class, "column_name"
            )
            if self.column_class and "columns" in obj
            else []
        )

    def get_extra_cache_keys(self, query_obj: QueryObjectDict) -> List[Hashable]:
        """
        如果数据源需要提供额外的键来计算缓存键，那么可以通过此方法提供这些键。

        :param query_obj: 查询对象字典。
        :return: 缓存键列表。
        """
        return []

    def __hash__(self) -> int:
        return hash(self.uid)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseDatasource):
            return NotImplemented
        return self.uid == other.uid

    def raise_for_access(self) -> None:
        """
        如果用户无法访问资源，则引发异常。

        :raises RabbitaiSecurityException: 如果用户无法访问资源。
        """

        security_manager.raise_for_access(datasource=self)

    @classmethod
    def get_datasource_by_name(
        cls, session: Session, datasource_name: str, schema: str, database_name: str
    ) -> Optional["BaseDatasource"]:
        """
        派生类重写，依据名称获取数据源对象。

        :param session: 数据库会话对象。
        :param datasource_name: 数据源名称。
        :param schema: 模式。
        :param database_name: 数据库名称。
        :return: 数据源对象关系模型实例。
        """

        raise NotImplementedError()


class BaseColumn(AuditMixinNullable, ImportExportMixin):
    """列对象关系模型，所有数据源列对象的基类。"""

    __tablename__: Optional[str] = None  # {connector_name}_column

    # region Column

    id = Column(Integer, primary_key=True)
    """唯一标识"""
    column_name = Column(String(255), nullable=False)
    """列名称"""
    verbose_name = Column(String(1024))
    """显示名称"""
    is_active = Column(Boolean, default=True)
    """是否活动的"""
    type = Column(String(32))
    """数据类型"""
    groupby = Column(Boolean, default=True)
    """是否可分组"""
    filterable = Column(Boolean, default=True)
    """是否可过滤"""
    description = Column(Text)
    """描述"""

    # endregion

    # region Fields

    is_dttm = None
    """是否时间字段"""
    # [optional] Set this to support import/export functionality
    export_fields: List[Any] = []
    """导出字段列表，用于导入导出操作。"""

    bool_types = ("BOOL",)
    """布尔值类型名称的元组。"""
    num_types = (
        "DOUBLE",
        "FLOAT",
        "INT",
        "BIGINT",
        "NUMBER",
        "LONG",
        "REAL",
        "NUMERIC",
        "DECIMAL",
        "MONEY",
    )
    """数值类型名称的列表。"""
    date_types = ("DATE", "TIME")
    """日期类型名称的元组。"""
    str_types = ("VARCHAR", "STRING", "CHAR")
    """字符串类型名称的元组。"""

    # endregion

    def __repr__(self) -> str:
        return str(self.column_name)

    # region Properties

    @property
    def is_numeric(self) -> bool:
        """是否数值类型。"""
        return self.type and any(map(lambda t: t in self.type.upper(), self.num_types))

    @property
    def is_temporal(self) -> bool:
        """是否日期时间类型。"""
        return self.type and any(map(lambda t: t in self.type.upper(), self.date_types))

    @property
    def is_string(self) -> bool:
        """是否字符串类型"""
        return self.type and any(map(lambda t: t in self.type.upper(), self.str_types))

    @property
    def is_boolean(self) -> bool:
        """是否布尔类型"""
        return self.type and any(map(lambda t: t in self.type.upper(), self.bool_types))

    @property
    def type_generic(self) -> Optional[utils.GenericDataType]:
        """获取该列对象的通用数据类型。"""

        if self.is_string:
            return utils.GenericDataType.STRING
        if self.is_boolean:
            return utils.GenericDataType.BOOLEAN
        if self.is_numeric:
            return utils.GenericDataType.NUMERIC
        if self.is_temporal:
            return utils.GenericDataType.TEMPORAL
        return None

    @property
    def expression(self) -> Column:
        """获取表达式列对象。"""
        raise NotImplementedError()

    @property
    def python_date_format(self) -> Column:
        """获取Python日期格式列对象。"""
        raise NotImplementedError()

    @property
    def data(self) -> Dict[str, Any]:
        """
        返回该列对象的数据（属性名称及其值的字典）。

        属性名称：id, column_name, verbose_name, description, expression, filterable, groupby, is_dttm, type。

        """

        attrs = (
            "id",
            "column_name",
            "verbose_name",
            "description",
            "expression",
            "filterable",
            "groupby",
            "is_dttm",
            "type",
        )
        return {s: getattr(self, s) for s in attrs if hasattr(self, s)}

    # endregion


class BaseMetric(AuditMixinNullable, ImportExportMixin):
    """指标（计算）对象关系模型，

    - 定义列：id、metric_name、verbose_name、metric_type、description、d3format、warning_text。

    - 定义属性：perm、expression、data
    """

    __tablename__: Optional[str] = None  # {connector_name}_metric

    id = Column(Integer, primary_key=True)
    """唯一标识"""
    metric_name = Column(String(255), nullable=False)
    """指标名称"""
    verbose_name = Column(String(1024))
    """显示名称。"""
    metric_type = Column(String(32))
    """指标类型"""
    description = Column(Text)
    """描述信息"""
    d3format = Column(String(128))
    """格式字符串"""
    warning_text = Column(Text)
    """警告文本"""

    """
    接口还应该声明一个指向 BaseDatasource 的派生的 datasource 关系，以及一个FK

    datasource_name = Column(
        String(255),
        ForeignKey('datasources.datasource_name'))
    
    datasource = relationship(
        # 需要修改为指向 {Connector}Datasource
        'BaseDatasource',
        backref=backref('metrics', cascade='all, delete-orphan'),
        enable_typechecks=False)
    """

    @property
    def perm(self) -> Optional[str]:
        """获取权限。"""
        raise NotImplementedError()

    @property
    def expression(self) -> Column:
        """获取表达式。"""
        raise NotImplementedError()

    @property
    def data(self) -> Dict[str, Any]:
        """获取发送到前端的数据。"""

        attrs = (
            "id",
            "metric_name",
            "verbose_name",
            "description",
            "expression",
            "warning_text",
            "d3format",
        )
        return {s: getattr(self, s) for s in attrs}
