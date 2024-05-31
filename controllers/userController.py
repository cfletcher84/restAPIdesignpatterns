from flask import request, jsonify
from schemas.userSchema import user_schema, users_schema, user_login_schema
from services import userService
from marshmallow import ValidationError

def save():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    user_save = userService.save(user_data)
    return user_schema.jsonify(user_save), 201

def find_all():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    users = userService.find_all(page, per_page)
    return users_schema.jsonify(users)

def get_user(username):
    user = userService.get_user(username)
    return user

def get_token():
    try:
        user_data = user_login_schema.loads(request.json)
        token = userService.get_token(user_data['username'], user_data['password'])
        if token:
            response = {
                'status': 'success',
                'message': 'Authentication completed.',
                'token': token
            }
            return jsonify(response), 200
        else:
            response = {
                'status': 'error'
                'message' 'Authentication error'
            }
            return jsonify(response), 401
    except ValidationError as err:
        return jsonify(err.messages), 400
