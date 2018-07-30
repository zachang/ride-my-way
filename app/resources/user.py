from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (create_access_token,
 jwt_required, get_jwt_identity, get_raw_jwt)
from app.models.user import User
from app.schemas.user import UsersSchema

users_schema = UsersSchema(many=True)
user_schema = UsersSchema() 

class UserRegistration(Resource):

    def post(self):
        payload = request.get_json()
        errors = UsersSchema().validate(payload)
        
        if errors:
            return errors, 400
        else:
            username = User.filter_by_any(username=payload['username'].strip())
            email = User.filter_by_any(email=payload['email'].strip())

            if username is None and email is None:
                user = User(
                    firstName=payload['firstName'].strip(),
                    lastName=payload['lastName'].strip(),
                    username=payload['username'].strip(),
                    email=payload['email'].strip(),
                    password=User.generate_hash(payload['password'].strip())
                )
                user.save()
                access_token = create_access_token(identity = payload['username'])
                response = jsonify({
                'status': 'success',
                'user': user_schema.dump(user).data,
                'token': access_token
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

class UserLogin(Resource):

    def post(self):
        payload = request.get_json()
        try:
            username = payload['username'].strip()
            password = payload['password'].strip()
            if len(username) == 0:
                return {'message': 'username is required'}, 400
            elif len(password) == 0:
                return {'message': 'password is required'}, 400
            else:
                current_user = User.filter_by_any(username=username)

                if not current_user: 
                    return {'message': 'User {} does not exist'.format(payload['username'])}, 404
                elif User.verify_hash(password, current_user.password):
                    access_token = create_access_token(identity = payload['username'])
                    return {
                    'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    }, 200
                else:
                    return {'message': 'Wrong credentials'}
        except KeyError as errors:
            return {'message': '{} is required'.format(errors)}, 400
