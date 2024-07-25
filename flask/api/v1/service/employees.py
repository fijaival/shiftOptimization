from datetime import datetime
from api.v1.utils.error import InvalidAPIUsage
from sqlalchemy.orm.session import Session as BaseSession
from ..validators import post_employee_schema, put_employee_schema
from ..models import Qualification, EmployeeConstraint, Constraint, Employee, Facility, EmployeeType, Dependency, EmployeeSchema
from ..utils.context_maneger import session_scope
from ..utils.validate import validate_data


def get_all_employees_service(facility_id):
    with session_scope() as session:
        employees = session.query(Employee).filter_by(facility_id=facility_id,is_delete = 0).all()
        res = EmployeeSchema().dump(employees, many=True)
        return res


def add_employee_service(facility_id, data):
    with session_scope() as session:
        validate_data(post_employee_schema, data)
        has_employee_type(data['employee_type_id'], session)
        has_constraint(facility_id, data['constraints'], session)
        has_qualification(facility_id, data['qualifications'], session)
        has_employee(facility_id, data["dependencies"], session)
        new_employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            employee_type_id=data['employee_type_id'],
            facility_id=facility_id,
            is_delete = 0
        )
        for const_data in data['constraints']:
            found_cons = session.query(Constraint).filter_by(constraint_id=const_data["constraint_id"]).first()
            employee_constraint = EmployeeConstraint(constraint=found_cons, value=const_data["value"])
            new_employee.employee_constraints.append(employee_constraint)
        for qual_data in data['qualifications']:
            found_qual = session.query(Qualification).filter_by(qualification_id=qual_data["qualification_id"]).first()
            new_employee.qualifications.append(found_qual)
        for dep_data in data['dependencies']:
            dependency = Dependency(dependent_employee_id=dep_data)
            new_employee.dependencies.append(dependency)
        session.add(new_employee)
        session.flush()
        print(EmployeeSchema().dump(new_employee))
        return EmployeeSchema().dump(new_employee)


def delete_employee_service(employee_id):
    with session_scope() as session:
        employee: Employee = session.query(Employee).filter_by(employee_id=employee_id).first()
        if not employee or employee.is_delete == 1:
            return None
        employee.is_delete = 1
        session.add(employee)
        session.flush()
        res = EmployeeSchema().dump(employee)
        return res


def update_employee_service(facility_id, employee_id, data):
    with session_scope() as session:
        validate_data(put_employee_schema, data)
        employee: Employee = session.query(Employee).filter_by(employee_id=employee_id, facility_id=facility_id).first()
        if not employee or employee.is_delete == 1:
            raise InvalidAPIUsage("Employee not found", 404)

        has_employee_type(data['employee_type_id'], session)
        has_constraint(facility_id, data['constraints'], session)
        has_qualification(facility_id, data['qualifications'], session)
        has_employee(facility_id, data["dependencies"], session)

        employee.first_name = data['first_name']
        employee.last_name = data['last_name']
        employee.employee_type_id = data['employee_type_id']
        employee.updated_at = datetime.now()

        employee.employee_constraints.clear()
        for const_data in data['constraints']:
            found_cons = session.query(Constraint).filter_by(constraint_id=const_data["constraint_id"]).first()
            employee_constraint = EmployeeConstraint(constraint=found_cons, value=const_data["value"])
            employee.employee_constraints.append(employee_constraint)

        employee.qualifications.clear()
        for qual_data in data['qualifications']:
            found_qual = session.query(Qualification).filter_by(qualification_id=qual_data["qualification_id"]).first()
            employee.qualifications.append(found_qual)

        session.query(Dependency).filter_by(employee_id=employee_id).delete()
        for dep_data in data['dependencies']:
            dependency = Dependency(employee_id=employee_id, dependent_employee_id=dep_data)
            employee.dependencies.append(dependency)

        session.add(employee)
        session.flush()
        res = EmployeeSchema().dump(employee)
        return res


def has_employee_type(employee_type_id, session: BaseSession):
    employee_type = session.query(EmployeeType).filter_by(employee_type_id=employee_type_id).first()
    if not employee_type:
        raise InvalidAPIUsage("Employee type not found", 404)


def has_constraint(facility_id, constraints, session: BaseSession):
    facility = session.query(Facility).filter_by(facility_id=facility_id).first()
    for q in constraints:
        constraint = session.query(Constraint).filter_by(constraint_id=q["constraint_id"]).first()
        if not constraint:
            raise InvalidAPIUsage("Constraint not found", 404)
        if not any(con.constraint_id == q["constraint_id"] for con in facility.constraints):
            raise InvalidAPIUsage("This facility does not have the constraint with ID" +
                                  f"{q['constraint_id']} registered.", 404)


def has_qualification(facility_id, qualifications, session: BaseSession):
    facility = session.query(Facility).filter_by(facility_id=facility_id).first()
    for q in qualifications:
        qualification = session.query(Qualification).filter_by(qualification_id=q["qualification_id"]).first()
        if not qualification:
            raise InvalidAPIUsage("Qualification not found", 404)
        if not any(qual.qualification_id == q["qualification_id"] for qual in facility.qualifications):
            raise InvalidAPIUsage("This facility does not have the qualification with ID" +
                                  f"{q['qualification_id']} registered.", 404)


def has_employee(facility_id, dependencies, session: BaseSession):
    for d in dependencies:
        employee = session.query(Employee).filter_by(employee_id=d, facility_id=facility_id).first()
        if not employee:
            raise InvalidAPIUsage("dependency not found", 404)
