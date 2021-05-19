from Commands.Command import Command
from Engine import Engine
from Servo import Servo


class PickupMaskCommand(Command):
    def __init__(self, camera):
        self.engine = Engine()
        self.servo = Servo()
        self.camera = camera
        self.stop = False

    def excecute(self) -> None:
        if self.stop:
            return
        print("Pickup Mask Command")

    def stop(self):
        self.stop = True