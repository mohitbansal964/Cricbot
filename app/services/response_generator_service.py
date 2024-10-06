import json
from typing import Any, List
from langchain_openai import ChatOpenAI
from constants import Constants
from models import MatchDetails
from utils import read_prompt_from_file
from langchain.prompts import PromptTemplate

class ResponseGeneratorService:
    """
    A service class to generate responses using the OpenAI language model.

    Attributes:
    ----------
    __llm_chain : ChatOpenAI
        An instance of ChatOpenAI configured with a specific model and API key.

    Methods:
    -------
    get_live_score_response(user_input: str, match_details: MatchDetails) -> str
        Generates a response for live cricket scores based on user input and match details.

    get_fallback_response(user_input: str, reason: str) -> str
        Generates a fallback response when the input cannot be processed as expected.

    __get_live_score_prompt(user_input: str, match_details: MatchDetails) -> str
        Constructs the prompt for generating a live score response.

    __get_live_score_prompt_template() -> PromptTemplate
        Retrieves the template for live score prompts.

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
        self.__llm_chain = ChatOpenAI(
            model=Constants.RESPONSE_GENERATOR_GPT_MODEL, 
            api_key=openai_api_key
        )

    def get_live_score_response(self, user_input: str, match_details: MatchDetails) -> str:
        """
        Generates a response for live cricket scores based on user input and match details.

        Parameters:
        ----------
        user_input : str
            The input text from the user.
        match_details : MatchDetails
            The details of the cricket match.

        Returns:
        -------
        str
            The generated response content.
        """
        prompt = self.__get_live_score_prompt(user_input, match_details)
        output = self.__llm_chain.invoke(prompt)
        return output.content

    def get_fallback_response(self, user_input: str, reason: str) -> str:
        """
        Generates a fallback response when the input cannot be processed as expected.

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
        prompt = self.__get_fallback_prompt(user_input, reason)
        output = self.__llm_chain.invoke(prompt)
        return output.content

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
            t1_name=match_details.team_1.name,
            t1_abr=match_details.team_1.abr,
            t1_run=match_details.team_1.run,
            t1_wkt=match_details.team_1.wicket,
            t1_ovr=match_details.team_1.over,
            t2_name=match_details.team_2.name,
            t2_abr=match_details.team_2.abr,
            t2_run=match_details.team_2.run,
            t2_wkt=match_details.team_2.wicket,
            t2_ovr=match_details.team_2.over,
            status=match_details.status
        )
        return prompt

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
