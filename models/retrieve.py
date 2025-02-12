from utils.utils import *
import pandas as pd

def convert_to_features(features:list) -> list:
    res = ["team_1_{}".format(feature) for feature in features]
    res += ["team_2_{}".format(feature) for feature in features]
    return res


def make_full_query(id:int, features:list[str]) -> str:
    res = '''
    SELECT
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

def head_2_head_query(id_1:int, id_2:int) -> float:
    
    query = '''SELECT
    CASE 
        WHEN team_1_id = {} THEN team_1_h2h_win_pct
        WHEN team_2_id = {} THEN team_2_h2h_win_pct
    END AS h2h_win_pct
    FROM matches WHERE (team_1_id = {} AND team_2_id = {}) OR (team_1_id = {} AND team_2_id = {}) ORDER BY date DESC LIMIT 1;'''.format(id_1, id_1, id_1, id_2, id_2, id_1)

    data = retrieveFromDB(query=query)

    return data["h2h_win_pct"].iloc[0]

def stadium_win_pct(id:int, stadium:str):
    query = '''
    SELECT
        CASE 
            WHEN team_1_id = {} THEN team_1_stadium_win_pct
            WHEN team_2_id = {} THEN team_2_stadium_win_pct
        END AS stadium_win_pct
    FROM matches WHERE (team_1_id = {} OR team_2_id = {}) AND stadium ILIKE '%%{}%%' ORDER BY date DESC LIMIT 1;
    '''.format(id, id, id, id, stadium)

    data = retrieveFromDB(query=query)

    return data["stadium_win_pct"].iloc[0]

def h2h_stadium_win_pct(id_1:int, id_2:int, stadium:str) -> float:
    query = '''
    SELECT 
        CASE
            WHEN team_1_id = {} THEN team_1_h2h_stadium_win_pct
            WHEN team_2_id = {} THEN team_2_h2h_stadium_win_pct
        END AS h2h_stadium_win_pct
    FROM matches WHERE ((team_1_id = {} AND team_2_id = {}) OR (team_1_id = {} AND team_2_id = {})) AND stadium ILIKE '%%{}%%' ORDER BY date DESC LIMIT 1;
    '''.format(id_1, id_1, id_1, id_2, id_2, id_1, stadium)

    data = retrieveFromDB(query=query)

    return data["h2h_stadium_win_pct"].iloc[0]

def get_team_1(ip:dict, features:list[str]):
    res = pd.DataFrame()

    res = pd.concat([res, retrieveFromDB(query=make_full_query(id=ip["id_1"], features=features))], axis=1)
    res["h2h_win_pct"] = head_2_head_query(id_1=ip["id_1"], id_2=ip["id_2"])

    if ip["stadium"] is not None:
        res["stadium_win_pct"] = stadium_win_pct(id=ip["id_1"], stadium=ip["stadium"])
        res["h2h_stadium_win_pct"] = h2h_stadium_win_pct(id_1=ip["id_1"], id_2=ip["id_2"], stadium=ip["stadium"])
    else:
        res["stadium_win_pct"] = None
        res["h2h_stadium_win_pct"] = None

    return res

def get_team_2(ip:dict, features:list[str]):
    res = pd.DataFrame()

    res = pd.concat([res, retrieveFromDB(query=make_full_query(id=ip["id_2"], features=features))], axis=1)
    res["h2h_win_pct"] = head_2_head_query(id_1=ip["id_2"], id_2=ip["id_1"])

    if ip["stadium"] is not None:
        res["stadium_win_pct"] = stadium_win_pct(id=ip["id_2"], stadium=ip["stadium"])
        res["h2h_stadium_win_pct"] = h2h_stadium_win_pct(id_1=ip["id_2"], id_2=ip["id_1"], stadium=ip["stadium"])
    else:
        res["stadium_win_pct"] = None
        res["h2h_stadium_win_pct"] = None

    return res



def get_row(ip:dict) -> pd.DataFrame:
    individual = ["elo", "win_pct", "rr", "boundaries_scored_per_over", "boundaries_conceded_per_over", "boundary_idx", "boundary_inv_idx", "rwb_idx", "wicket_idx", "wicket_inv_idx", "econ", "cumulative_runs_scored", "cumulative_runs_conceded", "cumulative_balls_faced", "cumulative_balls_bowled", "cumulative_wickets_taken", "cumulative_wickets_fallen", "cumulative_boundaries_scored", "cumulative_boundaries_conceded", "cumulative_matches_played"]
    
    team_1 = get_team_1(ip=ip, features=individual).iloc[0].rename(lambda x: "team_1_{}".format(x))
    team_2 = get_team_2(ip=ip, features=individual).iloc[0].rename(lambda x: "team_2_{}".format(x))

    res = pd.DataFrame(pd.concat([team_1, team_2]))

    return res.transpose()