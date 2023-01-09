from graphicElement.plugs.plugGraphic import plugGraphic
from graphicElement.plugs.plugData import plugData


class plugInterface:
    plugGraphic: plugGraphic

    def __init__(self, name, index, nodeData: 'AbstractNodeData', diameter=8):
        self.nodeInterface = nodeData.interface
        self.nodeData = nodeData
        self.plugData = plugData(index, name, 0, self.nodeInterface, self)

        self.plugGraphic = None
        self.connection = None

    @property
    def name(self):
        return self.plugData.name

    @name.setter
    def name(self, _name):
        self.plugData.name = _name

    @property
    def resetValue(self):
        return self.plugData.resetValue

    @property
    def value(self):
        return self.plugData.value

    @value.setter
    def value(self, _value):
        self.plugData.value = _value

    @property
    def connectedWith(self):
        return self.plugData.connectedWith

    @connectedWith.setter
    def connectedWith(self, plug):
        self.plugData.connectedWith = plug

    def disconnect(self):
        self.connection = None
        self.plugData.connectedWith = None
        self.plugData.value = self.resetValue

    def createPlug(self, _type: str, graphicNode):
        self.plugGraphic = plugGraphic(self, parent=graphicNode)
        return self.plugGraphic
