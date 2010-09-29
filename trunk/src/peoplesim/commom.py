# To change this template, choose Tools | Templates
# and open the template in the editor.

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