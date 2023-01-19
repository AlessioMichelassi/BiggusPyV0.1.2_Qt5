import json
from collections import OrderedDict

from graphicElement.connections.Connection import Connection
from graphicElement.nodes.pythonNodes.pythonNodeData import *
from graphicElement.nodes.AbstractNodeGraphics import AbstractNodeGraphic
import importlib

from graphicEngine.graphicViewOverride import graphicViewOverride

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
        # print(f"updating from {self.mainNode.title}")
        for observed_node in self.observedNodesList:
            observed_node.nodeData.calculate()
            self.mainNode.nodeData.calculate()


class AbstractNodeInterface:
    nodeGraphic: AbstractNodeGraphic
    nodeData: AbstractNodeData
    observer: Observer
    lockPlug = False
    addFunctionStringAtEndOfCreation = None
    isTextTitleNeedToBeUpdate = False

    def __init__(self, className: str, *args, view: 'graphicViewOverride', **kwargs):

        # Crea l'istanza del nodoData
        self.type = className
        self.nodeData = self.createNode(className, *args, _interface=self, **kwargs)
        if isinstance(view, type('Canvas')):
            self.canvas = view
            self.graphicView = self.canvas.graphicView
        elif isinstance(view, graphicViewOverride):
            self.graphicView = view
            self.canvas = self.graphicView.canvas
        # Crea l'istanza del nodoGrafico
        self.nodeGraphic = AbstractNodeGraphic(self.graphicView, self)
        self.nodeGraphic.nodeData = self.nodeData
        self.nodeGraphic.nodeInterface = self
        self.createPlug()
        self.nodeData.isNodeInCreation = False
        if 'value' in kwargs:
            self.nodeGraphic.setValueFromGraphics(kwargs['value'])

        self.nodeData.redefineGraphics()
        if self.addFunctionStringAtEndOfCreation:
            if self.isTextTitleNeedToBeUpdate:
                self.isTextTitleNeedToBeUpdate = False
                self.updateTitleInNodeGraphic()
            self.nodeData.functionString = self.addFunctionStringAtEndOfCreation
        self.observer = Observer(self)

    @property
    def title(self):
        return str(self.nodeData.title)

    @title.setter
    def title(self, _name):
        self.nodeGraphic.setTitle(self.nodeData.title)

    def updateTitleInNodeGraphic(self):
        if self.nodeData.isNodeInCreation:
            self.isTextTitleNeedToBeUpdate = True
        else:
            self.nodeGraphic.setTitle(self.title)

    def changeIndex(self, _index):
        self.nodeData.index = _index
        self.nodeGraphic.setTitle(self.nodeData.title)

    def forceNodeNameOnLoad(self, name: str, index: int):
        self.nodeData.forceNodeNameOnLoad(name, index)

    def createPlug(self):
        numInputs = self.nodeData.numberOfInputPlugs
        self.nodeGraphic.createPlugsIn(numInputs)

        numOutputs = self.nodeData.numberOfOutputPlugs
        self.nodeGraphic.createPlugsOut(numOutputs)

    def addPlugs(self, inPlugNumber: int, outPlugNumber: int):
        if not self.lockPlug:
            self.addInPlug(inPlugNumber)
            self.addOutPlug(outPlugNumber)
            self.nodeGraphic.repositionThePlugForDefaultFigure()
            self.lockPlug = True

    def addInPlug(self, inPlugNumber):
        plugLeft = inPlugNumber - len(self.nodeData.dataInPlugs)
        if plugLeft > 0:
            inIndex = len(self.nodeData.dataInPlugs)
            for _ in range(plugLeft):
                # aggiunge il plugData
                self.nodeData.numberOfInputPlugs += 1
                plugIn = self.nodeData.addInPlug(inIndex)
                # aggiunge il plugGraphic
                plug = plugIn.createGraphicPlug("In", self.nodeGraphic)
                self.nodeGraphic.graphicInputPlugs.append(plug)
                inIndex += 1

    def addOutPlug(self, outPlugNumber):
        plugRight = outPlugNumber - len(self.nodeData.dataOutPlugs)
        if plugRight > 0:
            outIndex = len(self.nodeData.dataOutPlugs)
            for _ in range(plugRight):
                # aggiunge il plugData
                self.nodeData.numberOfOutputPlugs += 1
                plugOut = self.nodeData.addOutPlug(outIndex)
                # aggiunge il plugGraphic
                plug = plugOut.createGraphicPlug("Out", self.nodeGraphic)
                self.nodeGraphic.graphicOutputPlugs.append(plug)
                outIndex += 1

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
        try:
            node_class = getattr(module, className)
            return node_class(*args, interface=_interface, **kwargs)
        except Exception as e:
            print(e)

    def filterConnection(self, connection: Connection):

        outputNode = connection.outputNode
        print(f"debug from filter connection: self={self.title} {connection.outputNode.title} -> {connection.inputNode.title}")
        if type(outputNode) is AbstractNodeInterface:
            if outputNode.title != self.title:
                print("filtered")
                return False
        elif type(outputNode) is AbstractNodeData:
            if outputNode.title != self.title:
                print("filtered")
                return False
        else:
            print("notFiltered")
            return True

    def connectPlug(self, connectedNode: AbstractNodeData, connectedPlug, whichOutPlug, connection):
        if self.filterConnection(connection):
            if "Out" in whichOutPlug.name:

                if connection not in self.nodeData.outConnection:
                    print(f"appendecConnection in {self.title}: {connection.outputNode.title} -> {connection.inputNode.title}")
                    self.nodeData.outConnection.append(connection)
        else:
            self.nodeData.inConnection.append(connection)
        self.nodeData.dataOutPlugs[whichOutPlug.index].connectedWith = connectedPlug
        self.nodeData.dataOutPlugs[whichOutPlug.index].connection = connection
        connectedNode.changeInputValue(connectedPlug.index, whichOutPlug.plugData.value)
        self.nodeData.calculate()

    def disconnectPlug(self, connectedNode: AbstractNodeData, connectedPlug, whichOutPlug):
        pass

    def addObservedNode(self, node):
        self.observer.addObservedNode(node)

    def notifyToObserver(self):
        self.observer.update()

    def updateOutputText(self):
        self.nodeGraphic.updateTextValue()

    def serialize(self):
        connections = []
        for connection in self.nodeData.outConnection:
            connections.append(connection.serialize())

        dicts = OrderedDict([
            ('className', self.nodeData.className),
            ('name', self.nodeData.name),
            ('title', self.nodeData.title),
            ('index', self.nodeData.index),
            ('type', self.type),
            ('value', self.nodeData.value),
            ('functionString', self.nodeData.functionString),
            ('pos', (self.nodeGraphic.pos().x(), self.nodeGraphic.pos().y())),
            ('inPlugsNumb', self.nodeData.numberOfInputPlugs),
            ('outPlugsNumb', self.nodeData.numberOfOutputPlugs),
            ('connections', connections)
        ])
        print(dicts)
        return json.dumps(dicts, indent=4)
