#!/usr/bin/env

virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=development # enables debug mode
flask run