import pandas as pd
from tqdm import tqdm
from utils.utils import *

def calculate_cumulative_stats(data):
    data = data.sort_values(by=["date", "match_id"]).reset_index(drop=True)
    
    data["team_1_rr"] = data["team_1_total"] / (data["team_1_balls"] / 6)
    data["team_2_rr"] = data["team_2_total"] / (data["team_2_balls"] / 6)
    
    data["team_1_nrr"] = (data["team_1_total"] / (data["team_1_balls"] / 6)) - (data["team_2_total"] / (data["team_2_balls"] / 6))
    data["team_2_nrr"] = (data["team_2_total"] / (data["team_2_balls"] / 6)) - (data["team_1_total"] / (data["team_1_balls"] / 6))
    
    cumulative_cols = [
        "cumulative_runs_scored", "cumulative_runs_conceded", "cumulative_balls_faced",
        "cumulative_balls_bowled", "cumulative_wickets_taken", "cumulative_wickets_fallen",
        "cumulative_boundaries_scored", "cumulative_boundaries_conceded"
    ]
    
    team_stats = {}
    
    for team_col, opponent_col in [("team_1", "team_2"), ("team_2", "team_1")]:
        for stat in cumulative_cols:
            data[f"{team_col}_{stat}"] = 0
        
        for team in pd.concat([data["team_1"], data["team_2"]]).unique():
            team_stats[team] = {
                "runs_scored": 0, "runs_conceded": 0, "balls_faced": 0, "balls_bowled": 0,
                "wickets_taken": 0, "wickets_fallen": 0, "boundaries_scored": 0, "boundaries_conceded": 0
            }
    
    for index, row in tqdm(data.iterrows(), total=data.shape[0], unit="game", desc="Calculating Cumulative Statistics"):
        for team_col, opponent_col in [("team_1", "team_2"), ("team_2", "team_1")]:
            team = row[team_col]
            
            team_stats[team]["runs_scored"] += row[f"{team_col}_total"]
            team_stats[team]["runs_conceded"] += row[f"{opponent_col}_total"]
            team_stats[team]["balls_faced"] += row[f"{team_col}_balls"]
            team_stats[team]["balls_bowled"] += row[f"{opponent_col}_balls"]
            team_stats[team]["wickets_taken"] += row[f"{opponent_col}_wickets"]
            team_stats[team]["wickets_fallen"] += row[f"{team_col}_wickets"]
            team_stats[team]["boundaries_scored"] += row[f"{team_col}_boundaries"]
            team_stats[team]["boundaries_conceded"] += row[f"{opponent_col}_boundaries"]
            
            data.at[index, f"{team_col}_cumulative_runs_scored"] = team_stats[team]["runs_scored"]
            data.at[index, f"{team_col}_cumulative_runs_conceded"] = team_stats[team]["runs_conceded"]
            data.at[index, f"{team_col}_cumulative_balls_faced"] = team_stats[team]["balls_faced"]
            data.at[index, f"{team_col}_cumulative_balls_bowled"] = team_stats[team]["balls_bowled"]
            data.at[index, f"{team_col}_cumulative_wickets_taken"] = team_stats[team]["wickets_taken"]
            data.at[index, f"{team_col}_cumulative_wickets_fallen"] = team_stats[team]["wickets_fallen"]
            data.at[index, f"{team_col}_cumulative_boundaries_scored"] = team_stats[team]["boundaries_scored"]
            data.at[index, f"{team_col}_cumulative_boundaries_conceded"] = team_stats[team]["boundaries_conceded"]
    
    return data

# def calculate_performance_indices(data):

data = retrieveFromDB(query="SELECT * FROM elo_ratings")
data = calculate_cumulative_stats(data=data)

pushToDB(data=data, tablename="elo_ratings")