import json

import pandas as pd
import polyline
from sqlalchemy import String, Text

from rabbitai import db
from rabbitai.utils.core import get_example_database

from .helpers import get_example_data, get_table_connector_registry


def load_bart_lines(only_metadata: bool = False, force: bool = False) -> None:
    tbl_name = "San Franciso BART Lines"
    database = get_example_database()
    table_exists = database.has_table_by_name(tbl_name)

    if not only_metadata and (not table_exists or force):
        content = get_example_data("bart-lines.json.gz")
        df = pd.read_json(content, encoding="latin-1")
        df["path_json"] = df.path.map(json.dumps)
        df["polyline"] = df.path.map(polyline.encode)
        del df["path"]

        df.to_sql(
            tbl_name,
            database.get_sqla_engine(),
            if_exists="replace",
            chunksize=500,
            dtype={
                "color": String(255),
                "name": String(255),
                "polyline": Text,
                "path_json": Text,
            },
            index=False,
        )

    print("Creating table {} reference".format(tbl_name))
    table = get_table_connector_registry()
    tbl = db.session.query(table).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = table(table_name=tbl_name)
    tbl.description = "BART lines"
    tbl.database = database
    tbl.filter_select_enabled = True
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()
