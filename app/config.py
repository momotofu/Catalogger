import os

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///catalog.db'

    IMAGE_FOLDER = 'app/static/images'
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])
    SECRET_KEY = 'super_secret_key'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    WEBPACK_MANIFEST_PATH = '../build/manifest.json'
    WEBPACK_ASSETS_URL = '../build/public/'
    CREDENTIALS_PATH = os.path.abspath('credentials/config.json')

class DevelopmentConfig(Config):
    DEBUG = True
    WEBPACK_ASSETS_URL = None
