from Commands.Command import Command
from Engine import Engine
from Servo import Servo


class MoveGripperCommand(Command):
    def __init__(self, jsx1, jsy1, jsx2, jsy2):
        self.engine = Engine()
        self.servo = Servo()
        self.stop = False
        self.jsx1 = jsx1
        self.jsx2 = jsx2
        self.jsy1 = jsy1
        self.jsy2 = jsy2

    def excecute(self) -> None:
        if self.stop:
            return
        print("Move Gripper Command")

    def stop(self):
        self.stop = True
