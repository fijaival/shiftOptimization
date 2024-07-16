from ..models import Employee
from sqlalchemy.orm.session import Session as BaseSession


def has_employee(facility_id, employee_id, session: BaseSession):
    employee = session.query(Employee).filter_by(facility_id=facility_id, employee_id=employee_id).first()

    if not employee:
        raise ValueError("The employee dosen't exit in this facility", 400)
