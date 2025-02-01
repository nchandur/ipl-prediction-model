from utils.utils import *
import pandas as pd
from tqdm import tqdm

query = "SELECT * FROM elo_ratings WHERE winner IS NOT NULL ORDER BY date"

data = retrieveFromDB(query=query)

team_stats = {}
win_percentages = []

for _, row in tqdm(data.iterrows(), desc="Calculating Win Percentages", total=data.shape[0], unit="game"):
    team1, team2 = row['team_1_id'], row['team_2_id']
    winner = row['winner_id']
    
    if team1 not in team_stats:
        team_stats[team1] = {'played': 0, 'won': 0}
    if team2 not in team_stats:
        team_stats[team2] = {'played': 0, 'won': 0}
    
    team1_win_pct = (team_stats[team1]['won'] / team_stats[team1]['played']) if team_stats[team1]['played'] > 0 else 0
    team2_win_pct = (team_stats[team2]['won'] / team_stats[team2]['played']) if team_stats[team2]['played'] > 0 else 0
    
    win_percentages.append({'team_1_win_pct': team1_win_pct, 'team_2_win_pct': team2_win_pct})
    
    team_stats[team1]['played'] += 1
    team_stats[team2]['played'] += 1
    
    if winner == team1:
        team_stats[team1]['won'] += 1
    elif winner == team2:
        team_stats[team2]['won'] += 1

win_percentage_df = pd.DataFrame(win_percentages).round(4)

data = pd.concat([data, win_percentage_df], axis=1)

pushToDB(data=data, tablename="elo_ratings")