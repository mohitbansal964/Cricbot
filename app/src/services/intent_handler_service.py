from .live_match_service import LiveMatchService
from src.constants import Constants
from src.enums import Intent
from src.models import IntentDetails

class IntentHandlerService:
    """
    A service class to handle user intents and fetch additional data related to cricket matches.

    Attributes:
    ----------
    __live_match_service : LiveMatchService
        An instance of LiveMatchService to fetch live match data.

    Methods:
    -------
    get_addtional_data(data: dict) -> dict
        Processes the input data to fetch additional information based on the identified intent.

    __get_current_matches_intent_data(intent_details: IntentDetails) -> dict
        Handles the 'live_matches' intent and returns relevant match data.

    __get_live_score_intent_data(intent_details: IntentDetails) -> dict
        Handles the 'live_score' intent and returns the match score or fallback data.

    __get_fallback_intent_data(intent_details: IntentDetails) -> dict
        Handles fallback scenarios when the intent is not recognized.
    """

    def __init__(self):
        """
        Initializes the IntentHandlerService.
        """
        self.__live_match_service = LiveMatchService()

    def get_addtional_data(self, data: dict) -> dict:
        """
        Processes the input data to fetch additional information based on the identified intent.

        Parameters:
        ----------
        data : dict
            The input data containing intent and entities.

        Returns:
        -------
        dict
            The enriched data with additional information based on the intent.
        """
        intent_details = IntentDetails(**data)
        match intent_details.intent:
            case Intent.live_matches:
                additional_data = self.__get_current_matches_intent_data(intent_details)
            case Intent.live_score:
                additional_data = self.__get_live_score_intent_data(intent_details)
            case _:
                additional_data = self.__get_fallback_intent_data(intent_details)
        return {**data, **additional_data}

    def __get_current_matches_intent_data(self, intent_details: IntentDetails) -> dict:
        """
        Handles the 'live_matches' intent and returns relevant match data.

        Parameters:
        ----------
        intent_details : IntentDetails
            The details of the identified intent.

        Returns:
        -------
        dict
            Additional data for live matches.
        """
        entities = intent_details.entities
        live_matches = self.__live_match_service.fetch_all_matches(entities.date)
        series = entities.series
        if series:
            live_matches_of_series = [match for match in live_matches if match.series_name.lower() == series.lower()]
            additional_data = {
                "series": series,
                "live_matches": live_matches_of_series
            }
        else:
            additional_data = {
                "live_matches": live_matches
            }
        return additional_data

    def __get_live_score_intent_data(self, intent_details: IntentDetails) -> dict:
        """
        Handles the 'live_score' intent and returns the match score or fallback data.

        Parameters:
        ----------
        intent_details : IntentDetails
            The details of the identified intent.

        Returns:
        -------
        dict
            Additional data for the live score or fallback information.
        """
        entities = intent_details.entities
        match_score, live_matches = self.__live_match_service.fetch_live_score(
            entities.team1, 
            entities.team2
        )
        if match_score is None and len(live_matches) > 0:
            additional_data = {
                "intent": Intent.live_matches,
                "entities": {},
                "live_matches": live_matches
            }
        elif match_score is None:
            additional_data = {
                "intent": Intent.fallback,
                "entities": {
                    "reason": Constants.MATCHES_NOT_PRESENT_REASON
                }
            }
        else:
            additional_data = {
                "match_score": match_score
            }
        return additional_data

    def __get_fallback_intent_data(self, intent_details: IntentDetails) -> dict:
        """
        Handles fallback scenarios when the intent is not recognized.

        Parameters:
        ----------
        intent_details : IntentDetails
            The details of the identified intent.

        Returns:
        -------
        dict
            Fallback data with a reason if available.
        """
        entities = intent_details.entities
        if not entities.reason:
            return {
                "entities": {
                    "reason": Constants.REASON_NOT_PRESENT
                }
            }
        return {}
