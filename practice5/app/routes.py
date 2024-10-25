from flask import request
from app.models import User
from app import app, db, cache
from app.utils import internal_error_response, is_user_exist, make_user_id_cache_key
from app.constants import USER_ALREADY_EXISTS, USER_NOT_FOUNDED


@app.get('/users')
def get_users():
    """Get all users from database"""
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return users_list


@app.route('/user/<int:user_id>')
@cache.cached(timeout=300, make_cache_key=make_user_id_cache_key)
def get_user(user_id):
    """Gets user by id"""
    user = User.query.get(user_id)

    if not user:
        return USER_NOT_FOUNDED, 404

    return user.to_dict(), 200


@app.post('/users')
def create_user():
    """Create new user in database"""
    data = request.get_json()
    username, email = data['username'], data['email']

    if is_user_exist(email):
        return USER_ALREADY_EXISTS, 404

    try:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
    except Exception as err:
        return internal_error_response(err)

    return {'message': f'User with id = {new_user.id} created successfully'}


@app.put('/users/<int:user_id>')
def update_user(user_id):
    """Update user in database"""
    user = User.query.get(user_id)
    data = request.get_json()

    if not user:
        return USER_NOT_FOUNDED, 404

    try:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
    except Exception as err:
        return internal_error_response(err)

    return {'message': 'User updated successfully'}


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user from database"""
    user = User.query.get(user_id)

    if not user:
        return USER_NOT_FOUNDED, 404

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as err:
        return internal_error_response(err)

    return {'message': 'User deleted successfully'}


@app.get('/clear_cache/<int:user_id>')
def clear_user_cache(user_id):
    """Clear cache for user with id"""
    cache.delete(f'user_data::{user_id}')
    return {'message': f'Cache for user {user_id} cleared'}
