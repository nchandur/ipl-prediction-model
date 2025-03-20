from django.shortcuts import render

def home(response):
    return render(response, "home.html")

def player(response):
    return render(response, "player.html")

def team(response):
    return render(response, "team.html")

def match(response):
    if response.method == "POST":
        team1 = response.POST.get("team_1", "")
        team2 = response.POST.get("team_2", "")
        return render(response, "match.html", {"team_1": team1, "team_2": team2})   
    return render(response, "match.html", {'data': None})