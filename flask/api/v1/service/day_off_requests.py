from datetime import datetime
from sqlalchemy import extract, and_
from typing import List
from ..models import DayOffRequest, Employee, DayOffRequestSchema,getAllRequestSchema,getIndividualRequestSchema
from ..validators import post_day_off_request_schema, put_day_off_request_schema
from ..utils.context_maneger import session_scope
from ..utils.validate import validate_data
from ..utils.has_employee import has_employee
from collections import defaultdict
from sqlalchemy.orm import joinedload


def get_all_requests_service(facility_id, year, month):
    with session_scope() as session:
        query = (
            session.query(Employee, DayOffRequest)
            .outerjoin(DayOffRequest, and_(
                Employee.employee_id == DayOffRequest.employee_id,
                extract('year', DayOffRequest.date) == year,
                extract('month', DayOffRequest.date) == month
            ))
            .filter(Employee.facility_id == facility_id)
        )        
        results= query.all()
        employee_requests = defaultdict(list)
        for emp, req in results:
            if req is not None:
                employee_requests[emp].append(req)
            else:
                employee_requests[emp] = []

        res = getAllRequestSchema.dump([
            {"employee": emp, "requests": reqs} for emp, reqs in employee_requests.items()
        ])
        return res

def get_requests_service(facility_id, employee_id, year, month):
    with session_scope() as session:
        has_employee(facility_id, employee_id, session)
        request = session.query(DayOffRequest).filter(
            extract('year', DayOffRequest.date) == year,
            extract('month', DayOffRequest.date) == month,
            DayOffRequest.employee_id == employee_id
        ).all()
        res = getIndividualRequestSchema.dump(request)
        return res


def post_day_off_request_service(facility_id, employee_id, data):
    with session_scope() as session:
        validate_data(post_day_off_request_schema, data)
        has_employee(facility_id, employee_id, session)
        new_request = DayOffRequest(
            employee_id=employee_id,
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            type_of_vacation=data['type_of_vacation']
        )
        session.add(new_request)
        session.flush()
        res = DayOffRequestSchema().dump(new_request)
        return res


def delete_request_service(employee_id, request_id):
    with session_scope() as session:
        request = session.query(DayOffRequest).filter_by(employee_id=employee_id, request_id=request_id).first()
        if not request:
            return None
        session.delete(request)
        return request


def update_request_service(employee_id, request_id, data):
    with session_scope() as session:
        validate_data(put_day_off_request_schema, data)
        request = session.query(DayOffRequest).filter_by(employee_id=employee_id, request_id=request_id).first()
        if not request:
            return None
        request.type_of_vacation = data['type_of_vacation']
        request.updated_at = datetime.now()
        session.add(request)
        return DayOffRequestSchema().dump(request)
