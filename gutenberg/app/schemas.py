from pydantic import BaseModel


class User(BaseModel):

    id: int


class Prompt(BaseModel):

    id: int
    item_name: str
    item_description: str
    platform: str
    user_id: int


class Prediction(BaseModel):

    id: int
    prompt_id: int
    text: str


class Feedback(BaseModel):

    user_id: int
    prediction_id: int
