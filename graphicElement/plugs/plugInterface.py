from graphicElement.plugs.plugGraphic import plugGraphic


class plugData:
    name: str = ""

    def __init__(self, index, name, value, parentNode):
        self.index = index
        self.name += f"{name}{index}"
        self.value = value
        self.connectedPlug = None
        self.parentNode = parentNode

    def changeValue(self, value):
        self.value = value

    def update(self):
        self.value = self.connectedPlug.value


class plugInterface:

    def __init__(self, name, index, nodeData: 'AbstractNodeData', diameter=8):
        self.nodeInterface = nodeData.interface
        self.nodeData = nodeData
        print(type(self.nodeInterface))
        self.name = name
        self.plugData = plugData(index, name, 0, self.nodeInterface)
        self.plugGraphic = []

    @property
    def value(self):
        return self.plugData.value

    @value.setter
    def value(self, _value):
        self.plugData.value = _value
