Practicing Udemy Course: Create an advanced REST API with Python,\
Django REST Framework and Docker using Test Driven Development (TDD)\
-----------------------------------------------------------------------\
Notes:\
\
SETUP Docker\
  https://docs.docker.com/install/linux/docker-ce/ubuntu/ \
  (install using the convenience script)\
  $ curl -fsSL https://get.docker.com -o get-docker.sh\
  $ sudo sh get-docker.sh\
\
  https://docs.docker.com/compose/install/ \
  $ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
  $ sudo chmod +x /usr/local/bin/docker-compose\
\
EDIT /Dockerfile\
EDIT /requirements.txt\
EDIT /docker-compose.yml\
\
CREATE a django project (inside docker container)\
  $ sudo docker-compose run app sh -c "django-admin.py startproject app ."\
\
SETUP travis\
  https://travis-ci.org/ (sign in with github)\
  EDIT /.travis.yml\
  EDIT /app/.flake8\
\
CREATE a django core app\
  $ sudo docker-compose run app sh -c "python manage.py startapp core"\
  (remove tests.py and views.py from /app/core)\
  (create directory /app/core/tests with __init__.py)\
  (add 'core' in INSTALLED_APPS list in /app/app/settings.py)\
\
CREATE & RUN tests (and flake8 for linting)\
    (create /app/core/test_models.py)\
    $ sudo docker-compose run app sh -c "python manage.py test && flake8"\
\
CREATE a custom user model\
  (create user model in models.py in the core app)\
  (add in /app/app/settings.py: AUTH_USER_MODEL = 'core.User')\
  $ sudo docker-compose run app sh -c "python manage.py makemigrations core"\
\
ADD a supper user\
  $ sudo docker-compose run app sh -c "python manage.py createsuperuser"\
\
SETUP postgres instead of default sqlite\
  (add in requirements.txt: psycopg2)\
  (modify Dockerfile)\
  $ sudo docker-compose build\
  (modify in /app/app/settings.py: DATABASES = ...)\
\
CREATE custom command wait_for_db\
  (/app/core/management/commands/wait_for_db.py)\
  (add in docker-compose.yml: wait_for_db and migrate before runserver)\
  $ sudo docker-compose up\
\
CREATE a user app\
  $ sudo docker-compose run app sh -c "python manage.py startapp user"\
  (remove migrations, admin.py, models.py from /app/user -keep in core app)\
  (remove tests.py but create directory /app/user/tests with __init__.py)\
  (add 'user' in INSTALLED_APPS list in /app/app/settings.py)\
  (add 'rest_framework' in INSTALLED_APPS list in /app/app/settings.py)\
  (add 'rest_framework.authtoken' in INSTALLED_APPS list in /app/app/settings.py)\
  (add 'admin.site.register(models.User, UserAdmin)' in /app/core/admin.py)\
\
CREATE a recipe app\
  $ sudo docker-compose run app sh -c "python manage.py startapp recipe"\
  (remove migrations, admin.py, models.py from /app/user -keep in core app)\
  (remove tests.py but create directory /app/user/tests with __init__.py)\
  (add 'recipe' in INSTALLED_APPS list in /app/app/settings.py)\
\
CREATE a tag model\
  (create tag model in models.py in the core app)\
  $ sudo docker-compose run app sh -c "python manage.py makemigrations core"\

ADD in recipe app tag operations\
  (add 'admin.site.register(models.Tag)' in /app/core/admin.py)\
  (create recipe/tests/test_tags_api.py)\
  (modify recipe/serializers.py, recipe/views.py, recipe/urls.py)\

CREATE an ingredient model (similar to tag model)\
  (create ingredient model in models.py in the core app)\
  $ sudo docker-compose run app sh -c "python manage.py makemigrations core"\

ADD in recipe app ingredient operations (similar to tag operations)\
  (add 'admin.site.register(models.Ingredient)' in /app/core/admin.py)\
  (create recipe/tests/test_ingredients_api.py)\
  (modify recipe/serializers.py, recipe/views.py, recipe/urls.py)\

SETUP upload files operation\
  (add python package Pillow in /requirements.txt)\
  (add linux package jpeg-dev in /Dockerfile (permanent dependencies))\
  (add linux packages musl-dev zlib zlib-dev in /Dockerfile (temp depend...))\
  (add 'RUN mkdir -p /vol/web/static' in /Dockerfile)\
  (add 'RUN mkdir -p /vol/web/media' in /Dockerfile)\
  (add 'RUN chown -R user:user /vol/' in Dockerfile)\
  (add 'RUN chmod -R 755 /vol/web' in Dockerfile (full permissions to user))\
  (add 'MEDIA_URL = '/media/'' in /app/settings.py)\
  (add 'MEDIA_ROOT = '/vol/web/media'' in /app/settings.py)\
  (add 'STATIC_ROOT = '/vol/web/static'' in /app/settings.py)\
  (add 'from.django.conf.urls.static import static' in /app/urls.py)\
  (add 'from.django.conf import settings' in /app/urls.py)\
  (add '+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)' in /app/urls.py)\
  ($ sudo docker-compose build (rebuild docker image))\
