from pydantic import BaseModel, Field
from enum import Enum

class NLUChoice(str, Enum):
    YES = "yes"
    NO = "no"

class NLUAnswer(BaseModel):
    answer: NLUChoice = Field(..., description="The answer, either 'yes' or 'no'")

class SafeAIChoice(str, Enum):
    YES = "yes"
    NO = "no"

class SafeAIAnswer(BaseModel):
    answer: SafeAIChoice = Field(..., description="The answer, either 'yes' or 'no'")

class DetectiveChoice(str, Enum):
    HUMAN = "human"
    AI = "ai"
    UNSURE = "unsure"

class DetectivesAnswer(BaseModel):
    answer: DetectiveChoice = Field(..., description="The detective's answer: 'human', 'ai', or 'unsure'")


# print(NLUAnswer.model_json_schema())