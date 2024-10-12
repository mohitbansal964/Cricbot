import os
from dotenv import find_dotenv, load_dotenv
from src.utils import generate_metadata
from src.chains import generate_chain
from src.services import CricbotService

# Load environment variables from a .env file
load_dotenv(find_dotenv(), override=True)

if __name__ == "__main__":
    """
    Main script to run the CricbotService for user interaction.

    The script initializes the CricbotService with the OpenAI API key
    and enters a loop to continuously accept user input and generate responses.
    """

    # Retrieve the OpenAI API key from environment variables
    openai_api_key = os.environ.get('OPENAI_API_KEY')

    # Initialize the CricbotService with the API key
    cricbot_service = CricbotService(openai_api_key)

    # Continuously prompt the user for input and generate responses
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        # Using langchain to sequence LLMs and Data fetching components
        metadata = generate_metadata(user_input=user_input)
        response = generate_chain(openai_api_key, metadata).invoke(metadata)

        # Using custom service
        # response = cricbot_service.bot_response(user_input)
        
        print("Cricbot:", response)
