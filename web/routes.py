from flask import Blueprint, render_template, request, redirect, url_for

web_blueprint = Blueprint('web', __name__, template_folder='templates')


@web_blueprint.route("/")
def home():
    return render_template("home.html")


# TODO: Add more routes here!
