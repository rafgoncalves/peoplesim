from math import copysign

from peoplesim.actions import *
from peoplesim.common import *

class Actor(Element):
    def __init__(self, name):
        super().__init__(name)
        self.attributes = {}
        self._setDefault()
        self._action_queue = ActionQueue()
        self._current_action = None

    def _setDefault(self):
        self._addAttribute(Attribute("energy", 100, 50, .98))
        self._addAttribute(Attribute("social", 100, 50, .9))
        self._addAttribute(Attribute("culture", 100, 50, .9))

        self._addAction(Sleep())

    def _addAttribute(self, attr):
        if attr.name not in self.attributes:
            self.attributes[attr.name] = attr;
        else:
            raise NameError(''.join(("The attribute ", attr.name, " is already set.")))

    def _chooseAction(self):
        """ Returns the actor's next action.

        This iterates over all _listPossibleActions(self.introspection) results,
        calculating the _finessFunction(action) for each and returning the best
        fitted.
        """
        fitness = None
        actions = self._listPossibleActions()

        for action in actions:
            current_fit = self._motivationFunction(action)

            # Order matters. If we chose to invert this conditions it leads to
            # an exception since we can't compare None and Float.
            if fitness is None or current_fit > fitness:
                fitness = current_fit
                chose = action
        return chose

    def _listPossibleActions(self):
        # Uses the Actor, the Room where it is and the objects in the room
        # to generate a list of sources for possible actions.
        actions = []
        sources = [self]
        if self.room is not None:
            sources.append(self.room)
            sources += list(self.room.objects[k] for k in self.room.objects.keys())

        # Note that they are not currently lists, we deal with that at the end.
        for source in sources:
            for key in source.actions.keys():
                actions.append(source.actions[key])

        return actions

    def _motivationFunction(self, action):
        """Receives an action and returns the calculated motivation score.

        This method shall be overriden in the child classes to create different
        personalites.
        """
        fit = 0;
        predictor = action.predict(self)
        n_times = action.length
        max = self._attributesMax()

        for i in range(0,n_times):
            for k in max:
                k_fit = predictor[k] - max[k]
                fit += copysign(pow(k_fit,2),k_fit)

        return fit/n_times

    def _attributesMax(self):
        """Returns a dict of {"attribute_name":max_value} containing all
        attributes defined for the Actor.
        """
        attributes_max = {}
        for k,v in self.attributes.items():
            attributes_max[k] = v.max
        return attributes_max

    def _attributesCurrent(self):
        """Returns a dict of {"attribute_name":current_value} containing all
        attributes defined for the Actor.
        """
        attributes_current = {}
        for k,v in self.attributes.items():
            attributes_current[k] = v.value
        return attributes_current

    def update(self):
        """Updates the attributes, manages the action_queue and executes the
        scheduled action. Returns nothing.
        """
        # First iterate through the attributes and update it's values using the
        # rules of each.
        for attr in self.attributes.values():
            attr.update()

        # Verify the queue status.
        self._analyseQueue()
        self._current_action = self._action_queue.popleft()
        self._current_action.execute(self)

    def _analyseQueue(self):
        # If there is no actions in the queue, schedule new ones
          if len(self._action_queue) == 0:
            self._action_queue.append(self._chooseAction())

    def printStatus(self):
        """ Prints the actor status in a human-readable form."""
        print("------------------")
        print("Actor: %s" % self.name)
        for attribute, value in self._attributesCurrent().items():
            print(" + %s: %f" % (attribute, value))

        if self._current_action is not None:
            print(" - Action: %s" % self._current_action.name)
        if len(self._action_queue) > 0:
            print(" - Queue: %s" % self._action_queue)
        else:
            print(" - Queue: <Empty>")
