from marshmallow import Schema, fields, validate


class PostShiftsSchema(Schema):
    date = fields.Date(required=True)
    employee_id = fields.Int(required=True)
    shift_number = fields.Int(required=True)
    task_id = fields.Int(required=True)


put_shifts_schema = PostShiftsSchema()
post_shifts_schema = PostShiftsSchema(many=True)
