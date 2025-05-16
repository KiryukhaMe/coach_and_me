import os

SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'app/db/coach_and_me.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
