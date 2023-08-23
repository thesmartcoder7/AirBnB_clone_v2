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

    @classmethod
    def tearDownClass(cls):
        """Teardown for HBNBCommand testing.

        Restores the original 'file.json'.
        Deletes the test HBNBCommand instance.
        Closes the session if using DBStorage.
        """
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.HBNB
        if isinstance(models.storage, DBStorage):
            models.storage._DBStorage__session.close()

    def setUp(self):
        """Set up for each test case.

        Resets the dictionary of FileStorage objects.
        """
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Teardown for each test case.

        Deletes any created 'file.json'.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass

