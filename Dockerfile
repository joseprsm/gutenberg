FROM python:3.8-slim-buster AS backend

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY gutenberg/app gutenberg/app

COPY setup.py setup.py
COPY setup.cfg setup.cfg

RUN pip install -e .

CMD python gutenberg/app/main.py