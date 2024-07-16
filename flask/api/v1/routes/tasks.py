from flask import Blueprint, jsonify, request
from api.v1.utils.error import InvalidAPIUsage
from extensions import admin_required
from ..service.tasks import get_task_service, add_task_service, delete_task_service

tasks_bp = Blueprint('task', __name__)


@tasks_bp.route('/tasks', methods=['GET'])
@admin_required
def get_tasks():
    res = get_task_service()
    return jsonify({"tasks": res}), 200


@tasks_bp.route('/tasks', methods=['POST'])
@admin_required
def add_task():
    data = request.json
    res = add_task_service(data)
    return res, 201


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@admin_required
def delete_task(task_id):
    res = delete_task_service(task_id)
    if not res:
        raise InvalidAPIUsage("Task not found", 404)
    return jsonify({"message": "Task deleted successfully!"}), 200
