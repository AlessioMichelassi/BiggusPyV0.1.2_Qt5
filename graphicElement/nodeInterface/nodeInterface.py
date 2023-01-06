from graphicElement.nodeData.pythonNodes.nodeTypes import *
from graphicElement.nodeGraphics.abstractNodeGraphics import AbstractGraphicNode
import importlib


class AbstractNodeInterface:
    nodeGraphic: AbstractGraphicNode
    nodeData: AbstractNodeData
    hasConnection = False
    nodeCounter = 0

    def __init__(self, className: str, *args, view, **kwargs):
        # Crea l'istanza del nodoData
        self.nodeData = self.createNode(className, *args, **kwargs)
        self.nodeData.interface = self
        self.nodeData.name = className
        # Crea l'istanza del nodoGrafico
        self.nodeGraphic = AbstractGraphicNode(view, self)
        self.nodeGraphic.nodeData = self.nodeData
        if 'value' in kwargs:
            self.nodeGraphic.setValue(kwargs['value'])
        self.createPlug()

    @property
    def title(self):
        return self.nodeData.title

    @title.setter
    def title(self, _name=None):
        self.nodeData.name = _name
        self.nodeGraphic.setTitle(self.nodeData.title)

    def changeIndex(self, _index):
        self.nodeData = _index

    def createPlug(self):
        if self.nodeData.inPlugs is not None:
            numInputs = len(self.nodeData.inPlugs)
            self.nodeGraphic.createPlugsIn(numInputs)
        if self.nodeData.outPlugs is not None:
            numOutputs = len(self.nodeData.outPlugs)
            self.nodeGraphic.createPlugsOut(numOutputs)

    @staticmethod
    def createNode(className: str, *args, **kwargs) -> AbstractNodeData:
        """
        Carica dinamicamente il modulo che contiene la classe del nodo
        Crea un'istanza della classe del nodo passando eventuali argomenti e keyword arguments
        Crea un'istanza della classe del nodo passando eventuali argomenti e keyword arguments
        :param className: il nome della classe del nodeTypes ad Es: SumNode o ProductNode
        :param args:
        :param kwargs:
        :return:
        """
        module = importlib.import_module("graphicElement.nodeData.pythonNodes.nodeTypes")
        node_class = getattr(module, className)
        return node_class(*args, **kwargs)

    def connectPlug(self, startNode: AbstractNodeData, startPlug, endNode: AbstractNodeData, endPlug):
        startNode.connect(endNode, endPlug.index, startPlug.index)

        print(f"debug print from connect inputIndex is {startPlug.index} outputIndex is {endPlug.index}")

    def disconnectPlug(self, _startNode, startPlug, _endNode, endPlug):
        # sourcery skip: assign-if-exp
        startNode = _startNode
        endNode = _endNode
        if type(_startNode) is AbstractNodeInterface or type(_startNode) is AbstractGraphicNode:
            startNode = _startNode.nodeData
        if type(_endNode) is AbstractNodeInterface or type(_endNode) is AbstractGraphicNode:
            endNode = _endNode.nodeData

        startNode.disconnect(endNode, startPlug.index, endPlug.index)
        if startNode.hasAValue:
            value = startNode.txtValue
        else:
            value = None
        self.nodeGraphic.setValue(value)

    def deleteNode(self):
        for plug in self.nodeGraphic.inputPlugs:
            if plug.connection is not None:
                plug.connection.deleteConnection()
            else:
                print("no connection")
        for plug in self.nodeGraphic.outputPlugs:
            if plug.connection is not None:
                plug.connection.deleteConnection()
