from enum import Enum

class Intent(str, Enum):
    """
    An enumeration class to represent different user intents in a chatbot application.

    Attributes:
    ----------
    live_matches : str
        Represents the intent to inquire about live cricket matches.
    live_score : str
        Represents the intent to inquire about the live score of a specific match.
    fallback : str
        Represents a fallback intent when the user's input does not match any known intents.
    """
    
    live_matches = "live_matches"
    live_score = "live_score"
    fallback = "fallback"
