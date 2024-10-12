import os
from dotenv import find_dotenv, load_dotenv
import streamlit as st
from src.services import CricbotService

# Define avatars for assistant and user
avatars = {
    "assistant": "🏏",  # Cricket bat and ball emoji for the assistant
    "user": "🙋‍♂️"       # Person raising hand emoji for the user
}

def initialize_environment():
    """
    Loads environment variables from a .env file.
    """
    load_dotenv(find_dotenv(), override=True)

def get_openai_api_key() -> str:
    """
    Retrieves the OpenAI API key from environment variables.

    Returns:
    -------
    str
        The OpenAI API key.
    """
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")
    return api_key

def initialize_chatbot(api_key: str) -> CricbotService:
    """
    Initializes the CricbotService with the provided API key.

    Parameters:
    ----------
    api_key : str
        The OpenAI API key.

    Returns:
    -------
    CricbotService
        An instance of CricbotService.
    """
    return CricbotService(api_key)

def display_initial_messages():
    """
    Displays the initial message from the assistant.
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I am Cricbot. You can ask me questions about cricket"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"], avatar=avatars[msg["role"]]).write(msg["content"])

def handle_user_input(cricbot_service: CricbotService):
    """
    Handles user input and generates a response using CricbotService.

    Parameters:
    ----------
    cricbot_service : CricbotService
        An instance of CricbotService to generate responses.
    """
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar=avatars["user"]).write(prompt)
        
        # Create a placeholder for the loading spinner
        with st.spinner("Generating response..."):
            try:
                response = cricbot_service.bot_response(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.chat_message("assistant", avatar=avatars["assistant"]).write(response)
            except Exception as e:
                print(e)
                error_message = "Error generating response"
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                st.chat_message("assistant", avatar=avatars["assistant"]).write(error_message)

def main():
    """
    Main function to run the Streamlit application.
    """
    st.set_page_config(page_title="Cricbot", page_icon="🏏")
    st.title("🏏 Cricbot")
    initialize_environment()
    api_key = get_openai_api_key()
    cricbot_service = initialize_chatbot(api_key)
    display_initial_messages()
    handle_user_input(cricbot_service)

if __name__ == "__main__":
    main()
