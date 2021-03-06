# -*- coding: utf-8 -*-

import json
import logging
from typing import Any, Dict, Optional, Type, TYPE_CHECKING
from urllib import parse

import sqlalchemy as sqla
from flask_appbuilder import Model
from flask_appbuilder.models.decorators import renders
from markupsafe import escape, Markup
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import relationship
from sqlalchemy.orm.mapper import Mapper

from rabbitai import ConnectorRegistry, db, is_feature_enabled, security_manager
from rabbitai.legacy import update_time_range
from rabbitai.models.helpers import AuditMixinNullable, ImportExportMixin
from rabbitai.models.tags import ChartUpdater
from rabbitai.tasks.thumbnails import cache_chart_thumbnail
from rabbitai.utils import core as utils
from rabbitai.utils.hashing import md5_sha_from_str
from rabbitai.utils.memoized import memoized
from rabbitai.utils.urls import get_url_path
from rabbitai.viz import BaseViz, viz_types

if TYPE_CHECKING:
    from rabbitai.connectors.base.models import BaseDatasource

metadata = Model.metadata

slice_user = Table(
    "slice_user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("ab_user.id")),
    Column("slice_id", Integer, ForeignKey("slices.id")),
)
"""切片-用户关系数据表。"""
logger = logging.getLogger(__name__)


class Slice(Model, AuditMixinNullable, ImportExportMixin):
    """切片（图表）对象关系模型，切片本质上是一个报告或数据视图。"""

    __tablename__ = "slices"

    id = Column(Integer, primary_key=True)
    slice_name = Column(String(250))
    datasource_id = Column(Integer)
    datasource_type = Column(String(200))
    datasource_name = Column(String(2000))
    viz_type = Column(String(250))
    params = Column(Text)
    query_context = Column(Text)
    description = Column(Text)
    cache_timeout = Column(Integer)
    perm = Column(String(1000))
    schema_perm = Column(String(1000))
    # the last time a user has saved the chart, changed_on is referencing
    # when the database row was last written
    last_saved_at = Column(DateTime, nullable=True)
    last_saved_by_fk = Column(Integer, ForeignKey("ab_user.id"), nullable=True,)
    last_saved_by = relationship(
        security_manager.user_model, foreign_keys=[last_saved_by_fk]
    )
    owners = relationship(security_manager.user_model, secondary=slice_user)
    table = relationship(
        "SqlaTable",
        foreign_keys=[datasource_id],
        primaryjoin="and_(Slice.datasource_id == SqlaTable.id, "
        "Slice.datasource_type == 'table')",
        remote_side="SqlaTable.id",
        lazy="subquery",
    )

    token = ""

    export_fields = [
        "slice_name",
        "datasource_type",
        "datasource_name",
        "viz_type",
        "params",
        "query_context",
        "cache_timeout",
    ]
    """导出字段名称列表"""
    export_parent = "table"

    def __repr__(self) -> str:
        return self.slice_name or str(self.id)

    @property
    def cls_model(self) -> Type["BaseDatasource"]:
        """获取数据源对象关系模型类。"""

        return ConnectorRegistry.sources[self.datasource_type]

    @property
    def datasource(self) -> Optional["BaseDatasource"]:
        """获取数据源对象实例。"""
        return self.get_datasource

    def clone(self) -> "Slice":
        """返回该实例的副本。"""

        return Slice(
            slice_name=self.slice_name,
            datasource_id=self.datasource_id,
            datasource_type=self.datasource_type,
            datasource_name=self.datasource_name,
            viz_type=self.viz_type,
            params=self.params,
            description=self.description,
            cache_timeout=self.cache_timeout,
        )

    @datasource.getter  # type: ignore
    @memoized
    def get_datasource(self) -> Optional["BaseDatasource"]:
        """从数据库中查询第一个满足条件的数据源对象实例。"""
        return db.session.query(self.cls_model).filter_by(id=self.datasource_id).first()

    @renders("datasource_name")
    def datasource_link(self) -> Optional[Markup]:
        """获取数据源连接。"""

        datasource = self.datasource
        return datasource.link if datasource else None

    @renders("datasource_url")
    def datasource_url(self) -> Optional[str]:
        """获取数据源访问地址。"""

        if self.table:
            return self.table.explore_url
        datasource = self.datasource
        return datasource.explore_url if datasource else None

    def datasource_name_text(self) -> Optional[str]:
        """获取数据源名称。"""

        if self.table:
            if self.table.schema:
                return f"{self.table.schema}.{self.table.table_name}"
            return self.table.table_name
        if self.datasource:
            if self.datasource.schema:
                return f"{self.datasource.schema}.{self.datasource.name}"
            return self.datasource.name
        return None

    @property
    def datasource_edit_url(self) -> Optional[str]:
        """获取数据源编辑地址。"""

        datasource = self.datasource
        return datasource.url if datasource else None

    @property
    @memoized
    def viz(self) -> Optional[BaseViz]:
        """获取可视化对象。"""

        form_data = json.loads(self.params)
        viz_class = viz_types.get(self.viz_type)
        datasource = self.datasource
        if viz_class and datasource:
            return viz_class(datasource=datasource, form_data=form_data)
        return None

    @property
    def description_markeddown(self) -> str:
        """获取描述信息的 markdown 文本。"""
        return utils.markdown(self.description)

    @property
    def data(self) -> Dict[str, Any]:
        """获取在模板中渲染切片的数据。"""

        data: Dict[str, Any] = {}
        self.token = ""
        try:
            viz = self.viz
            data = viz.data if viz else self.form_data
            self.token = utils.get_form_data_token(data)
        except Exception as ex:
            logger.exception(ex)
            data["error"] = str(ex)

        return {
            "cache_timeout": self.cache_timeout,
            "changed_on": self.changed_on.isoformat(),
            "changed_on_humanized": self.changed_on_humanized,
            "datasource": self.datasource_name,
            "description": self.description,
            "description_markeddown": self.description_markeddown,
            "edit_url": self.edit_url,
            "form_data": self.form_data,
            "query_context": self.query_context,
            "modified": self.modified(),
            "owners": [
                f"{owner.first_name} {owner.last_name}" for owner in self.owners
            ],
            "slice_id": self.id,
            "slice_name": self.slice_name,
            "slice_url": self.slice_url,
        }

    @property
    def digest(self) -> str:
        """
        Returns a MD5 HEX digest that makes this dashboard unique
        """
        return md5_sha_from_str(self.params or "")

    @property
    def thumbnail_url(self) -> str:
        """
        Returns a thumbnail URL with a HEX digest. We want to avoid browser cache
        if the dashboard has changed
        """
        return f"/api/v1/chart/{self.id}/thumbnail/{self.digest}/"

    @property
    def json_data(self) -> str:
        return json.dumps(self.data)

    @property
    def form_data(self) -> Dict[str, Any]:
        """获取表单数据，该数据存储在 params 字段中，再加上：slice_id、viz_type、datasource、cache_timeout等。"""

        form_data: Dict[str, Any] = {}
        try:
            form_data = json.loads(self.params)
        except Exception as ex:
            logger.error("Malformed json in slice's params", exc_info=True)
            logger.exception(ex)
        form_data.update(
            {
                "slice_id": self.id,
                "viz_type": self.viz_type,
                "datasource": "{}__{}".format(self.datasource_id, self.datasource_type),
            }
        )

        if self.cache_timeout:
            form_data["cache_timeout"] = self.cache_timeout
        update_time_range(form_data)

        return form_data

    def get_explore_url(
        self,
        base_url: str = "/rabbitai/explore",
        overrides: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        获取浏览地址 {base_url}/?form_data={params}。

        :param base_url: 基地址，默认为：/rabbitai/explore。
        :param overrides: 查询参数字典。
        :return:
        """

        overrides = overrides or {}
        form_data = {"slice_id": self.id}
        form_data.update(overrides)
        params = parse.quote(json.dumps(form_data))
        return f"{base_url}/?form_data={params}"

    @property
    def slice_url(self) -> str:
        """获取访问该切片的地址。"""
        return self.get_explore_url()

    @property
    def explore_json_url(self) -> str:
        """获取访问该切片Json的地址。"""
        return self.get_explore_url("/rabbitai/explore_json")

    @property
    def edit_url(self) -> str:
        """获取编辑该切片的地址：/chart/edit/{self.id}。"""
        return f"/chart/edit/{self.id}"

    @property
    def chart(self) -> str:
        """获取图表名称。"""
        return self.slice_name or "<empty>"

    @property
    def slice_link(self) -> Markup:
        """获取切片连接 Markup"""
        name = escape(self.chart)
        return Markup(f'<a href="{self.url}">{name}</a>')

    @property
    def changed_by_url(self) -> str:
        """获取更改者信息地址：/rabbitai/profile/{self.changed_by.username}。"""
        return f"/rabbitai/profile/{self.changed_by.username}"

    @property
    def icons(self) -> str:
        """获取图标的Html元素字符串。"""
        return f"""
        <a
                href="{self.datasource_edit_url}"
                data-toggle="tooltip"
                title="{self.datasource}">
            <i class="fa fa-database"></i>
        </a>
        """

    @property
    def url(self) -> str:
        """获取地址。"""
        return f"/rabbitai/explore/?form_data=%7B%22slice_id%22%3A%20{self.id}%7D"


def set_related_perm(_mapper: Mapper, _connection: Connection, target: Slice) -> None:
    """
    设置指定目标对象的权限。

    :param _mapper: 映射。
    :param _connection: 连接。
    :param target: 目标对象（切片）。
    :return:
    """

    src_class = target.cls_model
    id_ = target.datasource_id
    if id_:
        ds = db.session.query(src_class).filter_by(id=int(id_)).first()
        if ds:
            target.perm = ds.perm
            target.schema_perm = ds.schema_perm


def event_after_chart_changed(
    _mapper: Mapper, _connection: Connection, target: Slice
) -> None:
    """
    处理图表更改后事件。

    :param _mapper:
    :param _connection:
    :param target:
    :return:
    """

    url = get_url_path("rabbitai.slice", slice_id=target.id, standalone="true")
    cache_chart_thumbnail.delay(url, target.digest, force=True)


sqla.event.listen(Slice, "before_insert", set_related_perm)
sqla.event.listen(Slice, "before_update", set_related_perm)

# events for updating tags
if is_feature_enabled("TAGGING_SYSTEM"):
    sqla.event.listen(Slice, "after_insert", ChartUpdater.after_insert)
    sqla.event.listen(Slice, "after_update", ChartUpdater.after_update)
    sqla.event.listen(Slice, "after_delete", ChartUpdater.after_delete)

# events for updating tags
if is_feature_enabled("THUMBNAILS_SQLA_LISTENERS"):
    sqla.event.listen(Slice, "after_insert", event_after_chart_changed)
    sqla.event.listen(Slice, "after_update", event_after_chart_changed)
