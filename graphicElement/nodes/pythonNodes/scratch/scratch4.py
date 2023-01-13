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
            self.function = self.createFunctionFromString("default_function", self.resetValue)
        else:
            try:
                functionTemp = function.split("(")
                functionName = functionTemp[0].replace("def ", "").strip()
                self.function = self.createFunctionFromString(functionName, function)
            except Exception as e:
                print(e)
        self.args = []
        self.kwargs = {}

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, function):
        self._function = function

    def createFunctionFromString(self, name, functionString):
        functionCode = f"{functionString}"
        functionGlobals = {}
        exec(functionCode, functionGlobals)
        return functionGlobals[name]

    def calculateOutput(self, outIndex: int):  # sourcery skip: assign-if-exp
        functionCode = self.mainWidget.txtFunction.toPlainText()
        functionTemp = functionCode.split("(")
        functionName = functionTemp[0].replace("def ", "").strip()
        q = self.createFunctionFromString(functionName, functionCode)

        if self.dataInPlugs[0].connectedWith:
            arg1 = self.dataInPlugs[0].value
        else:
            arg1 = 0
        if self.dataInPlugs[1].connectedWith:
            arg2 = self.dataInPlugs[1].value
        else:
            arg2 = 1
        self.dataOutPlugs[outIndex].value = q(arg1, arg2)
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
