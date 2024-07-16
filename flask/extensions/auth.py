from flask import jsonify


from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, get_jwt, jwt_required
)
from functools import wraps
jwt = JWTManager()


@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    from api.v1.models import User
    user = User.query.filter_by(user_id=identity).first()
    return {
        'user_id': identity,
        'is_admin': user.is_admin,
        'facility_id': user.facility_id
    }

# トークンの有効期限切れ時の挙動


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    token_type = jwt_payload['type']
    if token_type == 'access':
        message = "access token has expired"
    else:
        message = "refresh token has expired"
    response = jsonify({
        "error": {
            "message": "token has expired",
            "code": 401
        }
    })
    response.status_code = 401
    return response

# 無効な形式のトークン時の挙動


@jwt.invalid_token_loader
def my_invalid_token_callback(error_string):
    response = jsonify({
        "error": {
            "message": error_string,
            "code": 401
        }
    })
    response.status_code = 401
    return response

# 認証エラー時の挙動


@jwt.unauthorized_loader
def custom_unauthorized_response(error_string):
    response = jsonify({
        "error": {
            "message": error_string,
            "code": 401
        }
    })
    response.status_code = 401
    return response


@jwt.token_in_blocklist_loader
def token_block(jwt_header, jwt_payload):
    from api.v1.models import TokenBlocklist
    if TokenBlocklist.query.filter_by(jti=jwt_payload["jti"]).first():
        return True
    return False


'''アクセス制限用にデコレータを作成する'''
# 自分の施設のみアクセスできるエンドポイント


def self_facility_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # 通常のトークン認証
        claims = get_jwt()
        if claims['facility_id'] != kwargs['facility_id']:  # カスタマイズした権限情報の確認
            response = jsonify({
                "error": {"massage": "unauthorized", "code": 403}
            })
            response.status_code = 401
            return response
        else:
            return fn(*args, **kwargs)
    return wrapper

# 管理者のみアクセスできるエンドポイント


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # 通常のトークン認証
        claims = get_jwt()
        if claims['is_admin'] != 1:  # カスタマイズした権限情報の確認
            response = jsonify({
                "error": {"massage": "unauthorized", "code": 403}
            })
            response.status_code = 403
            return response
        else:
            return fn(*args, **kwargs)
    return wrapper
