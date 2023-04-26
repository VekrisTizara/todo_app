from pydantic import BaseModel, Field
from enum import Enum

class StatusEnum(str, Enum):
    completed = "completed"
    not_completed = "not completed"

class Task(BaseModel):
    id: str = Field()
    title: str = Field(max_length=250)
    description: str = Field(max_length=4000)
    status: StatusEnum


