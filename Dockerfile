# to implement Dockerfile: $ sudo docker build .
# to implement when modified: $ sudo docker-compose build

FROM python:3.7-alpine
# alpine = lightweight version

MAINTAINER Giannis Clipper
# optional

ENV PYTHONUNBUFFERED 1
# recommended when running python into docker containers

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev
# apk = run package manager which comes with Alpine to add a new package
# --no-cache = no store registry index in docker file
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# temporary packages

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps
# remove temporary packages

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/media

RUN adduser -D user
# with -D the user can simply run processes, not having home directory or log in authorization
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web

USER user
# switch to the user for security reasons (instead of root access)
