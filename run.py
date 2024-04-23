import os
from flask import Flask
from models.database import db
from api.api import api_blueprint
from web.routes import web_blueprint
from config import Config
from extensions import init_app
import web.auth.auth
from commands import create_admin, create_admin_if_not_exists


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_app(app)  # Initialize Flask extensions

    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(web_blueprint, url_prefix="/")

    # Register the custom Flask CLI command for creating an admin user
    app.cli.add_command(create_admin)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    # Ensures this runs only once and not on the reloader subprocess
    PROD = True if os.environ.get('PROD', False) == 'True' else False
    if PROD:
        with app.app_context():
            create_admin_if_not_exists()

    app.run(debug=not PROD)
