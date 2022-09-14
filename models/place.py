#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship, backref


if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id",
                                 String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True,
                                 nullable=False),
                          Column("amenity_id",
                                 String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base if (getenv("HBNB_TYPE_STORAGE")=="db") else object):
    """ A place to stay"""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            "Review",
            cascade="all,delete",
            backref=backref("place", cascade="all,delete"),
            passive_deletes=True
        )
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            back_populates="place_amenities"
        )

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list
