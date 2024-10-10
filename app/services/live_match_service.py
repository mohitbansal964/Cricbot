from datetime import datetime
from typing import Any, List, Optional, Tuple
import requests

from models import MatchDetails, TeamScoreDetails
from utils import clean_team_name, clean_team_names

class LiveMatchService:
    """
    A service class to fetch and identify live cricket match scores.

    Methods:
    -------
    fetch_live_score(team1: str, team2: str) -> Tuple[MatchDetails, List[MatchDetails]]
        Fetches live scores and finds the match between the specified teams.

    fetch_all_live_matches(date: Optional[str] = None) -> List[MatchDetails]
        Retrieves all live matches from the external API for a given date.

    __process_matches_data(response: Any) -> List[MatchDetails]
        Processes the API response to extract match details.

    __create_match_details(event: dict, series_id: str, series_name: str) -> MatchDetails
        Creates a MatchDetails object from event data.

    __create_team_details(event: dict, team_key: str, score_prefix: str) -> TeamScoreDetails
        Creates a TeamScoreDetails object from event data.

    __safe_int(value: Optional[str]) -> Optional[int]
        Safely converts a string to an integer.

    __safe_float(value: Optional[str]) -> Optional[float]
        Safely converts a string to a float.

    __find_match(matches: List[MatchDetails], team1: str, team2: str) -> Optional[MatchDetails]
        Finds a match between the specified teams from the list of matches.
    """

    def fetch_live_score(self, team1: str, team2: str) -> Tuple[Optional[MatchDetails], List[MatchDetails]]:
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
        Tuple[Optional[MatchDetails], List[MatchDetails]]
            A tuple containing the details of the match between the specified teams, 
            or None if not found, and a list of all live matches.
        """
        live_matches = self.fetch_all_live_matches()
        return (self.__find_match(live_matches, team1, team2), live_matches)

    def fetch_all_live_matches(self, date: Optional[str] = None) -> List[MatchDetails]:
        """
        Retrieves all live matches from the external API for a given date.

        Parameters:
        ----------
        date : Optional[str]
            The date for which to fetch live matches in YYYYMMDD format. Defaults to today.

        Returns:
        -------
        List[MatchDetails]
            A list of MatchDetails objects representing live matches.
        """
        cur_date = date if date else datetime.today().strftime("%Y%m%d")
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
        for stage in response.get('Stages', []):
            series_id = stage.get('Scd', '')
            series_name = stage.get('Snm', '')

            for event in stage.get('Events', []):
                match_details = self.__create_match_details(event, series_id, series_name)
                matches.append(match_details)
        return matches

    def __create_match_details(self, event: dict, series_id: str, series_name: str) -> MatchDetails:
        """
        Creates a MatchDetails object from event data.

        Parameters:
        ----------
        event : dict
            The event data containing match information.
        series_id : str
            The ID of the series.
        series_name : str
            The name of the series.

        Returns:
        -------
        MatchDetails
            The MatchDetails object populated with event data.
        """
        match_details = MatchDetails(
            id=event.get('Eid'),
            format=event.get('EtTx', ''),
            series_id=series_id,
            series_name=series_name,
            status=event.get('ECo', '')
        )

        match_details.team1 = self.__create_team_details(event, 'T1', 'Tr1')
        match_details.team2 = self.__create_team_details(event, 'T2', 'Tr2')

        return match_details

    def __create_team_details(self, event: dict, team_key: str, score_prefix: str) -> TeamScoreDetails:
        """
        Creates a TeamScoreDetails object from event data.

        Parameters:
        ----------
        event : dict
            The event data containing team information.
        team_key : str
            The key in the event data for the team.
        score_prefix : str
            The prefix for score-related fields in the event data.

        Returns:
        -------
        TeamScoreDetails
            The TeamScoreDetails object populated with team data.
        """
        team_data = event.get(team_key, [{}])[0]
        return TeamScoreDetails(
            name=team_data.get('Nm', ''),
            abr=team_data.get('Abr', ''),
            run=self.__safe_int(event.get(f'{score_prefix}C1')),
            wicket=self.__safe_int(event.get(f'{score_prefix}CW1')),
            over=self.__safe_float(event.get(f'{score_prefix}CO1')),
            declared=event.get(f'{score_prefix}CD1', False),
            run2=self.__safe_int(event.get(f'{score_prefix}C2')),
            wicket2=self.__safe_int(event.get(f'{score_prefix}CW2')),
            over2=self.__safe_float(event.get(f'{score_prefix}CO2')),
            declared2=event.get(f'{score_prefix}CD2', False)
        )

    def __safe_int(self, value: Optional[str]) -> Optional[int]:
        """
        Safely converts a string to an integer.

        Parameters:
        ----------
        value : Optional[str]
            The string to convert.

        Returns:
        -------
        Optional[int]
            The converted integer or None if conversion fails.
        """
        try:
            return int(value) if value is not None else None
        except ValueError:
            return None

    def __safe_float(self, value: Optional[str]) -> Optional[float]:
        """
        Safely converts a string to a float.

        Parameters:
        ----------
        value : Optional[str]
            The string to convert.

        Returns:
        -------
        Optional[float]
            The converted float or None if conversion fails.
        """
        try:
            return float(value) if value is not None else None
        except ValueError:
            return None

    def __find_match(self, matches: List[MatchDetails], team1: str, team2: str) -> Optional[MatchDetails]:
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
        Optional[MatchDetails]
            The details of the match between the specified teams, or None if not found.
        """
        if team1.lower() == team2.lower():
            return None
        for match in matches:
            teams = clean_team_names([
                match.team1.name, 
                match.team2.name, 
                match.team1.abr, 
                match.team2.abr
            ])
            if clean_team_name(team1) in teams and clean_team_name(team2) in teams:
                return match
        return None
