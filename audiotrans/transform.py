from abc import ABCMeta, abstractmethod


class Transform(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, args):
        pass

    @abstractmethod
    def transform(self, data):
        pass
