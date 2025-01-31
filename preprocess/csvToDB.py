import pandas as pd
from sqlalchemy import create_engine
import json

with open("config.json") as file:
    config = json.load(file)

engine = create_engine(
    "postgresql://{}:{}@{}:{}/{}".format(
        config["user"],
        config["password"],
        config["host"],
        config["port"],
        config["database"],
    )
)

print("Importing batting to PSQL")
batting = pd.read_csv("data/preprocessed/batting.csv")
batting.to_sql("batting", con=engine, index=False, if_exists="replace")

print("Importing bowling to PSQL")
bowling = pd.read_csv("data/preprocessed/bowling.csv")
bowling.to_sql("bowling", con=engine, index=False, if_exists="replace")

print("Importing details to PSQL")
details = pd.read_csv("data/preprocessed/details.csv")
details.to_sql("details", con=engine, index=False, if_exists="replace")

print("Importing total to PSQL")
total = pd.read_csv("data/preprocessed/total.csv")
total.to_sql("total", con=engine, index=False, if_exists="replace")

print("Importing extras to PSQL")
extras = pd.read_csv("data/preprocessed/extras.csv")
extras.to_sql("extras", con=engine, index=False, if_exists="replace")
