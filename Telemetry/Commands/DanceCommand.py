from Commands.Command import Command
from Engine import Engine
from Servo import Servo


class DanceCommand(Command):

    def __init__(self):
        self.engine = Engine()
        self.servo = Servo()
        self.stop = False

    def excecute(self) -> None:
        if self.stop:
            return
        print("Dance Command")

    def stop(self):
        self.stop = True
