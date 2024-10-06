
import os
from constants.constants import Constants

def clean_team_name(team):
    return team.strip().lower()

def clean_team_names(teams):
    return [clean_team_name(team) for team in teams]

def read_prompt_from_file(file_name: str) -> str:
    file_path = os.path.join(Constants.BASE_FILE_PATH, file_name)
    with open(file_path, 'r') as f:
        return f.read()
