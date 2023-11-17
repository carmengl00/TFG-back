FROM python:3.11-bullseye AS builder
ENV PYTHONUNBUFFERED=1
WORKDIR /home/ubuntu/webs/backend/backend
COPY pyproject.toml /home/ubuntu/webs/backend/backend
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
COPY . .

FROM builder AS local
RUN poetry install -n --no-ansi --with local,testing

FROM builder AS deploy
RUN poetry install -n --no-ansi --with deploy
