import os
import click
import subprocess
import shlex
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from sqlalchemy import exists


@click.command("create-admin")
@click.argument("email")
@click.argument("password")
@click.argument("name")
@with_appcontext
def create_admin(email, password, name):
    """Create an admin user

    Args:
        email: Email of the admin user
        password: Password of the admin user
        name: Name of the admin user

    Returns:
        None
    """
    from models import User
    from models.database import db

    if not db.session.query(exists().where(User.email == email)).scalar():
        try:
            hashed_password = generate_password_hash(
                password, method='pbkdf2:sha256', salt_length=8
            )
            admin_user = User(
                email=email, name=name, password=hashed_password, is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            click.echo(f"Admin {name} created successfully.")
        except Exception as e:
            click.echo(f"Failed to create admin due to: {str(e)}")
    else:
        click.echo("Admin with this email already exists.")


def create_admin_if_not_exists():
    """Create an admin user if it does not exist

    Returns:
        None
    """
    from models import User
    from models.database import db

    # Ensure environment variables are set
    admin_email = os.getenv('ADMIN_EMAIL', '').strip()
    admin_password = os.getenv('ADMIN_PASSWORD', '').strip()
    admin_name = os.getenv('ADMIN_NAME', '').strip()

    if not admin_email or not admin_password or not admin_name:
        click.echo("Admin environment variables are not set correctly.")
        return

    # Check if admin user already exists
    admin_exists = db.session.query(exists().where(User.email == admin_email)).scalar()
    if not admin_exists:
        try:
            # Create a new admin user
            hashed_password = generate_password_hash(
                admin_password, method='pbkdf2:sha256', salt_length=8
            )
            new_admin = User(
                email=admin_email,
                password=hashed_password,
                name=admin_name,
                is_admin=1,
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created successfully.")
        except Exception as e:
            print(f"Failed to create admin user: {str(e)}")
    else:
        print("Admin user already exists.")
