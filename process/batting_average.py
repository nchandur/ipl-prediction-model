import numpy as np
import pandas as pd
from utils.utils import *
from tqdm import tqdm

query = "SELECT * FROM batting"

data = retrieveFromDB(query=query)
data["date"] = pd.to_datetime(data["date"])
data.sort_values(by=['player_id', 'date'], inplace=True)

data['batting_avg'] = 0.0
data['strike_rate_over_time'] = 0.0
data["boundary_per_ball"] = 0.0
data["boundary_idx"] = 0.0
data["finishing_idx"] = 0.0
data["runs_without_boundary"] = 0.0
data["big_impact_idx"] = 0.0

groups = data.groupby("player_id", group_keys=False)

for _, group in tqdm(groups, desc="Calculating Batting Average", unit="player"):
    cumulative_runs = group['runs'].cumsum().shift(fill_value=0)
    cumulative_balls = group['balls'].cumsum().shift(fill_value=0)
    cumulative_boundaries = (group['fours'] + group['sixes']).cumsum().shift(fill_value=0)
    cumulative_50 = ((group["runs"] >= 50) & (group['runs'] < 100)).cumsum()
    cumulative_100 = (group["runs"] >= 100).cumsum()

    innings = group.groupby('player_id').cumcount()
    dismissals = (~group['dismissal_info'].str.contains("not out", case=False, na=False)).cumsum()
    dismissals.replace(0, 1, inplace=True)
    
    data.loc[group.index, 'batting_avg'] = cumulative_runs / dismissals
    data.loc[group.index, 'strike_rate_over_time'] = (cumulative_runs / cumulative_balls) * 100
    data.loc[group.index, 'boundary_per_ball'] = cumulative_boundaries / cumulative_balls
    data.loc[group.index, 'boundary_idx'] = cumulative_boundaries / innings
    data.loc[group.index, 'finishing_idx'] = np.where(innings > 0, dismissals / innings, 0)
    data.loc[group.index, 'runs_without_boundary'] = (cumulative_runs - cumulative_boundaries) / innings
    data.loc[group.index, 'big_impact_idx'] = ((2 * cumulative_100) + cumulative_50) / innings

data = data.fillna(value=0).round(4)

pushToDB(data=data, tablename="batting")