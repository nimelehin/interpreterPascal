class Token():

    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({0}, {1})".format(self.type, self.value)
