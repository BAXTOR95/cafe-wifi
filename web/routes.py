import os
from flask import Blueprint, render_template, request, redirect, url_for

web_blueprint = Blueprint('web', __name__, template_folder='templates')


# Context processor to inject the MAPS_API_KEY into all templates
@web_blueprint.app_context_processor
def inject_maps_key():
    maps_api_key = os.getenv('MAPS_API_KEY')
    return dict(MAPS_API_KEY=maps_api_key)


@web_blueprint.route("/")
def home():
    return render_template("home.html")


# TODO: Add more routes here!
