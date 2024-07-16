from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from api.v1.utils.error import InvalidAPIUsage
from ..service.auth import signup_user, login_user, refresh_token, logout_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    input_data = request.json
    res = signup_user(input_data)
    if not res:
        raise InvalidAPIUsage("This username is already used")
    return res, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    res = login_user(data)
    return res, 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    resp,  = refresh_token()
    return resp, 200


@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def modify_token():
    resp = logout_user()
    return resp, 200
