from typing import List, Optional

from rabbitai import ConnectorRegistry, db, security_manager
from rabbitai.models.slice import Slice


class InsertChartMixin:
    """
    Implements shared logic for tests to insert charts (slices) in the DB
    """

    def insert_chart(
        self,
        slice_name: str,
        owners: List[int],
        datasource_id: int,
        created_by=None,
        datasource_type: str = "table",
        description: Optional[str] = None,
        viz_type: Optional[str] = None,
        params: Optional[str] = None,
        cache_timeout: Optional[int] = None,
    ) -> Slice:
        obj_owners = list()
        for owner in owners:
            user = db.session.query(security_manager.user_model).get(owner)
            obj_owners.append(user)
        datasource = ConnectorRegistry.get_datasource(
            datasource_type, datasource_id, db.session
        )
        slice = Slice(
            cache_timeout=cache_timeout,
            created_by=created_by,
            datasource_id=datasource.id,
            datasource_name=datasource.name,
            datasource_type=datasource.type,
            description=description,
            owners=obj_owners,
            params=params,
            slice_name=slice_name,
            viz_type=viz_type,
        )
        db.session.add(slice)
        db.session.commit()
        return slice
