#!/usr/bin/python3
"""Creates test cases for the functionality in console.py."""
import os
from io import StringIO
from console import HBNBCommand
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
import unittest
import models
from unittest.mock import patch


class TestHBNBCommand(unittest.TestCase):
   """Unit tests designed to assess the functionality of the HBNB command interpreter."""
   @classmethod
   def setUpClass(cls):
    """Setup for HBNBCommand testing.

    Renames any existing 'file.json' to 'tmp' temporarily.
    Resets the dictionary of FileStorage objects.
    Creates an instance of the command interpreter.
    """
    try:
        os.rename("file.json", "tmp")
    except IOError:
        pass
    cls.HBNB = HBNBCommand()
