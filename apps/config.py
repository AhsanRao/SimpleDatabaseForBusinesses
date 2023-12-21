import os
import random
import string

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

    # Database pooling configurations
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv('SQLALCHEMY_POOL_TIMEOUT', 30))  # Connection timeout
    SQLALCHEMY_POOL_SIZE = int(os.getenv('SQLALCHEMY_POOL_SIZE', 100))  # Pool size
    SQLALCHEMY_POOL_OVERFLOW = int(os.getenv('SQLALCHEMY_POOL_OVERFLOW', 20))  # increase overflow
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv('SQLALCHEMY_POOL_RECYCLE', 1800))  # Recycle connections after 1800 seconds

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', ''.join(random.choice(string.ascii_lowercase) for i in range(32)))

    # Social AUTH context
    SOCIAL_AUTH_GITHUB = False
    GITHUB_ID = os.getenv('GITHUB_ID', None)
    GITHUB_SECRET = os.getenv('GITHUB_SECRET', None)

    # Enable/Disable Github Social Login
    if GITHUB_ID and GITHUB_SECRET:
        SOCIAL_AUTH_GITHUB = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database Configuration
    DB_ENGINE = os.getenv('DB_ENGINE', 'mysql+mysqlconnector')
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASS = os.getenv('DB_PASS', '1234')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'simple')

    # Construct the SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = f'{DB_ENGINE}://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
