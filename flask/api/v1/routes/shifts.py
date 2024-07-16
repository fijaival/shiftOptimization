from flask import Blueprint, request, jsonify
from extensions import self_facility_required
from api.v1.utils.error import InvalidAPIUsage
from ..service.scheduler.run_optimization import run_optimization
from ..service.shift import post_shifts_service, get_shifts_service, update_shift_service, delete_shift_service, delete_shifts_by_month_service
shifts_bp = Blueprint("shift", __name__)


@shifts_bp.route('/facilities/<int:facility_id>/shifts/generate', methods=['POST'])
@self_facility_required
def generate_shift(facility_id):
    year = request.args.get('year')
    month = request.args.get('month')
    res: list = run_optimization(facility_id, year, month)
    if not res:
        raise InvalidAPIUsage("Facility not found", 404)
    return jsonify({"shifts": res}), 200


@shifts_bp.route('/facilities/<int:facility_id>/shifts', methods=['GET'])
@self_facility_required
def get_shifts(facility_id):
    year = request.args.get('year')
    month = request.args.get('month')
    res = get_shifts_service(facility_id, year, month)
    if not res:
        raise InvalidAPIUsage("shifts not found", 404)
    return jsonify({"shifts": res}), 200


@shifts_bp.route('/facilities/<int:facility_id>/shifts', methods=['POST'])
@self_facility_required
def confirm_shift(facility_id):
    """こいつのdataはshifts属性をもつ"""
    data = request.json
    post_shifts_service(data)
    return jsonify({"message": "Shifts confirmed successfully!"}), 200


@shifts_bp.route('/facilities/<int:facility_id>/shifts', methods=['DELETE'])
@self_facility_required
def delete_shifts_by_month(facility_id):
    year = request.args.get('year')
    month = request.args.get('month')
    res = delete_shifts_by_month_service(facility_id, year, month)
    if not res:
        raise InvalidAPIUsage("Shifts not found", 404)
    return jsonify({"message": "Shifts deleted successfully!"}), 200


@shifts_bp.route('/facilities/<int:facility_id>/shifts/<int:shift_id>', methods=['PUT'])
@self_facility_required
def update_shift(facility_id, shift_id):
    data = request.json
    res = update_shift_service(facility_id, shift_id, data)
    if not res:
        raise InvalidAPIUsage("Shift not found", 404)
    return res, 200


@shifts_bp.route('/facilities/<int:facility_id>/shifts/<int:shift_id>', methods=['DELETE'])
@self_facility_required
def delete_shift(facility_id, shift_id):
    res = delete_shift_service(shift_id)
    if not res:
        raise InvalidAPIUsage("Shift not found", 404)
    return jsonify({"message": "Shift deleted successfully!"}), 200
