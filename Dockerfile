# pull official base image
FROM python:3.12.0-slim-bullseye AS app

# set work directory
WORKDIR /usr/src/app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \ 
  && mkdir -p /usr/src/app/media/


ENV PYTHONDONTWRITEBYTECODE="true" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="/usr/src/app" \
    PATH="${PATH}:/home/python/.local/bin" \
    APP_ALLOWED_HOSTS='["*"]' \ 
    APP_DATABASES__default__ENGINE="django.db.backends.postgresql" \
    APP_DATABASES__default__NAME="ecomm" \
    APP_DATABASES__default__USER="admin" \
    APP_DATABASES__default__PASSWORD="admin" \
    APP_DATABASES__default__HOST="postgres" \
    APP_MEDIA_ROOT="/usr/src/app/media" \
    APP_MEDIA_URL="/media/" \
    APP_DOMAIN="http://0.0.0.0:8000/"\
    APP_REDIS_HOST="redis"\
    APP_REDIS_PORT=6379\
    DJANGO_SETTINGS_MODULE="core.settings" 
 

# install dependencies

COPY ./requirements.txt .
RUN pip install -r requirements.txt \
    && pip install --upgrade pip 

# copy project
COPY . .

COPY ./entrypoint.sh .
COPY ./task_trigger.py .


RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh



ENTRYPOINT ["/usr/src/app/entrypoint.sh"]