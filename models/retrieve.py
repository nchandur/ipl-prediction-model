from utils.utils import *
import pandas as pd

def convert_to_features(features:list) -> list:
    res = ["team_1_{}".format(feature) for feature in features]
    res += ["team_2_{}".format(feature) for feature in features]
    return res


def make_full_query(id:int, features:list[str]) -> str:
    res = '''
    SELECT date,
    '''

    n = len(features)
    for i in range(n):
        if i != n-1:
            res += make_partial_query(id, feature=features[i]) + ",\n"
        else:
            res += make_partial_query(id, feature=features[i]) + "\n"

    res += '''
    FROM matches
    
    WHERE (team_1_id = {} OR team_2_id = {}) ORDER BY DATE DESC LIMIT 1; 
    '''.format(id, id)

    return res

def make_partial_query(id:int, feature:str) -> str:
    
    res = '''
    CASE
        WHEN team_1_id = {} THEN team_1_{}
        WHEN team_2_id = {} THEN team_2_{}
    END AS {}'''.format(id, feature, id, feature, feature)
    
    return res


individual = ["win_pct", "rr", "nrr", "boundaries_scored_per_over", "boundaries_conceded_per_over", "boundary_idx", "boundary_inv_idx", "rwb_idx", "wicket_idx", "wicket_inv_idx", "econ", "cumulative_runs_scored", "cumulative_runs_conceded", "cumulative_balls_faced", "cumulative_balls_bowled", "cumulative_wickets_taken", "cumulative_wickets_fallen", "cumulative_boundaries_scored", "cumulative_boundaries_conceded", "cumulative_matches_played"]

query = make_full_query(id=15, features=individual)

data = retrieveFromDB(query=query)
print(data)