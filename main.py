import pandas as pd
from utils import retrieveFromDB



query = "SELECT player_name, runs, balls, fours, sixes FROM batting"

data = retrieveFromDB(query=query)

data["batPoints"] = (data["runs"]) + (data["fours"]) + (data["sixes"]) 

data.loc[(data["runs"] >= 30) & (data["runs"] < 50), "batPoints"] += 4
data.loc[(data["runs"] >= 50) & (data["runs"] < 100), "batPoints"] += 8
data.loc[(data["runs"] >= 100), "batPoints"] += 16
data.loc[(data["runs"] == 0) & (data["balls"] > 0), "batPoints"] -= 2
