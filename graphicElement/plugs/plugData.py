
class plugData:
    _name: str = ""
    connectedWith: 'plugInterface'

    def __init__(self, index, name, value, parentNode, plugInterface):
        self.index = index
        self.plugInterface = plugInterface
        self._name = name
        self.resetValue = value
        self.value = value
        self.parentNode = parentNode
        self.connectedWith = None

    @property
    def name(self):
        return f"{self._name}_{self.index}"

    @name.setter
    def name(self, _name):
        self._name = _name

    def changeValue(self, value):
        self.value = value

    def update(self):
        self.value = self.connectedWith.value
