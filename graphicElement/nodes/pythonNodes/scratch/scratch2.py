import ast
import random
from typing import Dict, Union, List

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphicElement.nodes.AbstractNodeData import AbstractNodeData


class NumberNode(AbstractNodeData):
    lineEdit: QLineEdit

    def __init__(self, value: Union[int, float], interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = "Number"
        self.resetValue = value
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value
        return self.dataOutPlugs[0].value


class SumNode(AbstractNodeData):
    lineEdit: QLineEdit

    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "Sum"
        self.resetValue = 0
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value + self.dataInPlugs[1].value
        return self.dataOutPlugs[outIndex].value


class ProductNode(AbstractNodeData):
    lineEdit: QLineEdit

    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "Product"
        self.resetValue = 0
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value * self.dataInPlugs[1].value
        return self.dataOutPlugs[outIndex].value


class ExpNode(AbstractNodeData):
    lineEdit: QLineEdit

    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "Exponential"
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value ** self.dataInPlugs[1].value
        return self.dataOutPlugs[outIndex].value


class DivisionNode(AbstractNodeData):
    def __init__(self, isInteger=False, interface=None):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.isInteger = isInteger
        self.name = "Division"
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        try:
            if self.isInteger:
                self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value // self.dataInPlugs[1].value
            else:
                self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value / self.dataInPlugs[1].value
        except ZeroDivisionError:
            self.dataOutPlugs[outIndex].value = 0
        return self.dataOutPlugs[outIndex].value


class RemainderNode(AbstractNodeData):
    def __init__(self, isInteger=False, interface=None):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "Reminder"
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value % self.dataInPlugs[1].value
        return self.dataOutPlugs[outIndex].value


class StringNode(AbstractNodeData):
    lineEdit = QLineEdit

    def __init__(self, value: str, interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = "String"
        self.resetValue = value
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value
        return self.dataOutPlugs[0].value


class ListNode(AbstractNodeData):
    lineEdit = QLineEdit

    def __init__(self, value: List[Union[int, float, str]], interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = "List"
        self.resetValue = value
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value
        return self.dataOutPlugs[0].value


class DictNode(AbstractNodeData):

    def __init__(self, value: dict, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "Dictionary"
        self.resetValue = ""
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        key = self.dataInPlugs[0].value
        value = self.dataInPlugs[1].value
        self.dataOutPlugs[outIndex].value = {key: value}
        return self.dataOutPlugs[outIndex].value

    def createProxyWidget(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setStyleSheet(
            "background-color: \
                                       rgba(10,10,10,90); \
                                       color: rgba(255, 255, 102,255); \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: rgba(70,0,0,255);"
        )
        self.lineEdit.returnPressed.connect(self.returnName)
        self.nodeInterface.nodeGraphic.setProxyWidget(self.lineEdit)
        self.lineEdit.setText(str(self.resetValue))

    def returnName(self):
        self.changeInputValue(0, int(self.lineEdit.text()))

    def updateText(self, value):
        self.lineEdit.setText(str(value))


class ConcatNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "ConcatNode"
        self.resetValue = ""
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        returnValue = str(self.dataInPlugs[0].value) + str(self.dataInPlugs[1].value)
        self.dataOutPlugs[outIndex].value = returnValue
        return returnValue


class ReplaceNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=3, numOuts=1, interface=interface)
        self.name = "Replace"
        self.resetValue = ""
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        returnValue = str(self.dataInPlugs[0].value).replace(str(self.dataInPlugs[1].value),
                                                             str(self.dataInPlugs[2].value))
        self.dataOutPlugs[outIndex].value = returnValue
        return returnValue


class PrintNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = "Print"
        self.resetValue = ""
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex):
        return self.dataInPlugs[0].value

    def connect(self, endNode: "AbstractNodeData", input_index: int, output_index: int):
        endNode.dataInPlugs[input_index] = self.dataOutPlugs[output_index]


class AndNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "And"
        self.resetValue = ""
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        input1 = self.dataInPlugs[0].value
        input2 = self.dataInPlugs[1].value
        self.dataOutPlugs[outIndex].value = input1 and input2
        return self.dataOutPlugs[outIndex].value


class OrNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "Or"
        self.resetValue = ""
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        input1 = self.dataInPlugs[0].value
        input2 = self.dataInPlugs[1].value
        self.dataOutPlugs[outIndex].value = input1 or input2
        return self.dataOutPlugs[outIndex].value


class IfNode(AbstractNodeData):

    def __init__(self, interface):
        super().__init__(numIn=3, numOuts=1, interface=interface)
        self.name = "if"
        self.resetValue = False
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int):
        condition = self.dataInPlugs[0].value
        if condition:
            self.dataOutPlugs[outIndex].value = self.dataInPlugs[1].value
        else:
            self.dataOutPlugs[outIndex].value = self.dataInPlugs[2].value


class FunctionNode(AbstractNodeData):
    _function = None

    def __init__(self, function, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)  # il nodo For Loop ha un solo ingresso e due uscite
        self.name = "Function"
        self.resetValue = "def default_function(arg1, arg2):\n    return arg1 + arg2"
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        if function is None:
            self.function = self.resetValue
        else:
            try:
                self.function = function
            except Exception as e:
                print(e)
        self.args = []
        self.kwargs = {}

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, function):
        functionTemp = function.split("(")
        functionName = functionTemp[0].replace("def ", "").strip()
        self._function = self.createFunctionFromString(functionName, function)

    def createFunctionFromString(self, name, functionString):
        functionCode = f"{functionString}"
        functionGlobals = {}
        exec(functionCode, functionGlobals)
        return functionGlobals[name]

    def calculateOutput(self, outIndex: int):  # sourcery skip: assign-if-exp
        """functionCode = self.mainWidget.txtFunction.toPlainText()
        functionTemp = functionCode.split("(")
        functionName = functionTemp[0].replace("def ", "").strip()
        q = self.createFunctionFromString(functionName, functionCode)"""

        if self.dataInPlugs[0].connectedWith:
            arg1 = self.dataInPlugs[0].value
        else:
            arg1 = 0
        if self.dataInPlugs[1].connectedWith:
            arg2 = self.dataInPlugs[1].value
        else:
            arg2 = 1

        return self.dataOutPlugs[outIndex].value


class CallNode(AbstractNodeData):
    def __init__(self, name: str, interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = name
        self.resetValue = False
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> any:
        input_value = self.dataInPlugs[0].value
        result = getattr(input_value, self.name)()
        self.dataOutPlugs[outIndex].value = result
        return result


class VariableNode(AbstractNodeData):
    def __init__(self, name: str, value: any, interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = name
        self.resetValue = value
        self._value = value
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: any):
        self._value = value

    def calculateOutput(self, outIndex: int) -> any:
        self.dataOutPlugs[outIndex].value = self.value
        return self.value


class ForNode(AbstractNodeData):
    def __init__(self, interface=None):
        super().__init__(numIn=3, numOuts=1, interface=interface)  # il nodo For Loop ha un solo ingresso e due uscite
        self.name = "ForLoopNode"
        self.resetValue = False
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int):
        iterable = self.dataInPlugs[0].value
        function = self.dataInPlugs[1].value
        accumulator = self.dataInPlugs[2].value
        for value in iterable:
            accumulator = function(accumulator, value)
        self.dataOutPlugs[outIndex].value = accumulator
        return self.dataOutPlugs[outIndex].value


class CodeToGraph:
    def __init__(self):
        self.nodes = []
        self.node_name_list = ["NumberNode", "StringNode", "ListNode", "DictNode", "SumNode",
                               "ProductNode", "PowerNode", "DivisionNode", "RemainderNode",
                               "PrintNode", "ReplaceNode", "ConcatNode", "IfNode", "ForNode",
                               "FunctionNode", "CallNode", "VariableNode"]

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
                        variable_node = VariableNode(variable_name, 0, None)
                        self.checkIfNameExist(variable_node)
                        variable_node.connect(call_node, 0, 0)
                        self.nodes.append(variable_node)

                        for i, arg in enumerate(_node.value.args):
                            if isinstance(arg, ast.Num):
                                number_node = NumberNode(arg.n, None)
                                self.checkIfNameExist(number_node)
                                number_node.connect(call_node, i, 0)
                                self.nodes.append(number_node)

    def checkIfNameExist(self, _node):
        for node in self.nodes:
            while _node.title == node.title:
                _node.index += 1

    def getNodeByName(self, name: str):
        # sourcery skip: use-next
        for _node in self.nodes:
            if _node.name == name:
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
            function_node = FunctionNode(returnCode, interface=None)
            function_node.name = _node.name
            function_node.numberOfInputPlugs = len(_node.args.args)
            function_node.numberOfOutputPlugs = 1
            function_node.createPlugs()

            self.nodes.append(function_node)
            self.node_name_list.append(function_node.name)
            remainingCode = originalCode.replace(returnCode, "")
            self.parseCode(remainingCode)

    def create_graph(self):  # sourcery skip: merge-isinstance
        # Create connections between nodes based on variable names
        for i, node in enumerate(self.nodes):
            if isinstance(node, NumberNode):
                for j, node2 in enumerate(self.nodes):
                    if i == j:
                        continue
                    if isinstance(node2, SumNode) or isinstance(node2, CallNode):
                        for input_plug in node2.dataInPlugs:
                            if input_plug.name == node.name:
                                node.connect(node2, 0, input_plug.index)
                                break
        return self.nodes


code = """
def add_and_multiply(a, b, c):
    d = a + b
    e = d * c
    return e

x = add_and_multiply(1, 2, 3)
y = add_and_multiply(4, 5, 6)
z = x + y
print(z)
"""
parser = CodeToGraph()
parser.parseCode(code)
nodes = parser.create_graph()

for node in nodes:
    print(f"{node.title}")
