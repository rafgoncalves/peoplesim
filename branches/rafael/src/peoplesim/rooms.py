from peoplesim.common import *

class Room(Element):
    def __init__(self, name):
        super().__init__(name)
        self.room = self
        self.actors = {}
        self.objects = {}
        self.passages = {}

    def _addElement(self, element, collection):
        if element not in collection:
            collection[element.name] = element
            element.room = self
        else:
            raise NameError(''.join(("The element ", element.name, " is already in the room.")))

    def addActor(self, actor):
        self._addElement(actor, self.actors)

    def addObject(self, object):
        self._addElement(object, self.objects)

    def addPassage(self, room):
        self._addElement(room, self.passage)