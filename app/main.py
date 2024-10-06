import os
from dotenv import find_dotenv, load_dotenv
from services import CricbotService

# loading the API Keys from .env
load_dotenv(find_dotenv(), override=True)

if __name__ == "__main__":
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    cricbot_service = CricbotService(openai_api_key)
    while True:
        user_input = input("User: ")
        if user_input == "exit":
            break
        cricbot_service.bot_response(user_input)
