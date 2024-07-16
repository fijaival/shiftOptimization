from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, get_jwt,
                                set_access_cookies, set_refresh_cookies, unset_jwt_cookies)
from flask import jsonify
from datetime import datetime, timezone
from ..models import User, UserSchema, TokenBlocklist
from ..validators import post_user_schema, login_user_schema
from api.v1.utils.error import InvalidAPIUsage
from ..utils.context_maneger import session_scope
from ..utils.validate import validate_data


def signup_user(data):
    with session_scope() as session:
        validate_data(post_user_schema, data)
        user = session.query(User).filter_by(username=data["username"]).first()
        if user:
            return None
        new_user = User(**data)
        session.add(new_user)
        session.flush()
        res = UserSchema().dump(new_user)
        return res


def login_user(data):
    with session_scope() as session:
        validate_data(login_user_schema, data)
        auth_user = session.query(User).filter_by(username=data['username']).first()
        if auth_user is not None and auth_user.check_password(data['password']):
            access_token = create_access_token(identity=auth_user.user_id)
            refresh_token = create_refresh_token(identity=auth_user.user_id)
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        else:
            raise InvalidAPIUsage('Invalid User.', 401)


def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    resp = jsonify({'refresh': True})
    resp.set_cookie('access_token_cookie', '', expires=datetime(1970, 1, 1))
    resp.set_cookie('access_token_cookie', access_token,
                    samesite='None', secure=True)
    return resp


def logout_user():
    with session_scope() as session:
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        new_block_token = TokenBlocklist(jti=jti, type=ttype, created_at=now)
        session.add(new_block_token)
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp
