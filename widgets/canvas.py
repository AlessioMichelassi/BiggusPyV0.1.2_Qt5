from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphicElement.nodes.AbstractNodeInterface import *
from graphicEngine.graphicViewOverride import graphicViewOverride
from graphicEngine.graphicsSceneOverride import graphicSceneOverride


class canvas(QWidget):
    mainLayout: QLayout
    graphicView: graphicViewOverride
    graphicScene: graphicSceneOverride
    filename = "untitled"
    sceneWidth = 5000
    sceneHeight = 5000
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
        _sumNode = contextMenu.addAction("sum Node")
        _productNode = contextMenu.addAction("product Node")
        _printNode = contextMenu.addAction("print Node")
        contextMenu.addSeparator()

        _mousePosition = self.graphicView.mousePosition
        action = contextMenu.exec(self.mapToGlobal(event.pos()))
        node_interface = AbstractNodeInterface("NumberNode", value=10, view=self.graphicView)
        if action == _stringNode:
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