import json
from extract_scorecard import extractScorecard
from tqdm import tqdm 
from random import randint

with open("data/scorecards.json") as file:
    seasons = json.load(file)

years = list(seasons.keys())
years.sort()

with open("data/errors.csv", "a") as error:
    error.write("season, link, error\n")

    for season in years[:1]:
        links = seasons[season]
        for link in tqdm(links):
            try: 
                details, batting, bowling = extractScorecard(url=link)

                details.to_csv("data/details.csv", mode="a", index=False, header=False)

                if batting is not None:
                    batting.to_csv("data/batting.csv", mode="a", index=False, header=False)

                if bowling is not None:
                    bowling.to_csv("data/bowling.csv", mode="a", index=False, header=False)

                error.write("{}, {}, {}\n".format(season, link, None))

                randint(5, 10)

            except Exception as e:
                error.write("{}, {}, {}\n".format(season, link, e.__class__))
        
        randint(120, 240)
