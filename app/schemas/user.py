from marshmallow import Schema, fields, validates, ValidationError


class UsersSchema(Schema):
    id = fields.Integer(dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

    @validates('firstName')
    def validate_firstName(self, firstName):
        if len(firstName) < 2:
            raise ValidationError('firstName should be at least 2 characters')
            

    @validates('lastName')
    def validate_lastName(self, lastName):
        if len(lastName) < 2:
            raise ValidationError('lastName should be at least 2 characters')

    
    @validates('username')
    def validate_username(self, username):
        if len(username) < 2:
            raise ValidationError('username should be at least 2 characters')


    @validates('password')
    def validate_password(self, password):
        if len(password) < 2:
            raise ValidationError('password should be at least 2 characters')

