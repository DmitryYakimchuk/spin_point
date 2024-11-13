FROM python:3.11.4-slim as build_app

ENV APP_ROOT=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$APP_ROOT

RUN apt update \
    && apt install -y postgresql postgresql-contrib libpq-dev gcc

RUN pip install poetry==1.8.2

WORKDIR $APP_ROOT
COPY pyproject.toml poetry.lock poetry.toml $APP_ROOT
RUN poetry install --without dev --no-root

FROM build_app as build_app_dev

RUN poetry install --only dev

FROM build_app as app

COPY . .

ARG USER_NAME=app
ARG GROUP_NAME=app

RUN addgroup --system $GROUP_NAME
RUN adduser --system $USER_NAME

RUN chown -R $USER_NAME:$GROUP_NAME $APP_ROOT

USER $USER_NAME

FROM build_app_dev as app_dev

COPY . .

ARG USER_NAME=app
ARG GROUP_NAME=app

RUN addgroup --system $GROUP_NAME
RUN adduser --system $USER_NAME

RUN chown -R $USER_NAME:$GROUP_NAME $APP_ROOT

USER $USER_NAME
