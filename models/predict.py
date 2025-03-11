import xgboost
import pandas as pd
from utils.utils import retrieveFromDB

def get_info(id:int, feature:str) -> float:
    query = '''
    SELECT                                                                                        
    CASE 
        WHEN team_1_id = {} THEN team_1_{}
        WHEN team_2_id = {} THEN team_2_{}
    END AS {}
    FROM matches 
    WHERE team_1_id = {} OR team_2_id = {}
    ORDER BY date DESC 
    LIMIT 1;
    '''.format(id, feature, id, feature, feature, id, id)

    data = retrieveFromDB(query=query)

    return data.values[0][0]

def get_latest_info(teams:list) -> pd.DataFrame:
    features = ['h2h_win_pct', 'boundary_inv_idx', 'cumulative_boundaries_scored', 'nrr', 'balls', 'h2h_stadium_win_pct', 'cumulative_balls_faced', 'cumulative_wickets_taken', 'boundaries_scored_per_over', 'cumulative_boundaries_conceded', 'dots', 'elo', 'cumulative_balls_bowled', 'wicket_inv_idx', 'wickets', 'cumulative_runs_conceded', 'win_pct', 'boundaries_conceded_per_over', 'wicket_idx', 'pts', 'cumulative_runs_scored', 'cumulative_matches_played', 'extras', 'total', 'rr', 'econ', 'rwb_idx', 'boundary_idx', 'cumulative_wickets_fallen', 'stadium_win_pct', 'boundaries']

    instance = {"team_1": {}, "team_2": {}}

    for feature in features:
        instance['team_1'].update({"team_1_{}".format(feature): get_info(id=teams[0], feature=feature)})
        instance['team_2'].update({"team_2_{}".format(feature): get_info(id=teams[1], feature=feature)})

    team_1 = pd.DataFrame([instance["team_1"]])
    team_2 = pd.DataFrame([instance["team_2"]])
    data = pd.concat([team_1, team_2], axis=1)

    return data


def predict_game(teams: list):
    instance = get_latest_info(teams=teams)

    model = xgboost.XGBClassifier()
    model.load_model("data/weights.json")
    
    features = model.get_booster().feature_names
    instance = instance[features]

    prediction = model.predict_proba(instance)

    return prediction[0]

print(predict_game(teams=[13, 15]))