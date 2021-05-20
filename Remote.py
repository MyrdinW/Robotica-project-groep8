class Remote:
    def __init__(self):
        self.autonomous_on = False
        self.gripper_on = False
        self.movements = [0, 0, 0, 0]

    def get_joy_positions(self):
        return self.movements

    def get_gripper_on(self):
        return self.gripper_on

    def get_autonomous_on(self):
        return self.autonomous_on

    def moved(self):
        for movement in self.movements:
            if movement != 0:
                return True
        return False

    def update(self):
        # update values
        pass
