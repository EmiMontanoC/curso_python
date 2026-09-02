import json
from Game import Game
from Athlete import Athlete
from Team import Team
from Sport import Sport
from itertools import combinations
def load_json(filename):
        """ Load a Tournament object from a JSON file."""
        data = None
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
        return data

def json_to_team(data):
    teams = []
    for team_data in data:
        team_name = team_data['name']
        sport_name = team_data['sport']['name']
        league = team_data['sport']['league']
        num_players = team_data['sport']['num_players']
        sport = Sport(sport_name, league, num_players)
        athletes = []
        for athlete_data in team_data['athletes']:
            athlete_name = athlete_data['name']
            age = athlete_data['number']
            athlete_sport = sport.sport_name
            athlete = Athlete(athlete_name, age, athlete_sport)
            athletes.append(athlete)
        team = Team(team_name, sport)
        team.set_athletes(athletes)
        teams.append(team)
    return teams
def main():
    
    tournament_data = load_json('tournament.json')
    teams = json_to_team(tournament_data)
    team_combinations=list(combinations(teams, 2))
    for local,visitor in team_combinations:
        game = Game(local,visitor)
        game.play()
        game.display()
        print("\n")

if __name__ == "__main__":
    main()