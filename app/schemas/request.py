from marshmallow import Schema, fields, validate
from app.schemas.user import UserSchema

class RequestSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String(required=True, dump_to='userId',
    error_messages={
        'required': {'message': 'A userId is required.'}
    })
    ride_id = fields.String(required=True, dump_to='rideId',
    error_messages={
        'required': {'message': 'A rideId is required.'}
    })
    status = fields.String()
    completed = fields.String()
    created_at = fields.DateTime(dump_to='createdAt')
    updated_at = fields.DateTime(dump_to='updatedAt')


class CancelRequestSchama(Schema):
    user_id = fields.String(required=True, dump_to='userId',
    error_messages={
        'required': {'message': 'A userId is required.'}
    })
    ride_id = fields.String(dump_to='rideId')
    status = fields.String()
    completed = fields.String()
    created_at = fields.DateTime(dump_to='createdAt')
    updated_at = fields.DateTime(dump_to='updatedAt')


class ApproveRequestSchama(Schema):
    user_id = fields.String(dump_to='userId')
    ride_id = fields.String(dump_to='rideId')
    status = fields.String()
    completed = fields.String()
    created_at = fields.DateTime(dump_to='createdAt')
    updated_at = fields.DateTime(dump_to='updatedAt')
