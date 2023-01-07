from graphicElement.nodeData.pythonNodes.AbstractNodeData import *
from graphicElement.nodeGraphics.abstractNodeGraphics import AbstractGraphicNode
from graphicElement.nodeGraphics.plug import Plug
from graphicElement.nodeGraphics.Connection import *
import importlib

"""
La classe AbstractNodeInterface é una sorta di "ponte" tra la parte grafica 
e quella di dati di un nodo. Ha una proprietà nodeData di tipo AbstractNodeData 
che rappresenta il nodo di dati, e una proprietà nodeGraphic di tipo AbstractGraphicNode 
che rappresenta il nodo grafico.

La classe AbstractNodeData, d'altra parte, é la classe base per tutti i nodi di dati. 
Ha proprietà inPlugs e outPlugs, che sono liste di oggetti di tipo AbstractPlug, 
e metodi per gestire le connessioni tra i nodi.

La classe AbstractGraphicNode, infine, è la classe base per tutti i nodi grafici. 
Ha una proprietà nodeData di tipo AbstractNodeData che rappresenta il nodo di dati associato, 
e metodi per gestire l'interfaccia grafica del nodo.

Il metodo addNodeToTheScene della classe canvas viene chiamato quando viene creato un nuovo nodo. 
Crea un'istanza di AbstractNodeInterface, imposta la posizione del nodo grafico e lo aggiunge 
alla scena grafica. Inoltre, aggiunge l'istanza di AbstractNodeInterface alla lista nodesInTheScene.

"""


class AbstractNodeInterface:
    nodeGraphic: AbstractGraphicNode
    nodeData: AbstractNodeData
    hasConnection = False

    def __init__(self, className: str, *args, view, **kwargs):

        # Crea l'istanza del nodoData
        self.nodeData = self.createNode(className, *args, **kwargs)
        self.nodeData.interface = self
        # Crea l'istanza del nodoGrafico
        self.nodeGraphic = AbstractGraphicNode(view, self)
        self.nodeGraphic.nodeData = self.nodeData
        self.nodeGraphic.nodeInterface = self
        if 'value' in kwargs:
            self.nodeGraphic.setValue(kwargs['value'])
        self.createPlug()

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
        module = importlib.import_module("graphicElement.nodeData.pythonNodes.AbstractNodeData")
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
        for plug in self.nodeGraphic.graphicInputPlugs:
            if plug.connection is not None:
                plug.connection.deleteConnection()
            else:
                print("no connection")
        for plug in self.nodeGraphic.graphicOutputPlugs:
            if plug.connection is not None:
                plug.connection.deleteConnection()
