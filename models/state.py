#!/usr/bin/python3
""" State Module for HBNB project """

from os import getenv
import models
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City',
            backref='state',
            cascade='all, delete-orphan'
            )
    else:
        name = ''

        @property
        def cities(self):
            """
            Returns the list of City instances with
            state_id equals to the current State.id
            """
            cities = list()

            for _id, city in models.storage.all(City).items():
                if city.state_id == self.id:
                    cities.append(city)

            return (cities)
