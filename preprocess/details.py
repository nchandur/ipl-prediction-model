import pandas as pd

data = pd.read_csv("data/raw/details.csv", header=None)
data.columns = [
    "match_type",
    "team_1",
    "team_2",
    "stadium",
    "toss",
    "player_of_the_match",
    "match_days",
    "match_id",
]

data["match_days"] = data["match_days"].fillna(data["player_of_the_match"])
data.loc[data["player_of_the_match"] == data["match_days"], "player_of_the_match"] = (
    None
)

data["date"] = data["match_days"].str.extract(r"(.+) \-")
data["time"] = data["match_days"].str.extract(r"\-(.+?)\(")

data.drop(columns=["match_days"], inplace=True)

data = data.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
data["date"] = pd.to_datetime(data["date"], format="mixed", dayfirst=True)

data["season"] = data["date"].dt.year

data.to_csv("data/preprocessed/details.csv", index=False)