#TODO: Implement cross reference so if we add an object to a room, the object
#      knows where it's.
#TODO: Implement multiple ticks actions. (Partialy done)
#TODO: Implement the GRID object for rooms.
#TODO: Implement Events concept (something that trigers methods like actor.die())

# This is a sandbox implementation, please avoid asking about comments. :)

# Imports the library content
from peoplesim.actions import *
from peoplesim.actors import *
from peoplesim.buildings import *
from peoplesim.common import *
from peoplesim.events import *
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

    Alice = Actor("Alice")
    Phone = Phone()
    ClassBook = ClassBook()

    Lounge = Room("Lounge")
    Lounge.addActor(Bob)
    Lounge.addActor(Alice)
    Lounge.addObject(Phone)
    Lounge.addObject(ClassBook)

    for tick in range(0,100):
        print("------------------")
        print(''.join(("ROUND #: ", str(tick))));
        Bob.update()
        Alice.update()
        Bob.printStatus()
        Alice.printStatus()