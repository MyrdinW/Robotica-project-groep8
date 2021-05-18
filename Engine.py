class Engine:
    def __init__(self):
        self.offset = 0
        self.value = 0

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_offset(self, offset):
        self.offset = offset

    def get_offset(self):
        return self.offset