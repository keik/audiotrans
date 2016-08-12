from abc import ABCMeta, abstractmethod


class Transform(metaclass=ABCMeta):

    @abstractmethod
    def transform(self):
        pass
