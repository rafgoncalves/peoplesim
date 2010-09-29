#TODO: Implement expected value based decisions.
#TODO: Implement cross reference so if we add an object to a room, the object
#      knows where it's.
#TODO: Implement the concept of event.
#TODO: Implement a "test" action that allows the actor to know the object.
#TODO: Get rid of introspection?
#TODO: Implement multiple ticks actions.
#TODO: Implement the rule based system for actors.
#TODO: Implement the GRID object for rooms.
#TODO: Implement TAGS for motivation
#TODO: Implement Facts concept (something that trigers methods like actor.die())

# This is a sandbox implementation, please avoid asking about comments. :)

from peoplesim.actions import *
from peoplesim.actors import *
from peoplesim.common import *
from peoplesim.objects import *
from peoplesim.rooms import *

# This will be executed if the script is directly run.

if __name__ == "__main__":
    """ Executes a demo run using the roleplay model.

    Initializes two default actors - Bob and Alice -, a Phone object, a
    ClassBook object and a Room object, namely the "Lounge". The script then
    adds the Actors and the Objects to the room.

    Finally, it iterates 20 ticks of time for both the actors, allowing then to
    predict and execute actions.

    """

    Bob = Actor("Bob")
    Bob.introspection = 2

    Alice = Actor("Alice")
    Phone = Phone()
    ClassBook = ClassBook()

    Lounge = Room("Lounge")
    Lounge.addActor(Bob)
    Lounge.addActor(Alice)
    Lounge.addObject(Phone)
    Lounge.addObject(ClassBook)

    for tick in range(0,20):
        print("------------------")
        print(''.join(("ROUND #: ", str(tick))));
        Bob.printStatus()
        Bob.update()

        Alice.printStatus()
        Alice.update()

if __name__ == "!__main__":
    Bob = Actor("Bob")
    Bob.introspection = 2
    Phone = Phone()

    Lounge = Room("Lounge")
    Lounge.addActor(Bob)
    Lounge.addObject(Phone)

    Bob.printStatus()
    Bob.update()

