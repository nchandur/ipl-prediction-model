from utils.utils import *
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

data = retrieveFromDB(query="SELECT team_1_win_pct, team_2_win_pct, team_1_h2h_win_pct, team_2_h2h_win_pct, team_1_victory FROM matches ORDER BY date")

train, test = train_test_split(data, test_size=0.05, random_state=42)

cols = data.columns.to_list()

features = cols[:-1]
label = cols[-1]

model = DecisionTreeClassifier(criterion="gini", random_state=42)

model.fit(train[features], train[label])

pred = model.predict(test[features])

report = classification_report(pred, test[label])

print(report)