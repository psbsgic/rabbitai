# -*- coding: utf-8 -*-

from typing import Any, cast, Optional

from flask_appbuilder.models.filters import BaseFilter
from flask_babel import lazy_gettext
from sqlalchemy import or_
from sqlalchemy.orm import Query

from rabbitai import security_manager


class FilterRelatedOwners(BaseFilter):
    """
    A filter to allow searching for related owners of a resource.

    Use in the api by adding something like:
    related_field_filters = {
      "owners": RelatedFieldFilter("first_name", FilterRelatedOwners),
    }
    """

    name = lazy_gettext("Owner")
    arg_name = "owners"

    def apply(self, query: Query, value: Optional[Any]) -> Query:
        user_model = security_manager.user_model
        like_value = "%" + cast(str, value) + "%"
        return query.filter(
            or_(
                # could be made to handle spaces between names more gracefully
                (user_model.first_name + " " + user_model.last_name).ilike(like_value),
                user_model.username.ilike(like_value),
            )
        )
