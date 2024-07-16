
from marshmallow import Schema, fields, validate


class PostFacilitySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))


class PostFcilityAtributeSchema(Schema):
    id = fields.Int(required=True)


class FacilityConstraintSchema(Schema):
    constraint_id = fields.Int(required=True)


class FacilityQualificationSchema(Schema):
    qualification_id = fields.Int(required=True)


class FacilityTaskSchema(Schema):
    task_id = fields.Int(required=True)


class PutFacilitySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))

    constraints = fields.List(fields.Nested(FacilityConstraintSchema), required=True)
    qualifications = fields.List(fields.Nested(FacilityQualificationSchema), required=True)
    tasks = fields.List(fields.Nested(FacilityTaskSchema), required=True)


post_facility_schema = PostFacilitySchema()
post_facility_atrubute_schema = PostFcilityAtributeSchema()
put_facility_schema = PutFacilitySchema()
