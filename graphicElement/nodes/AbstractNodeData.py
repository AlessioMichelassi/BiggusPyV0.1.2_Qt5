import contextlib
from typing import *

from graphicElement.plugs.plugInterface import plugInterface

"""
La classe AbstractNodeData rappresenta l'interfaccia di base per la gestione dei dati di un nodo di un grafico. 

La classe fornisce i seguenti metodi:

    __init__: 
                inizializza il nodo con il numero di plugs di input e output e l'interfaccia di input.
    createPlugs: 
                crea i plugs di input e output del nodo in base al numero specificato.
    changeInputValue: 
                modifica il valore di un plug di input specifico e chiama il metodo calculate per aggiornare 
                il valore dei plugs di output del nodo.
    calculate: aggiorna il valore dei plugs di output del nodo in base ai valori dei plugs di input.
    notifyToObserver: 
                notifica a tutti i nodi osservatori che il valore del nodo è cambiato, in modo da permettergli 
                di aggiornare i loro valori di conseguenza.

Inoltre, la classe definisce le seguenti variabili di istanza:

    index: indice del nodo.
    dataInPlugs: lista di plugs di input del nodo.
    dataOutPlugs: lista di plugs di output del nodo.
    resetValue: valore di reset del nodo.
    isDebugging: indica se il nodo è in modalità debug.
    name: nome del nodo.
    interface: interfaccia di input del nodo.
    numberOfInputPlugs: numero di plugs di input del nodo.
    numberOfOutputPlugs: numero di plugs di output del nodo.
"""


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
            plugIn = plugInterface("In", i, self)
            self.dataInPlugs.append(plugIn)
        for i in range(self.numberOfOutputPlugs):
            plugOut = plugInterface("Out", i, self)
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
        try:
            self.calculate()
            self.interface.notifyToObserver()
        except Exception as e:
            self.calculate()

    def calculate(self):
        """
        La funzione calculate di AbstractNodeData viene
        chiamata quando si vuole calcolare il nuovo valore dei plugs di output del nodo.
        :return:
        """
        for i, outPlug in enumerate(self.dataOutPlugs):
            outPlug.value = self.calculateOutput(i)
            if outPlug.connectedWith:
                outPlug.connection.endPlug.value = outPlug.value
                outPlug.connection.endPlug.nodeGraphic.updateTextValue()
        with contextlib.suppress(AttributeError):
            self.interface.nodeGraphic.updateTextValue()

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

        # put the plug object in self.connectWith of plugData class
        node.dataInPlugs[inIndex].connectedWith = self.dataOutPlugs[outIndex]
        self.dataOutPlugs[outIndex].connectedWith = node.dataInPlugs[outIndex]

    def disconnect(self, node: "AbstractNodeData", input_index: int, output_index: int):
        node.dataInPlugs[input_index].value = node.dataInPlugs[input_index].plugData.resetValue

    def redefineGraphics(self):
        """
        La parte grafica del nodo viene creata dopo la parte dati, utilizzando
        le loro classi astratte. Per ridefinire la grafica al momento, modificando solo
        la parte dati, si può fare l'override di questa classe che verrà chiamata in automatico.
        :return:
        """
        pass
