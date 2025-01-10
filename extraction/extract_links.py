import json
import requests
from os.path import basename
from time import sleep, perf_counter
from random import randint
from tqdm import tqdm
from bs4 import BeautifulSoup


def gameLinks(seasonLink: str) -> list[str]:

    resp = requests.get(url=seasonLink)

    if resp.status_code != 200:
        return []

    try:
        soup = BeautifulSoup(resp.text, "html.parser")

        gamecards = soup.find("div", class_="ds-mb-4")

        links = [
            "https://www.espncricinfo.com{}".format(tag["href"].strip())
            for tag in gamecards.find_all("a")
            if basename(tag["href"]) == "full-scorecard"
        ]

        return links

    except:
        return []


start = perf_counter()

with open("data/seasons.json") as file:
    seasons = json.load(file)

linksJSON = dict()

for season in tqdm(seasons):
    linksJSON[season] = gameLinks(seasons[season])

    sleep(randint(2, 4))

linksJSONstr = json.dumps(linksJSON, indent=4)

with open("data/scorecards.json", "w") as file:
    file.write(linksJSONstr)
