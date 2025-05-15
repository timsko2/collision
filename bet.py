import discord
class Bet:
    def __init__(self,author,  score1: int, score2: int):
        self.author = author
        self.score1 = score1
        self.score2 = score2
        self.score_reel1 = None
        self.score_reel2 = None
        self.loss = None
    
    def __str__(self):
        return f"{self.score1} : {self.score2} par {self.author}"
    def __repr__(self):
        return f"{self.score1} : {self.score2} par {self.author}"
    
    def set_score_reel(self, score_reel1 : int, score_reel2 : int):
        self.score_reel1 = score_reel1
        self.score_reel2 = score_reel2
        self.loss = abs(self.score1 - self.score_reel1) + abs(self.score2 - self.score_reel2)
    
    def __lt__(self, other):
        if self.score_reel1 is None:
            raise ValueError("Comparaison impossible")
        return self.loss < other.loss
    
    def __eq__(self, other):
        return self.loss < other.loss