from marshmallow import Schema, fields, ValidationError, validate
from app.schemas.user import UserSchema

class RideSchema(Schema):
    id = fields.String(dump_only=True)
    car_name = fields.String(required=True, dump_to='carName',
    validate=[validate.Length(min=2, max=100)],
    error_messages={
        'required': {'message': 'A carName is required.'}
    })
    start_pos = fields.String(required=True, dump_to='startPos',
    validate=[validate.Length(min=2, max=100)],
    error_messages={
        'required': {'message': 'A startPos is required.'}
    })
    destination = fields.String(required=True, validate=[validate.Length(min=2, max=100)],
    error_messages={
        'required': {'message': 'A destination is required.'}
    })
    departure_time = fields.DateTime(required=True, dump_to='departureTime',
    error_messages={
        'required': {'message': 'A departureTime is required.'}
    })
    seat_count = fields.Integer(required=True, dump_to='seatCount',
    error_messages={
        'required': {'message': 'You need to specify the number of seats your car can accommodate.'}
    })
    seat_taken = fields.Integer(dump_to='seatTaken')
    available = fields.Boolean()
    completed = fields.String()
    user = fields.Nested(UserSchema, only=['id', 'first_name', 'last_name', 
    'username', 'phone_no', 'user_image', 'email'])


class RideSchemaEdit(Schema):
    car_name = fields.String(dump_to='carName', validate=[validate.Length(min=2, max=100)],
    error_messages={
        'required': {'message': 'A carName is required.'}
    })
    start_pos = fields.String(dump_to='startPos', validate=[validate.Length(min=2, max=100)],
    error_messages={
        'required': {'message': 'A startPos is required.'}
    })
    destination = fields.String(validate=[validate.Length(min=2, max=100)],
    error_messages={
        'required': {'message': 'A destination is required.'}
    })
    departure_time = fields.DateTime(dump_to='departureTime')
    seat_count = fields.Integer(dump_to='seatCount')
    user_id = fields.String(required=True, dump_to='userId',
    error_messages={
        'required': {'message': 'A userId is required.'}
    })


class RideSchemaDelete(Schema):
    user_id = fields.String(required=True, dump_to='userId',
    error_messages={
        'required': {'message': 'A userId is required.'}
    })
