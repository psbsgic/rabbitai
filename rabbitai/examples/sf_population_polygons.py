import json

import pandas as pd
from sqlalchemy import BigInteger, Float, Text

from rabbitai import db
from rabbitai.utils import core as utils

from .helpers import get_example_data, TBL


def load_sf_population_polygons(
    only_metadata: bool = False, force: bool = False
) -> None:
    tbl_name = "sf_population_polygons"
    database = utils.get_example_database()
    table_exists = database.has_table_by_name(tbl_name)

    if not only_metadata and (not table_exists or force):
        data = get_example_data("sf_population.json.gz")
        df = pd.read_json(data)
        df["contour"] = df.contour.map(json.dumps)

        df.to_sql(
            tbl_name,
            database.get_sqla_engine(),
            if_exists="replace",
            chunksize=500,
            dtype={
                "zipcode": BigInteger,
                "population": BigInteger,
                "contour": Text,
                "area": Float,
            },
            index=False,
        )

    print("Creating table {} reference".format(tbl_name))
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = "Population density of San Francisco"
    tbl.database = database
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()
