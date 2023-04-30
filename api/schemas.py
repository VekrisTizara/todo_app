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

class TokenTypeEnum(str, Enum):
    google = "google"
    custom = "custom"

class Token(BaseModel):
    token_value: str
    token_type: TokenTypeEnum
    username: str

class User(BaseModel):
    username: str
    email: str
    disabled: bool
