class Part:
    def __init__(self):
        self.is_on = False

    def switch(self):
        if self.is_on:
            self.is_on = False
        else:
            self.is_on = True
