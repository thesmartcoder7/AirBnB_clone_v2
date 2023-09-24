#!/usr/bin/python3
"""This is the db storage class for AirBnB"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from os import environ
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage():
    """
    """
    __engine = None
    __session = None
    cla = [State, City, User, Place, Review, Amenity]

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if 'HBNB_ENV' in environ and environ['HBNB_ENV'] == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """all"""
        dic = {}
        if cls is None:
            for c in self.cla:
                row = self.__session.query(c).all()
                for k in row:
                    key = ".".join([c.__name__, k.id])
                    dic.update({key: k})
            return dic
        row = self.__session.query(eval(cls)).all()
        for k in row:
            key = ".".join([cls, k.id])
            dic.update({key: k})
        return dic

    def new(self, obj):
        """new"""
        self.__session.add(obj)

    def save(self):
        """save"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reload"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)()

    def close(self):
        """close"""
        self.__session.close()
