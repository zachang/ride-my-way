from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (create_access_token,
 jwt_required, get_jwt_identity, get_raw_jwt)
from app.models.user import User
from app.schemas.user import UserSchema, UserSchemaEdit
from app.utils.response_builder import response_builder
from app.utils.to_lower_strip import to_lower_strip

users_schema = UserSchema(many=True)
user_schema = UserSchema()
users_schema_edit = UserSchemaEdit(many=True)
user_schema_edit = UserSchemaEdit()
 

class UserRegistration(Resource):

    def post(self):
        payload = request.get_json()
        errors = user_schema.validate(payload)
        
        if errors:
            return errors, 400
        else:
            username = User.filter_by_any(username=to_lower_strip(payload['username']))
            email = User.filter_by_any(email=to_lower_strip(payload['email']))

            if username is None and email is None:
                user = User(
                    first_name=to_lower_strip(payload['first_name']),
                    last_name=to_lower_strip(payload['last_name']),
                    username=to_lower_strip(payload['username']),
                    email=to_lower_strip(payload['email']),
                    password=User.generate_hash(to_lower_strip(payload['password']))
                )
                user.save()
                access_token = create_access_token(identity = user.id)
                return response_builder({
                'status': 'success',
                'user': user_schema.dump(user).data,
                'token': access_token
                }, 201)
            else:
                return response_builder({
                'status': 'fail',
                'message': 'this user already exist'
                }, 409)

class UserLogin(Resource):

    def post(self):
        payload = request.get_json()
        try:
            username = to_lower_strip(payload['username'])
            password = to_lower_strip(payload['password'])
            if not username:
                return response_builder({'message': 'username is required'}, 400)
            elif not password:
                return response_builder({'message': 'password is required'}, 400)
            else:
                current_user = User.filter_by_any(username=username)

                if not current_user: 
                    return response_builder({
                        'message': 'User {} does not exist'.format(payload['username'])
                        }, 404)
                elif current_user.verify_hash(password, current_user.password):
                    access_token = create_access_token(identity = current_user.id)
                    return response_builder({
                    'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    })
                else:
                    return response_builder({'message': 'Wrong credentials'}, 400)
        except KeyError as errors:
            return response_builder({'message': '{} is required'.format(errors)}, 400)


class UserDetails(Resource):
    @jwt_required
    def get(self):
        all_users = User.get_all()
      
        if all_users:
            return response_builder({
                'status': 'success',
                'user': users_schema.dump(all_users).data
                })
        else:
            return response_builder({
                'status': 'success',
                'user': 'users not available yet'
                })

class SingleUserDetails(Resource):
    @jwt_required
    def put(self, user_id):
        current_user = get_jwt_identity()
        valid_user = User.get_one(user_id)
        payload = request.get_json(silent=True)
        errors = user_schema_edit.validate(payload)
        
        if errors:
            return errors, 400

        if not valid_user:
            return response_builder({
                'status': 'fail',
                'message': 'User not found'
                }, 404)

        if valid_user.id != current_user:
            return response_builder({
                'status': 'fail',
                'message': 'You can only edit your data'
                }, 403)

        if payload:
            if payload.get('first_name'):
                valid_user.first_name = to_lower_strip(payload.get('first_name'))
            if payload.get('last_name'):
                valid_user.last_name = to_lower_strip(payload.get('last_name'))
            if payload.get('username'):
                valid_user.username = to_lower_strip(payload.get('username'))
            if payload.get('email'):
                valid_user.email = to_lower_strip(payload.get('email'))
            if payload.get('phone_no'):
                valid_user.phone_no = to_lower_strip(payload.get('phone_no'))
            valid_user.save()
            return response_builder({
                'status': 'success',
                'message': 'Edit completed',
                'user': user_schema.dump(valid_user).data
                })
        else: 
            return response_builder({
            'status': 'Fail',
            'message': 'At least one data field for editing must be provided'
            }, 400)


    @jwt_required
    def get(self, user_id):
        current_user = get_jwt_identity()
        valid_user = User.get_one(user_id) 

        if not valid_user:
            return response_builder({
                'status': 'fail',
                'message': 'User not found'
                }, 404)

        if valid_user.id != current_user:
            return response_builder({
                'status': 'fail',
                'message': 'You can only view your details'
                }, 403)

        return response_builder({
            'status': 'success',
            'user': user_schema.dump(valid_user).data
            })


    @jwt_required
    def delete(self, user_id):
        current_user = get_jwt_identity()
        valid_user = User.get_one(user_id) 

        if not valid_user:
            return response_builder({
                'status': 'fail',
                'message': 'User not found'
                }, 404)

        if valid_user.id != current_user:
            return response_builder({
                'status': 'fail',
                'message': 'You can only delete your account'
                }, 403)

        valid_user.delete()
        return response_builder({
            'status': 'success',
            'message': 'Your account has been deleted'
            })