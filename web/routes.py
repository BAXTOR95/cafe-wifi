import os
from flask import Blueprint, render_template, request, redirect, url_for
from models import Cafe
from models.database import db

web_blueprint = Blueprint('web', __name__, template_folder='templates')


# Context processor to inject the MAPS_API_KEY into all templates
@web_blueprint.app_context_processor
def inject_maps_key():
    maps_api_key = os.getenv('MAPS_API_KEY')
    return dict(MAPS_API_KEY=maps_api_key)


@web_blueprint.route("/")
def home():
    # Fetch all cafes from the database
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template("home.html", cafes=cafes)


# TODO: Add more routes here!
