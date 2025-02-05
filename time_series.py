from utils.utils import *
import pandas as pd
import plotly.express as px

team_id = 9
feature = "boundary_idx"

query = '''
SELECT 
    date, 
    CASE 
        WHEN team_1_id = {} THEN team_1_{}
        WHEN team_2_id = {} THEN team_2_{}
    END AS feature
FROM elo_ratings
WHERE (team_1_id = {} OR team_2_id = {}) AND season = 2024
ORDER BY date;
'''.format(team_id, feature, team_id, feature, team_id, team_id)

data = retrieveFromDB(query=query)
data["date"] = pd.to_datetime(data["date"])

fig = px.scatter(data, x="date", y="feature")
fig.show()