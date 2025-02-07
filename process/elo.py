from tqdm import tqdm
from utils.utils import *

data = retrieveFromDB(query="SELECT * FROM matches ORDER BY date")

elo_ratings = {}

data["team_1_elo"] = 0.0
data["team_2_elo"] = 0.0

for index, row in tqdm(
    data.iterrows(), total=data.shape[0], unit="game", desc="Calculating Elo"
):
    team_1, team_2, winner = row["team_1_id"], row["team_2_id"], row["winner_id"]

    team_1_elo = elo_ratings.get(team_1, 1500)
    team_2_elo = elo_ratings.get(team_2, 1500)

    data.at[index, "team_1_elo"] = team_1_elo
    data.at[index, "team_2_elo"] = team_2_elo

    expected_1 = 1 / (1 + 10 ** ((team_2_elo - team_1_elo) / 400))
    expected_2 = 1 - expected_1

    score_1 = 1 if winner == team_1 else 0
    score_2 = 1 - score_1

    new_team_1_elo = team_1_elo + 32 * (score_1 - expected_1)
    new_team_2_elo = team_2_elo + 32 * (score_2 - expected_2)

    elo_ratings[team_1] = new_team_1_elo
    elo_ratings[team_2] = new_team_2_elo

pushToDB(data=data, tablename="matches")
