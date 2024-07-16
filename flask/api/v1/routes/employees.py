from flask import Blueprint, jsonify, request
from api.v1.utils.error import InvalidAPIUsage
from extensions import self_facility_required
from ..service.employees import get_all_employees_service, add_employee_service, delete_employee_service, update_employee_service

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/facilities/<int:facility_id>/employees', methods=["GET"])
@self_facility_required
def get_employee(facility_id):
    res = get_all_employees_service(facility_id)
    return jsonify({"employees": res}), 200


@employees_bp.route('/facilities/<int:facility_id>/employees', methods=["POST"])
@self_facility_required
def add_employee(facility_id):
    data = request.json
    res = add_employee_service(facility_id, data)
    return res, 201


@employees_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>', methods=["DELETE"])
@self_facility_required
def delete_employee(facility_id, employee_id):
    employee = delete_employee_service(employee_id)
    if not employee:
        raise InvalidAPIUsage("Employee not found", 404)
    return jsonify({"message": "Employee deleted successfully!"}), 200


@employees_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>', methods=["PUT"])
@self_facility_required
def update_employee(facility_id, employee_id):
    data = request.json
    res = update_employee_service(facility_id, employee_id, data)
    return res, 201
