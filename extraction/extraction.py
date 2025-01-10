import json
from extract_scorecard import extractScorecard
from tqdm import tqdm
from random import randint
import os

with open("data/scorecards.json") as file:
    seasons = json.load(file)

years = list(seasons.keys())
years.sort()

destination = "data/raw"

if not os.path.exists(destination):
    os.mkdir(destination)


with open("data/errors.csv", "a") as error:
    error.write("season, link, error\n")

    for season in years:
        links = seasons[season]
        for link in tqdm(links):
            try:
                details, batting, bowling = extractScorecard(url=link)

                details.to_csv(
                    os.path.join(destination, "details.csv"),
                    mode="a",
                    index=False,
                    header=False,
                )

                if batting is not None:
                    batting.to_csv(
                        os.path.join(destination, "batting.csv"),
                        mode="a",
                        index=False,
                        header=False,
                    )

                if bowling is not None:
                    bowling.to_csv(
                        os.path.join(destination, "bowling.csv"),
                        mode="a",
                        index=False,
                        header=False,
                    )

                error.write("{}, {}, {}\n".format(season, link, None))

                randint(5, 10)

            except Exception as e:
                error.write("{}, {}, {}\n".format(season, link, e.__class__))

        randint(120, 240)
