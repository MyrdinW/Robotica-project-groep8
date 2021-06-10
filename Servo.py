from pyax12.connection import Connection

class Servo:
    def __init__(self):
        try:
            self.torque = 0
            self.value = 0
            self.serial_connection = Connection(port="/dev/ttyAMA0", rpi_gpio=True)
            self.dynamixel_id = 3

            # Ping the third dynamixel unit
            self.is_available = serial_connection.ping(dynamixel_id)
        except:
            print("Servo not working yet")
    def move(self):
        # Go to -45° (45° CW)
        self.serial_connection.goto(dynamixel_id, -45, speed=512, degrees=True)
        time.sleep(1)    # Wait 1 second
    
    def set_value(self, value):
        """
        Args:
            value:
        """
        self.value = value

    def get_value(self):
        return self.value

    def set_torque(self, torque):
        """
        Args:
            torque:
        """
        self.torque = torque

    def get_torque(self):
        return self.torque
