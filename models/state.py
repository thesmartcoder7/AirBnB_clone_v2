#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from os import environ
import models


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if 'HBNB_TYPE_STORAGE' in environ and environ['HBNB_TYPE_STORAGE'] == 'db':
        cities = relationship('City', cascade="all, delete-orphan",
                              backref="state")
    else:
        @property
        def cities(self):
            my_list = []
            stat = self.id
            for k, v in models.storage.all().items():
                if "City" in k and v.state_id == self.id:
                    my_list.append(v)
            return my_list
        