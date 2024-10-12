from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from src.enums import Intent

class Entities(BaseModel):
    """
    A Pydantic model to represent entities related to a cricket match.

    Attributes:
    ----------
    series : Optional[str]
        The series of a cricket match.
    team1 : Optional[str]
        The name of the first team.
    team2 : Optional[str]
        The name of the second team.
    reason : Optional[str]
        The reason why intent identification might have failed.
    date : Optional[datetime]
        The date of the match.
    """
    series: Optional[str] = Field(None, description="Series of a cricket match")
    team1: Optional[str] = Field(None, description="Name of team 1")
    team2: Optional[str] = Field(None, description="Name of team 2")
    reason: Optional[str] = Field(None, description="Reason why intent identification failed")
    date: Optional[datetime] = Field(None, description="Date of the match")

class IntentDetails(BaseModel):
    """
    A Pydantic model to represent the details of a user's intent.

    Attributes:
    ----------
    intent : Intent
        The identified intent of the text message.
    entities : Optional[Entities]
        The entities found in the text message.
    """
    intent: Intent = Field(description="intent of the text message")
    entities: Optional[Entities] = Field(default_factory=Entities, description="Entities to find in the text message")
