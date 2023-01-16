import ast

from PyQt5.QtCore import QPoint

from graphicElement.connections.Connection import Connection
from graphicElement.nodes.AbstractNodeInterface import AbstractNodeInterface


class CodeToGraph:
    centerPoint = QPoint(100, 100)
    NodeToBeCreated = []
    functionToBeConnected = []

    def __init__(self, canvas: 'canvas'):
        self.canvas = canvas
        self.nodes = []
        self.node_name_list = self.canvas.node_name_list
        self.nodeNameCreated = []
        self.onlyNodes = []
        self.connect = []

    def parseCode2(self, _code: str):
        # sourcery skip: for-index-underscore
        tree = ast.parse(_code)
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
                        self.createVariableNode(variableName, callNode)
                        for i, arg in enumerate(_node.value.args):
                            # Crea un NumberNode
                            if isinstance(arg, ast.Num):
                                self.createNumberNode(arg, variableName, callNode)
            elif isinstance(_node, ast.BinOp) and isinstance(_node.op,
                                                             (ast.Add, ast.Mult, ast.Sub, ast.Div)):
                leftNode = self.getNodeByName(_node.left.id)
                rightNode = self.getNodeByName(_node.right.id)
                if leftNode and rightNode:
                    self.createSumNode(_node.op, leftNode, rightNode)

    def parseCode(self, _code: str):
        index = 0
        # sourcery skip: for-index-underscore
        tree = ast.parse(_code)
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
                        var = self.createVariableNode(variableName, callNode)
                        self.dictionaryCreator(index, var.title, var, [callNode])

                        self.dictionaryCreator(index, callNode.title, callNode, [])
                        for i, arg in enumerate(_node.value.args):
                            # Crea un NumberNode
                            if isinstance(arg, ast.Num):
                                var = self.createNumberNode(arg, variableName, callNode)
                                self.dictionaryCreator(index, var.title, var, [callNode])
                index += 1
            if isinstance(_node, ast.BinOp) and isinstance(_node.op, (ast.Add, ast.Mult, ast.Sub, ast.Div)):
                leftNode = self.getNodeByName(_node.left.id)
                rightNode = self.getNodeByName(_node.right.id)
                if leftNode and rightNode:
                    var = self.createSumNode(_node.op, leftNode, rightNode)
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

    def dictionaryCreator(self, index, nodeType: str, nodeName: str, *args):
        if nodeType not in self.NodeToBeCreated:
            self.NodeToBeCreated.append([])
            self.onlyNodes.append([])
        self.NodeToBeCreated[index] += ([nodeName, nodeType, *args])
        self.onlyNodes[index] += [nodeName]

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
            functionNode.nodeData.madeArbitraryName(_node.name)
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
        variableNode.nodeData.madeArbitraryName(_name)
        print(f"created a VariableNode Called {variableNode.title}")
        self.checkIfNameExist(variableNode)
        variableNode.nodeGraphic.setTitle(variableNode.title)
        self.connect.append((variableNode, _callNode, 0, 0, None))
        self.nodes.append(variableNode)
        return variableNode

    def createNumberNode(self, _arg, _name, _callNode):
        numberNode = self.canvas.createNodeFromDialog("NumberNode", self.centerPoint)
        print(f"created a NumberNode Called {numberNode.title} with value {_arg.n}")
        numberNode.nodeData.changeInputValue(0, _arg.n)
        self.checkIfNameExist(numberNode)

        self.nodes.append(numberNode)
        self.connect.append((numberNode, _callNode, 0, 0, None))
        print(f"NumberNode with title {numberNode.title} will be connected to {_callNode.title}")
        return numberNode

    def createSumNode(self, operator, leftNode, rightNode):
        sumNode = self.canvas.createNodeFromDialog("SumNode", self.centerPoint)
        self.checkIfNameExist(sumNode)
        # sumNode.nodeData.operator = operator

        # self.connect(leftNode, 0, sumNode, 0)
        # self.connect(rightNode, 0, sumNode, 1)
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

    def positionNodes(self):
        x_0_pos = (500, 500)
        rect = (500, 500, 500, 500)
        add_and_multiply_0_pos = (x_0_pos[0] - 350 - 200, 500)
        number_node_0_pos = (add_and_multiply_0_pos[0], add_and_multiply_0_pos[1] + 50)
        number_node_1_pos = (add_and_multiply_0_pos[0], add_and_multiply_0_pos[1] + 100)
        number_node_2_pos = (add_and_multiply_0_pos[0], add_and_multiply_0_pos[1] + 150)
        # posiziona i nodi
        for node in self.onlyNodes:
            if node is not []:
                print(node)
        node = self.onlyNodes[0]
        node[0].nodeGraphic.setPos(x_0_pos[0], x_0_pos[1])
        node[1].nodeGraphic.setPos(add_and_multiply_0_pos[0], add_and_multiply_0_pos[1])
        node[2].nodeGraphic.setPos(number_node_0_pos[0], number_node_0_pos[1])
        node[3].nodeGraphic.setPos(number_node_1_pos[0], number_node_1_pos[1])
        node[4].nodeGraphic.setPos(number_node_2_pos[0], number_node_2_pos[1])
        # continua con le altre righe del codice

    def create_graph(self):  # sourcery skip: merge-isinstance
        # Create connections between nodes based on variable names
        for i, node in enumerate(self.nodes):
            if isinstance(node, 'NumberNode'):
                for j, node2 in enumerate(self.nodes):
                    if i == j:
                        continue
                    if isinstance(node2, 'SumNode') or isinstance(node2, 'CallNode'):
                        for input_plug in node2.dataInPlugs:
                            if input_plug.name == node.name:
                                node.connect(node2, 0, input_plug.index)
                                break
        return self.nodes
