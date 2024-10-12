from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from src.enums import Intent

class Entities(BaseModel):
    series: Optional[str] = Field(None, description="Series of a cricket match")
    team1: Optional[str] = Field(None, description="Name of team 1")
    team2: Optional[str] = Field(None, description="Name of team 2")
    reason: Optional[str] = Field(None, description="Reason why intent identification failed")
    date: Optional[datetime] = Field(None, description="Date of the match")

class IntentDetails(BaseModel):
    intent: Intent = Field(description="intent of the text message")
    entities: Optional[Entities] = Field(default_factory=Entities, description="Entities to find in the text message")