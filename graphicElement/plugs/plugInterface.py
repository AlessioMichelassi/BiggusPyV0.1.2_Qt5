from graphicElement.plugs.plugGraphic import plugGraphic
from graphicElement.plugs.plugData import plugData


class plugInterface:
    plugGraphic: plugGraphic

    def __init__(self, name, index, nodeData: 'AbstractNodeData', diameter=8):
        self.nodeInterface = nodeData.interface
        self.nodeData = nodeData
        self.name = name
        self.plugData = plugData(index, name, 0, self.nodeInterface)
        self.plugGraphic = None

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
        self.connectedWith = None
        self.plugData.value = self.resetValue

    def createPlug(self, _type: str, index: int, graphicNode, diameter =8):

        if _type in {"in", "In", "IN"}:
            self.plugGraphic = plugGraphic(f"In_{index}", diameter, graphicNode, self)
        elif _type in {"out", "Out", "OUT"}:
            self.plugGraphic = plugGraphic(f"Out_{index}", diameter, graphicNode, self)

        return self.plugGraphic
