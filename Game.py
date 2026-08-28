import random
from Athlete import Athlete
from Team import Team
from Sport import Sport
class Game:
    """
    Represents a game between two teams. It has a sport, two teams and a score for each team.
    """
    def __init__(self, A:Team, B:Team):
        self.team_a = A
        self.team_b = B
        self.score ={self.team_a.name:0,self.team_b.name:0}
        self.winner = None
        self.loser = None

    def play(self):
        """
        Simulates the game between and updates the score based on the performnace of the teams.
        """
        a = random.randint(0,100)
        b = random.randint(0,100)
        self.score[self.team_a.name] = a
        self.score[self.team_b.name] = b
        if a>b:
            self.winner = self.team_a
            self.loser = self.team_b
        elif b>a:
            self.winner = self.team_b
            self.loser = self.team_a
        else:
            self.winner = "Draw"
            self.loser = "Draw"
    def __str__(self):
        '''
        Returns a string representation of the game, including the teams, their scores, and the winner.
        '''
        return f"{self.team_a.name:<20} {self.score[self.team_a.name]} \n {self.team_b.name:<20}{self.score[self.team_b.name]} \n Winner: {self.winner.name if self.winner != 'Draw' else 'Draw'}"
    def display(self):
        """
        Displays the game result in a formatted manner
        """
        print(f"|{self.team_a.name:<20}|{self.score[self.team_a.name]:>3}| {self.team_b.name:<20}|{self.score[self.team_b.name]:>3}| Winner: {self.winner.name if self.winner != 'Draw' else 'Draw'}")
    
if __name__ == "__main__":
    a = Athlete("Oscar Bladimir",45,"Soccer")
    b = Athlete("Cristiano Ronaldo",40,"Soccer")
    c = Athlete("Ronaldinho",46,"Soccer")
    d = Athlete("Lionel Messi",38,"Soccer")
    e = Athlete("Neymar",32,"Soccer")
    f = Athlete("Mbappe",25,"Soccer")
    g = Athlete("Zidane",50,"Soccer")
    h = Athlete("Ronaldo Nazario",47,"Soccer")
    i = Athlete("Pele",82,"Soccer")
    j = Athlete("Maradona",60,"Soccer")
    k = Athlete("Kaka",41,"Soccer")
    
    a2 = Athlete("Gael",42,"Soccer")
    b2 = Athlete("Berumen",43,"Soccer")
    c2 = Athlete("Gonzalez",44,"Soccer")
    d2 = Athlete("Jonathan",45,"Soccer")
    e2 = Athlete("Oscar Bladimir",45,"Soccer")
    f2 = Athlete("Angel",37,"Soccer")
    g2 = Athlete("Luis",36,"Soccer")
    h2 = Athlete("Jorge",35,"Soccer")
    i2 = Athlete("Carlos",34,"Soccer")
    j2 = Athlete("Miguel",33,"Soccer")
    k2 = Athlete("Orlando",50,"Soccer")
    
    t1 = Team("Stars",Sport("Soccer",11,"FIFA"))
    t1.add_athlete(a)
    t1.add_athlete(b)
    t1.add_athlete(c)
    t1.add_athlete(d)
    t1.add_athlete(e)
    t1.add_athlete(f)
    t1.add_athlete(g)
    t1.add_athlete(h)
    t1.add_athlete(i)
    t1.add_athlete(j)
    t1.add_athlete(k)
    
    t2 = Team("Nobodies",Sport("Soccer",11,"FIFA"))
    t2.add_athlete(a2)
    t2.add_athlete(b2)
    t2.add_athlete(c2)
    t2.add_athlete(d2)
    t2.add_athlete(e2)
    t2.add_athlete(f2)
    t2.add_athlete(g2)
    t2.add_athlete(h2)
    t2.add_athlete(i2)
    t2.add_athlete(j2)
    t2.add_athlete(k2)
    
    game = Game(t1,t2)
    game.play()
    print(game)
    game.display()
       
        