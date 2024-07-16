from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import extract
from ..validators import post_shifts_schema, put_shifts_schema
from ..models import Shift, ShiftSchema, Employee, Facility
from ..utils.context_maneger import session_scope
from ..utils.validate import validate_data


def get_shifts_service(facility_id, year, month):
    with session_scope() as session:
        employee = session.query(Employee).filter_by(facility_id=facility_id).all()
        if not employee:
            return None
        employee_ids = [emp.employee_id for emp in employee]
        shifts = session.query(Shift).filter(
            extract('year', Shift.date) == year,
            extract('month', Shift.date) == month,
            Shift.employee_id.in_(employee_ids)
        ).all()
        res = ShiftSchema().dump(shifts, many=True)
        return res


def post_shifts_service(data):
    with session_scope() as session:
        shifts = data["shifts"]
        validate_data(post_shifts_schema, shifts)
        for item in shifts:
            new_shift = Shift(**item)
            session.add(new_shift)


def delete_shifts_by_month_service(facility_id, year, month):
    with session_scope() as session:
        employee = session.query(Employee).filter_by(facility_id=facility_id).all()
        if not employee:
            return None
        employee_ids = [emp.employee_id for emp in employee]
        shifts = session.query(Shift).filter(
            extract('year', Shift.date) == year,
            extract('month', Shift.date) == month,
            Shift.employee_id.in_(employee_ids)
        ).all()
        for shift in shifts:
            session.delete(shift)
        return shifts


def update_shift_service(facility_id, shift_id, data):
    with session_scope() as session:
        validate_data(put_shifts_schema, data)
        shift = session.query(Shift).filter_by(shift_id=shift_id).first()
        if not shift:
            return None
        if shift.task_id != data["task_id"]:
            facility = session.query(Facility).filter_by(facility_id=facility_id).first()
            if data["task_id"] not in [task.task_id for task in facility.tasks]:
                raise ValueError("this task is not in the facility tasks")
            shift.task_id = data["task_id"]
        shift.shift_number = data["shift_number"]
        shift.updated_at = datetime.now()
        session.add(shift)
        return ShiftSchema().dump(shift)


def delete_shift_service(shift_id):
    with session_scope() as session:
        shift = session.query(Shift).filter_by(shift_id=shift_id).first()
        if not shift:
            return None
        session.delete(shift)
        return shift
