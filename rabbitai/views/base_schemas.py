from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Union

from flask import current_app, g
from flask_appbuilder import Model
from marshmallow import post_load, pre_load, Schema, ValidationError
from sqlalchemy.orm.exc import NoResultFound


def validate_owner(value: int) -> None:
    try:
        (
            current_app.appbuilder.get_session.query(
                current_app.appbuilder.sm.user_model.id
            )
            .filter_by(id=value)
            .one()
        )
    except NoResultFound:
        raise ValidationError(f"User {value} does not exist")


class BaseRabbitaiSchema(Schema):
    """
    Extends Marshmallow schema so that we can pass a Model to load
    (following marshamallow-sqlalchemy pattern). This is useful
    to perform partial model merges on HTTP PUT
    """

    __class_model__: Model = None

    def __init__(self, **kwargs: Any) -> None:
        """模型Model实例"""
        self.instance: Optional[Model] = None
        super().__init__(**kwargs)

    def load(
        self,
        data: Union[Mapping[str, Any], Iterable[Mapping[str, Any]]],
        many: Optional[bool] = None,
        partial: Union[bool, Sequence[str], Set[str], None] = None,
        instance: Optional[Model] = None,
        **kwargs: Any,
    ) -> Any:
        """
        反序列化指定数据为该架构的对象实例。

        :param data: 数据（属性名称/值的映射、属性名称/值的映射的迭代器）。
        :param many: 是否多对象。
        :param partial: 是否部分。
        :param instance: 模型实例。
        :param kwargs: 其它关键字参数。
        :return:
        """
        self.instance = instance
        if many is None:
            many = False
        if partial is None:
            partial = False
        return super().load(data, many=many, partial=partial, **kwargs)

    @post_load
    def make_object(
        self, data: Dict[Any, Any], discard: Optional[List[str]] = None
    ) -> Model:
        """
        反序列化后要调用的方法，依据 POST 或 PUT 请求创建一个模型对象。PUT 将使用端点处理提取的 self.instance。

        :param data: Schema data payload
        :param discard: List of fields to not set on the model
        """

        discard = discard or []
        if not self.instance:
            self.instance = self.__class_model__()

        for field in data:
            if field not in discard:
                setattr(self.instance, field, data.get(field))

        return self.instance


class BaseOwnedSchema(BaseRabbitaiSchema):
    """基本拥有者架构，反序列化前后进行拥有者验证。"""

    owners_field_name = "owners"

    @post_load
    def make_object(
        self, data: Dict[str, Any], discard: Optional[List[str]] = None
    ) -> Model:
        discard = discard or []
        discard.append(self.owners_field_name)
        instance = super().make_object(data, discard)
        if "owners" not in data and g.user not in instance.owners:
            instance.owners.append(g.user)
        if self.owners_field_name in data:
            self.set_owners(instance, data[self.owners_field_name])
        return instance

    @pre_load
    def pre_load(self, data: Dict[Any, Any]) -> None:
        # if PUT request don't set owners to empty list
        if not self.instance:
            data[self.owners_field_name] = data.get(self.owners_field_name, [])

    @staticmethod
    def set_owners(instance: Model, owners: List[int]) -> None:
        owner_objs = list()
        if g.user.get_id() not in owners:
            owners.append(g.user.get_id())
        for owner_id in owners:
            user = current_app.appbuilder.get_session.query(
                current_app.appbuilder.sm.user_model
            ).get(owner_id)
            owner_objs.append(user)
        instance.owners = owner_objs
