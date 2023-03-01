ARG PYTHON_VERSION=3.11-slim-bullseye
ARG POETRY_VERSION=1.4.0
ARG APP_HOME=/app

FROM --platform=$TARGETPLATFORM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as builder

ARG APP_HOME
ARG POETRY_VERSION
WORKDIR ${APP_HOME}

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential

# Speed up installing poetry
RUN python3 -m pip install poetry==${POETRY_VERSION} \
    && poetry --version

# Requirements are installed here to ensure they will be cached.
COPY ./poetry.lock ./pyproject.toml ./
# Use poetry to install python dependencies
RUN  poetry install --only main --no-interaction --no-ansi --no-root


# Python 'run' stage
FROM python as runtime

ARG APP_HOME
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="${APP_HOME}/.venv/bin:$PATH"
WORKDIR ${APP_HOME}

RUN addgroup --system fastapi \
    && adduser --system --ingroup fastapi fastapi

# Install required system dependencies
RUN apt-get update \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency packages from builder
COPY --from=builder --chown=fastapi:fastapi ${APP_HOME} ${APP_HOME}

COPY --chown=fastapi:fastapi ./docker/start /start
RUN sed -i 's/\r$//g' /start \
    && chmod +x /start

# copy application code to WORKDIR
COPY --chown=fastapi:fastapi . ${APP_HOME}
# make django owner of the WORKDIR directory as well.
RUN chown fastapi:fastapi ${APP_HOME}

USER fastapi

ENTRYPOINT ["/start"]
