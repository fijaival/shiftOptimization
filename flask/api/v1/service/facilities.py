from datetime import datetime
from ..validators import post_facility_schema, put_facility_schema
from ..models import Facility, FacilitySchema, Qualification, Constraint, Task
from api.v1.utils.error import InvalidAPIUsage
from ..utils.context_maneger import session_scope
from ..utils.validate import validate_data


def validate_and_create_facility_service(data):
    with session_scope() as session:
        validate_data(post_facility_schema, data)
        new_facility = Facility(**data)
        session.add(new_facility)
        session.flush()
        res = FacilitySchema().dump(new_facility)
        return res


def delete_facility_service(facility_id):
    with session_scope() as session:
        facility = session.query(Facility).filter_by(facility_id=facility_id).first()
        if not facility:
            return None
        session.delete(facility)
        return facility


def get_facility_service(facility_id):
    with session_scope() as session:
        facility = session.query(Facility).filter_by(facility_id=facility_id).first()
        if not facility:
            return None
        return FacilitySchema().dump(facility)


def update_facility_service(facility_id, data):
    with session_scope() as session:
        validate_data(put_facility_schema, data)
        facility = session.query(Facility).filter_by(facility_id=facility_id).first()
        if not facility:
            raise InvalidAPIUsage("Facility not found", 404)

        facility.name = data["name"]
        facility.updated_at = datetime.now()
        facility.constraints.clear()
        facility.qualifications.clear()
        facility.tasks.clear()

        append_data_to_facility(session, facility, data, Constraint, 'constraints',
                                'constraint_id', 'constraints', "Constraint not found")
        append_data_to_facility(session, facility, data, Qualification, 'qualifications',
                                'qualification_id', 'qualifications', "Qualification not found")
        append_data_to_facility(session, facility, data, Task, 'tasks', 'task_id', 'tasks', "Task not found")
        session.add(facility)
        return FacilitySchema().dump(facility)


def append_data_to_facility(session, facility, data, model, data_key, model_id_key, append_attr, not_found_message):
    for item_data in data[data_key]:
        found_item = session.query(model).filter_by(**{model_id_key: item_data[model_id_key]}).first()
        if not found_item:
            raise InvalidAPIUsage(not_found_message, 404)
        getattr(facility, append_attr).append(found_item)
