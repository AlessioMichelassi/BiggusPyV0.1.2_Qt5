import random
from typing import Dict, Union, List

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QGraphicsProxyWidget

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
    """
    La classe IfNode eredita da AbstractNode e ha un numero di input
    e di output pari a 1. Nel metodo calculate,
    viene valutata la condizione presente nell'input 0: se essa è vera,
    viene assegnato all'output 0 il valore presente nell'input 1,
    altrimenti viene assegnato all'output 0 il valore presente nell'input 2.

    Per utilizzare questo nodo, dovrai connettere i nodi di input
    e output in modo appropriato.

    Ad esempio, potresti utilizzare un NumberNode per l'input 0
    (che rappresenta la condizione) e altri due NumberNode
    per gli input 1 e 2 (che rappresentano i valori da assegnare
    all'output in base al risultato della condizione).

    In questo modo, il IfNode funzionerà come una sorta di
    "selettore" di valori, a seconda del risultato della condizione.
    """

    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=2, interface=interface)
        self.name = "if"
        self.resetValue = False
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int):
        condition = self.dataInPlugs[0].value
        if_value = self.dataInPlugs[1].value
        else_value = "self.dataInPlugs[2].value"
        print(f"if {condition} , value 1 {if_value}, value2 {else_value}")
        if condition:
            self.dataOutPlugs[outIndex].value = if_value
        else:
            self.dataOutPlugs[outIndex].value = else_value
        return self.dataOutPlugs[outIndex]

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(125, 255, 146)
        self.nodeInterface.nodeGraphic.backGroundColor = backgroundColor
        self.createProxyWidget()
        self.nodeInterface.nodeGraphic.redesign(120, 80, "diamond")

    def createProxyWidget(self):
        self.lineEdit = QLineEdit()
        self.lineEdit.setStyleSheet(
            "background-color: \
                                       rgba(10,10,10,90); \
                                       color: rgba(255, 255, 102,255); \
                                       border-style: solid; \
                                       border-radius: 4px; border-width: 1px; \
                                       border-color: rgba(30,70,0,255);"
        )
        self.lineEdit.returnPressed.connect(self.returnName)
        self.nodeInterface.nodeGraphic.setProxyWidget(self.lineEdit)
        self.lineEdit.setText(str(self.resetValue))

    def returnName(self):
        self.changeInputValue(0, int(self.lineEdit.text()))

    def updateText(self, value):
        self.lineEdit.setText(str(value))


class ForLoopNode(AbstractNodeData):
    def __init__(self, start: int, end: int, step: int = 1, interface=None):
        super().__init__(numIn=1, numOuts=2, interface=interface)  # il nodo For Loop ha un solo ingresso e due uscite
        self.name = "ForLoopNode"
        self.resetValue = False
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)
        self.start = start
        self.end = end
        self.step = step
        self.currentValue = start

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        if outIndex == 0:  # l'uscita 0 indica se il ciclo è ancora valido
            return 1 if self.currentValue < self.end else 0
        else:  # l'uscita 1 indica il valore corrente del ciclo
            return self.currentValue

    def calculate(self):
        self.currentValue += self.step
        if self.currentValue >= self.end:
            self.currentValue = self.start
        super().calculate()  # esegue il calcolo delle uscite come al solito

    def redefineGraphics(self):
        borderColorDefault = generateColorVariation().returnColor(255, 204, 0)
        self.nodeInterface.nodeGraphic.borderColorDefault = borderColorDefault
        borderColorSelectColor = generateColorVariation().returnColor(255, 0, 0)
        self.nodeInterface.nodeGraphic.borderColorSelect = borderColorSelectColor
        backgroundColor = generateColorVariation().returnColor(83, 47, 252)
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


if __name__ == "__main__":
    # Crea alcuni nodi
    number1 = NumberNode(10)
    number2 = NumberNode(20)
    sum_node = SumNode()
    print(number1)
    print(number2)

    # print_node = PrintNode()

    # Collega i nodi tra loro
    number1.connect(sum_node, 0, 0)
    number2.connect(sum_node, 1, 0)
    print(sum_node)
    number1.disconnect(sum_node, 0, 0)
    number2.disconnect(sum_node, 1, 0)

    prod = ProductNode()
    number1.connect(prod, 0, 0)
    number2.connect(prod, 1, 0)
    print(prod)

    number1.disconnect(prod, 0, 0)
    number2.disconnect(prod, 1, 0)

    number1.changeInputValue(0, 2)
    number2.changeInputValue(0, 2)

    exp = ExpNode()
    number1.connect(exp, 0, 0)
    number2.connect(exp, 1, 0)
    print(exp)

    # crea il nodo For Loop che itera da 0 a 5 con passo 1
    forLoopNode = ForLoopNode(0, 5)

    # connetti un nodo che stampa il valore corrente del ciclo all'uscita 1 del nodo For Loop
    # printNode = PrintNode()
    # forLoopNode.connect(printNode, 0, 1)
    print(forLoopNode)
