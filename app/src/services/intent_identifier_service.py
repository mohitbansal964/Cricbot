# Import necessary modules and classes
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
    get_prompt_template(parser: JsonOutputParser)
        Constructs a prompt template for the language model.
    """

    def __init__(self, openai_api_key: str):
        """
        Initializes the IntentIdentifierService with the specified OpenAI API key.

        Parameters:
        ----------
        openai_api_key : str
            The API key for accessing the OpenAI service.
        """
        # Initialize the language model with the specified model and API key
        self.llm = ChatOpenAI(
            model=Constants.INTENT_IDENTIFIER_GPT_MODEL, 
            api_key=openai_api_key
        )
    
    def get_prompt_template(self, parser: JsonOutputParser) -> PromptTemplate:
        """
        Constructs a chat prompt template for the language model.

        Parameters:
        ----------
        parser : JsonOutputParser
            The parser to format the output.

        Returns:
        -------
        PromptTemplate
            The constructed chat prompt template.
        """
        # Create a prompt template using a predefined template file and parser instructions
        return PromptTemplate.from_template(
            template=read_prompt_from_file(Constants.INTENT_IDENTIFIER_PROMPT),
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )