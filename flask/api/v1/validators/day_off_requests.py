from marshmallow import Schema, fields, validate


class PostDayOffRequestSchema(Schema):
    date = fields.Date(required=True)
    type_of_vacation = fields.Str(required=True, validate=validate.OneOf(["×", "有", "前×", "後×"]))


class PutDayOffRequestSchema(Schema):
    type_of_vacation = fields.Str(required=True, validate=validate.OneOf(["×", "有", "前×", "後×"]))


post_day_off_request_schema = PostDayOffRequestSchema()
put_day_off_request_schema = PutDayOffRequestSchema()
