FROM python:3.8-slim-buster AS backend

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY gutenberg gutenberg

CMD python rexify/app/main.py