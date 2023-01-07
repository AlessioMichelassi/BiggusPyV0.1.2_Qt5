from typing import Dict, Union, List


class Observer:
    def __init__(self):
        self.observedNodesList = []

    def addObservedNode(self, node):
        self.observedNodesList.append(node)
        node.addObserver(self)

    def update(self, node):
        for observed_node in self.observedNodesList:
            observed_node.calculate()


class AbstractDataPlug:
    name: str = ""

    def __init__(self, index, name, value, parentNode):
        self.index = index
        self.name += f"{name}{index}"
        self.value = value
        self.connectedPlug = None
        self.parentNode = parentNode

    def changeValue(self, value):
        self.value = value

    def update(self):
        self.value = self.connectedPlug.value


class AbstractNodeData:
    index = 0
    dataInPlugs: list[AbstractDataPlug] = []
    dataOutPlugs: list[AbstractDataPlug] = []
    resetValue = None
    isDebugging = True

    def __init__(self, numIn: int, numOuts: int, interface=None):
        self.name = "abstractDataNode"
        self.interface = interface
        self.numberOfInputPlugs = numIn
        self.numberOfOutputPlugs = numOuts
        self.dataInPlugs: list[AbstractDataPlug] = []
        self.dataOutPlugs: list[AbstractDataPlug] = []

        self.observers = []

    @property
    def title(self):
        return f"{self.name}_{str(self.index)}"

    def createPlugs(self):
        for i in range(self.numberOfInputPlugs):
            plugIn = AbstractDataPlug(i, "In_", i, self)
            self.dataInPlugs.append(plugIn)
        for i in range(self.numberOfOutputPlugs):
            plugOut = AbstractDataPlug(i, "Out_", i, self)
            self.dataOutPlugs.append(plugOut)

    def addObserver(self, node):
        observer = Observer()
        observer.addObservedNode(node)
        self.observers.append(observer)

    def notifyToObserver(self):
        for observer in self.observers:
            observer.update()

    def __str__(self):
        returnString = f"Print from {self.name}:\n"
        for i in self.dataInPlugs:
            returnString += f"{i.name} = {i.value} "
        for i in self.dataOutPlugs:
            returnString += f"{i.name} = {i.value} "
        if self.interface is not None:
            return f"{self.interface.name} InputNumber: {self.numberOfInputPlugs}, OutputNumber {self.numberOfOutputPlugs}"
        else:
            return f"{returnString}: InPlugNumber: {self.numberOfInputPlugs}," \
                   f"OutPlugNumber {self.numberOfOutputPlugs}"

    def changeInputValue(self, inputIndex, value):
        """
        La funzione changeInputValue viene chiamata quando un plug
        di input viene collegato a un altro plug di output.
        La funzione riceve in input l'indice del plug di input
        del nodo che viene modificato e il valore che deve assumere.
        Dopodiché assegna il valore al plug di input e chiama la funzione calculate().

        La funzione calculate() viene implementata in modo diverso per ogni nodo,
        in quanto ogni nodo può essere utilizzato per effettuare un'operazione differente.
        In generale, questa funzione viene utilizzata per aggiornare il valore dei plugs
        di output del nodo in base ai valori dei plugs di input.

        Una volta che il valore dei plugs di output viene aggiornato,
        il nodo chiama la funzione notifyToObserver(),
        che notifica a tutti i nodi osservatori che il valore del nodo è cambiato,
        in modo da permettergli di aggiornare i loro valori di conseguenza.
        :param inputIndex: Indice del pLug in ingresso da cambiare
        :param value: valore da cambiare
        :return:
        """
        self.dataInPlugs[inputIndex].value = value
        isDebugging = False
        if isDebugging:
            print(f"debugging from ChangeInputValue:"
                  f"{self.name} - changed Input value "
                  f"{self.dataInPlugs[inputIndex].name} "
                  f"= {self.dataInPlugs[inputIndex].value}")
        self.calculate()

    def calculate(self):
        """
        La funzione calculate di AbstractNodeData viene
        chiamata quando si vuole calcolare il nuovo valore dei plugs di output del nodo.
        :return:
        """
        for i, out_plug in enumerate(self.dataOutPlugs):
            out_plug.value = self.calculateOutput(i)
        self.notifyToObserver()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        """
        La funzione calculateOutput è una funzione astratta,
        ovvero una funzione che deve essere implementata nelle
        classi che estendono AbstractNodeData, ma che non ha
        un'implementazione di default.

        Ciò significa che ogni classe che estende AbstractNodeData
        deve implementare calculateOutput, che dovrà calcolare
        il nuovo valore del plug di output in base all'indice
        del plug passato come argomento.

        Quando calculate viene chiamata, per ogni plug di output
        del nodo viene chiamata calculateOutput passando come argomento
        l'indice del plug e il risultato viene assegnato al valore del plug.

        In questo modo, ogni volta che si vuole calcolare il nuovo valore
        dei plugs di output del nodo, basta chiamare calculate e tutti
        i plugs di output verranno aggiornati.

        :param outIndex:
        :return:
        """
        raise NotImplementedError()

    def connect(self, node: "AbstractNodeData", inIndex: int, outIndex: int):
        value = self.dataOutPlugs[outIndex].value
        node.changeInputValue(inIndex, value)

    def disconnect(self, node: "AbstractNodeData", input_index: int, output_index: int):
        node.dataInPlugs[input_index] = self.resetValue


#####################################################
#
#           OPERATORI MATH
#
#


class NumberNode(AbstractNodeData):

    def __init__(self, value: Union[int, float]):
        super().__init__(numIn=1, numOuts=1)
        self.name = "NumberNode"
        self.resetValue = value
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)
        print(self)

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value
        return self.dataOutPlugs[0].value


class SumNode(AbstractNodeData):
    def __init__(self):
        super().__init__(numIn=2, numOuts=1)
        self.name = "SumNode"
        self.dataInPlugs = []
        self.dataOutPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.dataOutPlugs[outIndex].value = self.dataInPlugs[0].value + self.dataInPlugs[1].value
        self.notifyToObserver()
        return self.dataOutPlugs[outIndex].value


class ProductNode(AbstractNodeData):
    def __init__(self):
        super().__init__(numIn=2, numOuts=1)
        self.name = "ProductNode"
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.outPlugs[outIndex].value = self.inPlugs[0].value * self.inPlugs[1].value
        self.notifyToObserver()
        return self.outPlugs[outIndex].value


class ExpNode(AbstractNodeData):
    def __init__(self):
        super().__init__(numIn=2, numOuts=1)
        self.name = "ExponentialNode"
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.outPlugs[outIndex].value = self.inPlugs[0].value ** self.inPlugs[1].value
        self.notifyToObserver()
        return self.outPlugs[outIndex].value


class DivisionNode(AbstractNodeData):
    def __init__(self, isInteger=False):
        super().__init__(numIn=2, numOuts=1)
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
        self.notifyToObserver()
        return self.outPlugs[outIndex].value


class RemainderNode(AbstractNodeData):
    def __init__(self):
        super().__init__(numIn=2, numOuts=1)
        self.name = "ReminderNode"
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        self.outPlugs[outIndex].value = self.inPlugs[0].value % self.inPlugs[1].value
        self.notifyToObserver()
        return self.outPlugs[outIndex].value


#####################################################
#
#           OPERATORI STRINGA
#
#

class StringNode(AbstractNodeData):
    def __init__(self, value: str):
        super().__init__(numIn=0, numOuts=1)
        self.name = "StringNode"
        self.resetValue = value
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        self.outPlugs[outIndex].value = self.inPlugs[0].value
        return self.outPlugs[0].value


class ListNode(AbstractNodeData):
    def __init__(self, value: List[Union[int, float, str]]):
        super().__init__(numIn=0, numOuts=1)
        self.name = "StringNode"
        self.resetValue = value
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        self.outPlugs[outIndex].value = self.inPlugs[0].value
        return self.outPlugs[0].value


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

    def __init__(self):
        super().__init__(numIn=2, numOuts=1)
        self.name = "StringNode"
        self.resetValue = {}
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        key = self.inPlugs[0].value
        value = self.inPlugs[1].value
        self.outPlugs[outIndex].value = {key: value}
        return self.outPlugs[outIndex].value


class ConcatNode(AbstractNodeData):
    def __init__(self):
        super().__init__(numIn=2, numOuts=1)
        self.name = "ConcatNode"
        self.resetValue = ""
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        returnValue = str(self.inPlugs[0].value) + str(self.inPlugs[1].value)
        self.outPlugs[outIndex].value = returnValue
        return returnValue


class ReplaceNode(AbstractNodeData):
    def __init__(self):
        super().__init__(numIn=3, numOuts=1)
        self.name = "ReplaceNode"
        self.resetValue = ""
        self.inPlugs = []
        self.outPlugs = []
        self.createPlugs()
        self.changeInputValue(0, self.resetValue)

    def calculateOutput(self, outIndex: int) -> Union[str]:
        returnValue = str(self.inPlugs[0].value).replace(str(self.inPlugs[1].value), str(self.inPlugs[2].value))
        self.outPlugs[outIndex].value = returnValue
        return returnValue


class PrintNode(AbstractNodeData):
    def __init__(self):
        super().__init__(numIn=1, numOuts=0)
        self.dataInPlugs[0].value = None

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
    def __init__(self):
        super().__init__(numIn=2, numOuts=1)
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
    def __init__(self):
        super().__init__(numIn=2, numOuts=1)
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

    def __init__(self):
        super().__init__(numIn=3, numOuts=1)
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
    def __init__(self, start: int, end: int, step: int = 1):
        super().__init__(numIn=1, numOuts=2)  # il nodo For Loop ha un solo ingresso e due uscite
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
