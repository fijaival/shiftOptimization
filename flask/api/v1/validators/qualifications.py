from marshmallow import Schema, fields, validate


class PostQualificationSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))


post_qualification_schema = PostQualificationSchema()
