import pandas as pd

data = pd.read_csv("data/raw/details.csv")

data.columns = ["match_type", "stadium", "toss", "player_of_the_match", "match_days", "match_id"]

data["date"] = data["match_days"].str.extract(r"(.+) \-")
data["time"] = data["match_days"].str.extract(r"\-(.+?)\(")

data.drop(columns=["match_days"], inplace=True)

data = data.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
data['date'] = pd.to_datetime(data['date'], format='mixed', dayfirst=True)

data['season'] = data['date'].dt.year

total = pd.read_csv("data/processed/total.csv")

first = total[total["innings"] == 1]
second = total[total["innings"] == 2]

merged = pd.merge(data, first[["match_id", "team"]], how="left", left_on="match_id", right_on="match_id")
merged = merged.rename(columns={"team": "team_1"})

merged = pd.merge(merged, second[["match_id", "team"]], how="left", left_on="match_id", right_on="match_id")
merged = merged.rename(columns={"team": "team_2"})

merged.to_csv("data/processed/details.csv", index=False)