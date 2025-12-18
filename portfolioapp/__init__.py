from flask import Flask
from portfolioapp.db import db
from portfolioapp.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from portfolioapp.routes.user_routes import user_bp
    from portfolioapp.routes.portfolio_routes import portfolio_bp
    from portfolioapp.routes.security_routes import security_bp
    from portfolioapp.routes.transaction_routes import transaction_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(transaction_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return {"message": "Portfolio API is running"}

    return app
