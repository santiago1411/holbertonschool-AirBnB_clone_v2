#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.schema import MetaData
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


user = getenv('HBNB_MYSQL_USER')
password = getenv('HBNB_MYSQL_PWD')
host = getenv('HBNB_MYSQL_HOST')
database = getenv('HBNB_MYSQL_DB')
env = getenv('HBNB_ENV')
config = 'mysql+mysqldb://{}:{}@{}/{}'.format(
    user, password, host, database)


class DBStorage:
    """
    Class that configures a database
    """
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(config, pool_pre_ping=True)

        """ Drop all tables"""
        if env == "test":
            metadata = MetaData(self.__engine)
            metadata.reflect()
            metadata.drop_all()

    def all(self, cls=None):
        """Retrives a dictionary of class instances"""
        new_dict = {}
        classes = {
            'User': User, 'Place': Place, 'Review': Review,
            'State': State, 'City': City, 'Amenity': Amenity
        }
        if cls:
            if cls in classes.keys():
                data = self.__session.query(classes[cls]).all()
                for obj in data:
                    new_dict[obj.__class__.__name__ + '.' + obj.id] = obj
            else:
                data = self.__session.query(cls).all()
                for obj in data:
                    new_dict[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for class_name in classes:
                data = self.__session.query(classes[class_name]).all()
                for obj in data:
                    new_dict[obj.__class__.__name__ + '.' + obj.id] = obj

        return new_dict

    def new(self, obj):
        """ Add new elements """
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Configure and create a session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Public method to close the session"""
        self.__session.close()
