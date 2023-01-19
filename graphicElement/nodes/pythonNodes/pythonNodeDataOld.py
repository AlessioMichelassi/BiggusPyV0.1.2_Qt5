import random
from typing import Dict, Union, List

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphicElement.nodes.AbstractNodeData import AbstractNodeData


class generateColorVariation:

    def returnColor(self, r, g, b, colorDominant=None, percentage=10):
        percs = 255 * percentage // 100
        r_var = random.randint(-percs, percs)
        g_var = random.randint(-percs, percs)
        b_var = random.randint(-percs, percs)
        if colorDominant == "r":
            r_var = random.randint(-percs, percs)
            g_var = random.randint(-percs // 2, percs // 2)
            b_var = random.randint(-percs // 2, percs // 2)
        elif colorDominant == "g":
            r_var = random.randint(-percs // 2, percs // 2)
            g_var = random.randint(-percs, percs)
            b_var = random.randint(-percs // 2, percs // 2)
        elif colorDominant == "b":
            r_var = random.randint(-percs // 2, percs // 2)
            g_var = random.randint(-percs // 2, percs // 2)
            b_var = random.randint(-percs, percs)

        r += r_var
        g += g_var
        b += b_var

        r = min(255, max(r, 0))
        g = min(255, max(g, 0))
        b = min(255, max(b, 0))
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0
        return QColor(r, g, b)


#####################################################
#
#           OPERATORI MATH
#
#


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

    def redefineGraphics(self):
        self.nodeInterface.nodeGraphic.borderColorDefault = QColor(10, 200, 10)
        self.nodeInterface.nodeGraphic.borderColorSelect = QColor(255, 70, 10)
        self.nodeInterface.nodeGraphic.backGroundColor = QColor(30, 50, 40)
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(50, 120)

    def createProxyWidget(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setStyleSheet(
            "background-color: \
                                       rgba(10,10,0,90); \
                                       color: rgba(200,255,200,255); \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: rgba(0,70,0,255);"
        )
        self.lineEdit.returnPressed.connect(self.returnName)
        self.nodeInterface.nodeGraphic.setProxyWidget(self.lineEdit)
        self.lineEdit.setText(str(self.resetValue))

    def returnName(self):
        self.changeInputValue(0, int(self.lineEdit.text()))

    def updateText(self, value):
        self.lineEdit.setText(str(value))


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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0, "r")
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0, "r")
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 153, 0, "r")
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)

    def createProxyWidget(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setStyleSheet(
            "background-color: \
                                       rgba(10,10,10,90); \
                                       color: rgba(255, 255, 102,255); \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: rgba(70,0,0,255);"
        )
        self.nodeInterface.nodeGraphic.setProxyWidget(self.lineEdit)
        self.lineEdit.setText(str(self.resetValue))

    def returnName(self):
        self.changeInputValue(0, int(self.lineEdit.text()))

    def updateText(self, value):
        self.lineEdit.setText(str(value))


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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 244, 52, percentage=80)
        print(f"{backgroundColor.red()}, {backgroundColor.green()}, {backgroundColor.blue()}")
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 251, 67)
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 128, 65)
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 218, 0)
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 70)

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


#####################################################
#
#           OPERATORI STRINGA
#
#

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

    def redefineGraphics(self):
        print("graphic redesign")
        self.nodeInterface.nodeGraphic.borderColorDefault = QColor(10, 10, 10)
        self.nodeInterface.nodeGraphic.borderColorSelect = QColor(255, 70, 10)
        self.nodeInterface.nodeGraphic.backGroundColor = QColor(30, 30, 40)
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(180, 80)

    def createProxyWidget(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setStyleSheet(
            "background-color: \
                                       rgba(10,10,0,90); \
                                       color: rgba(255,255,255,255); \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: rgba(0,0,70,255);"
        )
        self.lineEdit.returnPressed.connect(self.returnName)
        self.nodeInterface.nodeGraphic.setProxyWidget(self.lineEdit)
        self.lineEdit.setText(self.resetValue)

    def returnName(self):
        self.changeInputValue(0, self.lineEdit.text())

    def updateText(self, value):
        self.lineEdit.setText(str(value))


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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 209, 159)
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 70)

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


class DictNode(AbstractNodeData):
    lineEdit = QLineEdit
    """
    Questa classe ha due input, uno per la chiave e uno per il valore del dizionario,
    e un output che rappresenta il dizionario costruito a partire da questi input.
    Nel metodo calculate, viene creato un dizionario utilizzando la chiave e il
    valore presenti negli input, e questo dizionario viene assegnato all'output.

    Per utilizzare questo nodo, dovrai connettere i nodi di input e output in modo appropriato.
    Ad esempio, potresti utilizzare un StringNode per l'input 0 (che rappresenta
    la chiave del dizionario) e un NumberNode per l'input 1
    (che rappresenta il valore del dizionario).

    In questo modo, il DictNode funzionerà come una sorta di "costruttore" di dizionari.
    """

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(178, 255, 177)
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 70)

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(76, 63, 0)
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)

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


#####################################################
#
#           OPERATORI BOOLEANI
#
#

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(109, 255, 232)
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 172, 161)
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 244, 52, percentage=80)
        print(f"{backgroundColor.red()}, {backgroundColor.green()}, {backgroundColor.blue()}")
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)
        self.nodeInterface.nodeGraphic.changeTextToInPlug(0, "condition")
        self.nodeInterface.nodeGraphic.changeTextToInPlug(1, "true")
        self.nodeInterface.nodeGraphic.changeTextToInPlug(2, "false")

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


class functionWidget(QWidget):

    def __init__(self, node: AbstractNodeData, parent=None):
        super().__init__(parent)
        self.node = node
        self.txtFunction = QPlainTextEdit()
        self.lineEdit = QLineEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.txtFunction)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

        self.setStyleX()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        contextMenu = QMenu(self)
        contextMenu.addSection("Function Widget Context Menu")
        _updateFunction = contextMenu.addAction("Update Function")
        contextMenu.addSeparator()

        action = contextMenu.exec(self.mapToGlobal(event.pos()))

        if action == _updateFunction:
            function_string = self.txtFunction.toPlainText()
            functionTemp = function_string.split("(")
            functionName = functionTemp[0].replace("def ", "").strip()
            self.node.function = self.node.createFunctionFromString(functionName, function_string)

    def updateFunctionText(self, value):
        self.txtFunction.setPlainText(str(value))

    def setStyleX(self):
        self.lineEdit.setStyleSheet(
            "background-color: \
                                       rgba(10,10,10,90); \
                                       color: rgba(255, 255, 102,255); \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: rgba(70,0,0,255);"
        )
        self.txtFunction.setStyleSheet(
            "background-color: \
                                       rgba(10,10,10,90); \
                                       color: rgba(255, 255, 102,255); \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: rgba(70,0,0,255);"
        )


class FunctionNode(AbstractNodeData):
    mainWidget: functionWidget
    _function = None

    def __init__(self, function, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)  # il nodo For Loop ha un solo ingresso e due uscite
        self.name = "FunctionNode"
        self.resetValue = "def default_function(arg1, arg2):\n    return arg1 + arg2"
        self.functionString = function or self.resetValue
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        if function is None:
            print("function was None")
            self.functionString = self.resetValue
            self.function = self.createFunctionFromString("default_function", self.functionString)
        else:
            try:
                functionTemp = function.split("(")
                functionName = functionTemp[0].replace("def ", "").strip()
                self.function = self.createFunctionFromString(functionName, function)
                self.functionString = function
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
        try:
            functionCode = f"{functionString}"
            functionGlobals = {}
            exec(functionCode, functionGlobals)
            self.functionString = functionCode
            return functionGlobals[name]
        except Exception as e:
            print("this function not working for biggus")

    def calculate(self):
        """
        La funzione calculate di AbstractNodeData viene
        chiamata quando si vuole calcolare il nuovo valore dei plugs di output del nodo.
        :return:
        """
        returnString = f"{self.title} "
        for i, outPlug in enumerate(self.dataOutPlugs):
            outPlug.value = self.calculateOutput(i)
            returnString += f"{outPlug.name} = {outPlug.value}"
            if outPlug.connection:
                connection = outPlug.connection
                endNode = outPlug.connection.inputNode
                index = connection.inputPlug.plugData.index
                endNode.changeInputValue(index, outPlug.value, None)
        try:
            self.nodeInterface.nodeGraphic.updateTextValue()
        except Exception as e:
            print(e)

    def calculateOutput(self, outIndex: int):  # sourcery skip: assign-if-exp
        functionCode = self.mainWidget.txtFunction.toPlainText()
        functionTemp = functionCode.split("(")
        functionName = functionTemp[0].replace("def ", "").strip()
        q = self.createFunctionFromString(functionName, functionCode)
        if self.isNodeInCreation:
            return 0
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

    def updateText(self, value):
        self.mainWidget.lineEdit.setText(str(value))

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 113, 170)
        print(f"{backgroundColor.red()}, {backgroundColor.green()}, {backgroundColor.blue()}")
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        width = 400
        height = 250
        self.nodeInterface.nodeGraphic.redesign(width, height)
        self.nodeInterface.nodeGraphic.proxyWidget.setMinimumWidth(width - 20)
        self.nodeInterface.nodeGraphic.proxyWidget.setMaximumWidth(width - 20)
        self.nodeInterface.nodeGraphic.proxyWidget.setMinimumHeight(height - 100)
        self.nodeInterface.nodeGraphic.proxyWidget.setMaximumHeight(height - 100)
        x = 10
        self.nodeInterface.nodeGraphic.proxyWidget.setMaximumWidth(width - 20)
        y = height - self.nodeInterface.nodeGraphic.proxyWidget.size().height() - 5
        self.nodeInterface.nodeGraphic.proxyWidget.setPos(x, y)

    def createProxyWidget(self):
        self.mainWidget = functionWidget(self)
        self.nodeInterface.nodeGraphic.setProxyWidget(self.mainWidget)
        self.mainWidget.txtFunction.setPlainText(str(self.functionString))


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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 244, 52, percentage=80)
        print(f"{backgroundColor.red()}, {backgroundColor.green()}, {backgroundColor.blue()}")
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 255, 213)
        print(f"{backgroundColor.red()}, {backgroundColor.green()}, {backgroundColor.blue()}")
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)

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

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(255, 244, 52, percentage=80)
        print(f"{backgroundColor.red()}, {backgroundColor.green()}, {backgroundColor.blue()}")
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80)
        self.nodeInterface.nodeGraphic.changeTextToInPlug(0, "iterable")
        self.nodeInterface.nodeGraphic.changeTextToInPlug(1, "function")
        self.nodeInterface.nodeGraphic.changeTextToInPlug(2, "accumulator")

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
