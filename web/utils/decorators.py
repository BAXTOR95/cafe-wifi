from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    """Decorator to restrict access to admin users.

    Args:
        f (Callable): The view function to decorate.

    Returns:
        Callable: The decorated view function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You must be an admin to view this page.", "warning")
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    return decorated_function
