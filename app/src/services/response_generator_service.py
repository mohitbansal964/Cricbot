from typing import Any, List, Optional
from langchain_openai import ChatOpenAI
from src.enums import Intent
from src.models import TeamScoreDetails, MatchDetails
from src.utils import get_live_matches_as_string, read_prompt_from_file
from src.constants import Constants
from langchain.prompts import PromptTemplate

class ResponseGeneratorService:
    """
    A service class to generate responses using the OpenAI language model.

    Attributes:
    ----------
    llm : ChatOpenAI
        An instance of ChatOpenAI configured with a specific model and API key.

    Methods:
    -------
    get_prompt(data: dict) -> str

    
    __get_live_score_prompt(user_input: str, match_details: MatchDetails) -> str
        Constructs the prompt for generating a live score response.

    __extract_team_details(team_details: Optional[TeamScoreDetails], prefix: str) -> dict
        Extracts team details and formats them for prompt generation.

    __get_live_score_prompt_template() -> PromptTemplate
        Retrieves the template for live score prompts.

    __get_all_live_matches_prompt(user_input: str, live_matches: List[MatchDetails], series: str) -> str
        Constructs the prompt for generating a response listing all live matches.

    __get_all_live_matches_prompt_template() -> PromptTemplate
        Retrieves the template for all live matches prompts.

    __get_fallback_prompt(user_input: str, reason: str) -> str
        Constructs the prompt for generating a fallback response.

    __get_fallback_prompt_template() -> PromptTemplate
        Retrieves the template for fallback prompts.
    """

    def __init__(self, openai_api_key: str):
        """
        Initializes the ResponseGeneratorService with the specified OpenAI API key.

        Parameters:
        ----------
        openai_api_key : str
            The API key for accessing the OpenAI service.
        """
        self.llm = ChatOpenAI(
            model=Constants.RESPONSE_GENERATOR_GPT_MODEL, 
            api_key=openai_api_key
        )
    
    def get_prompt(self, data: dict) -> str:
        """
        Determines the appropriate prompt based on the intent in the provided data.

        Parameters:
        ----------
        data : dict
            A dictionary containing user input and intent details.

        Returns:
        -------
        str
            The constructed prompt string.
        """
        match data.get('intent'):
            case Intent.live_score:
                prompt = self.__get_live_score_prompt(
                    data.get("user_input"), 
                    data.get("match_score", {})
                )
            case Intent.live_matches:
                prompt = self.__get_all_live_matches_prompt(
                    data.get("user_input"), 
                    data.get("live_matches", []),
                    data.get("series")
                )
            case _:
                prompt = self.__get_fallback_prompt(
                    data.get("user_input"), 
                    data.get("reason")
                )
        return prompt

    def __get_live_score_prompt(self, user_input: str, match_details: MatchDetails) -> str:
        """
        Constructs the prompt for generating a live score response.

        Parameters:
        ----------
        user_input : str
            The input text from the user.
        match_details : MatchDetails
            The details of the cricket match.

        Returns:
        -------
        str
            The formatted prompt string.
        """
        prompt_template = self.__get_live_score_prompt_template()
        prompt = prompt_template.format(
            user_input=user_input,
            format=match_details.format,
            series=match_details.series_name,
            **self.__extract_team_details(match_details.team1, prefix='t1'),
            **self.__extract_team_details(match_details.team2, prefix='t2'),
            status=match_details.status
        )
        return prompt

    def __extract_team_details(self, team_details: Optional[TeamScoreDetails], prefix: str) -> dict:
        """
        Extracts team details and formats them for prompt generation.

        Parameters:
        ----------
        team_details : Optional[TeamScoreDetails]
            The details of the team.
        prefix : str
            The prefix to use for formatting keys.

        Returns:
        -------
        dict
            A dictionary of formatted team details.
        """
        if not team_details:
            return {}

        return {
            f"{prefix}_name": team_details.name,
            f"{prefix}_abr": team_details.abr,
            f"{prefix}_run": team_details.run,
            f"{prefix}_wkt": team_details.wicket,
            f"{prefix}_ovr": team_details.over,
            f"{prefix}_dec": team_details.declared,
            f"{prefix}_inn2_run": team_details.run2,
            f"{prefix}_inn2_wkt": team_details.wicket2,
            f"{prefix}_inn2_ovr": team_details.over2,
            f"{prefix}_inn2_dec": team_details.declared2,
        }

    def __get_live_score_prompt_template(self) -> PromptTemplate:
        """
        Retrieves the template for live score prompts.

        Returns:
        -------
        PromptTemplate
            The template object for live score prompts.
        """
        return PromptTemplate.from_template(
            template=read_prompt_from_file(Constants.LIVE_SCORE_RESPONSE_PROMPT)
        )
    
    def __get_all_live_matches_prompt(self, user_input: str, live_matches: List[MatchDetails], series: str) -> str:
        """
        Constructs the prompt for generating a response listing all live matches.

        Parameters:
        ----------
        user_input : str
            The input text from the user.
        live_matches : List[MatchDetails]
            A list of MatchDetails objects representing live matches.
        series : str
            The series name for filtering matches.

        Returns:
        -------
        str
            The formatted prompt string.
        """
        prompt_template = self.__get_all_live_matches_prompt_template()
        prompt = prompt_template.format(
            user_input=user_input,
            series=series,
            live_matches=get_live_matches_as_string(live_matches)
        )
        return prompt
    
    def __get_all_live_matches_prompt_template(self) -> PromptTemplate:
        """
        Retrieves the template for all live matches prompts.

        Returns:
        -------
        PromptTemplate
            The template object for all live matches prompts.
        """
        return PromptTemplate.from_template(
            template=read_prompt_from_file(Constants.ALL_LIVE_MATCHES_RESPONSE_PROMPT)
        )

    def __get_fallback_prompt(self, user_input: str, reason: str) -> str:
        """
        Constructs the prompt for generating a fallback response.

        Parameters:
        ----------
        user_input : str
            The input text from the user.
        reason : str
            The reason for the fallback.

        Returns:
        -------
        str
            The formatted prompt string.
        """
        prompt_template = self.__get_fallback_prompt_template()
        prompt = prompt_template.format(
            user_input=user_input,
            reason=reason
        )
        return prompt

    def __get_fallback_prompt_template(self) -> PromptTemplate:
        """
        Retrieves the template for fallback prompts.

        Returns:
        -------
        PromptTemplate
            The template object for fallback prompts.
        """
        return PromptTemplate.from_template(
            template=read_prompt_from_file(Constants.FALLBACK_RESPONSE_PROMPT)
        )
