from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
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
    
    def get_prompt_template(self, parser: JsonOutputParser):
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
        return PromptTemplate.from_template(
            template=read_prompt_from_file(Constants.INTENT_IDENTIFIER_PROMPT),
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )