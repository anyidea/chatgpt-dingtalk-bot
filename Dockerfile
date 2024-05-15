ARG PYTHON_VERSION=3.12-slim-bookworm
ARG POETRY_VERSION=1.8.3
ARG APP_HOME=/app

FROM --platform=$TARGETPLATFORM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as builder

ARG APP_HOME
ARG POETRY_VERSION
WORKDIR ${APP_HOME}

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="/root/.cargo/bin:${PATH}"


# Install apt packages
RUN apt-get update --fix-missing && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # dependencies for installing poetry
  pipx

# Speed up installing poetry
RUN pipx install poetry==${POETRY_VERSION} \
    && pipx ensurepath \
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

RUN addgroup --system chatbot \
    && adduser --system --ingroup chatbot chatbot

# Install required system dependencies
RUN apt-get update --fix-missing \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency packages from builder
COPY --from=builder --chown=chatbot:chatbot ${APP_HOME} ${APP_HOME}

COPY --chown=chatbot:chatbot ./docker/start /start
RUN sed -i 's/\r$//g' /start \
    && chmod +x /start

# copy application code to WORKDIR
COPY --chown=chatbot:chatbot . ${APP_HOME}
# make django owner of the WORKDIR directory as well.
RUN chown chatbot:chatbot ${APP_HOME}

USER chatbot

CMD ["/start"]
