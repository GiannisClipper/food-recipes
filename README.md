Practicing Udemy Course: Create an advanced REST API with Python,
Django REST Framework and Docker using Test Driven Development (TDD)


SETUP Docker

  https://docs.docker.com/install/linux/docker-ce/ubuntu/
  (install using the convenience script)
  $ curl -fsSL https://get.docker.com -o get-docker.sh
  $ sudo sh get-docker.sh

  https://docs.docker.com/compose/install/
  $ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
  $ sudo chmod +x /usr/local/bin/docker-compose

EDIT /Dockerfile

EDIT /requirements.txt

EDIT /docker-compose.yml


CREATE a django project (inside docker container)
  $ sudo docker-compose run app sh -c "django-admin.py startproject app ."


SETUP travis
  https://travis-ci.org/ (sign in with github)

  EDIT /.travis.yml

  EDIT /app/.flake8


CREATE a django core app
  $ sudo docker-compose run app sh -c "python manage.py startapp core"
  (remove tests.py and views.py from /app/core)
  (create directory /app/core/tests with __init__.py)
  (add 'core' in INSTALLED_APPS list in /app/app/settings.py)


CREATE & RUN tests
    (create /app/core/test_models.py)
    $ sudo docker-compose run app sh -c "python manage.py test"


IMPLEMENT custom user model
  (create user model in models.py in the core app)
  (add in /app/app/settings.py: AUTH_USER_MODEL = 'core.User')
  $ sudo docker-compose run app sh -c "python manage.py makemigrations core"
