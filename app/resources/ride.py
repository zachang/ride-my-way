from flask import request, jsonify
import datetime
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app.models.ride import Ride
from app.models.user import User
from app.schemas.ride import RideSchema
from app.utils.response_builder import response_builder
from app.utils.to_lower_strip import to_lower_strip

rides_schema = RideSchema(many=True)
ride_schema = RideSchema()


class Rides(Resource):
    """Resource class to create and retrieve rides"""

    @jwt_required
    def post(self):
        payload = request.get_json(silent=True)
        errors = ride_schema.validate(payload)
        current_user = get_jwt_identity()
        valid_user = User.get_one(current_user)
       
        if not valid_user:
            return response_builder({
                'status': 'fail',
                'message': 'User not found'
                }, 404)


        restrict_ride = valid_user.rides
        for ride in restrict_ride:
            if ride.completed == 'False' and ride.available:
                return response_builder({
                    'status': 'fail',
                    'message': 'You have an available ride and can not create another'
                    }, 403)

        if payload:
            departure = payload['departure_time']
            _format = '%Y-%m-%d %H:%M:%S'

            if errors:
                return errors, 400

            if datetime.datetime.strptime(departure, _format) < datetime.datetime.utcnow():
                return response_builder({
                    'status': 'fail',
                    'message': 'Your departure time can not be less than the current time'
                    }, 403)


            ride = Ride(
                        car_name=to_lower_strip(payload['car_name']),
                        departure_time=departure,
                        seat_count=payload['seat_count']
                    )
            ride.user_id = current_user
            ride.available = True
            ride.save()
            return response_builder({
                    'status': 'success',
                    'message': 'Ride created',
                    'ride': ride_schema.dump(ride).data
                    })
        else: 
            return response_builder({
            'status': 'Fail',
            'message': 'To create a ride, at least one data field must be provided'
            }, 400)


    @jwt_required
    def get(self):
        all_rides = Ride.get_all()
      
        if all_rides:
            return response_builder({
                'status': 'success',
                'rides': rides_schema.dump(all_rides).data
                })
        else:
            return response_builder({
                'status': 'success',
                'message': 'Rides not available yet'
                })


class UserRides(Resource):
    """Resource class to retrieve, delete and update rides created by a user"""

    @jwt_required
    def get(self, user_id):
        current_user = get_jwt_identity()
        valid_user = User.get_one(user_id)
        
        if not valid_user:
            return response_builder({
                'status': 'fail',
                'message': 'User not found'
                }, 404)

        if valid_user.id != current_user:
            return response_builder({
                'status': 'fail',
                'message': 'You can only view rides you created'
                }, 403)

        user_rides = valid_user.rides
        if user_rides:
            return response_builder({
                'status': 'success',
                'rides': rides_schema.dump(user_rides).data
                })
        else:
            return response_builder({
                'status': 'success',
                'message': 'You have not created any ride yet'
                })


    @jwt_required
    def delete(self, user_id):
        current_user = get_jwt_identity()
        valid_user = User.get_one(user_id)


        if not valid_user:
            return response_builder({
                'status': 'fail',
                'message': 'User not found'
                }, 404)

        if valid_user.id != current_user:
            return response_builder({
                'status': 'fail',
                'message': 'You can only update rides you created'
                }, 403)

        user_rides = valid_user.rides
        if user_rides:
            if user_rides[0].completed in ['False', 'cancelled']:
                user_rides[0].delete()
                return response_builder({
                    'status': 'success',
                    'message': 'Ride deleted'
                    })
            return response_builder({
                    'status': 'fail',
                    'message': 'You can not delete a completed Ride'
                    }, 403)
        else:
            return response_builder({
                'status': 'success',
                'message': 'You have not created any ride yet'
                })