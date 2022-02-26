from typing import List

import openai

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from gutenberg.app.db import get_db
from gutenberg.app import models
from gutenberg.app import schemas

router = APIRouter()


@router.post('/')
def predict(prompt: schemas.Prompt, db: Session = Depends(get_db)):

    db_prompt = models.Prompt(
        item_name=prompt.item_name,
        item_description=prompt.item_description,
        target_audience=prompt.target_audience,
        platform=prompt.platform,
        user_id=prompt.user_id
    )

    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)

    predictions: List[str] = openai.Completion.create(
        engine="text-davinci-001",
        prompt=prompt.generate(),
        temperature=0.6, n=1, max_tokens=1000
    ).choices

    for pred_text in predictions:
        db_pred = models.Prediction(prompt_id=db_prompt.id, text=pred_text)
        db.add(db_pred)
        db.commit()
        db.refresh(db_pred)


@router.get('/')
def get_predictions(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    return db.query(models.Prediction).offset(skip).limit(limit).all()

