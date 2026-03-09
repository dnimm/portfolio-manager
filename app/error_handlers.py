from flask import jsonify
from pydantic import ValidationError
from app.db import db
from app.service.authorization_service import AuthorizationError


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        db.session.rollback()
        return jsonify({
            "error": "ValidationError",
            "detail": err.errors(),
        }), 422

    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(err):
        db.session.rollback()
        return jsonify({
            "error": "Forbidden",
            "detail": str(err),
        }), 403

    @app.errorhandler(Exception)
    def handle_generic_error(err):
        db.session.rollback()
        return jsonify({
            "error": "Internal Server Error",
            "detail": str(err),
        }), 500