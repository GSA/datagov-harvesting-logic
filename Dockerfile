FROM python:3.11

ARG pyversion=3.11 

WORKDIR /app 

ADD . /app

RUN pip install poetry

RUN poetry env use $pyversion

RUN poetry install
