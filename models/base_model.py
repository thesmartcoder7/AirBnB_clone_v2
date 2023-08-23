#!/usr/bin/python3

"""
Module for the BaseModel class.

This module defines the BaseModel class, which is a
base class that defines common attributes and methods for
other classes.

"""

from models import storage
import uuid
from datetime import datetime


class BaseModel:
    """
    A base class that defines common attributes and methods for other classes.

    Public instance attributes:
    - id: string - A unique identifier assigned using uuid when an instance is
    created.
    - created_at: datetime - The datetime when an instance is created.
    - updated_at: datetime - The datetime when an instance is last updated.

    Public instance methods:
    - save(self): Updates the public instance attribute updated_at with the
    current datetime and calls the save() method of storage.
    - to_dict(self): Returns a dictionary representation of the BaseModel
    instance.

    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        If kwargs is not empty, it recreates an instance using the dictionary
        representation. Otherwise, it creates a new instance with a new id
        and created_at.

        Args:
            *args: Not used.
            **kwargs: A dictionary representing the instance attributes.

        """
        if kwargs:
            if 'id' not in kwargs:
                kwargs['id'] = str(uuid.uuid4())
            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        The string includes the class name, id, and instance attributes.

        Returns:
            str: A string representation of the BaseModel instance.

        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the public instance attribute updated_at with the current
        datetime and calls the save() method of storage.

        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the BaseModel instance.

        The dictionary contains all instance attributes, including the
        class name, id, created_at, and updated_at attributes.

        Returns:
            dict: A dictionary representation of the BaseModel instance.

        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
    