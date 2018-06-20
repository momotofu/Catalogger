from app.app import create_app
import sys


def main(argv):
    if '--debug' or '-d' in argv:
        # run debug mode for development
        from app.config import DevelopmentConfig as dev_config
        app = create_app(config=dev_config)
    else:
        # run app for production
        from app.config import Config as config
        app = create_app(config=config)

    app.run(host = '0.0.0.0', port=5000)

if __name__ == '__main__':
    main(sys.argv[1:])
