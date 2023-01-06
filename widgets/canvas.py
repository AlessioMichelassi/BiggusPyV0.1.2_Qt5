from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphicElement.nodeInterface.nodeInterface import *
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
    nodesInTheScene = []

    def __init__(self, parent=None):
        super(canvas, self).__init__(parent)

        self.nodes = []
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
        contextMenu.addSection("Test")
        testNode = contextMenu.addAction("abstract node")
        _numberNode = contextMenu.addAction("number node")
        _sumNode = contextMenu.addAction("sum Node")
        _productNode = contextMenu.addAction("product Node")
        _printNode = contextMenu.addAction("print Node")
        contextMenu.addSeparator()

        _mousePosition = self.graphicView.mousePosition
        action = contextMenu.exec(self.mapToGlobal(event.pos()))

        if action == testNode:
            node_interface = AbstractNodeInterface("AbstractDataNode", view=self.graphicView)
            self.addNodeToTheScene(node_interface, _mousePosition)
        elif action == _numberNode:
            node_interface = AbstractNodeInterface("NumberNode", value=10, view=self.graphicView)
            self.addNodeToTheScene(node_interface, _mousePosition)
        elif action == _sumNode:
            node_interface = AbstractNodeInterface("SumNode", view=self.graphicView)
            self.addNodeToTheScene(node_interface, _mousePosition)
        elif action == _printNode:
            node_interface = AbstractNodeInterface("PrintNode", view=self.graphicView)
            self.addNodeToTheScene(node_interface, _mousePosition)

    def addNodeToTheScene(self, nodeInterface, mousePos):
        # sourcery skip: move-assign-in-block, remove-unnecessary-cast, simplify-constant-sum, sum-comprehension
        index = 0
        self.graphicScene.addItem(nodeInterface.nodeGraphic)
        nodeInterface.nodeGraphic.setPos(mousePos)

        for x in self.nodesInTheScene:
            print(x.title)
            if nodeInterface.title == x.title:
                index += 1
            else:
                print(f"{nodeInterface.title} != {x.title}")

        nodeInterface.changeIndex(index)

        self.nodesInTheScene.append(nodeInterface)



