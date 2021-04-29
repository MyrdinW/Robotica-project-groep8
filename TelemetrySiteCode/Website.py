import numpy as np


class Website:
    def __init__(self):
        self.motor_values = 0
        self.servo_values = 0
        self.servo_torques = 0
        size = (1920, 1080, 3)
        self.camera_view = np.zeros(size, dtype=np.uint8)

    def update_view(self, image):
        self.camera_view = image

    def update_values(self, motor_values, servo_values, torque_values):
        self.motor_values = motor_values
        self.servo_values = servo_values
        self.servo_torques = torque_values
