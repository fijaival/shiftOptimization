from marshmallow import Schema, fields, validate


class PostConstraintSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))


post_constraint_schema = PostConstraintSchema()
