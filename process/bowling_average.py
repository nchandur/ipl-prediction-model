from utils.utils import *
import pandas as pd
import numpy as np
from tqdm import tqdm

query = "SELECT * FROM bowling"

data = retrieveFromDB(query=query)

data['date'] = pd.to_datetime(data['date'])

data.sort_values(by=['player_id', 'date'], inplace=True)

data['bowling_avg'] = 0.0
data['econ_over_time'] = 0.0
data["strike_rate_over_time"] = 0.0
data["balls_per_innings"] = 0.0
data["wickets_idx"] = 0.0
data["big_impact_idx"] = 0.0
data["small_impact_idx"] = 0.0
data["runs_idx"] = 0.0

groups = data.groupby('player_id', group_keys=False)

for _, group in tqdm(groups, desc="Calculating Bowling Average", unit="player"):
    
    cumulative_runs_conceded = group['runs'].cumsum().shift(fill_value=0)
    cumulative_wickets = group['wickets'].cumsum().shift(fill_value=0)
    cumulative_balls = group['balls'].cumsum().shift(fill_value=0)
    cumulative_overs = cumulative_balls / 6.0
    cumulative_big = (group["wickets"] >= 3).cumsum()
    cumulative_small = (group["wickets"] == 3).cumsum()
    cumulative_wickets.replace(0, 1, inplace=True)

    innings = group.groupby('player_id').cumcount()

    data.loc[group.index, 'bowling_avg'] = cumulative_runs_conceded / cumulative_wickets
    data.loc[group.index, 'econ_over_time'] = cumulative_runs_conceded / cumulative_overs
    data.loc[group.index, 'balls_per_innings'] = cumulative_balls / innings
    data.loc[group.index, 'wickets_idx'] = np.where(innings > 0, cumulative_wickets / innings, 0)
    data.loc[group.index, 'big_impact_idx'] = cumulative_big / innings
    data.loc[group.index, 'small_impact_idx'] = cumulative_small / innings
    data.loc[group.index, 'runs_idx'] = cumulative_runs_conceded / innings
    data.loc[group.index, 'strike_rate_over_time'] = cumulative_balls / cumulative_wickets

pushToDB(data=data, tablename="bowling")