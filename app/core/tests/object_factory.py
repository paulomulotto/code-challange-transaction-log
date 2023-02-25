from abc import ABC, abstractmethod

class ObjectFactory(ABC):
    index = 0

    @classmethod
    def create(cls, object):
        object.save()
        cls.index = cls.index + 1
        return object