from flask import Flask, jsonify
from config import Config
from flask_cors import CORS
from extensions import jwt, db_session, init_db
from api.v1 import api_v1_bp
from .v1.utils.error import InvalidAPIUsage


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_v1_bp, url_prefix='/v1')

    app.config.from_object(Config)
    CORS(app,
         resources={r"/*": {"origins": ["http://localhost:8000/*"]}},
         supports_credentials=True,
         )

    jwt.init_app(app)

    with app.app_context():
        init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.errorhandler(InvalidAPIUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
