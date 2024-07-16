from flask import Blueprint, jsonify, request
from api.v1.utils.error import InvalidAPIUsage
from extensions import admin_required
from ..service.qualifications import get_qualification_service, add_qualification_service, delete_qualification_service


qualifications_bp = Blueprint('qualification', __name__)


@qualifications_bp.route('/qualifications', methods=['GET'])
@admin_required
def get_qualifications():
    res = get_qualification_service()
    return jsonify({"qualifications": res}), 200


@qualifications_bp.route('/qualifications', methods=['POST'])
@admin_required
def add_qualification():
    data = request.json
    res = add_qualification_service(data)
    return res, 201


@qualifications_bp.route('/qualifications/<int:qualification_id>', methods=['DELETE'])
@admin_required
def delete_qualification(qualification_id):
    res = delete_qualification_service(qualification_id)
    if not res:
        raise InvalidAPIUsage("Qualification not found", 404)
    return jsonify({"message": "Qualification deleted successfully!"}), 200
