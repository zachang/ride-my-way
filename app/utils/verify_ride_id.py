from functools import wraps
from app.utils.response_builder import response_builder
from flask_jwt_extended import get_jwt_identity

def verify_ride_decorator(model):
    def verify_ride(func):
        wraps(func)
        def verified(self, ride_id):
            resource = model.get_one(ride_id)
            if not resource:
                return response_builder({
                    'status': 'fail',
                    'message': 'Ride not found'
                    }, 404)

            return func(self, ride_id)
        return verified
    return verify_ride
