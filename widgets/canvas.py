import ast
import json
import random

from PyQt5 import Qt
from PyQt5.QtCore import QPointF, QPoint
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphicElement.connections.Connection import Connection
from graphicElement.nodes.AbstractNodeInterface import *
from graphicEngine.graphicViewOverride import graphicViewOverride
from graphicEngine.graphicsSceneOverride import graphicSceneOverride
from widgets.codeToGraph import CodeToGraph

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


class Canvas(QWidget):
    node_name_list = ["NumberNode", "StringNode", "ListNode", "DictNode", "SumNode",
                      "ProductNode", "PowerNode", "DivisionNode", "RemainderNode",
                      "PrintNode", "ReplaceNode", "ConcatNode", "IfNode", "ForNode",
                      "FunctionNode", "CallNode", "VariableNode"]
    mainLayout: QLayout
    graphicView: graphicViewOverride
    graphicScene: graphicSceneOverride
    _filename = "untitled"
    sceneWidth = 5000
    sceneHeight = 5000
    isDebugActive = False

    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)

        self.nodesInTheScene = []
        self.connections = []
        self.nodeNames = []
        self.initUI()
        self.mainWin = parent

    @property
    def fileName(self):
        return self._filename

    @fileName.setter
    def fileName(self, fileName):
        self._filename = fileName
        self.mainWin.setWindowTitle(f"BiggusPyV0.1.2 - {fileName}")

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
        elif action == _expNode:
            node_interface = AbstractNodeInterface("ExpNode", view=self.graphicView)
        elif action == _divisionNode:
            node_interface = AbstractNodeInterface("DivisionNode", view=self.graphicView)
        elif action == _remainderNode:
            node_interface = AbstractNodeInterface("RemainderNode", view=self.graphicView)
        elif action == _replaceNode:
            node_interface = AbstractNodeInterface("ReplaceNode", view=self.graphicView)
        elif action == _concatNode:
            node_interface = AbstractNodeInterface("ConcatNode", view=self.graphicView)
        else:
            pass
        if node_interface:
            self.addNodeToTheScene(node_interface, _mousePosition)

    def createNodeFromDialog(self, nodeName, centerPoint, x=None, string=None):
        if x is None or x == "":
            x = random.randint(1, 100)
        try:
            if "Number" in nodeName:
                node = AbstractNodeInterface(nodeName, value=x, view=self.graphicView)
            elif "DictNode" in nodeName:
                node = AbstractNodeInterface(nodeName, value="", view=self.graphicView)
            elif "CallNode" in nodeName:
                node = AbstractNodeInterface(nodeName, name=nodeName, view=self.graphicView)
            elif "VariableNode" in nodeName:
                node = AbstractNodeInterface(nodeName, value=x, name=nodeName, view=self.graphicView)
            elif "Function" in nodeName:
                node = AbstractNodeInterface(nodeName, function=string, view=self.graphicView)
            else:
                node = AbstractNodeInterface(nodeName, view=self.graphicView)

            self.addNodeToTheScene(node, centerPoint)
            return node
        except Exception as e:
            print(f"{nodeName} not in list")

    def addNodeToTheScene(self, nodeInterface, mousePos):
        index = 0
        self.graphicScene.addItem(nodeInterface.nodeGraphic)
        nodeInterface.nodeGraphic.setPos(mousePos)

        for x in self.nodesInTheScene:
            if nodeInterface.title == x.title:
                index += 1
                nodeInterface.changeIndex(index)

        self.nodesInTheScene.append(nodeInterface)

    def createNodeFromCode(self, code: str):
        # parse the code into an AST
        parsed_code = ast.parse(code)

        # define a variable to keep track of the nodes
        nodes = []

        # iterate over the AST and create nodes for each statement
        for node in ast.walk(parsed_code):
            if isinstance(node, ast.FunctionDef):
                # _function_node = FunctionNode(node.name, None)
                _node = AbstractNodeInterface(node.name, view=self.graphicView)
                if _node is not None:
                    nodes.append(_node)
            elif isinstance(node, ast.For):
                # _for_node = ForNode(None)
                _node = AbstractNodeInterface("ForNode", view=self.graphicView)
                if _node is not None:
                    nodes.append(_node)
            elif isinstance(node, ast.If):
                _node = AbstractNodeInterface("IfNode", view=self.graphicView)
                if _node is not None:
                    nodes.append(_node)
            elif isinstance(node, ast.Call):
                try:
                    if isinstance(node.func, ast.Name):
                        # call_node = CallNode(node.func.id, None)
                        _node = AbstractNodeInterface("CallNode", value=node.func.id, view=self.graphicView)
                    elif isinstance(node.func, ast.Attribute):
                        # call_node = CallNode(node.func.attr, None)
                        _node = AbstractNodeInterface("CallNode", value=node.func.attr, view=self.graphicView)
                    if _node is not None:
                        nodes.append(_node)
                except Exception as e:
                    print("*" * 20)
                    print(e)
                    print("*" * 20)
            elif isinstance(node, ast.Name):
                # _variable_node = VariableNode(node.id, None, None)
                _node = AbstractNodeInterface(node.id, view=self.graphicView)
                if _node is not None:
                    nodes.append(_node)
            elif isinstance(node, ast.Num):
                # number_node = NumberNode(node.n, None)
                _node = AbstractNodeInterface(node.n, view=self.graphicView)
                if _node is not None:
                    nodes.append(_node)
        return nodes

    def pasteCode(self, code):
        if type(code) is json:
            print("json code find")
        else:
            parser = CodeToGraph(self)
            parser.parseCode(code)
            #nodes = parser.create_graph()
            #print(nodes)

    def newScene(self):
        self.graphicScene.clear()
        self.fileName = "untitled"

    def saveScene(self):
        return self.serialize()

    def saveAsScene(self):
        return self.serialize()

    def serialize(self):
        listOfDictionarySerialized = []
        for node in self.nodesInTheScene:
            listOfDictionarySerialized.append(node.serialize())

        dicts = OrderedDict([
            ('name', self.fileName),
            ('sceneWidth', self.sceneWidth),
            ('sceneHeight', self.sceneHeight),
            ('Nodes', listOfDictionarySerialized)])
        return json.dumps(dicts)

    def deserialize(self, serializedString):
        deserialized = json.loads(serializedString)
        self.fileName = deserialized['name']
        self.sceneWidth = deserialized['sceneWidth']
        self.sceneHeight = deserialized['sceneHeight']
        nodes = deserialized['Nodes']
        for node in nodes:
            self.deserializeNode(node)
        for node in nodes:
            self.deserializeConnections(node)

    def deserializeNode(self, serializedJsonDictionary):
        deserialized = json.loads(serializedJsonDictionary)
        _name = deserialized["name"]
        _index = deserialized["index"]
        _type = deserialized["type"]
        _value = deserialized["value"]
        _string = deserialized["functionString"]
        _pos = deserialized["pos"]
        _inPlugsNumb = deserialized["inPlugsNumb"]
        _outPlugsNumb = deserialized["outPlugsNumb"]
        pos = QPointF(float(_pos[0]), float(_pos[1]))
        node = self.createNodeFromDialog(_type, pos, _value, _string)
        node.forceNodeNameOnLoad(_name, _index)

    def deserializeConnections(self, serializedJsonDictionary):
        deserialized = json.loads(serializedJsonDictionary)
        connections = deserialized["connections"]
        nodeName = deserialized["name"]
        for inNode in self.nodesInTheScene:
            if inNode.title == nodeName:
                node = inNode
                break
        for connection in connections:
            node.deserializeConnection(connection)
