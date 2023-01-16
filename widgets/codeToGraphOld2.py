import ast
import json

from PyQt5.QtCore import QPoint
import networkx as nx
from matplotlib import pyplot as plt

from graphicElement.connections.Connection import Connection
from graphicElement.nodes.AbstractNodeInterface import AbstractNodeInterface


class CodeToGraph:
    centerPoint = QPoint(100, 100)
    NodeToBeCreated = []
    functionToBeConnected = []
    _graph: nx.DiGraph

    def __init__(self, canvas: 'canvas'):
        self.canvas = canvas
        self.nodes = []
        self.node_name_list = self.canvas.availableNode
        self.nodeNameCreated = []
        self.onlyNodes = []
        self.allNodes = []
        self.connect = []

    def parseCode(self, _code: str):
        index = 0
        # sourcery skip: for-index-underscore
        tree = ast.parse(_code)
        self.create_graph()
        for _node in ast.walk(tree):
            if isinstance(_node, ast.FunctionDef):
                self.createFunction(_code, _node, tree)
                break
            elif isinstance(_node, ast.Assign):
                for target in _node.targets:
                    if isinstance(target, ast.Name) and isinstance(_node.value, ast.Call):
                        # crea un VariableNode
                        variableName = target.id
                        callNode = self.getNodeByName(_node.value.func.id)
                        callNode.nodeData.index = index
                        var = self.createVariableNode(variableName, callNode)
                        self.add_node(str(var.title))
                        self.add_edge(str(callNode.title), str(var.title))
                        self.dictionaryCreator(index, var.title, var, [callNode])
                        self.dictionaryCreator(index, callNode.title, callNode, [])

                        for i, arg in enumerate(_node.value.args):
                            # Crea un NumberNode
                            if isinstance(arg, ast.Num):
                                var = self.createNumberNode(arg, variableName, callNode)
                                self.dictionaryCreator(index, var.title, var, [callNode])
                                self.add_node(str(var.title))
                                self.add_edge(str(callNode.title), str(var.title))
                index += 1
            if isinstance(_node, ast.BinOp) and isinstance(_node.op, (ast.Add, ast.Mult, ast.Sub, ast.Div)):
                leftNode = self.getNodeByName(_node.left.id)
                rightNode = self.getNodeByName(_node.right.id)
                if leftNode and rightNode:
                    var = self.createSumNode(_node.op, leftNode, rightNode)
                    self.add_node(var.title)
                    self.add_edge(leftNode.title, var.title)
                    self.add_edge(rightNode.title, var.title)
                    self.dictionaryCreator(index, var.title, var, [])
                index += 1

    def checkIfNameExist(self, _node):
        print(f"searching for {_node.title}")
        for node in self.nodes:
            while _node.title == node.title:
                _node.nodeData.index += 1

    def getNodeByName(self, name: str):
        # sourcery skip: use-next
        for _node in self.nodes:
            if _node.nodeData.name == name:
                return _node
        return None

    def dictionaryCreator(self, index, nodeType: str, nodeName, *args):
        if nodeType not in self.NodeToBeCreated:
            self.NodeToBeCreated.append([])
            self.onlyNodes.append([])
        self.NodeToBeCreated[index] += ([nodeName, nodeType, *args])
        self.onlyNodes[index] += [nodeName]
        if nodeName not in self.allNodes:
            self.allNodes.append(nodeName)

    def createFunction(self, originalCode, _node, tree):
        # sourcery skip: extract-method, move-assign, move-assign-in-block, use-join
        returnCode = ""
        lastBody = _node.body[-1]
        while isinstance(lastBody, (ast.For, ast.While, ast.If)):
            lastBody = lastBody.body[-1]
        lastLine = lastBody.lineno
        if isinstance(originalCode, str):
            _code = originalCode.split("\n")

            for i, line in enumerate(_code, 1):
                if i in range(_node.lineno, lastLine + 1):
                    returnCode += line
            returnCode = returnCode.replace("    ", "\n    ")
            functionNode = self.canvas.createNodeFromDialog("FunctionNode", self.centerPoint)
            self.centerPoint = QPoint(self.centerPoint.x() + 500, self.centerPoint.y())
            functionNode.nodeData.setArbitraryName(_node.name)
            self.checkIfNameExist(functionNode)
            functionNode.nodeData.isNodeInCreation = True
            functionNode.nodeData.functionString = returnCode
            functionNode.nodeData.mainWidget.txtFunction.setPlainText(returnCode)
            plugLeft = len(_node.args.args) - len(functionNode.nodeData.dataInPlugs)
            if plugLeft > 0:
                functionNode.nodeData.addPlug(plugLeft, 0)
            self.nodes.append(functionNode)
            self.node_name_list.append(functionNode.title)
            remainingCode = originalCode.replace(returnCode, "")
            self.parseCode(remainingCode)

    def createVariableNode(self, _name, _callNode):
        variableNode = self.canvas.createNodeFromDialog("VariableNode", self.centerPoint)
        variableNode.nodeData.setArbitraryName(_name)

        self.checkIfNameExist(variableNode)
        variableNode.nodeGraphic.setTitle(variableNode.title)
        self.connect.append((variableNode, _callNode, 0, 0, None))
        self.nodes.append(variableNode)
        return variableNode

    def createNumberNode(self, _arg, _name, _callNode):
        numberNode = self.canvas.createNodeFromDialog("NumberNode", self.centerPoint)

        numberNode.nodeData.changeInputValue(0, _arg.n)
        self.checkIfNameExist(numberNode)

        self.nodes.append(numberNode)
        self.connect.append((numberNode, _callNode, 0, 0, None))
        return numberNode

    def createSumNode(self, operator, leftNode, rightNode):
        sumNode = self.canvas.createNodeFromDialog("SumNode", self.centerPoint)
        self.checkIfNameExist(sumNode)
        return sumNode

    def createConnection(self):
        moveX = 100
        moveY = 100
        for conn in self.connect:
            # numberNode.connectPlug(call_node, 0, 0, None)
            self.centerPoint = QPoint(self.centerPoint.x() + moveX, self.centerPoint.y() + moveY)
            conn[0].connectPlug(conn[1], 0, 0, None)
            moveX += 100
            moveY += 100

    def create_graph(self):
        self._graph = nx.DiGraph()

    def add_node(self, node):
        self._graph.add_node(node)

    def add_edge(self, node1, node2):
        self._graph.add_edge(node1, node2)

    import matplotlib.pyplot as plt

    def positionNodes(self):
        startPosX = 500
        startPosY = 500
        for node in self.nodes:
            print(node.title)
        pos = nx.spring_layout(self._graph)
        edge_labels = {(n1, n2): w for n1, n2, w in self._graph.edges(data='weight')}
        nx.draw(self._graph, pos, with_labels=True, font_weight='bold')
        nx.draw_networkx_edge_labels(self._graph, pos, edge_labels=edge_labels)
        plt.show()
        for node in self._graph.nodes:
            x = pos[node][0]
            y = pos[node][1]
            jsonizedNode = []
            for MyNodes in self.nodes:
                jsonizedNode.append(MyNodes.serialize())
                if node == MyNodes.title:
                    print("finded")
                    newX = startPosX * x * 2
                    newY = startPosY * y * 2
                    MyNodes.nodeGraphic.setPos(newX, newY)
        for string in jsonizedNode:
            a = json.dumps(string.replace("    '\'", '\n'))
            print(a)








