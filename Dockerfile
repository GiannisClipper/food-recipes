#sudo docker build .

FROM python:3.7-alpine
#lightweight version

MAINTAINER Giannis Clipper
#optional

ENV PYTHONUNBUFFERED 1
#recommended when running python into docker containers

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
#with -D the user can simply run processes, not having home directory or log in authorization
USER user
#switch to the user for security reasons (instead of root access)
