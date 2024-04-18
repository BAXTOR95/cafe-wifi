from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin
from .database import db


class User(UserMixin, db.Model):
    """Represents a user in the database.

    Attributes:
        id (Mapped[int]): The unique identifier for the user.
        email (Mapped[str]): The email address of the user.
        password (Mapped[str]): The hashed password of the user.
        name (Mapped[str]): The name of the user.
        is_admin (Mapped[bool]): Whether the user is an admin or not.
        posts (relationship): A list of blog posts related to the user.
        comments (relationship): A list of comments related to the user.
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    is_admin: Mapped[bool] = mapped_column(Integer, default=0)
