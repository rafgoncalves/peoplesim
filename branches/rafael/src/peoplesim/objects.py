from peoplesim.actions import *
from peoplesim.common import *

class Object(Element):
    pass

class Phone(Object):
    def __init__(self):
        super(Phone, self).__init__(self.__class__.__name__)
        self._addAction(CallFriend())

class ClassBook(Object):
    def __init__(self):
        super(ClassBook, self).__init__(self.__class__.__name__)
        self._addAction(Study())