from marshmallow import Schema, fields, validate


class EmployeeConstraintSchema(Schema):
    constraint_id = fields.Int(required=True)
    value = fields.Int(required=True)


class EmployeeQualificationSchema(Schema):
    qualification_id = fields.Int(required=True)


class EmployeeDependencySchema(Schema):
    dependencies = fields.List(fields.Int)


class PostEmployeeSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    employee_type_id = fields.Int(required=True)

    constraints = fields.List(fields.Nested(EmployeeConstraintSchema), required=True)
    qualifications = fields.List(fields.Nested(EmployeeQualificationSchema), required=True)
    dependencies = fields.List(fields.Int(), required=True)


class PutEmployeeSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    employee_type_id = fields.Int(required=True)

    constraints = fields.List(fields.Nested(EmployeeConstraintSchema), required=True)
    qualifications = fields.List(fields.Nested(EmployeeQualificationSchema), required=True)
    dependencies = fields.List(fields.Int(), required=True)


post_employee_schema = PostEmployeeSchema()
put_employee_schema = PutEmployeeSchema()
