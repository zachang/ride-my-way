from marshmallow import Schema, fields, ValidationError, validate

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    first_name = fields.String(required=True, dump_to='firstName',
    validate=[validate.Length(min=2, max=50)],
    error_messages={
        'required': {'message': 'A firstname is required.'}
    })
    last_name = fields.String(required=True, dump_to='lastName',
    validate=[validate.Length(min=2, max=50)],
    error_messages={
        'required': {'message': 'A lastname is required.'}
    })
    username = fields.String(required=True,
    validate=[validate.Length(min=2, max=50)],
    error_messages={
        'required': {'message': 'A username is required.'}
    })
    email = fields.Email(required=True,
    validate=[validate.Length(max=150)],
    error_messages={
        'required': {'message': 'An email is required.'}
    })
    password = fields.String(required=True, load_only=True,
    validate=[validate.Length(min=2, max=20)],
    error_messages={
        'required': {'message': 'A password is required.'}
    })
    phone_no = fields.String(dump_to='phoneNo')
    user_image = fields.String(dump_to='userImage')
    is_social = fields.Boolean(dump_to='isSocial')
    reg_type = fields.String(dump_to='regType')
    created_at = fields.DateTime(dump_to='createdAt')
    updated_at = fields.DateTime(dump_to='updatedAt')


class UserSchemaEdit(Schema):
    first_name = fields.String(dump_to='firstName', validate=[validate.Length(min=2, max=50)])
    last_name = fields.String(dump_to='lastName', validate=[validate.Length(min=2, max=50)])
    username = fields.String(validate=[validate.Length(min=2, max=50)])
    email = fields.Email(validate=[validate.Length(max=150)])
    phone_no = fields.String(dump_to='phoneNo', validate=[validate.Length(min=11, max=14)])
