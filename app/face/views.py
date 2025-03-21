from django.shortcuts import render
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from models.predict import predict_game


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

        output = predict_game([team1, team2])
    
        return render(response, "match.html", {"output": output})   
    return render(response, "match.html", {})