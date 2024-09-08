from flask import Blueprint, jsonify, request
from api.v1.utils.error import InvalidAPIUsage
from extensions import self_facility_required
from ..service.day_off_requests import get_all_requests_service, get_requests_service, post_day_off_request_service, delete_request_service, update_request_service

day_off_requests_bp = Blueprint('day_off_requests', __name__)


@day_off_requests_bp.route('/facilities/<int:facility_id>/requests')
@self_facility_required
def get_all_requests(facility_id):
    year = request.args.get('year')
    month = request.args.get('month')
    print(year, month)
    res = get_all_requests_service(facility_id, year, month)
    return jsonify({"requests": res}), 200


@day_off_requests_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>/requests', methods=["GET"])
@self_facility_required  # ここは自分と管理者のみアクセス可能にすべし
def get_requests(facility_id, employee_id):
    year = request.args.get('year')
    month = request.args.get('month')
    res = get_requests_service(facility_id, employee_id, year, month)
    return jsonify({"requests": res}), 200


@day_off_requests_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>/requests', methods=["POST"])
@self_facility_required
def add_request(facility_id, employee_id):
    data = request.json
    res = post_day_off_request_service(facility_id, employee_id, data)
    return res, 201


@day_off_requests_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>/requests/<int:request_id>', methods=["DELETE"])
@self_facility_required
def delete_request(facility_id, employee_id, request_id):
    request = delete_request_service(employee_id, request_id)
    if not request:
        raise InvalidAPIUsage("Request not found", 404)
    return jsonify({"message": "Request deleted successfully!"}), 200


@day_off_requests_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>/requests/<int:request_id>', methods=["PUT"])
@self_facility_required
def update_request(facility_id, employee_id, request_id):
    data = request.json
    res = update_request_service(employee_id, request_id, data)
    if not res:
        raise InvalidAPIUsage("Request not found", 404)
    return res, 201
