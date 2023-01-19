import ast
import json
from collections import OrderedDict

from PyQt5.QtCore import QPoint
import networkx as nx
from matplotlib import pyplot as plt

from graphicElement.connections.Connection import Connection
from graphicElement.nodes.AbstractNodeInterface import AbstractNodeInterface
from graphicElement.nodes.pythonNodes.pythonNodeData import FunctionNode


class CodeToGraph:
    centerPoint = QPoint(100, 100)
    _graph: nx.DiGraph
    connection = []

    def __init__(self, canvas: 'canvas'):
        self.canvas = canvas
        self.nodes = []
        self.availableNode = self.canvas.node_name_list
        self.nodeCreatedHere = []
        self.connection = []

    def parseCode(self, _code: str):
        index = 0
        tree = ast.parse(_code)
        self.create_graph()
        for _node in ast.walk(tree):
            if isinstance(_node, ast.FunctionDef):
                self.createFunctionNode(_code, _node, tree)
                break
            elif isinstance(_node, ast.Assign):
                for target in _node.targets:
                    if isinstance(target, ast.Name) and isinstance(_node.value, ast.Call):
                        callNodeName = f"{_node.value.func.id}_{str(index)}"
                        callNode = self.checkForCallNode(_node, callNodeName)
                        variableName = target.id
                        var = self.createVariableNode(variableName, callNode)

                        for i, arg in enumerate(_node.value.args):
                            # Crea un NumberNode
                            if isinstance(arg, ast.Num):
                                var = self.createNumberNode(arg, variableName, callNode, i)

                index += 1
            if isinstance(_node, ast.BinOp) and isinstance(_node.op, (ast.Add, ast.Mult, ast.Sub, ast.Div)):
                leftNode = self.getNodeByName(_node.left.id)
                print(_node.left.id)
                rightNode = self.getNodeByName(_node.right.id)
                if leftNode and rightNode:
                    var = self.createSumNode("SumNode", _node.left.id, _node.right.id)
                    self.add_node(var.title)
                    self.add_edge(leftNode.title, var.title)
                    self.add_edge(rightNode.title, var.title)

    def getNodeByName(self, name: str):
        for _node in self.nodes:
            if _node.nodeData.name == name:
                return _node
        return None

    def getNodeByTitle(self, title: str):
        # sourcery skip: use-next
        listOFTile = ""
        for _node in self.nodes:
            listOFTile += f"{_node.title}, "
            if _node.title == title:
                print(f"nodeFound {title}")
                return _node
        print(listOFTile)

    def getFunctionByName(self, name: str):
        # sourcery skip: inline-immediately-returned-variable, remove-unnecessary-else
        listOFTile = ""
        for _node in self.nodes:
            listOFTile += f"{_node.title}, "
            if _node.nodeData.name == name:
                print(f"nodeFound {_node.name}")
                return _node
        print(listOFTile)

    def checkIfNameExist(self, _node):
        for node in self.nodes:
            while _node.title == node.title:
                _node.nodeData.index += 1
                _node.nodeGraphic.update()

    def checkForCallNode(self, _node, _title):
        callNode = self.getNodeByTitle(_title)
        if callNode is not None:
            return callNode

        print(f"warning from call Node... functionNode named {_title} not found with getNodeByTitle")
        tempName = _title.split('_')
        if callNode0 := self.getNodeByName(tempName[0]):
            callNode = self.createInstanceOfANode(callNode0, callNode0.nodeData.name, callNode0.nodeData.index)
            if callNode not in self.nodes:
                self.nodes.append(callNode)
            return callNode
        else:
            print(f"warning from call Node... functionNode named {_title} not found with createInstanceOfANode")
        if callNode is None:
            print(f"breakPoint: {_title}")

    def createFunctionNode(self, originalCode: str, _node: ast.FunctionDef, tree: ast.Module):
        returnCode = ""

        # this part exctract the function def part from the node
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

            # una volta estratto il codice crea il node FunctionNode
            returnNode = AbstractNodeInterface("FunctionNode", name=_node.name, function=returnCode,
                                               view=self.canvas.graphicView)

            self.nodeCreatedHere.append(returnNode)
            remainingCode = originalCode.replace(returnCode, "")
            returnNode.updateTitleInNodeGraphic()
            if returnNode not in self.nodes:
                self.nodes.append(returnNode)
            self.parseCode(remainingCode)
            return returnNode, returnCode

    def createNumberNode(self, _arg, _name, _callNode, index):
        # sourcery skip: use-next
        returnNode = AbstractNodeInterface("NumberNode", value=0, view=self.canvas.graphicView)

        self.checkIfNameExist(returnNode)
        returnNode.updateTitleInNodeGraphic()
        print(f"{returnNode.title} -> {_callNode.title} at index {index}")
        self.add_node(str(returnNode.title))
        self.add_edge(str(_callNode.title), str(returnNode.title))

        if [returnNode, _callNode, index] not in self.connection:
            print(f"create connection {returnNode.title} -> {_callNode.title} at index {index}")
            self.connection.append([returnNode, _callNode, index])

        if returnNode not in self.nodes:
            self.nodes.append(returnNode)

        return returnNode

    def createVariableNode(self, _name, _callNode):
        returnNode = AbstractNodeInterface("VariableNode", value=0, name=_name, view=self.canvas.graphicView)
        # returnNode.nodeData.madeArbitraryName(_name)
        self.checkIfNameExist(returnNode)
        returnNode.updateTitleInNodeGraphic()

        self.add_node(returnNode.title)
        self.add_edge(str(_callNode.title), returnNode.title)
        connectedPlugInIndex = 0
        # trova l'input del nodo callNode a cui è connesso il VariableNode
        for i, arg in enumerate(_callNode.nodeData.args):
            if arg == _name:
                connectedPlugInIndex = i
                print(f"check for {returnNode.title}. {_callNode.title} has index {i}")
                break

        if returnNode not in self.nodes:
            self.nodes.append(returnNode)
        if [_callNode, returnNode, connectedPlugInIndex] not in self.connection:
            self.connection.append([_callNode, returnNode, connectedPlugInIndex])
        return returnNode

    def createSumNode(self, _name, _leftNode, _rightNode):
        returnNode = AbstractNodeInterface("SumNode", view=self.canvas.graphicView)
        # returnNode.nodeData.madeArbitraryName(_name)
        self.checkIfNameExist(returnNode)
        returnNode.updateTitleInNodeGraphic()
        if returnNode not in self.nodes:
            self.nodes.append(returnNode)
        leftNode = self.getNodeByName(_leftNode)
        if [leftNode, returnNode, 0] not in self.connection:
            self.connection.append([leftNode, returnNode, 0])
        rightNode = self.getNodeByName(_rightNode)
        if [rightNode, returnNode, 0] not in self.connection:
            self.connection.append([rightNode, returnNode, 0])
        return returnNode

    def createInstanceOfANode(self, node, name, index=None):
        if index is None:
            for _node in self.nodes:
                if _node.nodeData.name == name:
                    index = _node.nodeData.index + 1

        returnCode = node.nodeData.mainWidget.txtFunction.toPlainText()
        _name = node.nodeData.name
        _index = node.nodeData.index
        returnNode = AbstractNodeInterface("FunctionNode", name=_name, function=returnCode,
                                           view=self.canvas.graphicView)
        returnNode.changeIndex(_index + 1)
        print(f"name was {_name}")
        print(
            f"debug from istance copy: created a node {returnNode.nodeData.className} named {returnNode.nodeData.name} titled {returnNode.nodeData.title}")

        return returnNode

    def create_graph(self):
        self._graph = nx.DiGraph()

    def add_node(self, node):
        self._graph.add_node(node)

    def add_edge(self, node1, node2):
        self._graph.add_edge(node1, node2)

    def connectNode(self):
        for conn in self.connection:
            _outputPlug = conn[0].nodeData.dataOutPlugs[0].plugGraphic
            conn[0].nodeData.isNodeInCreation = True
            conn[1].nodeData.isNodeInCreation = True
            _inputPlug = conn[1].nodeData.dataInPlugs[int(conn[2])].plugGraphic
            connection = Connection(_outputPlug, _inputPlug)
            self.canvas.connections.append(connection)

        for conn in self.connection:
            conn[0].nodeData.isNodeInCreation = False
            conn[1].nodeData.isNodeInCreation = False

    def positionNodes(self):
        startPosX = 500
        startPosY = 500

        pos = nx.spring_layout(self._graph)
        edge_labels = {(n1, n2): w for n1, n2, w in self._graph.edges(data='weight')}
        nx.draw(self._graph, pos, with_labels=True, font_weight='bold')
        nx.draw_networkx_edge_labels(self._graph, pos, edge_labels=edge_labels)
        plt.show()

        for node in self._graph.nodes:
            x = pos[node][0]
            y = pos[node][1]
            for MyNodes in self.nodes:
                if node == MyNodes.title:
                    newX = startPosX * x * 2
                    newY = startPosY * y * 2
                    MyNodes.nodeGraphic.setPos(newX, newY)

    def showGraph(self):
        for node in self.nodes:
            self.canvas.graphicView.scene().addItem(node.nodeGraphic)
        for connection in self.canvas.connections:
            self.canvas.graphicView.scene().addItem(connection)


    def serializeCodeToGraph(self):
        jsonizedNode = []
        for node in self.nodes:
            jsonizedNode.append(node.serialize())

        dicts = OrderedDict([
            ('name', "from paste"),
            ('sceneWidth', self.canvas.sceneWidth),
            ('sceneHeight', self.canvas.sceneHeight),
            ('Nodes', jsonizedNode)])
        serialized = json.dumps(dicts)
        # salva il file come fileTemp
        with open("saveDir/tempFile", "w+") as f:
            f.write(serialized)
        # importa nel canvas il file creato
        self.canvas.deserialize(serialized)
