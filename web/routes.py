import os
import requests
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from models import Cafe, User
from models.database import db
from web.forms import RegisterForm, LoginForm, CafeForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import (
    login_user,
    login_required,
    logout_user,
)
from dotenv import load_dotenv
from pathlib import Path
from extensions import gmaps_client

web_blueprint = Blueprint('web', __name__, template_folder='templates')

ENV_PATH = Path("..", "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)


# Context processor to inject the MAPS_API_KEY into all templates
@web_blueprint.app_context_processor
def inject_maps_key():
    maps_api_key = os.getenv('MAPS_API_KEY')
    return dict(MAPS_API_KEY=maps_api_key)


@web_blueprint.route("/config")
def config():
    return jsonify({"mapsApiKey": os.getenv('MAPS_API_KEY', 'defaultKey')})


@web_blueprint.route("/")
def home():
    """Displays the home page with a list of cafes."""
    # Fetch all cafes from the database
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template("home.html", cafes=cafes)


@web_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Handles user registration.

    GET: Displays the registration form.
    POST: Processes the submitted form. Registers a new user if validation succeeds and the email is not already taken.
    Redirects to the index page upon successful registration or back to the register form with validation errors.

    Returns:
        Response: The register template on GET or redirect on successful POST.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            name = form.name.data
            password = form.password.data
            password2 = form.password2.data
            if password != password2:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('web.register'))
            hashed_password = generate_password_hash(
                password, method='pbkdf2:sha256', salt_length=8
            )
            new_user = User(email=email, name=name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('web.home'))
        except IntegrityError:
            db.session.rollback()
            flash("That email already exists, please login.", category='error')
            return redirect(url_for('web.login'))
    return render_template("register.html", form=form)


@web_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login.

    GET: Displays the login form.
    POST: Processes the submitted form. Logs in the user if validation succeeds and the email and password match.
    Redirects to the index page upon successful login or back to the login form with validation errors.

    Returns:
        Response: The login template on GET or redirect on successful POST.
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('web.home'))
        flash('Invalid email or password.', 'danger')
    return render_template("login.html", form=form)


@web_blueprint.route('/logout')
@login_required
def logout():
    """Logs out the current user and redirects to the index page.

    Returns:
        Response: Redirect to the index page.
    """
    logout_user()
    flash("You have been logged out.", category='success')
    return redirect(url_for('web.home'))


def construct_full_address(form):
    """
    Constructs a full address string from the given form data.

    Args:
        form: The form object containing the address input fields.

    Returns:
        A string representing the full address, with empty parts filtered out.
    """
    address_parts = [
        form.location_input.data,
        form.address2_input.data if form.address2_input.data else "",
        form.locality_input.data,
        form.administrative_area_level_1_input.data,
        form.postal_code_input.data,
        form.country_input.data,
    ]
    return ", ".join(filter(None, address_parts))


def get_geocode(address):
    """
    Get the latitude and longitude coordinates for a given address.

    Parameters:
    address (str): The address to geocode.

    Returns:
    tuple: A tuple containing the latitude and longitude coordinates.
           If the geocoding fails, returns (None, None).
    """
    try:
        geocode_result = gmaps_client.geocode(address)
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        return latitude, longitude
    except (IndexError, requests.exceptions.RequestException) as e:
        return None, None


def cafe_exists(address):
    """
    Check if a cafe with the given address exists in the database.

    Args:
        address (str): The address of the cafe to check.

    Returns:
        bool: True if a cafe with the given address exists, False otherwise.
    """
    return Cafe.query.filter_by(location=address).first() is not None


def create_cafe(form, address, lat, lng):
    """
    Create a new Cafe object based on the provided form data, address, latitude, and longitude.

    Args:
        form (Form): The form data containing the cafe details.
        address (str): The address of the cafe.
        lat (float): The latitude of the cafe's location.
        lng (float): The longitude of the cafe's location.

    Returns:
        Cafe: The newly created Cafe object.
    """
    return Cafe(
        name=form.name.data,
        img_url=form.img_url.data,
        location=address,
        latitude=lat,
        longitude=lng,
        seats=form.seats.data,
        has_toilet=form.has_toilet.data,
        has_wifi=form.has_wifi.data,
        has_sockets=form.has_sockets.data,
        can_take_calls=form.can_take_calls.data,
        coffee_price=form.coffee_price.data,
    )


@web_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_cafe():
    """Handles adding a new cafe to the database.

    GET: Displays the add cafe form.
    POST: Processes the submitted form. Adds a new cafe if validation succeeds.
    Redirects to the index page upon successful addition or back to the add cafe form with validation errors.

    Returns:
        Response: The add cafe template on GET or redirect on successful POST.
    """
    form = CafeForm()
    if form.validate_on_submit():
        full_address = construct_full_address(form)
        latitude, longitude = get_geocode(full_address)

        if latitude is None or longitude is None:
            flash(
                "Address could not be geocoded. Please check the address details.",
                category='error',
            )
            return render_template("add_cafe.html", form=form)

        if cafe_exists(full_address):
            flash("Cafe already exists in the database.", category='error')
            return render_template("add_cafe.html", form=form)

        new_cafe = create_cafe(form, full_address, latitude, longitude)
        db.session.add(new_cafe)
        db.session.commit()
        flash("Successfully added the new cafe.", category='success')
        return redirect(url_for('web.home'))

    return render_template("add_cafe.html", form=form)


# TODO: Add more routes here!
