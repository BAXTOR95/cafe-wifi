import os


class Config:
    SECRET_KEY = os.environ.get('CSRF_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///cafes.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
