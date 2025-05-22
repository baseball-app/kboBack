FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    vim \
    curl \
    && apt-get clean

RUN pip install poetry

WORKDIR /backend
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction

EXPOSE 8001
