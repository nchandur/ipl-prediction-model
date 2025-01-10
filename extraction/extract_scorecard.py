import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def extractMatchDetails(soup):

    topDetails = soup.find("div", class_="ds-px-4 ds-py-3 ds-border-b ds-border-line")
    matchType = topDetails.find(
        "div", class_="ds-text-tight-m ds-font-regular ds-text-typo-mid3"
    ).text

    teams = soup.find(
        "div", class_="ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1"
    )
    teamNames = teams.find_all(
        "span",
        class_="ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate",
    )

    matchdetails = soup.find(
        "table", class_="ds-w-full ds-table ds-table-sm ds-table-auto"
    )

    trs = matchdetails.find_all("tr")

    details = {
        "match_type": matchType.split(", ")[0],
        "team_1": teamNames[0].text,
        "team_2": teamNames[1].text,
    }

    for tr in trs:
        tds = tr.find_all("td")

        if len(tds) == 1:
            details["stadium"] = tds[0].text.strip()

        if "Toss" in tds[0].text:
            details["toss"] = tds[1].text.strip()

        if "Player Of The Match" in tds[0].text:
            details["player_of_the_match"] = tds[1].text.strip()

        if "Match days" in tds[0].text:
            details["match_days"] = tds[1].text.strip()

    if "toss" not in details:
        details["toss"] = ""

    if "player_of_the_match" not in details:
        details["player_of_the_match"] = ""

    if "match_days" not in details:
        details["match_days"] = ""

    return pd.DataFrame([details])


def extractTable(table):
    columns = [
        col.text.strip() for col in table.find("thead").find("tr").find_all("th")
    ]

    players = table.find("tbody")

    trs = players.find_all("tr")

    rows = []

    for tr in trs:
        tds = tr.find_all("td")

        if len(tds) >= 2:
            rows.append([td.text.strip() for td in tds])

    columns[0] = "Players"

    data = pd.DataFrame(rows, columns=columns)

    return data


def extractStats(soup):
    teams = soup.find_all("div", class_="ds-rounded-lg ds-mt-2")

    teamNames = [
        team.find(
            "div",
            class_="ds-flex ds-px-4 ds-border-b ds-border-line ds-py-3 ds-bg-ui-fill-translucent-hover",
        ).text
        for team in teams
    ]
    teamNames = [re.sub(r"\(.+", "", team).strip() for team in teamNames]

    bat = [
        team.find(
            "table",
            class_="ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table",
        )
        for team in teams
    ]
    bowl = [
        team.find("table", class_="ds-w-full ds-table ds-table-md ds-table-auto")
        for team in teams
    ]

    firstBat = extractTable(bat[0])
    firstBat["innings"] = 1
    firstBat["team"] = teamNames[0]

    firstBowl = extractTable(bowl[0])
    firstBowl["innings"] = 1
    firstBowl["team"] = teamNames[1]

    secondBat = extractTable(bat[1])
    secondBat["innings"] = 2
    secondBat["team"] = teamNames[1]

    secondBowl = extractTable(bowl[1])
    secondBowl["innings"] = 2
    secondBowl["team"] = teamNames[0]

    batDF = pd.concat([firstBat, secondBat])
    bowlDF = pd.concat([firstBowl, secondBowl])

    return (batDF, bowlDF)


def extractScorecard(url):

    matchID = re.findall(r"\d{5,}", url)[1]

    resp = requests.get(url=url)

    soup = BeautifulSoup(resp.text, "html.parser")

    details = extractMatchDetails(soup=soup)
    details["match_id"] = matchID

    try:
        bat, bowl = extractStats(soup=soup)
    except:
        return details, None, None

    bat["match_id"] = matchID
    bowl["match_id"] = matchID

    return details, bat, bowl
