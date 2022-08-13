FROM python:3.10

RUN apt-get -y update \
    && apt-get install -y gettext git \
    # Cleanup apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry POETRY_VERSION=1.1.12 python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN bash -c "poetry install --no-root --no-dev"

COPY src/shutterbox ./src/shutterbox
RUN bash -c "poetry install"

COPY docker-entrypoint.sh ./

EXPOSE 8080

ENV APP_CLI=shutterbox

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
CMD gunicorn --config src/shutterbox/gunicorn.conf.py shutterbox.app:app
