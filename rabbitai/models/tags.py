from __future__ import absolute_import, division, print_function, unicode_literals

import enum
from typing import List, Optional, TYPE_CHECKING, Union

from flask_appbuilder import Model
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.orm.mapper import Mapper

from rabbitai.models.helpers import AuditMixinNullable

if TYPE_CHECKING:
    from rabbitai.models.core import FavStar
    from rabbitai.models.dashboard import Dashboard
    from rabbitai.models.slice import Slice
    from rabbitai.models.sql_lab import Query

Session = sessionmaker(autoflush=False)


class TagTypes(enum.Enum):
    """
    标签类型枚举。

    Objects (queries, charts and dashboards) will have with implicit tags based
    on metadata: types, owners and who favorited them. This way, user "alice"
    can find all their objects by querying for the tag `owner:alice`.
    """

    # explicit tags, added manually by the owner
    custom = 1

    # implicit tags, generated automatically
    type = 2
    owner = 3
    favorited_by = 4


class ObjectTypes(enum.Enum):
    """对象类型枚举。"""

    query = 1
    chart = 2
    dashboard = 3


class Tag(Model, AuditMixinNullable):
    """标签对象关系模型，附加到对象（查询、图表或仪表板）的标记。"""

    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True)
    type = Column(Enum(TagTypes))


class TaggedObject(Model, AuditMixinNullable):
    """标签化对象关系模型，对象和标记之间的关联。"""

    __tablename__ = "tagged_object"
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"))
    object_id = Column(Integer)
    object_type = Column(Enum(ObjectTypes))

    tag = relationship("Tag", backref="objects")


def get_tag(name: str, session: Session, type_: TagTypes) -> Tag:
    """
    从数据库中获取一个标签Tag对象，如果不存在则创建并添加到数据库。

    :param name: 名称。
    :param session: 数据库会话。
    :param type_: 类型。
    :return:
    """

    tag = session.query(Tag).filter_by(name=name, type=type_).one_or_none()
    if tag is None:
        tag = Tag(name=name, type=type_)
        session.add(tag)
        session.commit()

    return tag


def get_object_type(class_name: str) -> ObjectTypes:
    """
    依据指定类名称获取对象类型。

    :param class_name:
    :return:
    """

    mapping = {
        "slice": ObjectTypes.chart,
        "dashboard": ObjectTypes.dashboard,
        "query": ObjectTypes.query,
    }
    try:
        return mapping[class_name.lower()]
    except KeyError:
        raise Exception("No mapping found for {0}".format(class_name))


class ObjectUpdater:
    """对象关系模型更改器，提供监听对象更改相关方法。"""

    object_type: Optional[str] = None

    @classmethod
    def get_owners_ids(
        cls, target: Union["Dashboard", "FavStar", "Slice"]
    ) -> List[int]:
        """
        获取拥有者的标识列表。

        :param target: 目标对象。
        :return:
        """
        raise NotImplementedError("Subclass should implement `get_owners_ids`")

    @classmethod
    def _add_owners(
        cls, session: Session, target: Union["Dashboard", "FavStar", "Slice"]
    ) -> None:
        """
        添加拥有者，构建并存储 TaggedObject 到数据库。

        :param session:
        :param target:
        :return:
        """

        for owner_id in cls.get_owners_ids(target):
            name = "owner:{0}".format(owner_id)
            tag = get_tag(name, session, TagTypes.owner)
            tagged_object = TaggedObject(
                tag_id=tag.id, object_id=target.id, object_type=cls.object_type
            )
            session.add(tagged_object)

    @classmethod
    def after_insert(
        cls,
        _mapper: Mapper,
        connection: Connection,
        target: Union["Dashboard", "FavStar", "Slice"],
    ) -> None:
        """
        插入对象到数据库后要调用的方法，添加拥有者相关标签Tag对象到数据库。

        :param _mapper: 映射
        :param connection: 连接
        :param target: 对象。
        :return:
        """

        session = Session(bind=connection)

        # add `owner:` tags
        cls._add_owners(session, target)

        # add `type:` tags
        tag = get_tag("type:{0}".format(cls.object_type), session, TagTypes.type)
        tagged_object = TaggedObject(
            tag_id=tag.id, object_id=target.id, object_type=cls.object_type
        )
        session.add(tagged_object)

        session.commit()

    @classmethod
    def after_update(
        cls,
        _mapper: Mapper,
        connection: Connection,
        target: Union["Dashboard", "FavStar", "Slice"],
    ) -> None:
        """
        更新对象到数据库后要调用的方法，添加拥有者相关标签Tag对象到数据库。

        :param _mapper: 映射
        :param connection: 连接
        :param target: 对象。
        :return:
        """
        session = Session(bind=connection)

        # delete current `owner:` tags
        query = (
            session.query(TaggedObject.id)
            .join(Tag)
            .filter(
                TaggedObject.object_type == cls.object_type,
                TaggedObject.object_id == target.id,
                Tag.type == TagTypes.owner,
            )
        )
        ids = [row[0] for row in query]
        session.query(TaggedObject).filter(TaggedObject.id.in_(ids)).delete(
            synchronize_session=False
        )

        # add `owner:` tags
        cls._add_owners(session, target)

        session.commit()

    @classmethod
    def after_delete(
        cls,
        _mapper: Mapper,
        connection: Connection,
        target: Union["Dashboard", "FavStar", "Slice"],
    ) -> None:
        """
        删除对象到数据库后要调用的方法，从数据库中删除标签Tag对象。

        :param _mapper: 映射
        :param connection: 连接
        :param target: 对象。
        :return:
        """
        session = Session(bind=connection)

        # delete row from `tagged_objects`
        session.query(TaggedObject).filter(
            TaggedObject.object_type == cls.object_type,
            TaggedObject.object_id == target.id,
        ).delete()

        session.commit()


class ChartUpdater(ObjectUpdater):
    """图表更改器，提供图表对象更改后要调用的方法。"""
    object_type = "chart"

    @classmethod
    def get_owners_ids(cls, target: "Slice") -> List[int]:
        return [owner.id for owner in target.owners]


class DashboardUpdater(ObjectUpdater):
    """仪表盘更改器，提供仪表盘对象更改后要调用的方法。"""

    object_type = "dashboard"

    @classmethod
    def get_owners_ids(cls, target: "Dashboard") -> List[int]:
        return [owner.id for owner in target.owners]


class QueryUpdater(ObjectUpdater):
    """查询更改器，提供查询对象更改后要调用的方法。"""
    object_type = "query"

    @classmethod
    def get_owners_ids(cls, target: "Query") -> List[int]:
        return [target.user_id]


class FavStarUpdater:
    """星级更改器，提供插入和更改后要调用的类方法。"""

    @classmethod
    def after_insert(
        cls, _mapper: Mapper, connection: Connection, target: "FavStar"
    ) -> None:
        """插入后要调用的方法。"""

        session = Session(bind=connection)
        name = "favorited_by:{0}".format(target.user_id)
        tag = get_tag(name, session, TagTypes.favorited_by)
        tagged_object = TaggedObject(
            tag_id=tag.id,
            object_id=target.obj_id,
            object_type=get_object_type(target.class_name),
        )
        session.add(tagged_object)

        session.commit()

    @classmethod
    def after_delete(
        cls, _mapper: Mapper, connection: Connection, target: "FavStar"
    ) -> None:
        """
        删除后要调用的方法。

        :param _mapper:
        :param connection:
        :param target:
        :return:
        """
        session = Session(bind=connection)
        name = "favorited_by:{0}".format(target.user_id)
        query = (
            session.query(TaggedObject.id)
            .join(Tag)
            .filter(
                TaggedObject.object_id == target.obj_id,
                Tag.type == TagTypes.favorited_by,
                Tag.name == name,
            )
        )
        ids = [row[0] for row in query]
        session.query(TaggedObject).filter(TaggedObject.id.in_(ids)).delete(
            synchronize_session=False
        )

        session.commit()
