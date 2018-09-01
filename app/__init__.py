from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from instance.config import app_config

db = SQLAlchemy()


def create_app(config_name):

    from app.resources.user import (UserRegistration, UserLogin, UserDetails, 
    SingleUserDetails, UserRides, UserRequest)
    from app.resources.ride import (Rides, UserSingleRide)
    from app.resources.request import (CreatRequest, CancelRideRequest, 
    ApproveRideRequest, RejectRideRequest)

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

    # user routes
    api.add_resource(UserRegistration, '/register', '/register/')
    api.add_resource(UserLogin, '/login', '/login/')
    api.add_resource(UserDetails, '/users', '/users/')
    api.add_resource(SingleUserDetails, '/users/<string:user_id>', '/users/<string:user_id>')
    api.add_resource(UserRides, '/users/<string:user_id>/rides', '/users/<string:user_id>/rides/')
    api.add_resource(UserRequest, '/users/<string:user_id>/requests', '/users/<string:user_id>/requests/')

    # ride routes
    api.add_resource(Rides, '/rides', '/rides/')
    api.add_resource(UserSingleRide, '/rides/<string:ride_id>', '/rides/<string:ride_id>/')

    # request routes
    api.add_resource(CreatRequest, '/requests', '/requests/')
    api.add_resource(CancelRideRequest, '/requests/<string:request_id>/cancel', '/requests/<string:request_id>/cancel/')
    api.add_resource(ApproveRideRequest, '/requests/approve', '/requests/approve/')
    api.add_resource(RejectRideRequest, '/requests/reject', '/requests/reject/')

    return app
