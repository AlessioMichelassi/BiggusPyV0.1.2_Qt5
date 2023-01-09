
class plugData:
    name: str = ""
    connectedWith: 'plugInterface'

    def __init__(self, index, name, value, parentNode):
        self.index = index
        self.name += f"{name}{index}"
        self.resetValue = value
        self.value = value
        self.parentNode = parentNode
        self.connectedWith = None

    def changeValue(self, value):
        self.value = value

    def update(self):
        self.value = self.connectedWith.value
