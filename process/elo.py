from utils.utils import retrieveFromDB, pushToDB
from tqdm import tqdm

query = "SELECT * FROM details WHERE winner IS NOT NULL ORDER BY date"

data = retrieveFromDB(query=query)

elo_ratings = {}

team_1_elo_list = []
team_2_elo_list = []

for index, row in tqdm(
    data.iterrows(), total=data.shape[0], desc="Calculating Elo", unit="game"
):
    team_1 = row["team_1_id"]
    team_2 = row["team_2_id"]
    winner = row["winner_id"]

    elo_1 = elo_ratings.get(team_1, 0)
    elo_2 = elo_ratings.get(team_2, 0)

    team_1_elo_list.append(elo_1)
    team_2_elo_list.append(elo_2)

    diff = abs(elo_1 - elo_2)

    if elo_1 > elo_2:
        strong_team, weak_team = team_1, team_2
        strong_elo, weak_elo = elo_1, elo_2
    else:
        strong_team, weak_team = team_2, team_1
        strong_elo, weak_elo = elo_2, elo_1

    if diff >= 4:
        if winner == strong_team:
            elo_ratings[strong_team] = strong_elo + 1
            elo_ratings[weak_team] = weak_elo - 1
        else:
            elo_ratings[weak_team] = weak_elo + 9
            elo_ratings[strong_team] = strong_elo - 9
    else:
        if winner == team_1:
            elo_ratings[team_1] = elo_1 + 5
            elo_ratings[team_2] = elo_2 - 5
        else:
            elo_ratings[team_2] = elo_2 + 5
            elo_ratings[team_1] = elo_1 - 5

data["team_1_elo"] = team_1_elo_list
data["team_2_elo"] = team_2_elo_list

pushToDB(data=data, tablename="matches")