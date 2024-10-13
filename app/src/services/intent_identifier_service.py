import json
from typing import Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, BaseMessage, HumanMessage
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.models import MatchDetails
from src.constants import Constants
from src.utils import read_prompt_from_file, get_live_matches_as_string

class IntentIdentifierService:
    """
    A service class to identify user intents using the OpenAI language model.

    Attributes:
    ----------
    llm : ChatOpenAI
        An instance of ChatOpenAI configured with a specific model and API key.

    Methods:
    -------
    invoke(user_text: str, live_matches: List[MatchDetails]) -> Any
        Processes the user input text to identify the intent and returns the result.

    get_chat_prompt_template(parser: JsonOutputParser)
        Constructs a chat prompt template for the language model.

    __get_llm_messages(user_text: str, live_matches: List[MatchDetails]) -> List[BaseMessage]
        Constructs a list of messages for the language model, including system and human messages.

    __get_system_message(live_matches: List[MatchDetails]) -> SystemMessage
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
        self.llm = ChatOpenAI(
            model=Constants.INTENT_IDENTIFIER_GPT_MODEL, 
            api_key=openai_api_key
        )
    
    def get_chat_prompt_template(self, parser: JsonOutputParser):
        """
        Constructs a chat prompt template for the language model.

        Parameters:
        ----------
        parser : JsonOutputParser
            The parser to format the output.

        Returns:
        -------
        ChatPromptTemplate
            The constructed chat prompt template.
        """
        return ChatPromptTemplate.from_messages(
            [
                self.__get_system_message_prompt_template_for_chain(parser),
                self.__get_human_message_prompt_template_for_chain()
            ]
        )

    def __get_system_message_prompt_template_for_chain(self, parser: JsonOutputParser):
        """
        Retrieves the system message prompt template for the language model chain.

        Parameters:
        ----------
        parser : JsonOutputParser
            The parser to format the output.

        Returns:
        -------
        SystemMessagePromptTemplate
            The system message prompt template.
        """
        return SystemMessagePromptTemplate.from_template(
            template=read_prompt_from_file(Constants.INTENT_IDENTIFIER_SYS_MSG_FILE_NAME),
            input_variables=["live_matches"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
    
    def __get_human_message_prompt_template_for_chain(self):
        """
        Retrieves the human message prompt template for the language model chain.

        Returns:
        -------
        HumanMessagePromptTemplate
            The human message prompt template.
        """
        return HumanMessagePromptTemplate.from_template(
            template="{user_input}",
            input_variables=["user_input"],
        )