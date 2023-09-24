#!/usr/bin/python3
"""Amenity Module for the HBNB project."""

# Import necessary modules and classes
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    Class representing an Amenity in the HBNB project.

    Attributes:
        __tablename__ (str): The name of the corresponding
        database table.

        name (str): The name of the Amenity (up to 128 characters).

        place_amenities (relationship): A relationship to the Place model
        through the "place_amenity" table.
    """

    # Define the table name in the database
    __tablename__ = "amenities"

    # Define the 'name' attribute as a column in the table with
    # a maximum length of 128 characters
    name = Column(String(128), nullable=False)

    # Establish a many-to-many relationship with the Place model
    # through the "place_amenity" table
    place_amenities = relationship(
        "Place",
        secondary="place_amenity",
        viewonly=False
    )
