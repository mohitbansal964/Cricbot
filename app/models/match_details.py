class MatchDetails:
    """
    A class to represent the details of a cricket match.

    Attributes:
    ----------
    id : str or None
        A unique identifier for the match.
    status : str
        The current status of the match (e.g., 'ongoing', 'completed').
    team_1 : TeamScoreDetails
        An instance of TeamScoreDetails representing the first team.
    team_2 : TeamScoreDetails
        An instance of TeamScoreDetails representing the second team.
    """

    def __init__(self):
        self.id = None  # Initialize the match ID as None, can be set later
        self.status = ''  # Initialize the match status as an empty string
        self.team_1 = TeamScoreDetails()  # Initialize team 1 details
        self.team_2 = TeamScoreDetails()  # Initialize team 2 details


class TeamScoreDetails:
    """
    A class to represent the score details of a cricket team.

    Attributes:
    ----------
    name : str
        The name of the team.
    abr : str
        The abbreviation of the team's name.
    run : str
        The number of runs scored by the team.
    wicket : str
        The number of wickets lost by the team.
    over : str
        The number of overs played by the team.
    """

    def __init__(self):
        self.name = ''  # Initialize the team name as an empty string
        self.abr = ''  # Initialize the team abbreviation as an empty string
        self.run = ''  # Initialize the runs scored as an empty string
        self.wicket = ''  # Initialize the wickets lost as an empty string
        self.over = ''  # Initialize the overs played as an empty string
