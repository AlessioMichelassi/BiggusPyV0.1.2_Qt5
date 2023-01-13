import ast

from PyQt5.QtCore import QPoint

from graphicElement.connections.Connection import Connection
from graphicElement.nodes.AbstractNodeInterface import AbstractNodeInterface


class CodeToGraph:
    centerPoint = QPoint(100, 100)

    def __init__(self, canvas: 'canvas'):
        self.canvas = canvas
        self.nodes = []
        self.node_name_list = self.canvas.node_name_list
        self.nodeNameCreated = []

    def parseCode(self, _code: str):
        # sourcery skip: for-index-underscore
        tree = ast.parse(_code)
        for _node in ast.walk(tree):
            if isinstance(_node, ast.FunctionDef):
                self.createFunction(_code, _node, tree)
                break
            elif isinstance(_node, ast.Assign):
                for target in _node.targets:
                    if isinstance(target, ast.Name) and isinstance(_node.value, ast.Call):
                        variable_name = target.id
                        call_node = self.getNodeByName(_node.value.func.id)
                        variableNode = self.canvas.createNodeFromDialog("VariableNode", self.centerPoint)
                        self.centerPoint = QPoint(self.centerPoint.x() +100, self.centerPoint.y())
                        variableNode.nodeData.madeArbitraryName(variable_name)
                        self.checkIfNameExist(variableNode)
                        variableNode.connectPlug(call_node, 0, 0, None)
                        self.nodes.append(variableNode)

                        for i, arg in enumerate(_node.value.args):
                            if isinstance(arg, ast.Num):
                                numberNode = self.canvas.createNodeFromDialog("NumberNode", self.centerPoint)
                                self.centerPoint = QPoint(self.centerPoint.x() + 100, self.centerPoint.y())
                                numberNode.nodeData.madeArbitraryName(variable_name)
                                numberNode.nodeData.changeInputValue(0, arg.n)
                                self.checkIfNameExist(numberNode)
                                numberNode.connectPlug(call_node, 0, 0, None)
                                self.nodes.append(numberNode)

    def checkIfNameExist(self, _node):
        for node in self.nodes:
            while _node.title == node.title:
                _node.nodeData.index += 1

    def getNodeByName(self, name: str):
        # sourcery skip: use-next
        for _node in self.nodes:
            if _node.nodeData.name == name:
                return _node
        return None

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
            functionNode.nodeData.functionString = returnCode
            functionNode.nodeData.mainWidget.txtFunction.setPlainText(returnCode)
            """
            il codice a questo punto dovrebbe aggiornare il numero dei plug
            function_node.numberOfInputPlugs = len(_node.args.args)
            function_node.numberOfOutputPlugs = 1
            function_node.createPlugs()
            """
            plugLeft = len(_node.args.args) - len(functionNode.nodeData.dataInPlugs)
            if plugLeft > 0:
                functionNode.nodeData.addPlug(plugLeft, 0)
            self.nodes.append(functionNode)
            self.node_name_list.append(functionNode.title)
            remainingCode = originalCode.replace(returnCode, "")
            self.parseCode(remainingCode)

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
