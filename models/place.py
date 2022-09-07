#!/usr/bin/python3
""" Place Module for HBNB project """
from email.policy import default
import string
import models
from models.review import Review
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(string(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(string(60), ForeignKey('users.id'), nullable=False)
    name = Column(string(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(int, default=0, nullable=False)
    max_guest = Column(int, default=0, nullable=False)
    price_by_night = Column(int, default=0, nullable=False)
    latitude = Column(float, nullable=True)
    longitude = Column(float, nullable=True)
    amenity_ids = []
    reviews = relationship('Review', backref='place', cascade='all, delete-orfan')

    @property
    def reviews(self):
        """
        Returns the list of Reviews instances with
        place_id equals to the current Place.id
        """
        reviews = list()

        for _id, review in models.storage.all(Review).items():
            if review.place_id == self.id:
                reviews.append(review)

        return (reviews)
