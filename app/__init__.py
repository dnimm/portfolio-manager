from flask import Flask
from app.db import db
from app.cache import cache
from app.routes import user_bp, portfolio_bp, security_bp, trade_bp
from app.error_handlers import register_error_handlers
from flask_cors import CORS

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, origins=["http://localhost:5173"])

    db.init_app(app)
    cache.init_app(app)

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(portfolio_bp, url_prefix="/portfolios")
    app.register_blueprint(security_bp, url_prefix="/securities")
    app.register_blueprint(trade_bp, url_prefix="/trades")

    register_error_handlers(app)
    
    

    return app