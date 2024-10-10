from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TeamScoreDetails:
    """
    A class to represent the score details of a cricket team.

    Attributes:
    ----------
    name : str
        The name of the team.
    abr : str
        The abbreviation of the team's name.
    run : Optional[int]
        The number of runs scored by the team.
    wicket : Optional[int]
        The number of wickets lost by the team.
    over : Optional[float]
        The number of overs played by the team.
    declared : bool
        Indicates if the innings was declared.
    run2 : Optional[int]
        The number of runs scored in the second inning.
    wicket2 : Optional[int]
        The number of wickets lost in the second inning.
    over2 : Optional[float]
        The number of overs played in the second inning.
    declared2 : bool
        Indicates if the second innings was declared.
    """
    name: str = ''
    abr: str = ''
    run: Optional[int] = None
    wicket: Optional[int] = None
    over: Optional[float] = None
    declared: bool = False
    run2: Optional[int] = None
    wicket2: Optional[int] = None
    over2: Optional[float] = None
    declared2: bool = False

@dataclass
class MatchDetails:
    """
    A class to represent the details of a cricket match.

    Attributes:
    ----------
    id : Optional[str]
        A unique identifier for the match.
    format : str
        The format of the match (e.g., 'ODI', 'Test').
    series_id : Optional[str]
        The ID of the series.
    series_name : str
        The name of the series.
    status : str
        The current status of the match (e.g., 'ongoing', 'completed').
    team1 : TeamScoreDetails
        An instance of TeamScoreDetails representing the first team.
    team2 : TeamScoreDetails
        An instance of TeamScoreDetails representing the second team.
    """
    id: Optional[str] = None
    format: str = ''
    series_id: Optional[str] = None
    series_name: str = ''
    status: str = ''
    team1: TeamScoreDetails = field(default_factory=TeamScoreDetails)
    team2: TeamScoreDetails = field(default_factory=TeamScoreDetails)
