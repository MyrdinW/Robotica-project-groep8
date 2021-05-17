from Part import Part


class Light(Part):
    def __init__(self):
        super().__init__()
        self.value = 0

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value
