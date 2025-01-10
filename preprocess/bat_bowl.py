import pandas as pd
import re
from tqdm import tqdm
import os


def parseExtras(row):
    res = {
        "byes": 0,
        "leg_byes": 0,
        "no_balls": 0,
        "wides": 0,
        "extras": 0,
        "innings": 0,
        "team": 0,
        "match_id": 0,
    }
    try:
        text = row["dismissal_info"].replace("(", "").replace(")", "")

        for m in re.compile(r"^b (\d+)").finditer(text):
            res["byes"] = m.group(1)

        for m in re.compile(r"lb (\d+)").finditer(text):
            res["leg_byes"] = m.group(1)

        for m in re.compile(r"nb (\d+)").finditer(text):
            res["no_balls"] = m.group(1)

        for m in re.compile(r"w (\d+)").finditer(text):
            res["wides"] = m.group(1)
    except:
        pass

    res["extras"] = row["runs"]
    res["innings"] = row["innings"]
    res["team"] = row["team"]
    res["match_id"] = row["match_id"]

    return res


def extractExtras(extras):
    results = []

    n = len(extras)

    for _, row in tqdm(extras.iterrows(), total=n):
        results.append(parseExtras(row))

    return pd.DataFrame(results)


def parseTotal(row):
    res = {
        "overs": 0,
        "run_rate": 0,
        "total": 0,
        "wickets": 0,
        "innings": 0,
        "team": 0,
        "match_id": 0,
    }

    totalWithLoss = re.compile(r"(\d+)\/(\d+)")
    totalNoLoss = re.compile(r"\d+")

    try:
        for m in re.compile(r"(.+?)Ov").finditer(row["dismissal_info"]):
            res["overs"] = m.group(1).strip()

        for m in re.compile(r"RR:(.+?)\)").finditer(row["dismissal_info"]):
            res["run_rate"] = m.group(1).strip()

        for m in totalWithLoss.finditer(row["runs"]):
            res["total"] = m.group(1).strip()
            res["wickets"] = m.group(2).strip()

        if res["total"] == 0:
            for m in totalNoLoss.finditer(row["runs"]):
                res["total"] = m.group(0).strip()
                res["wickets"] = 10

        res["innings"] = row["innings"]
        res["match_id"] = row["match_id"]
        res["team"] = row["team"]

    except:
        pass

    return res


def extractTotal(total: pd.DataFrame):
    results = []
    n = len(total)

    for _, row in tqdm(total.iterrows(), total=n):
        results.append(parseTotal(row=row))

    return pd.DataFrame(results)


data = pd.read_csv("data/raw/batting.csv")

# rename columns
data.columns = [
    "player_name",
    "dismissal_info",
    "runs",
    "balls",
    "minutes_played",
    "fours",
    "sixes",
    "strike_rate",
    "innings",
    "team",
    "match_id",
]

# remove columns for extras and total
dropCols = ["player_name", "balls", "minutes_played", "fours", "sixes", "strike_rate"]

extras = data[data["player_name"] == "Extras"].reset_index(drop=True)
total = data[data["player_name"] == "Total"].reset_index(drop=True)

extras.drop(columns=dropCols, inplace=True)
total.drop(columns=dropCols, inplace=True)

total = extractTotal(total=total)
extras = extractExtras(extras=extras)


data = data[~data["player_name"].isin(["Extras", "Total"])].reset_index(drop=True)

data["player_name"] = data["player_name"].str.replace(r"\(c\)", "", regex=True)
data["player_name"] = data["player_name"].str.replace(r"[^a-zA-Z0-9\s]", "", regex=True)
data["minutes_played"] = data["minutes_played"].str.replace("-", "", regex=False)


data = data.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

destination = "data/preprocessed"

if not os.path.exists(destination):
    os.mkdir(destination)

total.to_csv(os.path.join(destination, "total.csv"), index=False)
extras.to_csv(os.path.join(destination, "extras.csv"), index=False)
data.to_csv(os.path.join(destination, "batting.csv"), index=False)

data = pd.read_csv("data/raw/bowling.csv")
data.columns = [
    "player_name",
    "overs",
    "m",
    "runs",
    "wickets",
    "econ",
    "dots",
    "fours",
    "sixes",
    "wides",
    "no_balls",
    "innings",
    "team",
    "match_id",
]

data.to_csv(os.path.join(destination, "bowling.csv"), index=False)
