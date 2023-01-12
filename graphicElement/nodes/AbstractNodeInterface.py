import json
from collections import OrderedDict

from graphicElement.nodes.pythonNodes.pythonNodeData import *
from graphicElement.nodes.AbstractNodeGraphics import AbstractNodeGraphic
import importlib

"""
La classe AbstractNodeInterface rappresenta l'interfaccia di un nodo di un grafico a nodi.

La classe contiene un'istanza della classe AbstractNodeData, che rappresenta i dati del nodo, e un'istanza della 
classe AbstractNodeGraphic, che rappresenta l'aspetto grafico del nodo.

La classe implementa i seguenti metodi:

    __init__(self, className: str, *args, view, **kwargs): 
                questo metodo viene chiamato per creare un'istanza della classe. Prende in input 
                il nome della classe del nodo, eventuali argomenti e keyword arguments, 
                e una vista (che  rappresenta la finestra in cui verrà visualizzato il nodo). 
                Crea l'istanza del nodo grafico e dei dati del nodo, e chiama il metodo createPlug() 
                per creare i plugs del nodo. 

    createPlug(self): 
                questo metodo viene chiamato per creare i plugs del nodo. Prende in input il numero 
                di plugs di input e di output del nodo e crea gli oggetti grafici che rappresentano i plugs.

    createNode(className: str, *args, _interface, **kwargs) -> AbstractNodeData:  
                questo metodo viene chiamato per creare un'istanza della classe dei dati del nodo. 
                Prende in input il nome della classe del nodo e eventuali argomenti e keyword arguments. 
                Carica dinamicamente il modulo che contiene la classe del nodo e crea un'istanza della classe 
                passando l'interfaccia del nodo come argomento.

    connectPlug(self, startNode: AbstractNodeData, startPlug, endNode: AbstractNodeData, endPlug): 

                questo metodo viene chiamato per connettere i plugs di due nodi. Prende in input i dati 
                dei nodi e i plugs da connettere e chiama il metodo connect() dell'oggetto startNode 
                passando i dati del nodo di destinazione e gli indici dei plugs da connettere. Aggiorna poi 
                gli oggetti connectedWith dei plugs con l'oggetto plugInterface dell'altro plug. 

    disconnectPlug(self, _startNode, startPlug, _endNode, endPlug): 

                questo metodo viene chiamato per scollegare i plugs di due nodi. Prende in input i dati dei nodi 
                e i plugs da scollegare e chiama il metodo disconnect() dell'oggetto nodeData del nodo di partenza 
                (startNode) passando come argomenti l'oggetto nodeData del nodo di arrivo (endNode) e 
                gli indici dei plugs da scollegare (startPlug.index e endPlug.index). 
                Inoltre, imposta il valore di connectedWith di entrambi i plugs scollegati a None. 
                Infine, imposta il valore del nodo di partenza a resetValue e chiama il metodo 
                setValueFromGraphics() del nodo grafico per impostare questo valore nel nodo grafico.

    addObserver(self, observer: Observer): 

                questo metodo viene chiamato per aggiungere un osservatore a un nodo. 
                Prende in input l'oggetto observer e lo aggiunge alla lista degli osservatori 
                del nodo (self.observers). Inoltre, chiama il metodo addObservedNode() dell'oggetto 
                observer passando come argomento il nodo stesso (self).

    notifyToObserver(self): 

                questo metodo viene chiamato quando il valore di un nodo cambia e gli osservatori 
                devono essere notificati. Itera sulla lista degli osservatori del nodo (self.observers) 
                e chiama il metodo update() di ognuno di essi.

    removeObserver(self, observer: Observer): 

                questo metodo viene chiamato per rimuovere un osservatore da un nodo. 
                Prende in input l'oggetto observer e lo rimuove dalla lista degli osservatori 
                del nodo (self.observers). Inoltre, chiama il metodo removeObservedNode() dell'oggetto 
                observer passando come argomento il nodo corrente, in modo che l'osservatore 
                non tenga più traccia del nodo.

    serialize(self): 
                questo metodo viene utilizzato per serializzare il nodo, 
                ovvero convertirlo in una stringa di testo che può essere salvata su un file 
                o inviata su una rete. Restituisce una stringa in formato JSON che rappresenta 
                il nodo e i suoi dati.

    deserialize(cls, data: str, graphicView): 

                questo metodo statico viene utilizzato per deserializzare un nodo, 
                ovvero ricostruirlo a partire da una stringa di testo. 
                Prende in input la stringa di dati serializzati del nodo e il riferimento 
                alla graphicView a cui appartiene il nodo e restituisce un'istanza del nodo deserializzato.

                """


class Observer:
    observedNodesList = []

    def __init__(self, node: 'AbstractNodeInterface'):
        self.mainNode = node

    def addObservedNode(self, node):
        # print(f"added node to observer: {node.title}")
        self.observedNodesList.append(node)

    def update(self):
        print(f"updating from {self.mainNode.title}")
        for observed_node in self.observedNodesList:
            observed_node.nodeData.calculate()
            self.mainNode.nodeData.calculate()


class AbstractNodeInterface:
    nodeGraphic: AbstractNodeGraphic
    nodeData: AbstractNodeData
    observer: Observer

    def __init__(self, className: str, *args, view, **kwargs):

        # Crea l'istanza del nodoData
        self.type = className
        self.nodeData = self.createNode(className, *args, _interface=self, **kwargs)
        self.graphicView = view
        # Crea l'istanza del nodoGrafico
        self.nodeGraphic = AbstractNodeGraphic(view, self)
        self.nodeGraphic.nodeData = self.nodeData
        self.nodeGraphic.nodeInterface = self
        self.createPlug()
        if 'value' in kwargs:
            self.nodeGraphic.setValueFromGraphics(kwargs['value'])

        self.nodeData.redefineGraphics()
        self.observer = Observer(self)

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
    def createNode(className: str, *args, _interface, **kwargs) -> AbstractNodeData:
        """
        Carica dinamicamente il modulo che contiene la classe del nodo
        Crea un'istanza della classe del nodo passando eventuali argomenti e keyword arguments
        Crea un'istanza della classe del nodo passando eventuali argomenti e keyword arguments
        :param _interface:
        :param className: il nome della classe del nodeTypes ad Es: SumNode o ProductNode
        :param args:
        :param kwargs:
        :return:
        """
        module = importlib.import_module("graphicElement.nodes.pythonNodes.pythonNodeData")
        node_class = getattr(module, className)
        return node_class(*args, interface=_interface, **kwargs)

    def connectPlug(self, startNode: AbstractNodeData, startPlug, endNode: AbstractNodeData, endPlug, connection):

        value = self.nodeData.dataOutPlugs[0].value
        endNode.changeInputValue(startPlug.plugData.index, value)

        startNode.dataInPlugs[startPlug.index].connectedWith = self.nodeData.dataOutPlugs[0]
        self.nodeData.dataOutPlugs[0].connectedWith = startNode.dataInPlugs[startPlug.index]
        self.nodeData.dataOutPlugs[0].connection = connection

        self.nodeData.connection.append(connection)
        self.addObservedNode(endNode.nodeInterface)
        self.nodeData.calculate()

    def disconnectPlug(self, _startNode, startPlug, _endNode, endPlug):
        # sourcery skip: assign-if-exp
        startNode = _startNode
        endNode = _endNode
        if type(_startNode) is AbstractNodeInterface or type(_startNode) is AbstractNodeGraphic:
            startNode = _startNode.nodeData
        if type(_endNode) is AbstractNodeInterface or type(_endNode) is AbstractNodeGraphic:
            endNode = _endNode.nodeData

        startNode.disconnect(endNode, startPlug.index, endPlug.index)
        value = startNode.resetValue
        self.nodeGraphic.setValueFromGraphics(value)

    def addObservedNode(self, node):
        self.observer.addObservedNode(node)

    def notifyToObserver(self):
        self.observer.update()

    def updateOutputText(self):
        self.nodeGraphic.updateTextValue()

    def serialize(self):
        dicts = OrderedDict([
            ('name', self.nodeData.name),
            ('index', self.nodeData.index),
            ('type', self.type),
            ('pos', (self.nodeGraphic.pos().x(), self.nodeGraphic.pos().y())),
            ('inPlugsNumb', self.nodeData.numberOfInputPlugs),
            ('outPlugsNumb', self.nodeData.numberOfOutputPlugs)
        ])
        return json.dumps(dicts)
