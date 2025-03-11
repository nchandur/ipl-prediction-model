import xgboost
from utils.utils import retrieveFromDB

data = retrieveFromDB(query="SELECT * FROM matches")

data["victory"] = data["team_1_id"] == data["winner_id"]

features = data.columns.to_list()[16:-1]
label = data.columns.to_list()[-1]

model = xgboost.XGBClassifier()

model.fit(data[features], data[label])

model.save_model("data/weights.json")
