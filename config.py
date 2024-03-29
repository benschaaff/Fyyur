import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode. Can also be set via env variable => FLASK_ENV=development
# DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://ben@localhost:5432/fyyur'

SQLALCHEMY_TRACK_MODIFICATIONS = False
