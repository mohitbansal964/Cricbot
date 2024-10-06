from constants import Constants
from .intent_identifier_service import IntentIdentifierService
from .live_score_service import LiveScoreService
from .response_generator_service import ResponseGeneratorService

class CricbotService:
    """
    A service class for the Cricbot chatbot to handle user interactions and provide responses.

    Attributes:
    ----------
    __intent_identifier_service : IntentIdentifierService
        An instance of IntentIdentifierService to identify user intents.
    __live_score_service : LiveScoreService
        An instance of LiveScoreService to fetch live cricket scores.
    __response_generator_service : ResponseGeneratorService
        An instance of ResponseGeneratorService to generate responses.

    Methods:
    -------
    bot_response(user_input: str)
        Processes the user input and prints the bot's response.

    __handle_live_score_intent(user_input: str, intent_details: dict) -> str
        Handles the 'live_score' intent and returns the appropriate response.

    __handle_fallback_intent(user_input: str, intent_details: dict) -> str
        Handles fallback scenarios when the intent is not recognized.

    __get_fallback_response(user_input: str, reason: str) -> str
        Generates a fallback response using the ResponseGeneratorService.
    """

    def __init__(self, openai_api_key: str):
        """
        Initializes the CricbotService with the specified OpenAI API key.

        Parameters:
        ----------
        openai_api_key : str
            The API key for accessing the OpenAI service.
        """
        self.__intent_identifier_service = IntentIdentifierService(openai_api_key)
        self.__live_score_service = LiveScoreService()
        self.__response_generator_service = ResponseGeneratorService(openai_api_key)

    def bot_response(self, user_input: str):
        """
        Processes the user input and prints the bot's response.

        Parameters:
        ----------
        user_input : str
            The input text from the user.
        """
        intent_details = self.__intent_identifier_service.invoke(user_input)
        response = ""
        match intent_details.get('intent'):
            case 'live_score':
                response = self.__handle_live_score_intent(user_input, intent_details)
            case _:
                response = self.__handle_fallback_intent(user_input, intent_details)
        print("Cricbot:", response)

    def __handle_live_score_intent(self, user_input: str, intent_details: dict) -> str:
        """
        Handles the 'live_score' intent and returns the appropriate response.

        Parameters:
        ----------
        user_input : str
            The input text from the user.
        intent_details : dict
            The details of the identified intent.

        Returns:
        -------
        str
            The generated response content.
        """
        entities = intent_details.get('entities')
        if 'team1' not in entities or 'team2' not in entities:
            return self.__get_fallback_response(user_input, Constants.TEAMS_NOT_PRESENT_REASON)
        
        live_score = self.__live_score_service.fetch_live_score(entities['team1'], entities['team2'])

        if live_score is None:
            return self.__get_fallback_response(
                user_input, 
                Constants.MATCH_NOT_PRESENT_REASON.format(
                    team1=entities['team1'], 
                    team2=entities['team2']
                )
            )
        
        return self.__response_generator_service.get_live_score_response(user_input, live_score)
    
    def __handle_fallback_intent(self, user_input: str, intent_details: dict) -> str:
        """
        Handles fallback scenarios when the intent is not recognized.

        Parameters:
        ----------
        user_input : str
            The input text from the user.
        intent_details : dict
            The details of the identified intent.

        Returns:
        -------
        str
            The generated fallback response content.
        """
        entities = intent_details.get('entities')
        if 'reason' not in entities or not entities['reason']:
            return self.__get_fallback_response(user_input, Constants.REASON_NOT_PRESENT)
        return self.__get_fallback_response(user_input, entities['reason'])

    def __get_fallback_response(self, user_input: str, reason: str) -> str:
        """
        Generates a fallback response using the ResponseGeneratorService.

        Parameters:
        ----------
        user_input : str
            The input text from the user.
        reason : str
            The reason for the fallback.

        Returns:
        -------
        str
            The generated fallback response content.
        """
        return self.__response_generator_service.get_fallback_response(user_input, reason)
