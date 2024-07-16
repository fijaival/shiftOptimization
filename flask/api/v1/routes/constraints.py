from flask import Blueprint, jsonify, request
from api.v1.utils.error import InvalidAPIUsage
from extensions import admin_required
from ..service.constraints import get_constraint_service, add_constraint_service, delete_constraint_service

constraints_bp = Blueprint('costraint', __name__)


@constraints_bp.route('/constraints', methods=['GET'])
@admin_required
def get_constraints():
    res = get_constraint_service()
    return jsonify({"constraints": res}), 200


@constraints_bp.route('/constraints', methods=['POST'])
@admin_required
def add_constraint():
    data = request.json
    res = add_constraint_service(data)
    return res, 201


@constraints_bp.route('/constraints/<int:constraint_id>', methods=['DELETE'])
@admin_required
def delete_constraint(constraint_id):
    res = delete_constraint_service(constraint_id)
    if not res:
        raise InvalidAPIUsage("Constraint not found", 404)
    return jsonify({"message": "Constraint deleted successfully!"}), 200
