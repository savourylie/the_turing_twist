from pydantic import BaseModel, Field
from datetime import datetime, timezone


class EloScore(BaseModel):
    model_name: str
    elo_score: float = 100.0
    play_count: int = 0
    detective_count: int = 0
    thief_count: int = 0
    detective_win_count: int = 0
    thief_win_count: int = 0
    fail_nlu_count: int = 0
    fail_willingness_count: int = 0
    created_datetime: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_modified_datetime: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    @classmethod
    def create(cls, **kwargs):
        current_time = datetime.now(timezone.utc)
        kwargs['created_datetime'] = current_time
        kwargs['last_modified_datetime'] = current_time
        return cls(**kwargs)
    
    @classmethod
    def from_dict(cls, elo_score_dict: dict):
        return cls(**elo_score_dict)