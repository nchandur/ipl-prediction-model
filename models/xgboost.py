import xgboost
from sklearn.model_selection import train_test_split
from utils.utils import retrieveFromDB
from sklearn.metrics import classification_report

data = retrieveFromDB(query="SELECT * FROM matches")

data["victory"] = data["team_1_id"] == data["winner_id"]

features = data.columns.to_list()[16:-1]
label = data.columns.to_list()[-1]

train, test = train_test_split(data, test_size=0.80, random_state=42)

model = xgboost.XGBClassifier()

model.fit(train[features], train[label])

preds = model.predict(test[features])

report = classification_report(preds, test[label])

print(report)