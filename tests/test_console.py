#!/usr/bin/python3
"""
Creates test cases for the functionality in console.py.
"""

import os
from io import StringIO
from console import HBNBCommand
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
import unittest
import models
from unittest.mock import patch


class TestHBNBCommand(unittest.TestCase):
   """
   Unit tests designed to assess the functionality of the HBNB command interpreter.
   """
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
    

    def test_docstrings(self):
        """
        Ensure docstrings are present for methods.
        """
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)

    def test_emptyline(self):
        """
        Test case for handling empty line input.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("\n")
            self.assertEqual("", f.getvalue())
    
    def test_quit(self):
        """
        Test case for 'quit' command input.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("quit")
            self.assertEqual("", f.getvalue())
    
    def test_EOF(self):
        """
        Test that using EOF quits the command interpreter.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(self.HBNB.onecmd("EOF"))


