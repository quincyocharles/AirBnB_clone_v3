#!/usr/bin/python3

"""
Module for handling the link between Place
and Amenity objects
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                methods=['GET'], strict_slashes=False)
def get_amenities_of_place(place_id):
    """ Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities = place.amenities
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(Place, place_id):
    """ Deletes an Amenity object from a Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenitites/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(Place, place_id):
    """ Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
