from os import environ

import pandas as pd
import snowflake.connector
from snowflake.connector import DictCursor
from .settings import Settings

settings = Settings().snowflake

USER=settings.user
PASSWORD=settings.password
ROLE=settings.role
ACCOUNT=settings.account
WAREHOUSE=settings.warehouse
DATABASE=settings.database

def quick_fetch_frame(sql):
    with Snowflake() as db:
        data = db.get_frame(sql)
    return data


def fetch_from_sql_file(fname, **kwargs):
    with open(fname, 'r') as f:
        sql = f.read()
    sql = sql.format(**kwargs)
    return quick_fetch_frame(sql)


class Snowflake:

    def __init__(self):

        self.con = snowflake.connector.connect(
            user=USER,
            password=PASSWORD,
            account=ACCOUNT,
        )

        cs = self.con.cursor()
        cs.execute("USE role {}".format(ROLE))
        cs.execute("USE warehouse {}".format(WAREHOUSE))
        cs.execute("USE database {}".format(DATABASE))

    def execute(self, sql):
        cs = self.con.cursor(DictCursor)
        cs.execute(sql)
        return cs

    def get_frame(self, sql):
        cs = self.execute(sql)
        frame = pd.DataFrame([dict(row) for row in cs])
        cs.close()
        frame.columns = [c.lower() for c in frame.columns]
        return frame

    def close(self):
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
