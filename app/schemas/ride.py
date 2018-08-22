from marshmallow import Schema, fields, ValidationError, validate
from app.schemas.user import UserSchema

class RideSchema(Schema):
    id = fields.String(dump_only=True)
    car_name = fields.String(required=True, dump_to='carName',
    validate=[validate.Length(min=2, max=100)],
    error_messages={
        'required': {'message': 'A carName is required.'}
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