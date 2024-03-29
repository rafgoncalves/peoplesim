from random import normalvariate

class Action:
    def __init__(self):
        self.name = self.__class__.__name__

    def getEffects(self):
        return {}

    def execute(self, actor):
        effects = self.getEffects()
        for e in self.getEffects():
            if e in actor.attributes:
                actor.attributes[e].value += effects[e]
            else:
                raise NameError(''.join(("The attribute ", e, " doesn't exist.")))

    def predict(self, actor):
        predictor = {}
        effects = self.getEffects()
        for attr in actor.attributes:
            predictor[attr] = actor.attributes[attr].value
            if attr in effects:
                predictor[attr] += effects[attr]
        return predictor

class Sleep(Action):
    def getEffects(self):
        return {
                "energy": normalvariate(10,2),
                "social": normalvariate(-5,2),
                "culture": normalvariate(2,1)
               }

class CallFriend(Action):
    def getEffects(self):
        return {
                "energy": normalvariate(-5,1),
                "social": normalvariate(12,2),
                "culture": normalvariate(4,1)
               }

class Study(Action):
    def getEffects(self):
        return {
                "energy": normalvariate(-10,3),
                "social": normalvariate(5,5),
                "culture": normalvariate(15,5)
               }
