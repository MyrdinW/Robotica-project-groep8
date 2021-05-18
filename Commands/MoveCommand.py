from Commands.Command import Command
from Engine import Engine
from Servo import Servo


class MoveCommand(Command):

    def __init__(self, camera, jsx1, jsy1, jsx2, jsy2):
        self.engine = Engine()
        self.servo = Servo()
        self.camera = camera
        self.jsx1 = jsx1
        self.jsx2 = jsx2
        self.jsy1 = jsy1
        self.jsy2 = jsy2
        self.stop = False

    def excecute(self) -> None:
        if self.stop:
            return
        print(f"Move Command {self.jsx1} {self.jsy1} {self.jsx2} {self.jsy2}")

    def stop(self):
        self.stop = True

