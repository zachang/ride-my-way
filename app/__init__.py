from flask import Flask
from instance.config import app_config


def create_app(config_name):
    """
    wrapper for the creation of a new Flask object

    :param config_name:
    :return:
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])

    return app
