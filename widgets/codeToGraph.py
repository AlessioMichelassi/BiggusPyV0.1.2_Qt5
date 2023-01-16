import ast
import json

from PyQt5.QtCore import QPoint
import networkx as nx
from matplotlib import pyplot as plt

from graphicElement.connections.Connection import Connection
from graphicElement.nodes.AbstractNodeInterface import AbstractNodeInterface


class CodeToGraph:
    centerPoint = QPoint(100, 100)
    _graph: nx.DiGraph

    def __init__(self, canvas: 'canvas'):
        self.canvas = canvas
        self.nodes = []
        self.availableNode = self.canvas.node_name_list
        self.nodeCreatedHere = []

    def parseCode(self, _code: str):
        print(f"debug: parsinCode {_code}")
        index = 0
        # sourcery skip: for-index-underscore
        tree = ast.parse(_code)
        self.create_graph()
        for _node in ast.walk(tree):
            if isinstance(_node, ast.FunctionDef):
                self.createFunctionNode(_code, _node, tree)
                break
            elif isinstance(_node, ast.Assign):
                for target in _node.targets:
                    if isinstance(target, ast.Name) and isinstance(_node.value, ast.Call):
                        # crea un VariableNode
                        variableName = target.id
                        _name = f"{_node.value.func.id}_{str(index)}"
                        callNode = self.getNodeByName(_name)
                        if callNode is None:
                            print(f"breakPoint: {_name}")
                            break
                        var = self.createVariableNode(variableName, callNode)

                        for i, arg in enumerate(_node.value.args):
                            # Crea un NumberNode
                            if isinstance(arg, ast.Num):
                                var = self.createNumberNode(arg, variableName, callNode)
                                self.add_edge(str(callNode.title), str(var.title))
                index += 1
            if isinstance(_node, ast.BinOp) and isinstance(_node.op, (ast.Add, ast.Mult, ast.Sub, ast.Div)):
                if ast.Add:
                    var = self.createSumNode("SumNode")

    def getNodeByName(self, name: str):
        # sourcery skip: use-next

        for _node in self.nodes:
            if _node.title == name:
                return _node
            else:
                tempName = _node.title.split('_')
                print(tempName)
                realName = tempName[0]
                print(tempName[1])
                realIndex = int(tempName[1])
                testName = f"{realName}_{realIndex-1}"
                for _nodeTest in self.nodes:
                    if _nodeTest.title == testName:
                        print(f"findedNode named: {testName}")
                        returnNode = self.createInstanceOfANode(_nodeTest, realName, realIndex)
                    else:
                        print(f"node with name: {testName} was not found")


    def checkIfNameExist(self, _node):
        for node in self.nodes:
            while _node.title == node.title:
                _node.nodeData.index += 1

    def createFunctionNode(self, originalCode: str, _node: ast.FunctionDef, tree: ast.Module):
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
            returnNode = AbstractNodeInterface("FunctionNode", function="", view=self.canvas.graphicView)
            returnNode.nodeData.setArbitraryName(_node.name)
            print(f"debug: create a functionNode named {returnNode.nodeData.name} titled {returnNode.title}")
            returnNode.nodeData.isNodeInCreation = True
            returnNode.nodeData.functionString = returnCode
            returnNode.nodeData.mainWidget.txtFunction.setPlainText(returnCode)
            plugLeft = len(_node.args.args) - len(returnNode.nodeData.dataInPlugs)
            if plugLeft > 0:
                returnNode.nodeData.addPlug(plugLeft, 0)
            self.nodeCreatedHere.append(returnNode)
            remainingCode = originalCode.replace(returnCode, "")

            self.nodes.append(returnNode)
            self.parseCode(remainingCode)
            return returnNode, returnCode

    def createNumberNode(self, _arg, _name, _callNode):
        returnNode = AbstractNodeInterface("NumberNode", value=0, view=self.canvas.graphicView)
        # returnNode.nodeData.madeArbitraryName(_name)
        self.checkIfNameExist(returnNode)
        returnNode.nodeGraphic.setTitle(returnNode.title)
        print(f"debug: createNumbereNode named: {returnNode.nodeData.name} titled {returnNode.title}")
        self.nodes.append(returnNode)
        return returnNode

    def createVariableNode(self, _name, _callNode):
        returnNode = AbstractNodeInterface("VariableNode", value=0, name=_name, view=self.canvas.graphicView)
        # returnNode.nodeData.madeArbitraryName(_name)
        self.checkIfNameExist(returnNode)
        returnNode.nodeGraphic.setTitle(returnNode.title)
        print(f"debug: createVariableNode named: {returnNode.nodeData.name} titled {returnNode.title}")
        self.nodes.append(returnNode)
        return returnNode

    def createSumNode(self, _name):
        returnNode = AbstractNodeInterface("SumNode", view=self.canvas.graphicView)
        # returnNode.nodeData.madeArbitraryName(_name)
        self.checkIfNameExist(returnNode)
        print(f"debug: createSumNode named: {returnNode.nodeData.name} titled {returnNode.title}")
        self.nodes.append(returnNode)
        return returnNode

    def createInstanceOfANode(self, node, name, index=None):
        if index is None:
            for _node in self.nodes:
                if _node.nodeData.name == name:
                    index = _node.nodeData.index + 1

        returnCode = node.nodeData.mainWidget.txtFunction.toPlainText()
        returnNode = AbstractNodeInterface("FunctionNode", function=returnCode, view=self.canvas.graphicView)
        returnNode.nodeData.setArbitraryName(name)
        numberOfInputPlugs = len(node.nodeData.dataInPlugs)
        plugLeft = numberOfInputPlugs - len(returnNode.nodeData.dataInPlugs)
        if plugLeft > 0:
            returnNode.nodeData.addPlug(plugLeft, 0)
        self.nodes.append(returnNode)
        print(f"copy of {returnNode.title} created")
        return returnNode

    def dictionaryCreator(self, index, nodeType: str, nodeName, *args):
        pass

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
        jsonizedNode = []
        for node in self._graph.nodes:
            x = pos[node][0]
            y = pos[node][1]
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
