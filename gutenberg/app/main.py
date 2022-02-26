import os

import openai
import uvicorn

from fastapi import FastAPI

from gutenberg.app.db import engine
from gutenberg.app.models import Base
from gutenberg.app.routes import router

openai.api_key = os.getenv("OPENAI_API_KEY")

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Gutenberg')
app.include_router(router)

if __name__ == '__main__':
    # noinspection PyTypeChecker
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
