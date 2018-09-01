from flask import request
from sqlalchemy import desc, asc
import datetime
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.ride import Ride
from app.models.user import User
from app.models.request import Request
from app.schemas.request import (RequestSchema, CancelRequestSchama, ApproveRequestSchama)
from app.utils.response_builder import response_builder
from app.utils.save_request import save_request
from app import db

request_schema = RequestSchema()
cancel_request_schema = CancelRequestSchama()
approve_request_schema= ApproveRequestSchama(many=True)

class CreatRequest(Resource):
    """Resource class to create request"""

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        payload = request.get_json(silent=True)
        errors = request_schema.validate(payload)
        
        if errors:
            return errors, 400

        if payload:
            user_id = payload.get('user_id')
            ride_id = payload.get('ride_id')
            user = User.get_one(user_id)
            if user:
                if user.id == current_user:
                    ride = Ride.get_one(ride_id)
                    if ride:
                        if ride.user_id != user.id:
                            user_requests = Request.filter_any(user_id=user_id)\
                            .order_by(desc('created_at')).limit(1).all()

                            if user_requests:
                                if user_requests[0].status == 'pending' and \
                                user_requests[0].completed == 'no':
                                    return response_builder({
                                        'status': 'fail',
                                        'message': 'You have an open request'
                                        }, 403)
                                else:
                                    return save_request(ride, Request, current_user, request_schema, 
                                        response_builder)
                            else:
                                return save_request(ride, Request, current_user, request_schema, 
                                    response_builder)
                                
                        else:
                            return response_builder({
                                'status': 'fail',
                                'message': 'You can not make a request for your own ride'
                                }, 403)
                    else:
                        return response_builder({
                            'status': 'fail',
                            'message': 'Ride not found'
                            }, 404)
                else:
                    return response_builder({
                            'status': 'fail',
                            'message': 'You need to make a request from your account'
                            }, 403)
            else: 
                return response_builder({
                    'status': 'fail',
                    'message': 'User not found'
                    }, 404)
        else: 
            return response_builder({
                'status': 'fail',
                'message': 'A user_id and ride_id must be provided in request'
                }, 400)


class CancelRideRequest(Resource):
    """Resource class for cancelling of a ride request"""

    @jwt_required
    def put(self, request_id):
        """Cancel ride request"""
        current_user = get_jwt_identity()
        payload = request.get_json(silent=True)
        errors = cancel_request_schema.validate(payload)
        
        if errors:
            return errors, 400

        if payload:
            user = User.get_one(payload.get('user_id'))
            if user:
                if user.id == current_user:
                    user_requests = user.request
                    if user_requests:
                        request_to_cancel = []
                        for user_request in user_requests:
                            if user_request.id == request_id:
                                request_to_cancel.append(user_request)
                                break
                                
                        if request_to_cancel:
                            if request_to_cancel[0].completed not in ['cancelled','yes']:
                                request_to_cancel[0].completed = 'cancelled'
                                request_to_cancel[0].save()
                                return response_builder({
                                    'status': 'success',
                                    'message': cancel_request_schema.dump(request_to_cancel[0]).data
                                    })
                            else:
                               return response_builder({
                                    'status': 'fail',
                                    'message': 'Oops! You can not cancel a completed or cancelled'+ 
                                    ' request'
                                    }, 403)
                        else:
                            return response_builder({
                                'status': 'fail',
                                'message': 'Oops! request_id invalid or not associated to you'
                                }, 406)
                    else:
                        return response_builder({
                                'status': 'fail',
                                'message': 'You have not made any ride request'
                                }, 404)
                else:
                    return response_builder({
                        'status': 'fail',
                        'message': 'Oops! This is not your account'
                        }, 403)
            else:
                return response_builder({
                    'status': 'fail',
                    'message': 'user not found'
                    }, 404)
        else:
            return response_builder({
                'status': 'fail',
                'message': 'A user_id is required in the request payload'
                }, 400)


class ApproveRideRequest(Resource):
    """Resource class for approving one or more ride request"""

    @jwt_required
    def put(self, request_id=None):
        payload = request.get_json(silent=True)

        if payload:
            current_user = get_jwt_identity()
            request_ids =  payload.get('request_ids', None)

            if request_ids is None:
                return response_builder(dict(
                    message='request_ids value is required'), 400)


            if not isinstance(request_ids, list):
                return response_builder(dict(
                    message='request_ids must be a list'), 400)
            
            if len(request_ids) > 10:
                return response_builder(dict(
                    message='Sorry, you can not approve more than 10 ride request at a go'), 406)


            request_approval = Request.query.filter(Request.user_id == current_user,
             Request.status == 'pending', Request.completed == 'no', Request.id.in_(request_ids))\
             .update({'status': 'approved'}, synchronize_session='fetch')

            request_approval_next = Request.query.filter(Request.user_id == current_user, 
            Request.id.in_(request_ids)).all()
            
            if request_approval:
                db.session.commit()
                return response_builder({
                'status': 'success',
                'request': approve_request_schema.dump(request_approval_next).data
                })
            else:
                return response_builder({
                    'status': 'fail',
                    'message': 'invalid request_ids, no pending requests for approval or request' +
                    ' is not associated with current user'
                    }, 400)

        else:
           return response_builder({
                'status': 'fail',
                'message': 'Data is required in the request payload'
                }, 400)
