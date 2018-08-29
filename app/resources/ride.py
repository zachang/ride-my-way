from flask import request, jsonify
import datetime
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app.models.ride import Ride
from app.models.user import User
from app.schemas.ride import RideSchema, RideSchemaEdit, RideSchemaDelete
from app.utils.response_builder import response_builder
from app.utils.to_lower_strip import to_lower_strip

rides_schema = RideSchema(many=True)
ride_schema = RideSchema()
ride_schema_edit = RideSchemaEdit()
ride_schema_delete = RideSchemaDelete()


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
            if ride.completed == 'no' and ride.available:
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
                        start_pos=to_lower_strip(payload['start_pos']),
                        destination=to_lower_strip(payload['destination']),
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
            available_rides = set([])
            for all_ride in all_rides:
                if not all_ride.available:
                    continue
                available_rides.add(all_ride)

            if available_rides:
                rides = rides_schema.dump(available_rides).data
                return response_builder({
                    'status': 'success',
                    'rides': rides,
                    'count': len(rides)
                    })

            return response_builder({
                    'status': 'success',
                    'message': 'No available rides yet'
                    })
        else:
            return response_builder({
                'status': 'success',
                'message': 'Rides not available yet'
                })


class UserSingleRide(Resource):
    """Resource class to update and delete a ride created by a user"""

    @jwt_required
    def put(self, ride_id):
        payload = request.get_json(silent=True)
        errors = ride_schema_edit.validate(payload)
        
        if errors:
            return errors, 400

        if payload:
            current_user = get_jwt_identity()
            valid_user = User.get_one(payload.get('user_id'))

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

            ride = Ride.get_one(ride_id)
            if ride:
                if ride.created_at < datetime.datetime.utcnow():
                    return response_builder({
                        'status': 'fail',
                        'message': 'You cannot update a ride created in the past'
                        }, 403) 
                    
                if ride.available:
                    if payload.get('departure_time'):
                        departure_time = payload.get('departure_time')
                        _format = '%Y-%m-%d %H:%M:%S'

                        if datetime.datetime.strptime(departure_time, _format) < datetime.datetime.utcnow():
                            return response_builder({
                                'status': 'fail',
                                'message': 'Your departure date/time must be at least current'
                                }, 403)
                        else:
                            ride.departure_time = departure_time

                    if payload.get('car_name'):
                        ride.car_name = to_lower_strip(payload.get('car_name'))
                    if payload.get('seat_count'):
                        ride.seat_count = payload.get('seat_count')
                    if payload.get('start_pos'):
                        ride.start_pos = to_lower_strip(payload.get('start_pos'))
                    if payload.get('destination'):
                        ride.destination = to_lower_strip(payload.get('destination'))

                    ride.save()
                    return response_builder({
                        'status': 'success',
                        'message': 'Edit completed',
                        'ride': ride_schema.dump(ride).data
                        })
                else:
                    return response_builder({
                        'status': 'fail',
                        'message': 'This ride is not available and can not be updated'
                        }, 403) 
            else:
                return response_builder({
                    'status': 'fail',
                    'message': 'Ride not found'
                    }, 404)
        else: 
            return response_builder({
            'status': 'Fail',
            'message': 'At least one data field for editing must be provided'
            }, 400)


    @jwt_required
    def delete(self, ride_id):
        payload = request.get_json(silent=True)
        errors = ride_schema_edit.validate(payload)
        
        if errors:
            return errors, 400

        if payload:
            current_user = get_jwt_identity()
            valid_user = User.get_one(payload.get('user_id'))

            if not valid_user:
                return response_builder({
                    'status': 'fail',
                    'message': 'User not found'
                    }, 404)

            if valid_user.id != current_user:
                return response_builder({
                    'status': 'fail',
                    'message': 'You can only delete rides you created'
                    }, 403)

            ride = Ride.get_one(ride_id)
            if ride:
                if ride.completed in ['no', 'cancelled']:
                    ride.delete()
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
                    'status': 'fail',
                    'message': 'Ride not found'
                    }, 404)
        else: 
            return response_builder({
            'status': 'Fail',
            'message': 'A data field must be provided'
            }, 400)