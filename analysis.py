import matplotlib.pyplot as plt
import seaborn as sns
from utils.utils import retrieveFromDB
import pandas as pd

def retrieveEloByID(id:int) -> pd.DataFrame:
    
    query = '''
        SELECT date, 
        CASE 
            WHEN team_1_id = {} THEN team_1
            WHEN team_2_id = {} THEN team_2
        END AS team_name,
        CASE 
            WHEN team_1_id = {} THEN team_1_elo
            WHEN team_2_id = {} THEN team_2_elo
        END AS team_elo
        FROM elo_ratings
        WHERE (team_1_id = {} OR team_2_id = {}) AND season = 2024;
        '''.format(id, id, id, id, id, id)


    data = retrieveFromDB(query=query)

    return data

def retrieveRatingsByID(id:int) -> pd.DataFrame:

    query = '''
        SELECT date, 
        CASE 
            WHEN team_1_id = {} THEN team_1
            WHEN team_2_id = {} THEN team_2
        END AS team_name,
        CASE 
            WHEN team_1_id = {} THEN team_1_pts
            WHEN team_2_id = {} THEN team_2_pts
        END AS team_pts
        FROM elo_ratings
        WHERE team_1_id = {} OR team_2_id = {} AND season = 2024;
        '''.format(id, id, id, id, id, id)


    data = retrieveFromDB(query=query)

    return data

def compareEloByID(ids:list) -> pd.DataFrame:
    data_list = [retrieveEloByID(id) for id in ids]

    for data in data_list:
        data["date"] = pd.to_datetime(data["date"])

    start = min([data["date"].min() for data in data_list])
    end = max([data["date"].max() for data in data_list])

    date_range = pd.date_range(start=start, end=end)

    data = pd.DataFrame({"date": date_range})

    for d in data_list:
        data = pd.merge(left=data, right=d, on="date", how="left")

    data = data.ffill()

    return data

def plotElos(ids:list) -> None:

    data = compareEloByID(ids=ids)
    
    sns.set_style("darkgrid")
    plt.figure(figsize=(30, 12))
    sns.lineplot(data=data, x="date", y="team_elo_x", label=data["team_name_x"].iloc[0])
    sns.lineplot(data=data, x="date", y="team_elo_y", label=data["team_name_y"].iloc[0])
    sns.lineplot(data=data, x="date", y="team_elo", label=data["team_name"].iloc[0])
    plt.xlabel("Date")
    plt.ylabel("Elo")
    plt.legend()
    plt.savefig("data/figs/elos.jpg")

def perfOverTime(metric:str, data:pd.DataFrame):
    sns.set_style("darkgrid")

    plt.figure(figsize=(30, 12))
    sns.lineplot(data=data, x="date", y=metric)
    plt.savefig("data/figs/fig.jpg")
