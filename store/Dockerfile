FROM python:3.11-slim

RUN apt-get update; apt install -y python3-venv python3-dev libpq-dev

COPY ./ /store

WORKDIR /store

RUN python -m pip install --no-cache-dir poetry; poetry self update && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi \
