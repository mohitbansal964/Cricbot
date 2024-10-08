import os
from typing import List
from constants import Constants

def clean_team_name(team: str) -> str:
    """
    Cleans a single team name by stripping whitespace and converting it to lowercase.

    Parameters:
    ----------
    team : str
        The name of the team to be cleaned.

    Returns:
    -------
    str
        The cleaned team name in lowercase.
    """
    return team.strip().lower()

def clean_team_names(teams: List[str]) -> List[str]:
    """
    Cleans a list of team names by applying the clean_team_name function to each.

    Parameters:
    ----------
    teams : list of str
        A list of team names to be cleaned.

    Returns:
    -------
    list of str
        A list of cleaned team names in lowercase.
    """
    return [clean_team_name(team) for team in teams]

def read_prompt_from_file(file_name: str) -> str:
    """
    Reads the content of a prompt file located in the base file path.

    Parameters:
    ----------
    file_name : str
        The name of the file to read.

    Returns:
    -------
    str
        The content of the file as a string.

    Raises:
    ------
    FileNotFoundError
        If the file does not exist at the specified path.
    IOError
        If there is an error reading the file.
    """
    file_path = os.path.join(Constants.BASE_FILE_PATH, file_name)
    with open(file_path, 'r') as f:
        return f.read()
