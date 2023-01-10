from graphicElement.plugs.PlugGraphic import PlugGraphic


class PlugData:
    _name: str = ""
    connectedWith: 'PlugData'
    _connection: 'Connection' = None
    plugGraphic: PlugGraphic

    def __init__(self, index, name, value, parentNode):
        self.index = index
        self._name = name
        self._resetValue = value
        self.value = value
        self.parentNode = parentNode
        self.connectedWith = None

    @property
    def name(self):
        return f"{self._name}_{self.index}"

    @name.setter
    def name(self, _name):
        self._name = _name

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, connection: 'Connection'):
        self._connection = connection

    def changeValue(self, value):
        self.value = value

    def update(self):
        self.value = self.connectedWith.value

    def resetValue(self):
        self._connection = None
        self.connectedWith = None
        self.value = self._resetValue
        self.parentNode.calculate()

    def createGraphicPlug(self, _type: str, graphicNode):
        self.plugGraphic = PlugGraphic(self, parent=graphicNode)
        return self.plugGraphic
