from app.app import create_app
from app.config import DevelopmentConfig as dev_config

app = create_app('catalog', config=dev_config)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)
