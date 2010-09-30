from collections import deque

class ActionQueue(deque):
    def __str__(self):
        string = ""
        for action in self:
            string = ''.join((string, action.name, " > "))

        return string[:len(string)-2]

class Attribute:
    def __init__(self, name, max, value, decr):
        self.name = name
        self.max = max
        self.value = value
        self.decr = decr

    def update(self):
        self.value *= self.decr

    def __str__(self):
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