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

    def test_create_errors(self):
        """
        Test cases for 'create' command errors.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create(self):
        """
        Test case for 'create' command with various classes.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create User")
            bm = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            us = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Place")
            st = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            pl = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Review")
            ct = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create City")
            rv = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Amenity")
            am = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            self.assertIn(bm, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all BaseModel")
            self.assertIn(us, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            self.assertIn(st, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all State")
            self.assertIn(pl, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Review")
            self.assertIn(ct, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all City")
            self.assertIn(rv, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Amenity")
            self.assertIn(am, f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create_kwargs(self):
        """
        Test 'create' command with keyword arguments.
        """
        call = ('create Place city_id="0001" name="My_house" '
                'number_rooms=4 latitude=37.77 longitude=a')

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd(call)
            pl = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            output = f.getvalue()

            self.assertIn(pl, output)
            self.assertIn("'city_id': '0001'", output)
            self.assertIn("'name': 'My house'", output)
            self.assertIn("'number_rooms': 4", output)
            self.assertIn("'latitude': 37.77", output)
            self.assertNotIn("'longitude'", output)

    def test_show(self):
        """
        Test cases for 'show' command.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """
        Test cases for 'destroy' command.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_all(self):
        """
        Test cases for 'all' command.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
    
    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_update(self):
        """
        Test cases for 'update' command.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update")
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update sldkfjsl")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(') + 1:obj.find(')')]

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User " + my_id)
            self.assertEqual("** attribute name missing **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User " + my_id + " Name")
            self.assertEqual("** value missing **\n", f.getvalue())
        
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User")
            self.assertEqual("** instance id missing **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User 12345")
            self.assertEqual("** no instance found **\n", f.getvalue())
    
    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_z_all(self):
        """
        Test alternate form of 'all' command.
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("asdfsdfsd.all()")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("State.all()")
            self.assertEqual("[]\n", f.getvalue())
    
    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_z_count(self):
        """
        Test 'count' command input.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("asdfsdfsd.count()")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
    
    def test_z_show(self):
        """
        Test alternate form of 'show' command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("BaseModel.show(abcd-123)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("safdsa.show()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
    
    def test_destroy(self):
        """
        Test alternate form of 'destroy' command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("Galaxy.destroy()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("User.destroy(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_update(self):
        """
        Test alternate form of 'update' command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("sldkfjsl.update()")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("User.update(12345)")
            self.assertEqual("** no instance found **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("create User")

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(') + 1:obj.find(')')]

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("User.update(" + my_id + ")")
            self.assertEqual("** attribute name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual("** value missing **\n", f.getvalue())


if __name__ == "__main__":
    unittest.main()