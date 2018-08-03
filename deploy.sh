#!/usr/bin/env bash
git push heroku master

heroku run python manage.py migrate
#heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic --no-input

heroku run python manage.py check --deploy
