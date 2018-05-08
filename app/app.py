from flask import Flask
from app.config import Config as default_config


def create_app(app_name, config=None):
    """
    Configure app object blueprints and global variables.
    """

    app = configure_app(Flask(__name__), config)
    configure_blueprints(app)
    return app


def configure_app(app, config_object=None):
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object(default_config)

    return app


def configure_blueprints(app):
    from .views.category import category

    for blueprint in [category]:
        app.register_blueprint(blueprint)

    return app
