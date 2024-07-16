from flask import Blueprint, jsonify, request
from api.v1.utils.error import InvalidAPIUsage
from extensions import admin_required, self_facility_required
from ..service.facilities import validate_and_create_facility_service, delete_facility_service, get_facility_service, update_facility_service

facilities_bp = Blueprint('facilities', __name__)


@facilities_bp.route('/', methods=['GET'])
@admin_required
def get_all_facilities():
    return jsonify({"message": "Hello, World!"}), 200


@facilities_bp.route('/', methods=['POST'])
@admin_required
def add_facility():
    data = request.json
    res = validate_and_create_facility_service(data)
    return res, 201


@facilities_bp.route('/<int:facility_id>', methods=['GET'])
@self_facility_required
def get_facility(facility_id):
    """ここだけ権限異なる"""
    facility = get_facility_service(facility_id)
    if not facility:
        return InvalidAPIUsage("Facility not found", 404)
    return facility, 200


@facilities_bp.route('/<int:facility_id>', methods=['DELETE'])
@admin_required
def delete_facility(facility_id):
    facility = delete_facility_service(facility_id)
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)
    return jsonify({"message": "Facility deleted successfully!"}), 200


@facilities_bp.route('/<int:facility_id>', methods=['PUT'])
@admin_required
def update_facility(facility_id):
    "update employee information"
    data = request.json
    res = update_facility_service(facility_id, data)
    return res, 201
