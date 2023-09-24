#!/usr/bin/python3
"""Defines the State class."""

# Import necessary modules and classes
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """
    Represents a state in the HBNB project.

    Attributes:
        __tablename__ (str): The name of the corresponding database table.
        name (str): The name of the state (up to 128 characters).
        cities (relationship): A one-to-many relationship to the City
        model with a "state" back reference.
    """

    # Define the table name in the database
    __tablename__ = "states"

    # Define the 'name' attribute as a column in the table with a
    # maximum length of 128 characters
    name = Column(String(128), nullable=False)

    # Establish a one-to-many relationship with the City model
    # with a "state" back reference
    cities = relationship("City", backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """A relationship between state and city."""
            city_list = []
            all_cities = models.storage.all(City)
            for value in all_cities.values():
                if value.state_id == self.id:
                    city_list.append(value)
            return city_list
