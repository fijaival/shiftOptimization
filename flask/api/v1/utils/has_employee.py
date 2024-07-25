from ..models import Employee
from sqlalchemy.orm.session import Session as BaseSession
from .error import InvalidAPIUsage


def has_employee(facility_id, employee_id, session: BaseSession):
    employee = session.query(Employee).filter_by(facility_id=facility_id, employee_id=employee_id).first()

    if not employee:
        raise InvalidAPIUsage("The employee dosen't exit in this facility", 400)
    
    if employee.is_delete:
        raise InvalidAPIUsage("The employee is already deleted", 400)
