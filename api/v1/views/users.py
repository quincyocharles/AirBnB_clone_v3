#!/usr/bin/python3
"""
Module for hanlding User RESTful API actions
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password', not in data:
        return jsonify({"error": "Missing password"}), 400

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400

        keys_to_ignore = ['id', 'email', 'created_at',]
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(user, key, value)

        storage.save()
        return jsonify(user.to_dict()), 200
    abort(404)
