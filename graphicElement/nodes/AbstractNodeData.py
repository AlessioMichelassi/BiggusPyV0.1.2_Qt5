from typing import *

from graphicElement.plugs.plugInterface import plugInterface


class AbstractNodeData:
    index = 0
    dataInPlugs: list[plugInterface] = []
    dataOutPlugs: list[plugInterface] = []
    resetValue = None
    isDebugging = True

    def __init__(self, numIn: int, numOuts: int, interface):
        self.name = "abstractDataNode"
        self.interface = interface
        self.numberOfInputPlugs = numIn
        self.numberOfOutputPlugs = numOuts
        self.dataInPlugs: list[plugInterface] = []
        self.dataOutPlugs: list[plugInterface] = []

    @property
    def title(self):
        return f"{self.name}_{str(self.index)}"

    def createPlugs(self):
        for i in range(self.numberOfInputPlugs):
            plugIn = plugInterface("In_", i, self)
            self.dataInPlugs.append(plugIn)
        for i in range(self.numberOfOutputPlugs):
            plugOut = plugInterface("Out_", i, self)
            self.dataOutPlugs.append(plugOut)

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
        La funzione changeInputValue viene chiamata quando un plugs
        di input viene collegato a un altro plugs di output.
        La funzione riceve in input l'indice del plugs di input
        del nodo che viene modificato e il valore che deve assumere.
        Dopodiché assegna il valore al plugs di input e chiama la funzione calculate().

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
        try:
            self.interface.nodeGraphic.updateTextValue()
            self.interface.notifyToObserver()
        except Exception as e:
            a = e

    def calculateOutput(self, outIndex: int) -> Union[int, float]:
        """
        La funzione calculateOutput è una funzione astratta,
        ovvero una funzione che deve essere implementata nelle
        classi che estendono AbstractNodeData, ma che non ha
        un'implementazione di default.

        Ciò significa che ogni classe che estende AbstractNodeData
        deve implementare calculateOutput, che dovrà calcolare
        il nuovo valore del plugs di output in base all'indice
        del plugs passato come argomento.

        Quando calculate viene chiamata, per ogni plugs di output
        del nodo viene chiamata calculateOutput passando come argomento
        l'indice del plugs e il risultato viene assegnato al valore del plugs.

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
