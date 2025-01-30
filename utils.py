import json
import pandas as pd
from sqlalchemy import create_engine

with open("config.json") as file:
    config = json.load(file)

def retrieveFromDB(query:str) -> pd.DataFrame:

    engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(config["user"], config["password"], config["host"], config["port"], config["database"]))

    try:
        data = pd.read_sql_query(query, engine)
    except:
        data = pd.DataFrame()

    return data
