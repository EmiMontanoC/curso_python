"""
Doc string for Team.py
Author: Federico Cirett Galán
Date: Aug 26,2026
"""
from Athlete import Athlete
from Sport import Sport
class Team:
    """ Team class represents a team in the tournament. It has a name, a sport and a list of athletes."""
    def __init__(self, name:str, sport:Sport):
        "Custom constructor for Team"
        self.name = name
        self.sport = self.set_sport(sport)
        self.athletes = []
    def set_sport(self, sport):
        """ Set the sport for the team."""
        if isinstance(sport, Sport):
            return  sport
        else:
            raise ValueError("Only Sport objects")
        return None
    def add_athlete(self, athlete):
        """ Add an Athlete to the list of athletes"""
        if isinstance(athlete, Athlete):
            self.athletes.append(athlete)
        else:
            raise ValueError("Only Athlete objects")
    def __str__(self):
        """ String representation of the Team class"""
        return f"{self.name} - {self.sport}: {[x for x in self.athletes]}"
    def set_athletes(self, athletes):
        """ Set the list of athletes for the team."""
        if isinstance(athletes, list) and all(isinstance(x, Athlete) for x in athletes):
            self.athletes = athletes
        else:
            raise ValueError("Only list of Athlete objects")

if __name__ == "__main__":
    a = Athlete("Lionel Messi",38,"Soccer")
    b = Athlete("Cristiano Ronaldo",40,"Soccer")
    c = Athlete("Ronaldinho",46,"Soccer")
    s = Sport("Soccer",11,"FIFA")
    stars = Team("Stars",s)
    stars.add_athlete(a)
    stars.add_athlete(b)
    stars.add_athlete(c)
    print(stars)