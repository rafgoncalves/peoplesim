from math import copysign
from copy import copy

from peoplesim.actions import *
from peoplesim.common import *

class Actor(Element):
    def __init__(self, name):
        super().__init__(name)
        self.attributes = {}
        self._setDefault()
        self._action_queue = ActionQueue()
        self._current_action = None
        self.introspection = 1

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
        """ Return the best fitted list of actions (always a list).

        This iterates over all _listPossibleActions(self.introspection) results,
        calculating the _finessFunction(action) for each and returning the best
        fitted.
        """
        fitness = None
        actions = self._listPossibleActions(self.introspection)

        for action in actions:
            # We check if it's a single action or a list of actions. The
            # _finessFunction(action) method shall receive only lists.
            if not isinstance(action, list):
                action = [action]

            current_fit = self._fitnessFunction(action)

            # Order matters. If we chose to invert this conditions it leads to
            # an exception since we can't compare None and Float.
            if fitness is None or current_fit > fitness:
                fitness = current_fit
                chose = action

        return chose

    # TODO: Rewrite this method. It's not working for introspection > 2
    def _listPossibleActions(self, introspection=1):
        """Returns a list of actions and lists of actions of all possible actions
        available to the Actor according with self, the room and the objects.

        The introspection is used to evaluate all possible combinations of N
        anctions and its subsets. For example, supose two actions A and B:

        _listPossibleActions(1) returns [A, B]
        _listPossibleActions(1) returns [A, B, [A, A], [A, B], [B, A], [B, B]]

        Please note that the use of introspection is not efficient, since its a
        NP problem.
        """

        # actions is a list of actions or lists of actions.
        actions = []

        # Uses the Actor, the Room where it is and the objects in the room
        # to generate a list of sources for possible actions.
        sources = [self]
        if self.room is not None:
            sources.append(self.room)
            sources += list(self.room.objects[k] for k in self.room.objects.keys())

        # Note that they are not currently lists, we deal with that at the end.
        for source in sources:
            for key in source.actions.keys():
                actions.append(source.actions[key])

        # Recursively defines the possible actions.
        if introspection > 1:
            # We employ this hack to avoid infinite looping since new items
            # will be added to actions.
            base_actions = copy(actions)

            # Executes the recursion.
            prior_actions_lists = self._listPossibleActions(introspection-1);
            for action in base_actions:
                for prior_actions_list in prior_actions_lists:
                    # Since it may be an action or a list of actions we check
                    # and act acordingly.
                    if isinstance(prior_actions_list, list):
                        actions.append(prior_actions_list.append(action))
                    else:
                        actions.append(list((prior_actions_list, action)))

        return actions

    # TODO: Decide about separating this into two diferents functions:
    #           - Calculating the fitness from a dict
    #           - Operating with an action list
    def _fitnessFunction(self, action_list):
        """Receives a list of actions and returns the calculated fitness score.

        This method shall be overriden in the child classes to create different
        personalites.
        """
        fit = 0;
        for action in action_list:
            predictor = action.predict(self)
            max = self._attributesMax()
            for k in max:
                k_fit = predictor[k] - max[k]
                fit += copysign(pow(k_fit,2),k_fit)

        # As an action_list may comprise any number of items we ajust the
        # fitness score.
        fit /= len(action_list)
        return fit

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

    # TODO: Extend this so it may also receive an action as parameter. Useful
    #       for rule based systems implemented in the fitnessFunction
    #       - Decide if it isn't better to implement a method for rule based
    #         systems.
    def update(self):
        """Updates the attributes, manages the action_queue and executes the
        scheduled action. Returns nothing.
        """
        # First iterate through the attributes and update it's values using the
        # rules of each.
        for attr in self.attributes.values():
            attr.update()

        # If there is no actions in the queue, schedule new ones
        if len(self._action_queue) == 0:
            self._action_queue.extend(self._chooseAction())

        self._current_action = self._action_queue.popleft()
        self._current_action.execute(self)

    def printStatus(self):
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
