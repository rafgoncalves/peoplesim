from collections import deque

class ActionQueue(deque):
    """Implements a special type of Queue where actions are appended considering
    it's lengths.

    Public methods:
    human_readable(): Returns a human-readable string for the queue.
    """
    def __init__(self):
        super(ActionQueue, self).__init__()
        self._tickCounter = 0
        self._current = None

    def humanReadable(self):
        actions = [self._current.name
                   for i in range(self._current.length - self._tickCounter)]
        
        actions.extend([action.name for action in self
                                    for i in range(action.length)])

        string = ' > '.join(actions)
        return string

    def popleft(self):
        if(self._current != None and self._tickCounter < self._current.length):
            self._tickCounter += 1;
        else:
            self._tickCounter = 0;
            self._current = super(ActionQueue, self).popleft()

        return self._current


class Attribute(object):
    def __init__(self, name, max, value, decr):
        self.name = name
        self.max = max
        self.value = value
        self.decr = decr

    def update(self):
        self.value *= self.decr

    def humanReadable(self):
        return ''.join((self.name,": ", str(self.value)));

class Element(object):
    def __init__(self, name):
        self.actions = {}
        self.room = None
        self.name = name

    def _addAction(self, action):
        if action.name not in self.actions:
            self.actions[action.name] = action;
            action.element = self
        else:
            raise NameError(''.join(("The action ", action.name, " is already set.")))
