from extensions import login_manager
from models.database import db
from models import User


# Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback.
    Args:
        user_id (int): The user ID.
    Returns:
        User: The user instance or None.
    """
    return db.session.get(User, user_id)
