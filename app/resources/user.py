from flask import request, jsonify
from flask_restful import Resource
from app.models.user import User
from app.schemas.user import UsersSchema

users_schema = UsersSchema(many=True)
user_schema = UsersSchema() 

class UserResource(Resource):

    def post(self):
        payload = request.get_json()

        errors = UsersSchema().validate(payload)
        
        if errors:
            return errors, 400
        else:
            username = User.filter_by_username(username=payload['username'])
            email = User.filter_by_email(email=payload['email'])

            if username is None and email is None:
                user = User(
                    firstName=payload['firstName'],
                    lastName=payload['lastName'],
                    username=payload['username'],
                    email=payload['email'],
                    password=User.generate_hash(payload['password'])
                )
                user.save()
                
                response = jsonify({
                'status': 'success',
                'user': user_schema.dump(user).data
                })
                response.status_code = 201
                return response
            else:
                response = jsonify({
                'status': 'fail',
                'message': 'this user already exist'
                })
                response.status_code = 409
                return response
                
