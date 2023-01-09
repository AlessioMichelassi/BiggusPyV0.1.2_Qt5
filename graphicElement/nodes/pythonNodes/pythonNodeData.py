from typing import Dict, Union, List

from graphicElement.nodes.AbstractNodeData import AbstractNodeData


#####################################################
#
#           OPERATORI MATH
#
#


class NumberNode(AbstractNodeData):

    def __init__(self, value: Union[int, float], interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = "NumberNode"
        self.resetValue = value
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value
        return self.dataOutPlugs[0].value


class SumNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "SumNode"
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value + self.dataInPlugs[1].value
        self.interface.notifyToObserver()
        return self.dataOutPlugs[outIndex].value


class ProductNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "ProductNode"
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.outPlugs[outIndex].value = self.inPlugs[0].value * self.inPlugs[1].value
        self.interface.notifyToObserver()
        return self.outPlugs[outIndex].value


class ExpNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "ExponentialNode"
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.outPlugs[outIndex].value = self.inPlugs[0].value ** self.inPlugs[1].value
        self.interface.notifyToObserver()
        return self.outPlugs[outIndex].value


class DivisionNode(AbstractNodeData):
    def __init__(self, isInteger=False,  interface=None):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.isInteger = isInteger
        self.name = "DivisionNode"
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        if self.isInteger:
            self.outPlugs[outIndex].value = self.inPlugs[0].value // self.inPlugs[1].value
        else:
            self.outPlugs[outIndex].value = self.inPlugs[0].value / self.inPlugs[1].value
        self.interface.notifyToObserver()
        return self.outPlugs[outIndex].value


class RemainderNode(AbstractNodeData):
    def __init__(self, isInteger=False,  interface=None):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "ReminderNode"
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.outPlugs[outIndex].value = self.inPlugs[0].value % self.inPlugs[1].value
        self.interface.notifyToObserver()
        return self.outPlugs[outIndex].value


#####################################################
#
#           OPERATORI STRINGA
#
#

class StringNode(AbstractNodeData):
    def __init__(self, value: str, interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = "StringNode"
        self.resetValue = value
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value
        return self.dataOutPlugs[0].value


class ListNode(AbstractNodeData):
    def __init__(self, value: List[Union[int, float, str]], interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = "ListNode"
        self.resetValue = value
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value
        return self.dataOutPlugs[0].value


class DictNode(AbstractNodeData):
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
        self.name = "StringNode"
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
        self.name = "ReplaceNode"
        self.resetValue = ""
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        returnValue = str(self.dataInPlugs[0].value).replace(str(self.dataInPlugs[1].value), str(self.dataInPlugs[2].value))
        self.dataOutPlugs[outIndex].value = returnValue
        return returnValue


class PrintNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=1, numOuts=1, interface=interface)
        self.name = "PrintNode"
        self.resetValue = ""
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex):
        return self.dataInPlugs[0].value

    def connect(self, endNode: "AbstractNodeData", input_index: int, output_index: int):
        endNode.dataInPlugs[input_index] = self.dataOutPlugs[output_index]


#####################################################
#
#           OPERATORI BOOLEANI
#
#


class AndNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "AndNode"
        self.resetValue = ""
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        input1 = self.inPlugs[0].value
        input2 = self.inPlugs[1].value
        self.outPlugs[outIndex].value = input1 and input2
        return self.outPlugs[outIndex].value


class OrNode(AbstractNodeData):
    def __init__(self, interface):
        super().__init__(numIn=2, numOuts=1, interface=interface)
        self.name = "OrNode"
        self.resetValue = ""
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        input1 = self.inPlugs[0].value
        input2 = self.inPlugs[1].value
        self.outPlugs[outIndex].value = input1 or input2
        return self.outPlugs[outIndex].value


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
        super().__init__(numIn=3, numOuts=1, interface=interface)
        self.name = "OrNode"
        self.resetValue = ""
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int):
        condition = self.inPlugs[0].value
        if_value = self.inPlugs[1].value
        else_value = self.inPlugs[2].value
        print(f"if {condition} , value 1 {if_value}, value2 {else_value}")
        if condition:
            self.outPlugs[outIndex].value = if_value
        else:
            self.outPlugs[outIndex].value = else_value
        return self.outPlugs[outIndex]


class ForLoopNode(AbstractNodeData):
    def __init__(self, start: int, end: int, step: int=1,  interface=None):
        super().__init__(numIn=1, numOuts=2, interface=interface) # il nodo For Loop ha un solo ingresso e due uscite
        self.name = "ForLoopNode"
        self.start = start
        self.end = end
        self.step = step
        self.currentValue = start

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        if outIndex == 0:  # l'uscita 0 indica se il ciclo è ancora valido
            return 1 if self.currentValue < self.end else 0
        else:  # l'uscita 1 indica il valore corrente del ciclo
            return self.currentValue

    def changeInputValue(self, inputIndex, value):
        self.dataInPlugs[inputIndex].value = value
        # il valore di ingresso del nodo For Loop non viene utilizzato,
        # quindi si può ignorare questa chiamata
        self.calculate()

    def calculate(self):
        self.currentValue += self.step
        if self.currentValue >= self.end:
            self.currentValue = self.start
        super().calculate()  # esegue il calcolo delle uscite come al solito


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
