from collections import deque

class ActionQueue(deque):
    """Implements a special type of Queue where actions are appended considering
    it's lengths.

    Public methods:
    human_readable(): Returns a human-readable string for the queue.
    """
    def humanReadable(self):
        string = ""
        for action in self:
            string = ''.join((string, action.name, " > "))
        return string[:len(string)-2]

    def append(self, action):
        super().extend(list(action for i in range(0, action.length)))

class Attribute:
    def __init__(self, name, max, value, decr):
        self.name = name
        self.max = max
        self.value = value
        self.decr = decr

    def update(self):
        self.value *= self.decr

    def humanReadable(self):
        return ''.join((self.name,": ", str(self.value)));

class Element:
    def __init__(self, name):
        self.actions = {}
        self.room = None
        self.name = name

    def _addAction(self, action):
        if action.name not in self.actions:
            self.actions[action.name] = action;
        else:
            raise NameError(''.join(("The action ", action.name, " is already set.")))