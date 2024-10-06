import os

class Constants:
    """
    A class to hold constant values used across the application.
    This includes model identifiers, file paths, and standard response messages.
    """

    # Model identifiers for different GPT models used in the application
    INTENT_IDENTIFIER_GPT_MODEL: str = "gpt-3.5-turbo"
    RESPONSE_GENERATOR_GPT_MODEL: str = "gpt-4o"

    # Base file path for storing prompt files
    BASE_FILE_PATH: str = os.path.join("app", "prompts")

    # File names for system messages and prompts
    INTENT_IDENTIFIER_SYS_MSG_FILE_NAME: str = "intent_identifier_system_message.txt"
    LIVE_SCORE_RESPONSE_PROMPT: str = "live_score_response_prompt.txt"
    FALLBACK_RESPONSE_PROMPT: str = "fallback_response_prompt.txt"

    # Standard response messages for various scenarios
    REASON_NOT_PRESENT: str = "Not able to understand the given input."
    TEAMS_NOT_PRESENT_REASON: str = "Couldn't identify teams from your response."
    MATCH_NOT_PRESENT_REASON: str = "Couldn't find a match between {team1} and {team2}"
