import json

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphicElement.nodes.AbstractNodeInterface import *
from graphicEngine.graphicViewOverride import graphicViewOverride
from graphicEngine.graphicsSceneOverride import graphicSceneOverride

"""
La classe canvas contiene una serie di metodi che inizializzano l'interfaccia utente, gestiscono il menu 
contestuale, aggiungono i nodi alla scena, salva e carica la scena e altre attività.

Il metodo init viene chiamato quando viene creata un'istanza della classe canvas e si occupa di inizializzare 
l'interfaccia utente chiamando il metodo initUI e di inizializzare alcune variabili d'istanza.

Il metodo initUI crea la scena grafica e la visuale grafica, imposta il widget graphicView come widget centrale del 
layout principale e imposta le dimensioni e il titolo della finestra.

Il metodo contextMenuEvent gestisce il menu contestuale che viene visualizzato quando l'utente fa clic con il tasto 
destro del mouse sulla scena. Al momento permette di inserire i nodi nella scena nel punto della scena 
dove si clicca con il tasto destro.

Il metodo addNodeToTheScene aggiunge un nodo alla scena e lo posiziona nella posizione del mouse.

I metodi saveScene e serialize serializzano la scena e i nodi in essa contenuti in un formato che può essere salvato 
su disco e successivamente caricato
"""


class canvas(QWidget):
    mainLayout: QLayout
    graphicView: graphicViewOverride
    graphicScene: graphicSceneOverride
    filename = "untitled"
    sceneWidth = 5000
    sceneHeight = 5000
    name = "untitled"
    isDebugActive = False

    def __init__(self, parent=None):
        super(canvas, self).__init__(parent)

        self.nodesInTheScene = []
        self.nodeNames = []
        self.initUI()
        self.mainWin = parent

    def initUI(self):
        self.graphicScene = graphicSceneOverride()
        self.graphicView = graphicViewOverride(self.graphicScene)
        self.graphicView.canvas = self
        self.graphicScene.setGraphicScene(self.sceneWidth, self.sceneHeight)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.graphicView)

        self.setGeometry(200, 200, 1200, 800)
        self.setWindowTitle("BiggusPy")

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        contextMenu = QMenu(self)
        contextMenu.addSection("VariableNode")
        _stringNode = contextMenu.addAction("string node")
        _numberNode = contextMenu.addAction("number node")
        _listNode = contextMenu.addAction("list node")
        _dictNode = contextMenu.addAction("dictionary node")
        contextMenu.addSeparator()
        contextMenu.addSection("Math")
        _sumNode = contextMenu.addAction("sum Node")
        _productNode = contextMenu.addAction("product Node")
        _expNode = contextMenu.addAction("power Node")
        _divisionNode = contextMenu.addAction("Division Node")
        _remainderNode = contextMenu.addAction("Remainder Node")
        _printNode = contextMenu.addAction("print Node")
        contextMenu.addSeparator()
        contextMenu.addSection("String")
        _replaceNode = contextMenu.addAction("ReplaceNode Node")
        _concatNode = contextMenu.addAction("ConcatNode Node")
        contextMenu.addSeparator()

        _mousePosition = self.graphicView.mousePosition
        action = contextMenu.exec(self.mapToGlobal(event.pos()))
        node_interface = None
        if action == _numberNode:
            node_interface = AbstractNodeInterface("NumberNode", value=10, view=self.graphicView)
        elif action == _stringNode:
            node_interface = AbstractNodeInterface("StringNode", value="Hello World!", view=self.graphicView)
        elif action == _listNode:
            node_interface = AbstractNodeInterface("ListNode", value="Hello World!", view=self.graphicView)
        elif action == _dictNode:
            node_interface = AbstractNodeInterface("DictNode", value="", view=self.graphicView)
        elif action == _sumNode:
            node_interface = AbstractNodeInterface("SumNode", view=self.graphicView)
        elif action == _productNode:
            node_interface = AbstractNodeInterface("ProductNode", view=self.graphicView)
        elif action == _printNode:
            node_interface = AbstractNodeInterface("PrintNode", view=self.graphicView)
        else:
            pass
        if node_interface:
            self.addNodeToTheScene(node_interface, _mousePosition)

    def addNodeToTheScene(self, nodeInterface, mousePos):
        index = 0
        self.graphicScene.addItem(nodeInterface.nodeGraphic)
        nodeInterface.nodeGraphic.setPos(mousePos)

        for x in self.nodesInTheScene:
            if nodeInterface.title == x.title:
                index += 1
                nodeInterface.changeIndex(index)

        self.nodesInTheScene.append(nodeInterface)

    def saveScene(self):
        return self.serialize()

    def serialize(self):
        listOfDictionarySerialized = []
        for node in self.nodesInTheScene:
            listOfDictionarySerialized.append(node.serialize())

        dicts = OrderedDict([
            ('name', self.name),
            ('sceneWidth', self.sceneWidth),
            ('sceneHeight', self.sceneHeight),
            ('Nodes', listOfDictionarySerialized)])
        return json.dumps(dicts)

    def deserialize(self, serializedString):
        deserialized = json.loads(serializedString)
        self.name = deserialized['name']
        self.sceneWidth = deserialized['sceneWidth']
        self.sceneHeight = deserialized['sceneHeight']
        nodes = deserialized['Nodes']
        for node in nodes:
            self.deserializeNode(node)

    def deserializeNode(self, serializedJsonDictionary):
        deserialized = json.loads(serializedJsonDictionary)
        _name = deserialized["name"]
        _index = deserialized["index"]
        _type = deserialized["type"]
        _pos = deserialized["pos"]
        _inPlugsNumb = deserialized["inPlugsNumb"]
        _outPlugsNumb = deserialized["outPlugsNumb"]
        node = AbstractNodeInterface(_type, value=10, view=self.graphicView)
        pos = QPointF(float(_pos[0]), float(_pos[1]))
        self.addNodeToTheScene(node, pos)
