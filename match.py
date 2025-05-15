from match_status import MatchStatus
class Match:
    def __init__(self, team1: str, team2: str):
        """
        Initialise un nouveau match
        :param team1: Nom de l'équipe 1
        :param team2: Nom de l'équipe 2
        :param score: Tuple contenant le score (score_team1, score_team2)
        """
        self.team1 = team1
        self.team2 = team2
        self.score = None
        self.status = MatchStatus.NOT_STARTED
    
    def __str__(self):
        """Représentation textuelle du match"""
        if self.score == None:
            return f"{self.team1} vs {self.team2} - En attente de débuter"
        return f"{self.team1} vs {self.team2} - Score: {self.score[0]}-{self.score[1]}"
    
    def getstatus(self):
        return self.status