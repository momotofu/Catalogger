import app
from app.app import create_app
from app.config import DefaultConfig as DevConfig

application = app.create_app('catalog', config=DevConfig)

if __name__ == '__main__':
    application.run(host = '0.0.0.0', port=7000)
