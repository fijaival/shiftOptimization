from ..validators import post_constraint_schema
from ..models import Constraint, ConstraintSchema
from ..utils.context_maneger import session_scope
from ..utils.validate import validate_data


def get_constraint_service():
    with session_scope() as session:
        employees = session.query(Constraint).all()
        res = ConstraintSchema().dump(employees, many=True)
        return res


def add_constraint_service(data):
    with session_scope() as session:
        validate_data(post_constraint_schema, data)
        new_constraint = Constraint(**data)
        session.add(new_constraint)
        session.flush()
        return ConstraintSchema().dump(new_constraint)


def delete_constraint_service(constraint_id):
    with session_scope() as session:
        constraint = session.query(Constraint).filter_by(constraint_id=constraint_id).first()
        if not constraint:
            return None
        session.delete(constraint)
        return constraint
