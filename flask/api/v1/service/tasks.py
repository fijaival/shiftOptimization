from ..validators import post_task_schema
from ..models import Task, TaskSchema
from ..utils.context_maneger import session_scope
from ..utils.validate import validate_data


def get_task_service():
    with session_scope() as session:
        employees = session.query(Task).all()
        res = TaskSchema().dump(employees, many=True)
        return res


def add_task_service(data):
    with session_scope() as session:
        validate_data(post_task_schema, data)
        new_task = Task(**data)
        session.add(new_task)
        session.flush()
        return TaskSchema().dump(new_task)


def delete_task_service(task_id):
    with session_scope() as session:
        task = session.query(Task).filter_by(task_id=task_id).first()
        if not task:
            return None
        session.delete(task)
        return task


def get_task_id(task_name):
    with session_scope() as session:
        task = session.query(Task).filter_by(name=task_name).first()
        if not task:
            return None
        return task.task_id
