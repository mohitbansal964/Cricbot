import json
from typing import Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, BaseMessage, HumanMessage
from langchain_core.prompts import SystemMessagePromptTemplate
from models import MatchDetails
from constants import Constants
from utils import read_prompt_from_file, get_live_matches_as_string

class IntentIdentifierService:
    """
    A service class to identify user intents using the OpenAI language model.

    Attributes:
    ----------
    __llm_chain : ChatOpenAI
        An instance of ChatOpenAI configured with a specific model and API key.

    Methods:
    -------
    invoke(user_text: str) -> Any
        Processes the user input text to identify the intent and returns the result.

    __get_llm_messages(user_text: str) -> List[BaseMessage]
        Constructs a list of messages for the language model, including system and human messages.

    __get_system_message() -> SystemMessage
        Retrieves the system message content from a predefined file.

    __get_human_message(user_text: str) -> HumanMessage
        Creates a human message object from the user input text.
    """

    def __init__(self, openai_api_key: str):
        """
        Initializes the IntentIdentifierService with the specified OpenAI API key.

        Parameters:
        ----------
        openai_api_key : str
            The API key for accessing the OpenAI service.
        """
        self.__llm_chain = ChatOpenAI(
            model=Constants.INTENT_IDENTIFIER_GPT_MODEL, 
            api_key=openai_api_key
        )

    def invoke(self, user_text: str, live_matches: List[MatchDetails]) -> Any:
        """
        Identifies the intent from the user's input text using the language model.

        Parameters:
        ----------
        user_text : str
            The input text from the user.

        Returns:
        -------
        Any
            The identified intent as a JSON object.
        """
        messages = self.__get_llm_messages(user_text, live_matches)
        output = self.__llm_chain.invoke(messages)
        return json.loads(output.content)

    def __get_llm_messages(self, user_text: str, live_matches: List[MatchDetails]) -> List[BaseMessage]:
        """
        Constructs the list of messages to be sent to the language model.

        Parameters:
        ----------
        user_text : str
            The input text from the user.

        Returns:
        -------
        List[BaseMessage]
            A list containing the system and human messages.
        """
        return [
            self.__get_system_message(live_matches),
            self.__get_human_message(user_text)
        ]

    def __get_system_message(self, live_matches: List[MatchDetails]) -> SystemMessage:
        """
        Retrieves the system message from a predefined file.

        Returns:
        -------
        SystemMessage
            The system message containing the prompt content.
        """
        system_msg_template = SystemMessagePromptTemplate.from_template(
            template=read_prompt_from_file(Constants.INTENT_IDENTIFIER_SYS_MSG_FILE_NAME)
        )
        return system_msg_template.format(live_matches=get_live_matches_as_string(live_matches))

    def __get_human_message(self, user_text: str) -> HumanMessage:
        """
        Creates a human message from the user's input text.

        Parameters:
        ----------
        user_text : str
            The input text from the user.

        Returns:
        -------
        HumanMessage
            The human message object containing the user's input.
        """
        return HumanMessage(content=user_text)
