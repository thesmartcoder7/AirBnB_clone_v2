#!/usr/bin/python3
"""This module defines a class User."""

# Import necessary modules and classes
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import Place
from models.review import Review


class User(BaseModel, Base):
    """
    Represents a user in the HBNB project.

    Attributes:
        __tablename__ (str): The name of the corresponding database table.
        email (str): The email address of the user (up to 128 characters).
        password (str): The password of the user (up to 128 characters).
        first_name (str): The first name of the user (up to 128 characters).
        last_name (str): The last name of the user (up to 128 characters).
        places (relationship): A one-to-many relationship to the Place model
        with a "user" back reference.
        reviews (relationship): A one-to-many relationship to the Review model
        with a "user" back reference.
    """

    # Define the table name in the database
    __tablename__ = "users"

    # Define columns for the User table
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))

    # Establish one-to-many relationships with Place and Review
    # models with "user" back references
    places = relationship("Place", backref="user", cascade="delete")
    reviews = relationship("Review", backref="user", cascade="delete")
