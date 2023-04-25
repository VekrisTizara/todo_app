from pydantic import BaseModel, Field
from enum import Enum

class StatusEnum(str, Enum):
    complited = "complited"
    not_complited = "not complited"

class Task(BaseModel):
    title: str = Field(max_length=250)
    description: str = Field(max_length=4000)
    status: StatusEnum


