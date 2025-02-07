from utils.utils import retrieveFromDB, pushToDB
from tqdm import tqdm

query = "SELECT * FROM details WHERE winner IS NOT NULL ORDER BY date"

data = retrieveFromDB(query=query)

points = {}

team_1_points_list = []
team_2_points_list = []

for index, row in tqdm(
    data.iterrows(), total=data.shape[0], desc="Calculating Points", unit="game"
):
    team_1 = row["team_1_id"]
    team_2 = row["team_2_id"]
    winner = row["winner_id"]

    points_1 = points.get(team_1, 0)
    points_2 = points.get(team_2, 0)

    team_1_points_list.append(points_1)
    team_2_points_list.append(points_2)

    diff = abs(points_1 - points_2)

    if points_1 > points_2:
        strong_team, weak_team = team_1, team_2
        strong_points, weak_points = points_1, points_2
    else:
        strong_team, weak_team = team_2, team_1
        strong_points, weak_points = points_2, points_1

    if diff >= 4:
        if winner == strong_team:
            points[strong_team] = strong_points + 1
            points[weak_team] = weak_points - 1
        else:
            points[weak_team] = weak_points + 9
            points[strong_team] = strong_points - 9
    else:
        if winner == team_1:
            points[team_1] = points_1 + 5
            points[team_2] = points_2 - 5
        else:
            points[team_2] = points_2 + 5
            points[team_1] = points_1 - 5

data["team_1_pts"] = team_1_points_list
data["team_2_pts"] = team_2_points_list

pushToDB(data=data, tablename="matches")
