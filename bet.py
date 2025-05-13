import discord
class Bet:
    def __init__(self,author,  score1: int, score2: int):
        self.author = author
        self.score1 = score1
        self.score2 = score2
        self.score_reel1 = None
        self.score_reel2 = None
    
    def __str__(self):
        return f"{self.score1} : {self.score2} par {self.author}"
    def __repr__(self):
        return f"{self.score1} : {self.score2} par {self.author}"
    
    def __lt__(self, other):
        if self.score_reel1 is None:
            raise ValueError("Comparaison impossible")
        return abs(self.score1 - self.score_reel1) + abs(self.score2 - self.score_reel2) < abs(other.score1 - other.score_reel1) + abs(other.score2 - other.score_reel2)
    
    def __eq__(self, other):
        return abs(self.score1 - self.score_reel1) + abs(self.score2 - self.score_reel2) < abs(other.score1 - other.score_reel1) + abs(other.score2 - other.score_reel2)