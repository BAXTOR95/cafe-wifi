from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from models.database import db

# Initialize Flask extensions
login_manager = LoginManager()
bootstrap = Bootstrap5()


def init_app(app):
    """Initialize Flask application."""
    # Initialize Flask extensions
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'web.login'

    bootstrap.init_app(app)
