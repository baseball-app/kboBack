FROM python:3.12

RUN apt-get update && apt-get install -y \
    vim \
    redis-server

RUN mkdir -p /server/backend
RUN mkdir /ssl
COPY . /server

WORKDIR /server/backend

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

WORKDIR /server/backend
RUN python manage.py makemigrations
RUN echo yes | python manage.py collectstatic

EXPOSE 8001
