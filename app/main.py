import os
from dotenv import find_dotenv, load_dotenv
from src.utils import generate_metadata
from src.chains import generate_chain

# Load environment variables from a .env file
load_dotenv(find_dotenv(), override=True)

if __name__ == "__main__":

    # Retrieve the OpenAI API key from environment variables
    openai_api_key = os.environ.get('OPENAI_API_KEY')

    # Continuously prompt the user for input and generate responses
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        # Using langchain to sequence LLMs and Data fetching components
        metadata = generate_metadata(user_input=user_input)
        response = generate_chain(openai_api_key, metadata).invoke(metadata)
        
        print("Cricbot:", response)
