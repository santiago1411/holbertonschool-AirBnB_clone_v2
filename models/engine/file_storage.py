#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                sp = key.split('.')
                if sp[0] == cls.__name__:
                    new_dict[key] = value
            return new_dict
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        dic_to_save = {}

        for key in self.__objects.keys():
            dic_to_save[key] = self.__objects.get(key).to_dict()

        with open(self.__file_path, mode='w', encoding="utf-8") as f:
            json.dump(dic_to_save, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(self.__file_path, 'r', encoding="utf-8") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except Exception:
            pass

    def delete(self, obj=None):
        """ Instance public method to delete an obj"""
        if obj is not None:
            key_obj = None
            for key, value in self.__objects.items():
                if value == obj:
                    key_obj = key
                    break
            del self.__objects[key_obj]

    def close(self):
        """
        Instance public method that calls reload method
        for deserializing the JSON file to objects
        """
        self.reload()
