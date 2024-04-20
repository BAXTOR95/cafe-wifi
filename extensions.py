import os
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from models.database import db
from web.utils.google_maps_client import GoogleMapsClient
from dotenv import load_dotenv
from pathlib import Path

# Initialize environment variables
ENV_PATH = Path(".env")
load_dotenv(dotenv_path=ENV_PATH)

# Initialize Flask extensions
login_manager = LoginManager()
bootstrap = Bootstrap5()
gmaps_client = GoogleMapsClient(api_key=os.getenv('MAPS_API_KEY'))


def init_app(app):
    """Initialize Flask application."""
    # Initialize Flask extensions
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'web.login'

    bootstrap.init_app(app)
