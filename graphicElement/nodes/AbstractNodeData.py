from typing import *

from graphicElement.plugs.PlugData import PlugData


class AbstractNodeData:
    isNodeInCreation = True
    index = 0
    dataInPlugs: list[PlugData] = []
    dataOutPlugs: list[PlugData] = []
    resetValue = None
    isDebugging = False
    value = 0
    functionString = ""
    inConnection: list['Connection'] = []
    outConnection: list['inConnection'] = []

    def __init__(self, numIn: int, numOuts: int, interface):
        self.name = "abstractDataNode"
        self.nodeInterface = interface
        self.numberOfInputPlugs = numIn
        self.numberOfOutputPlugs = numOuts
        self.dataInPlugs: list[PlugData] = []
        self.dataOutPlugs: list[PlugData] = []

    @property
    def title(self):
        return f"{self.name}_{str(self.index)}"

    def forceNodeNameOnLoad(self, name, index):
        tempName = name.split("_")
        self.index = index
        self.name = tempName[0]

    def madeArbitraryName(self, name):
        self.name = name

    def createPlugs(self):
        for i in range(self.numberOfInputPlugs):
            plugIn = PlugData(i, "In", 0, self)
            self.dataInPlugs.append(plugIn)
        for i in range(self.numberOfOutputPlugs):
            plugOut = PlugData(i, "Out", 0, self)
            self.dataOutPlugs.append(plugOut)

    def changeInputValue(self, inputIndex, value, boolean=True):
        self.dataInPlugs[inputIndex].value = value
        if self.isDebugging:
            print(f"debugging from ChangeInputValue:"
                  f"{self.title} - changed Input value "
                  f"{self.dataInPlugs[inputIndex].name} "
                  f"= {self.dataInPlugs[inputIndex].value}")
        if boolean:
            if self.isNodeInCreation:
                self.calculate()
            else:
                self.calculate()
                self.nodeInterface.nodeGraphic.updateTextValue()
                self.nodeInterface.notifyToObserver()

    def connect(self, node: "AbstractNodeData", input_index: int, output_index: int):
        if input_index < len(node.dataInPlugs):
            node.dataInPlugs[input_index] = self.dataOutPlugs[output_index]
        else:
            print(f"{self.title} has an input error. inputIndex was = {input_index} but plugNumb is {len(self.dataInPlugs)}")
            # raise IndexError("Input index out of range.")

    def disconnect(self, node: "AbstractNodeData", input_index: int, output_index: int):
        node.dataInPlugs[input_index] = node.resetValue
        node.dataOutPlugs[output_index] = node.calculateOutput(output_index)

    def calculate(self):
        """
        La funzione calculate di AbstractNodeData viene
        chiamata quando si vuole calcolare il nuovo valore dei plugs di output del nodo.
        :return:
        """
        returnString = f"From Calculate: {self.title} "
        for i, outPlug in enumerate(self.dataOutPlugs):
            outPlug.value = self.calculateOutput(i)
            returnString += f"{outPlug.name} = {outPlug.value}"
            if outPlug.connection:
                returnString += f"{returnString} outPlug is connected!"
                connection = outPlug.connection
                returnString += f"connected Plug is: {connection.inputPlug.plugData.name} = {connection.inputPlug.plugData.value}"
                endNode = outPlug.connection.inputNode
                returnString += f"endNode: {endNode.title}"

                index = connection.inputPlug.plugData.index
                endNode.changeInputValue(index, outPlug.value, None)
                returnString += f"changedValue at{index} -> {outPlug.value}"
                if self.isDebugging:
                    print(returnString)
        if not self.isNodeInCreation:
            self.nodeInterface.nodeGraphic.updateTextValue()

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

    def redefineGraphics(self):
        """
        La parte grafica del nodo viene creata dopo la parte dati, utilizzando
        le loro classi astratte. Per ridefinire la grafica al momento, modificando solo
        la parte dati, si può fare l'override di questa classe che verrà chiamata in automatico.
        :return:
        """
        pass
