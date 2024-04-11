from flask import Flask
from flask_bootstrap import Bootstrap5
from models.database import db
from api.api import api_blueprint
from web.routes import web_blueprint
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Bootstrap5(app)
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(web_blueprint, url_prefix="/")
    with app.app_context():
        db.create_all()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
