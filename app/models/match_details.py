class MatchDetails:
    def __init__(self):
        self.id = None
        self.status = ''
        self.team_1 = TeamScoreDetails()
        self.team_2 = TeamScoreDetails()

class TeamScoreDetails:
    def __init__(self):
        self.name = ''
        self.abr = ''
        self.run = ''
        self.wicket = ''
        self.over = ''
        