from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from instance.config import app_config

db = SQLAlchemy()


def create_app(config_name):

    from app.resources.user import (UserRegistration, UserLogin, UserDetails, SingleUserDetails)
    from app.resources.ride import (Ride)

    """
    wrapper for the creation of a new Flask object

    :param config_name:
    :return: app
    """
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    jwt = JWTManager(app)
    CORS(app)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    api.add_resource(UserRegistration, '/register', '/register/')
    api.add_resource(UserLogin, '/login', '/login/')
    api.add_resource(UserDetails, '/users', '/users/')
    api.add_resource(SingleUserDetails, '/users/<string:user_id>', '/users/<string:user_id>')

    api.add_resource(Ride, '/rides', '/rides/')

    return app
