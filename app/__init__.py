from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from instance.config import app_config

db = SQLAlchemy()


def create_app(config_name):
    from flask_restful import Api
    from app.resources.user import UserResource

    """
    wrapper for the creation of a new Flask object

    :param config_name:
    :return: app
    """
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api.add_resource(UserResource, '/user', '/user/')

    return app
