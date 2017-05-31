FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

ENV GUNICORN_CMD_ARGS="--bind=:8000 --workers=4"

ENV POSTGRES_HOST="storage-container"
ENV POSTGRES_PORT="5432"


CMD ["gunicorn", "app:app"]