from enum import Enum


class Intent(str, Enum):
    live_matches = "live_matches"
    live_score = "live_score"
    fallback = "fallback"
