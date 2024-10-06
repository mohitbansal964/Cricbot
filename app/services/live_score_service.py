from datetime import datetime
from typing import Any, List
import requests

from models import MatchDetails
from utils import clean_team_name, clean_team_names

class LiveScoreService:
    """
    A service class to fetch and identify live cricket match scores.

    Methods:
    -------
    fetch_live_score(team1: str, team2: str) -> MatchDetails
        Fetches live scores and finds the match between the specified teams.

    __fetch_all_live_matches() -> List[MatchDetails]
        Retrieves all live matches from the external API.

    __process_matches_data(response: Any) -> List[MatchDetails]
        Processes the API response to extract match details.

    __find_match(matches: List[MatchDetails], team1: str, team2: str) -> MatchDetails
        Finds a match between the specified teams from the list of matches.
    """

    def fetch_live_score(self, team1: str, team2: str) -> MatchDetails:
        """
        Fetches live scores and finds the match between the specified teams.

        Parameters:
        ----------
        team1 : str
            The name of the first team.
        team2 : str
            The name of the second team.

        Returns:
        -------
        MatchDetails
            The details of the match between the specified teams, or None if not found.
        """
        live_matches = self.__fetch_all_live_matches()
        return self.__find_match(live_matches, team1, team2)

    def __fetch_all_live_matches(self) -> List[MatchDetails]:
        """
        Retrieves all live matches from the external API.

        Returns:
        -------
        List[MatchDetails]
            A list of MatchDetails objects representing live matches.
        """
        cur_date = datetime.today().strftime("%Y%m%d")
        url = f"https://prod-public-api.livescore.com/v1/api/app/date/cricket/{cur_date}/5.30?locale=en&MD=1"
        response = requests.get(url)
        if response.ok:
            return self.__process_matches_data(response.json())
        else:
            return []

    def __process_matches_data(self, response: Any) -> List[MatchDetails]:
        """
        Processes the API response to extract match details.

        Parameters:
        ----------
        response : Any
            The JSON response from the API.

        Returns:
        -------
        List[MatchDetails]
            A list of MatchDetails objects extracted from the response.
        """
        matches = []
        for stage in response['Stages']:
            for event in stage['Events']:
                match_details = MatchDetails()
                match_details.id = event.get('Eid')
                match_details.status = event.get('ECo') or ''

                team1 = event.get('T1')
                if team1 and len(team1) > 0:
                    match_details.team_1.name = team1[0].get('Nm')
                    match_details.team_1.abr = team1[0].get('Abr')
                match_details.team_1.run = event.get('Tr1C1') or ''
                match_details.team_1.wicket = event.get('Tr1CW1') or ''
                match_details.team_1.over = event.get('Tr1CO1') or ''

                team2 = event.get('T2')
                if team2 and len(team2) > 0:
                    match_details.team_2.name = team2[0].get('Nm')
                    match_details.team_2.abr = team2[0].get('Abr')
                match_details.team_2.run = event.get('Tr2C1') or ''
                match_details.team_2.wicket = event.get('Tr2CW1') or ''
                match_details.team_2.over = event.get('Tr2CO1') or ''
                matches.append(match_details)
        return matches

    def __find_match(self, matches: List[MatchDetails], team1: str, team2: str) -> MatchDetails:
        """
        Finds a match between the specified teams from the list of matches.

        Parameters:
        ----------
        matches : List[MatchDetails]
            A list of MatchDetails objects to search through.
        team1 : str
            The name of the first team.
        team2 : str
            The name of the second team.

        Returns:
        -------
        MatchDetails
            The details of the match between the specified teams, or None if not found.
        """
        if team1.lower() == team2.lower():
            return None
        for match in matches:
            teams = clean_team_names([
                match.team_1.name, 
                match.team_2.name, 
                match.team_1.abr, 
                match.team_2.abr
            ])
            if clean_team_name(team1) in teams and clean_team_name(team2) in teams:
                return match
        return None
