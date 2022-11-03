import os
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)

class Config:
    DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    JSON_SORT_KEYS=True
    PER_PAGE=5
    JWT_EXPIRED_MINUTES = 30


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(Config):
    DB_FILE_PATH = base_dir / 'SportoweSwiryAPI_app' / 'tests'/ 'test.db'
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(DB_FILE_PATH)
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DB_HOST = os.environ.get('DB_HOST')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}