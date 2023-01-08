from graphicElement.nodes.pythonNodes.pythonNodeData import *
from graphicElement.nodes.AbstractNodeGraphics import AbstractNodeGraphic
import importlib


class Observer:
    def __init__(self):
        self.observedNodesList = []

    def addObservedNode(self, node):
        self.observedNodesList.append(node)
        node.addObserver(self)

    def update(self):
        print("observer in action")
        for observed_node in self.observedNodesList:
            observed_node.calculate()


class AbstractNodeInterface:
    nodeGraphic: AbstractNodeGraphic
    nodeData: AbstractNodeData
    hasConnection = False

    def __init__(self, className: str, *args, view, **kwargs):

        # Crea l'istanza del nodoData
        self.nodeData = self.createNode(className, *args, **kwargs)
        self.nodeData.interface = self
        # Crea l'istanza del nodoGrafico
        self.nodeGraphic = AbstractNodeGraphic(view, self)
        self.nodeGraphic.nodeData = self.nodeData
        self.nodeGraphic.nodeInterface = self
        if 'value' in kwargs:
            self.nodeGraphic.setValueFromGraphics(kwargs['value'])
        self.createPlug()
        self.observers = []

    @property
    def title(self):
        return str(self.nodeData.title)

    @title.setter
    def title(self, _name):
        self.nodeGraphic.setTitle(self.nodeData.title)

    def changeIndex(self, _index):
        self.nodeData.index = _index
        self.nodeGraphic.setTitle(self.nodeData.title)

    def createPlug(self):
        numInputs = self.nodeData.numberOfInputPlugs
        self.nodeGraphic.createPlugsIn(numInputs)

        numOutputs = self.nodeData.numberOfOutputPlugs
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
        module = importlib.import_module("graphicElement.nodes.pythonNodes.pythonNodeData")
        node_class = getattr(module, className)
        return node_class(*args, **kwargs)

    def connectPlug(self, startNode: AbstractNodeData, startPlug, endNode: AbstractNodeData, endPlug):
        startNode.connect(endNode, endPlug.index, startPlug.index)

        # print(f"debug print from connect inputIndex is {startPlug.index} outputIndex is {endPlug.index}")

    def disconnectPlug(self, _startNode, startPlug, _endNode, endPlug):
        # sourcery skip: assign-if-exp
        startNode = _startNode
        endNode = _endNode
        if type(_startNode) is AbstractNodeInterface or type(_startNode) is AbstractNodeGraphic:
            startNode = _startNode.nodeData
        if type(_endNode) is AbstractNodeInterface or type(_endNode) is AbstractNodeGraphic:
            endNode = _endNode.nodeData

        startNode.disconnect(endNode, startPlug.index, endPlug.index)
        if startNode.hasAValue:
            value = startNode.txtValue
        else:
            value = None
        self.nodeGraphic.setValueFromGraphics(value)

    def deleteNode(self):
        for plug in self.nodeGraphic.graphicInputPlugs:
            if plug.connection is not None:
                plug.connection.deleteConnection()
            else:
                print("no connections")
        for plug in self.nodeGraphic.graphicOutputPlugs:
            if plug.connection is not None:
                plug.connection.deleteConnection()

    def addObserver(self, node):
        observer = Observer()
        observer.addObservedNode(node)
        self.observers.append(observer)

    def notifyToObserver(self):
        for observer in self.observers:
            observer.update()
