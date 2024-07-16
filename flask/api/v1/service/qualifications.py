from ..validators import post_qualification_schema
from ..models import Qualification, QualificationSchema
from ..utils.context_maneger import session_scope
from ..utils.validate import validate_data


def get_qualification_service():
    with session_scope() as session:
        employees = session.query(Qualification).all()
        res = QualificationSchema().dump(employees, many=True)
        return res


def add_qualification_service(data):
    with session_scope() as session:
        validate_data(post_qualification_schema, data)
        new_qualification = Qualification(**data)
        session.add(new_qualification)
        session.flush()
        return QualificationSchema().dump(new_qualification)


def delete_qualification_service(qualification_id):
    with session_scope() as session:
        qualification = session.query(Qualification).filter_by(qualification_id=qualification_id).first()
        if not qualification:
            return None
        session.delete(qualification)
        return qualification
