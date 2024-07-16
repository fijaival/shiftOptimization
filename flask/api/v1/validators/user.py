from marshmallow import Schema, fields, validate


class PostUserListSchema(Schema):
    facility_id = fields.Int(required=True)
    username = fields.Str(
        required=True, validate=validate.Length(min=2, max=50))
    password = fields.Str(required=True, validate=validate.Regexp(
        regex='^([a-zA-Z0-9]{8,50})$', error='8文字以上50文字以下の半角英数字で入力してください'))
    is_admin = fields.Int(required=False, validate=validate.OneOf([0, 1]))


class LoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


post_user_schema = PostUserListSchema()
login_user_schema = LoginUserSchema()
