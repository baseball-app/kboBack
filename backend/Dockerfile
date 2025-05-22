FROM python:3.12

RUN apt-get update && apt-get install -y \
    vim \
    redis-server

WORKDIR /backend
COPY . .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction
RUN poetry run python manage.py makemigrations
RUN poetry run python manage.py collectstatic

EXPOSE 8001
