from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class MatchResultEnum(str, Enum):
    DETECTIVE_IDENTIFIED_THIEF = "Detective identified the thief"
    DETECTIVE_FAILED_TO_IDENTIFY_THIEF = "Detective failed to identify the thief"
    DETECTIVE_RAN_OUT_OF_TIME = "Detective ran out of time"
    THIEF_REFUSED_TO_PLAY = "Thief refused to play"
    THIEF_MISUNDERSTOOD_RULES = "Thief misunderstood the rules"


class MatchResultModel(BaseModel):
    result: MatchResultEnum


class TTTMatch(BaseModel):
    detective_model: str
    thief_model: str
    match_result: MatchResultModel
    created_datetime: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_modified_datetime: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    @classmethod
    def create(cls, **kwargs) -> "TTTMatch":
        current_time = datetime.now(timezone.utc)
        kwargs['created_datetime'] = current_time
        kwargs['last_modified_datetime'] = current_time
        return cls(**kwargs)

    @classmethod
    def from_dict(cls, match_dict: dict) -> "TTTMatch":
        return cls(**match_dict)

    def update_last_modified(self):
        self.last_modified_datetime = datetime.now(timezone.utc)