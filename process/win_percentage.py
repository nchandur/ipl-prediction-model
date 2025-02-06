import pandas as pd
from utils.utils import *
    

data = retrieveFromDB(query="SELECT * FROM details")

data = data.sort_values('date')

win_count, game_count = {}, {}
h2h_wins, h2h_games = {}, {}
stadium_wins, stadium_games = {}, {}
h2h_stadium_wins, h2h_stadium_games = {}, {}

team_1_win_pct, team_2_win_pct = [], []
team_1_h2h_win_pct, team_2_h2h_win_pct = [], []
team_1_stadium_win_pct, team_2_stadium_win_pct = [], []
team_1_h2h_stadium_win_pct, team_2_h2h_stadium_win_pct = [], []

for _, row in data.iterrows():
    team1, team2, winner, stadium = row['team_1_id'], row['team_2_id'], row['winner_id'], row['stadium']
    
    t1_win_pct = win_count.get(team1, 0) / game_count.get(team1, 1)
    t2_win_pct = win_count.get(team2, 0) / game_count.get(team2, 1)
    team_1_win_pct.append(t1_win_pct)
    team_2_win_pct.append(t2_win_pct)

    matchup = tuple(sorted([team1, team2]))
    t1_h2h_wins = h2h_wins.get((team1, team2), 0)
    t2_h2h_wins = h2h_wins.get((team2, team1), 0)
    h2h_total_games = h2h_games.get(matchup, 1)

    t1_h2h_pct = t1_h2h_wins / h2h_total_games
    t2_h2h_pct = t2_h2h_wins / h2h_total_games
    team_1_h2h_win_pct.append(t1_h2h_pct)
    team_2_h2h_win_pct.append(t2_h2h_pct)

    team1_stadium_key, team2_stadium_key = (team1, stadium), (team2, stadium)
    t1_stadium_wins = stadium_wins.get(team1_stadium_key, 0)
    t2_stadium_wins = stadium_wins.get(team2_stadium_key, 0)
    t1_stadium_games = stadium_games.get(team1_stadium_key, 1)
    t2_stadium_games = stadium_games.get(team2_stadium_key, 1)

    t1_stadium_pct = t1_stadium_wins / t1_stadium_games
    t2_stadium_pct = t2_stadium_wins / t2_stadium_games
    team_1_stadium_win_pct.append(t1_stadium_pct)
    team_2_stadium_win_pct.append(t2_stadium_pct)

    h2h_stadium_matchup = (matchup, stadium)
    t1_h2h_stadium_wins = h2h_stadium_wins.get((team1, team2, stadium), 0)
    t2_h2h_stadium_wins = h2h_stadium_wins.get((team2, team1, stadium), 0)
    h2h_stadium_total_games = h2h_stadium_games.get(h2h_stadium_matchup, 1)

    t1_h2h_stadium_pct = t1_h2h_stadium_wins / h2h_stadium_total_games
    t2_h2h_stadium_pct = t2_h2h_stadium_wins / h2h_stadium_total_games
    team_1_h2h_stadium_win_pct.append(t1_h2h_stadium_pct)
    team_2_h2h_stadium_win_pct.append(t2_h2h_stadium_pct)

    game_count[team1] = game_count.get(team1, 0) + 1
    game_count[team2] = game_count.get(team2, 0) + 1

    if winner == team1:
        win_count[team1] = win_count.get(team1, 0) + 1
    elif winner == team2:
        win_count[team2] = win_count.get(team2, 0) + 1

    h2h_games[matchup] = h2h_games.get(matchup, 0) + 1
    if winner == team1:
        h2h_wins[(team1, team2)] = h2h_wins.get((team1, team2), 0) + 1
    elif winner == team2:
        h2h_wins[(team2, team1)] = h2h_wins.get((team2, team1), 0) + 1

    stadium_games[team1_stadium_key] = stadium_games.get(team1_stadium_key, 0) + 1
    stadium_games[team2_stadium_key] = stadium_games.get(team2_stadium_key, 0) + 1

    if winner == team1:
        stadium_wins[team1_stadium_key] = stadium_wins.get(team1_stadium_key, 0) + 1
    elif winner == team2:
        stadium_wins[team2_stadium_key] = stadium_wins.get(team2_stadium_key, 0) + 1

    h2h_stadium_games[h2h_stadium_matchup] = h2h_stadium_games.get(h2h_stadium_matchup, 0) + 1
    if winner == team1:
        h2h_stadium_wins[(team1, team2, stadium)] = h2h_stadium_wins.get((team1, team2, stadium), 0) + 1
    elif winner == team2:
        h2h_stadium_wins[(team2, team1, stadium)] = h2h_stadium_wins.get((team2, team1, stadium), 0) + 1

data['team_1_win_pct'] = team_1_win_pct
data['team_2_win_pct'] = team_2_win_pct
data['team_1_h2h_win_pct'] = team_1_h2h_win_pct
data['team_2_h2h_win_pct'] = team_2_h2h_win_pct
data['team_1_stadium_win_pct'] = team_1_stadium_win_pct
data['team_2_stadium_win_pct'] = team_2_stadium_win_pct
data['team_1_h2h_stadium_win_pct'] = team_1_h2h_stadium_win_pct
data['team_2_h2h_stadium_win_pct'] = team_2_h2h_stadium_win_pct

pushToDB(data=data, tablename="details")