#!/usr/bin/python3
"""Module for DBStorage class."""

from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Database storage class for AirBnB clone."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a DBStorage instance and create a database engine."""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}"
            .format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB")
            ),
            pool_pre_ping=True
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Retrieve all objects from the database or by a specific class."""
        classes = {
            "State": State,
            "City": City,
            "User": User,
            "Place": Place,
            "Amenity": Amenity,
            "Review": Review
        }

        if cls is not None:
            cls = classes.get(cls)
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for class_ in classes.values():
                objs.extend(self.__session.query(class_).all())

        new_dict = {}
        for obj in objs:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """Add a new object to the database session."""
        self.__session.add(obj)

    def save(self):
        """Save changes made to the database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload the database session and create tables if necessary."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the database session."""
        self.__session.close()
