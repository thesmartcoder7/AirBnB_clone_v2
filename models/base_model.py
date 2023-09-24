#!/usr/bin/python3
"""Base class for other classes."""

# Import necessary modules and classes
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import models
import uuid

# Create a SQLAlchemy declarative base
Base = declarative_base()


class BaseModel:
    """
    The Base class for other classes in the project.

    Attributes:
        id (str): A unique identifier for the instance.
        created_at (datetime): The datetime when the instance was created.
        updated_at (datetime): The datetime when the instance was last updated.
    """

    # Define class attributes as columns in the table
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initialize a new instance of the Base class.

        Args:
            *args: Additional arguments (not used).
            **kwargs: Keyword arguments used to set instance attributes.
        """
        # Generate a unique identifier for the instance
        self.id = str(uuid.uuid4())

        # Set created_at and updated_at to the current datetime
        self.created_at = self.updated_at = datetime.utcnow()

        # Update instance attributes based on provided kwargs
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def save(self):
        """
        Update the updated_at attribute with the current datetime
        and save the instance to storage.
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def __str__(self):
        """Return a string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in obj_dict.keys():
            del obj_dict["_sa_instance_state"]
        return obj_dict

    def delete(self):
        """Delete the instance from storage."""
        models.storage.delete(self)
