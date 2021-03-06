from typing import Optional

from pydantic import BaseModel


class User(BaseModel):

    id: int


class Prompt(BaseModel):

    id: Optional[int]
    item_name: str
    item_description: str
    target_audience: str
    platform: str


class Prediction(BaseModel):

    id: Optional[int]
    prompt_id: int
    text: str


class Feedback(BaseModel):

    user_id: int
    prediction_id: int
