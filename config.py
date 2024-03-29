import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config(object):
    # General
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ADMINS = ['test@example.com']
    LANGUAGES = ['en', 'es']

    # Microblog
    POSTS_PER_PAGE = 25
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT') or 25
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Elasticsearch
    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST')

    # Redis
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
