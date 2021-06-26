import json

from rabbitai import db
from rabbitai.models.slice import Slice

from .birth_names import load_birth_names
from .helpers import merge_slice, misc_dash_slices
from .world_bank import load_world_bank_health_n_pop


def load_multi_line(only_metadata: bool = False) -> None:
    load_world_bank_health_n_pop(only_metadata)
    load_birth_names(only_metadata)
    ids = [
        row.id
        for row in db.session.query(Slice).filter(
            Slice.slice_name.in_(["Growth Rate", "Trends"])
        )
    ]

    slc = Slice(
        datasource_type="table",  # not true, but needed
        datasource_id=1,  # cannot be empty
        slice_name="Multi Line",
        viz_type="line_multi",
        params=json.dumps(
            {
                "slice_name": "Multi Line",
                "viz_type": "line_multi",
                "line_charts": [ids[0]],
                "line_charts_2": [ids[1]],
                "since": "1970",
                "until": "1995",
                "prefix_metric_with_slice_name": True,
                "show_legend": False,
                "x_axis_format": "%Y",
            }
        ),
    )

    misc_dash_slices.add(slc.slice_name)
    merge_slice(slc)
