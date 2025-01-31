import json
import pandas as pd
from sqlalchemy import create_engine

with open("config.json") as file:
    config = json.load(file)

engine = create_engine(
    "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        config["user"],
        config["password"],
        config["host"],
        config["port"],
        config["database"],
    )
)


def retrieveFromDB(query: str) -> pd.DataFrame:

    try:
        data = pd.read_sql_query(query, engine)
    except:
        data = pd.DataFrame()

    return data


def pushToDB(data: pd.DataFrame, tablename: str) -> None:
    data.to_sql(tablename, con=engine, index=False, if_exists="replace")
