# REF: https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
# A Docker multi-stage build was used to reduce the final image size. 
# The builder is a temporary image that's used for building the Python wheels. 
# The wheels are then copied over to the final production image and the builder image is discarded.
###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.1-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
#RUN pip install flake8
COPY . /usr/src/app/
#RUN flake8 --ignore=E501,F401 .

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.8.1-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
#RUN addgroup -S app && adduser -S app -G app
RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends netcat
# TODO: remove tools/apps after dev cycles complete
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat \
    procps \
    net-tools \
    lsof \
    vim

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

EXPOSE 5000

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
