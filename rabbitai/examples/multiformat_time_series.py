from typing import Dict, Optional, Tuple

import pandas as pd
from sqlalchemy import BigInteger, Date, DateTime, String

from rabbitai import db
from rabbitai.models.slice import Slice
from rabbitai.utils.core import get_example_database

from .helpers import (
    config,
    get_example_data,
    get_slice_json,
    merge_slice,
    misc_dash_slices,
    TBL,
)


def load_multiformat_time_series(
    only_metadata: bool = False, force: bool = False
) -> None:
    """Loading time series data from a zip file in the repo"""
    tbl_name = "multiformat_time_series"
    database = get_example_database()
    table_exists = database.has_table_by_name(tbl_name)

    if not only_metadata and (not table_exists or force):
        data = get_example_data("multiformat_time_series.json.gz")
        pdf = pd.read_json(data)
        # TODO(bkyryliuk): move load examples data into the pytest fixture
        if database.backend == "presto":
            pdf.ds = pd.to_datetime(pdf.ds, unit="s")
            pdf.ds = pdf.ds.dt.strftime("%Y-%m-%d")
            pdf.ds2 = pd.to_datetime(pdf.ds2, unit="s")
            pdf.ds2 = pdf.ds2.dt.strftime("%Y-%m-%d %H:%M%:%S")
        else:
            pdf.ds = pd.to_datetime(pdf.ds, unit="s")
            pdf.ds2 = pd.to_datetime(pdf.ds2, unit="s")

        pdf.to_sql(
            tbl_name,
            database.get_sqla_engine(),
            if_exists="replace",
            chunksize=500,
            dtype={
                "ds": String(255) if database.backend == "presto" else Date,
                "ds2": String(255) if database.backend == "presto" else DateTime,
                "epoch_s": BigInteger,
                "epoch_ms": BigInteger,
                "string0": String(100),
                "string1": String(100),
                "string2": String(100),
                "string3": String(100),
            },
            index=False,
        )
        print("Done loading table!")
        print("-" * 80)

    print(f"Creating table [{tbl_name}] reference")
    obj = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not obj:
        obj = TBL(table_name=tbl_name)
    obj.main_dttm_col = "ds"
    obj.database = database
    dttm_and_expr_dict: Dict[str, Tuple[Optional[str], None]] = {
        "ds": (None, None),
        "ds2": (None, None),
        "epoch_s": ("epoch_s", None),
        "epoch_ms": ("epoch_ms", None),
        "string2": ("%Y%m%d-%H%M%S", None),
        "string1": ("%Y-%m-%d^%H:%M:%S", None),
        "string0": ("%Y-%m-%d %H:%M:%S.%f", None),
        "string3": ("%Y/%m/%d%H:%M:%S.%f", None),
    }
    for col in obj.columns:
        dttm_and_expr = dttm_and_expr_dict[col.column_name]
        col.python_date_format = dttm_and_expr[0]
        col.dbatabase_expr = dttm_and_expr[1]
        col.is_dttm = True
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj

    print("Creating Heatmap charts")
    for i, col in enumerate(tbl.columns):
        slice_data = {
            "metrics": ["count"],
            "granularity_sqla": col.column_name,
            "row_limit": config["ROW_LIMIT"],
            "since": "2015",
            "until": "2016",
            "viz_type": "cal_heatmap",
            "domain_granularity": "month",
            "subdomain_granularity": "day",
        }

        slc = Slice(
            slice_name=f"Calendar Heatmap multiformat {i}",
            viz_type="cal_heatmap",
            datasource_type="table",
            datasource_id=tbl.id,
            params=get_slice_json(slice_data),
        )
        merge_slice(slc)
    misc_dash_slices.add("Calendar Heatmap multiformat 0")
