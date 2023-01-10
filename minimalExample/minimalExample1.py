import importlib
import os
import json
import logging
import sys
from collections import OrderedDict
from typing import Union

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

CANVAS_SCALE = 0.9
CENTER_ON = (430, 340)


class Arrow(QGraphicsItem):
    currentNode = None

    def __init__(self, startPlug: 'plugGraphic', end_point, parent=None):
        super().__init__(parent)
        self.startPlug = startPlug
        self.endPlug = None
        self.start_point = startPlug.scenePos()
        self.end_point = end_point

    def setEndPoint(self, endPlug: 'plugGraphic'):
        self.endPlug = endPlug
        self.end_point = self.endPlug.scenePos()
        self.update()  # Aggiorna la visualizzazione della freccia
        if self.currentNode is not None:
            self.currentNode.outputConnection.append(self)
            self.currentNode = None

    def establishConnection(self, endPlug: 'plugGraphic'):
        # Crea una nuova freccia

        conn = Connection(self.startPlug, endPlug)
        # Aggiungi la freccia alla scena
        self.startPlug.plugInterface.connection = conn
        self.scene().addItem(conn)
        endPlug.plugInterface.connection = conn
        return conn

    def updatePosition(self, pos):
        self.end_point = pos
        self.update()  # Aggiorna la visualizzazione della freccia

    def updateArrow(self):
        self.start_point = self.startPlug.scenePos()

    def boundingRect(self):
        # Definiamo un bounding rectangle che include entrambe i punti della freccia
        return QRectF(self.start_point, self.end_point).normalized()

    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        # Disegniamo la freccia utilizzando un QPainter
        painter.setPen(QPen(Qt.black, 2, Qt.DashLine))
        painter.drawLine(self.start_point, self.end_point)


class Connection(QGraphicsItem):
    def __init__(self, _startPlug, _endPlug, parent=None):
        super().__init__(parent)
        self.startPlug = _startPlug
        self.endPlug = _endPlug
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setZValue(-1)
        self.connect()

    def canConnect(self, endPlug):
        return True

    def connect(self):
        startNode = self.startPlug.nodeGraphic
        startNode.connection = startNode
        endNode = self.endPlug.nodeGraphic
        endNode.connection = endNode
        startNode.nodeGraphic.connectPlug(startNode.nodeData, self.startPlug, endNode.nodeData, self.endPlug)

    def deleteConnection(self):
        self.startPlug.nodeGraphic.disconnectPlug(self.startPlug.nodeGraphic.nodeData, self.startPlug,
                                                  self.endPlug.nodeGraphic.nodeData, self.endPlug)
        self.endPlug.nodeGraphic.disconnectPlug(self.endPlug.nodeGraphic.nodeData, self.endPlug,
                                                self.startPlug.nodeGraphic.nodeData, self.startPlug)
        self.scene().removeItem(self)

    def updateGeometry(self):
        # Aggiorna la posizione della connessione in base alla posizione dei plugs di origine e di destinazione
        self.setLine(QLineF(self.startPlug.scenePos(), self.endPlug.scenePos()))

    def boundingRect(self):
        return QRectF(self.startPlug.scenePos(), self.endPlug.scenePos()).normalized()

    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        if not self.isSelected():
            painter.setPen(QPen(QColor(0, 20, 20), 3))
        else:
            painter.setPen(QPen(QColor(250, 50, 50), 3))
        painter.drawLine(self.startPlug.scenePos(), self.endPlug.scenePos())


class plugGraphic(QGraphicsItem):
    index = 0
    txtTitle: QGraphicsTextItem

    def __init__(self, plugInterface, diameter=8, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.plugInterface = plugInterface
        self.nodeInterface = parent
        self.boundingRectangle = QRectF(-self.diameter // 2, -self.diameter // 2, self.diameter * 2, self.diameter * 2)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setZValue(1)
        self.connection = None
        self.createTitleText()

    @property
    def name(self):
        return self.plugInterface.plugData.name

    def __str__(self):
        self.nodeInterface.nodeData.calculate()
        # sourcery skip: inline-immediately-returned-variable
        returnString = f"name: {self.name}, index: {self.index}, " \
                       f"value: {self.nodeInterface.nodeData.dataInPlugs[self.index].value} " \
                       f"nodeParent {self.nodeInterface.nodeData.title}, connection: {self.plugInterface.connectedWith}"
        return returnString

    def createTitleText(self):
        font = QFont()
        font.setPointSize(10)
        self.txtTitle = QGraphicsTextItem(self)
        self.txtTitle.setFont(font)
        # self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.txtTitle.setPlainText(self.name)
        # Posiziona la label 20 pixel sopra il centro del nodo
        self.txtTitle.setDefaultTextColor(Qt.GlobalColor.white)
        self.defineTextPosition()
        self.txtTitle.setZValue(2)

    def defineTextPosition(self):
        x = self.txtTitle.boundingRect().width()
        if "In" in self.name:
            x = (x * -1) - 5
        elif "Out" in self.name:
            x = 10
        self.txtTitle.setPos(x, -10)

    def boundingRect(self):
        return self.boundingRectangle.normalized()

    def paint(self, painter, option, widget=None):
        # Draw the plugs
        painter.setBrush(Qt.GlobalColor.white)
        if not self.isSelected():
            painter.setPen(Qt.GlobalColor.black)
        else:
            painter.setPen(Qt.GlobalColor.red)
        _centerPoint = QPoint(self.diameter // 2, self.diameter // 2)
        painter.drawEllipse(_centerPoint, self.diameter, self.diameter)
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.black)
        _radius = self.diameter // 2

        painter.drawEllipse(_centerPoint, 3, 3)

class plugData:
    _name: str = ""
    connectedWith: 'plugInterface'

    def __init__(self, index, name, value, parentNode, plugInterface):
        self.index = index
        self.plugInterface = plugInterface
        self._name = name
        self.resetValue = value
        self.value = value
        self.parentNode = parentNode
        self.connectedWith = None

    @property
    def name(self):
        return f"{self._name}_{self.index}"

    @name.setter
    def name(self, _name):
        self._name = _name

    def changeValue(self, value):
        self.value = value

    def update(self):
        self.value = self.connectedWith.value


class plugInterface:
    plugGraphic: plugGraphic

    def __init__(self, name, index, nodeData: 'AbstractNodeData', diameter=8):
        self.nodeInterface = nodeData.interface
        self.nodeData = nodeData
        self.plugData = plugData(index, name, 0, self.nodeInterface, self)

        self.plugGraphic = None
        self.connection = None

    @property
    def name(self):
        return self.plugData.name

    @name.setter
    def name(self, _name):
        self.plugData.name = _name

    @property
    def resetValue(self):
        return self.plugData.resetValue

    @property
    def value(self):
        return self.plugData.value

    @value.setter
    def value(self, _value):
        self.plugData.value = _value

    @property
    def connectedWith(self):
        return self.plugData.connectedWith

    @connectedWith.setter
    def connectedWith(self, plug):
        self.plugData.connectedWith = plug

    def disconnect(self):
        self.connection = None
        self.plugData.connectedWith = None
        self.plugData.value = self.resetValue

    def createPlug(self, _type: str, graphicNode):
        self.plugGraphic = plugGraphic(self, parent=graphicNode)
        return self.plugGraphic

class superText(QGraphicsTextItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Imposta il flag di evento per consentire di filtrare gli eventi
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

    def setText(self, text):
        self.parent.setValueFromGraphics(int(text))

    def eventFilter(self, obj, event):
        # Verifica se l'evento è una pressione del tasto Invio
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            # Esegue l'azione desiderata (ad esempio, imposta il nuovo valore del testo)
            self.setText(self.toPlainText().strip())
            return True
        return super().eventFilter(obj, event)

class AbstractNodeGraphic(QGraphicsItem):
    # NodeGraphic parameter
    width: int = 50
    height: int = 100

    borderColorDefault = QColor(10, 120, 10)
    borderColorSelect = QColor(255, 70, 10)
    backGroundColor = QColor(10, 180, 40)

    # NodeGraphics variable
    outputConnection = []
    nodeCounter = 0
    txtTitle: QGraphicsTextItem
    txtValue: QGraphicsTextItem
    valueContent: int
    nodeData = None
    nodeInterface = None

    def __init__(self, view, nodeInterface, parent=None):
        super().__init__(parent)
        self.graphicView = view
        self.nodeInterface = nodeInterface
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setZValue(1)

        # Create the input and output plugs list as emptyList
        self.graphicInputPlugs = []
        self.graphicOutputPlugs = []

        # Create the label
        self.createTitleText()
        self.createValueText()

        # Create the bounding rect
        self.boundingRect = QRectF(0, 0, self.width, self.height)

        # Set the default position
        self.setPos(QPointF(0, 0))

    def createTitleText(self):
        self.txtTitle = QGraphicsTextItem(self)
        self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.txtTitle.setPlainText(self.nodeInterface.nodeData.title)
        x = (self.txtTitle.boundingRect().width()//3)
        self.txtTitle.setPos(-x, -30)  # Posiziona la label 20 pixel sopra il centro del nodo
        self.txtTitle.setDefaultTextColor(Qt.GlobalColor.white)
        self.txtTitle.setZValue(2)

    def createValueText(self):
        self.txtValue = superText(self)
        self.txtValue.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.txtValue.installEventFilter(self.txtValue)
        x = (self.txtValue.boundingRect().width() / 2)
        y = self.height / 2
        self.txtValue.setPos(x, y)  # Posiziona la label 20 pixel sopra il centro del nodo
        self.txtValue.setPlainText("")
        self.txtValue.setDefaultTextColor(Qt.GlobalColor.black)
        self.txtValue.setZValue(2)

    def setValueFromGraphics(self, value):
        # sourcery skip: assign-if-exp, hoist-statement-from-if
        if type(self.nodeData) == "NumberNode":
            self.nodeData.dataInPlugs[0].value = int(value)
        else:
            self.nodeData.dataInPlugs[0].value = value
        self.txtValue.setPlainText(str(value))

    def updateTextValue(self):
        value = self.nodeData.dataOutPlugs[0].value
        self.txtValue.setPlainText(str(value))

    def setTitle(self, text):
        self.txtTitle.setPlainText(text)
        textItemWidth = self.txtTitle.boundingRect().width()
        textItemHeight = self.txtTitle.boundingRect().height()
        x = (self.width - textItemWidth) / 2
        y = (self.height - textItemHeight) / 2
        self.txtTitle.setPos(x, -30)

    def createPlugsIn(self, inNumber):
        """
        La parte grafica dei Plug viene definita qui perchè
        varia in base alle dimensioni del nodo.
        :param inNumber:
        :return:
        """
        # Create the input and output plugs
        x = -8
        if inNumber == 0:
            return
        elif inNumber == 1:
            y = self.height // 2
        else:
            y = (self.height // inNumber)
        for i in range(inNumber):
            plug = self.nodeInterface.nodeData.dataInPlugs[i].createPlug("In", self)
            plug.index = i
            plug.setPos(QPointF(x, y))
            y += plug.diameter * 3
            self.graphicInputPlugs.append(plug)

    def createPlugsOut(self, outNumber):
        x = self.width - 2
        if outNumber == 0:
            return
        elif outNumber == 1:
            y = self.height // 2
        else:
            y = (self.height // outNumber)
        for i in range(outNumber):
            plug = self.nodeInterface.nodeData.dataOutPlugs[i].createPlug("Out", self)
            plug.index = i
            plug.setPos(QPointF(x, y))
            self.graphicOutputPlugs.append(plug)
            y += plug.diameter * 3

    def redesign(self, width, height):
        """
        Basandosi sulle nuove dimensioni del nodo ricalcola la posizione del
        titolo e dei plug.
        :param width:
        :param height:
        :return:
        """
        self.width = width
        self.height = height
        self.boundingRect = QRectF(0, 0, self.width, self.height)
        textItemWidth = self.txtTitle.boundingRect().width()
        textItemHeight = self.txtTitle.boundingRect().height()
        x = (self.width - textItemWidth) / 2
        self.txtTitle.setPos(x, -30)
        inNumber = len(self.graphicInputPlugs)
        x = -8
        for plug in self.graphicInputPlugs:
            if inNumber == 0:
                return
            elif inNumber == 1:
                y = self.height // 2
            else:
                y = (self.height // inNumber)
            plug.setPos(QPointF(x, y))
            y += plug.diameter * 3

        outNumber = len(self.graphicOutputPlugs)
        x = self.width -2
        for plug in self.graphicOutputPlugs:
            if outNumber == 0:
                return
            elif outNumber == 1:
                y = self.height // 2
            else:
                y = (self.height // outNumber)
            plug.setPos(QPointF(x, y))
            y += plug.diameter * 3

    def boundingRect(self):
        return self.boundingRect.normalized()

    def paint(self, painter, option, widget=None):
        # Draw the node
        if not self.isSelected():
            painter.setPen(self.borderColorDefault)
        else:
            painter.setPen(self.borderColorSelect)
        painter.setBrush(self.backGroundColor)
        painter.drawRoundedRect(self.boundingRect, 5, 5)

    def itemChange(self, change, value):
        # sourcery skip: merge-nested-ifs
        # Update the position of the plugs when the node is moved
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if len(self.outputConnection) > 0:
                for connection in self.outputConnection:
                    connection.updateGeometry()
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Imposta il flag "selezionato" a True
            self.setSelected(True)
        # Chiamare la versione della superclasse del metodo mousePressEvent
        # per gestire gli altri tipi di pulsanti del mouse
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Imposta il flag "selezionato" a False
            self.setSelected(False)
        # Chiamare la versione della superclasse del metodo mouseReleaseEvent
        # per gestire gli altri tipi di pulsanti del mouse
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            # Sposta il nodo di una distanza pari alla differenza tra la posizione attuale del mouse
            # e la posizione del mouse al momento del click
            self.setPos(self.pos() + event.pos() - event.lastPos())
        # Chiamare la versione della superclasse del metodo mouseMoveEvent
        # per gestire gli altri tipi di pulsanti del mouse
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.nodeData.calculate()

class Observer:
    def __init__(self):
        self.observedNodesList = []

    def addObservedNode(self, node):
        self.observedNodesList.append(node)
        node.addObservedNode(self)

    def update(self):
        print("observer in action")
        for observed_node in self.observedNodesList:
            observed_node.calculate()


class AbstractNodeData:
    index = 0
    dataInPlugs: list['plugInterface'] = []
    dataOutPlugs: list['plugInterface'] = []
    resetValue = None
    isDebugging = True

    def __init__(self, numIn: int, numOuts: int, interface):
        self.name = "abstractDataNode"
        self.interface = interface
        self.numberOfInputPlugs = numIn
        self.numberOfOutputPlugs = numOuts
        self.dataInPlugs: list['plugInterface'] = []
        self.dataOutPlugs: list['plugInterface'] = []

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


class AbstractNodeInterface:
    nodeGraphic: AbstractNodeGraphic
    nodeData: AbstractNodeData

    def __init__(self, className: str, *args, view, **kwargs):

        # Crea l'istanza del nodoData
        self.type = className
        self.nodeData = self.createNode(className, *args, _interface=self, **kwargs)
        self.graphicView = view
        # Crea l'istanza del nodoGrafico
        self.nodeGraphic = AbstractNodeGraphic(view, self)
        self.nodeGraphic.nodeData = self.nodeData
        self.nodeGraphic.nodeInterface = self
        if 'value' in kwargs:
            self.nodeGraphic.setValueFromGraphics(kwargs['value'])
        self.createPlug()
        self.nodeData.redefineGraphics()
        self.observers = []

    @property
    def title(self):
        return str(self.nodeData.title)

    @title.setter
    def title(self, _name):
        self.nodeGraphic.setTitle(self.nodeData.title)

    def changeIndex(self, _index):
        self.nodeData.index = _index
        self.nodeGraphic.setTitle(self.nodeData.title)

    def createPlug(self):
        numInputs = self.nodeData.numberOfInputPlugs
        self.nodeGraphic.createPlugsIn(numInputs)

        numOutputs = self.nodeData.numberOfOutputPlugs
        self.nodeGraphic.createPlugsOut(numOutputs)

    @staticmethod
    def createNode(className: str, *args, _interface, **kwargs) -> 'AbstractNodeData':
        """
        Carica dinamicamente il modulo che contiene la classe del nodo
        Crea un'istanza della classe del nodo passando eventuali argomenti e keyword arguments
        Crea un'istanza della classe del nodo passando eventuali argomenti e keyword arguments
        :param _interface:
        :param className: il nome della classe del nodeTypes ad Es: SumNode o ProductNode
        :param args:
        :param kwargs:
        :return:
        """
        module = importlib.import_module("graphicElement.nodes.pythonNodes.pythonNodeData")
        node_class = getattr(module, className)
        return node_class(*args, interface=_interface, **kwargs)

    def connectPlug(self, startNode: 'AbstractNodeData', startPlug, endNode: 'AbstractNodeData', endPlug):
        startNode.connect(endNode, endPlug.index, startPlug.index)
        endPlug.plugInterface.connectedWith = startPlug.plugInterface
        startPlug.plugInterface.connectedWith = endPlug.plugInterface

    def disconnectPlug(self, _startNode, startPlug, _endNode, endPlug):
        # sourcery skip: assign-if-exp
        startNode = _startNode
        endNode = _endNode
        if type(_startNode) is AbstractNodeInterface or type(_startNode) is AbstractNodeGraphic:
            startNode = _startNode.nodeData
        if type(_endNode) is AbstractNodeInterface or type(_endNode) is AbstractNodeGraphic:
            endNode = _endNode.nodeData

        startNode.disconnect(endNode, startPlug.index, endPlug.index)
        value = startNode.resetValue
        self.nodeGraphic.setValueFromGraphics(value)

    def addObserver(self, node):
        observer = Observer()
        observer.addObservedNode(node)
        self.observers.append(observer)

    def notifyToObserver(self):
        for observer in self.observers:
            observer.update()

    def serialize(self):
        dicts = OrderedDict([
            ('name', self.nodeData.name),
            ('index', self.nodeData.index),
            ('type', self.type),
            ('pos', (self.nodeGraphic.pos().x(), self.nodeGraphic.pos().y())),
            ('inPlugsNumb', self.nodeData.numberOfInputPlugs),
            ('outPlugsNumb', self.nodeData.numberOfOutputPlugs)
        ])
        return json.dumps(dicts)


class graphicViewOverride(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)
    isConnectingPlug = False

    arrowList = []
    nodeList = []
    tempArrow = None

    def __init__(self, _graphicScene, parent=None):
        super(graphicViewOverride, self).__init__(parent)

        self.lastCTRLCopyFont = None
        self.lastCTRLCopyColor = None
        self.selectedItem = None
        self.graphicScene = _graphicScene
        self.mousePosition = QPoint(0, 0)
        self.setScene(self.graphicScene)
        self.canvas = None
        self.setRenderProperties()

    def setRenderProperties(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing
                            | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def keyPressEvent(self, event):  # sourcery skip: merge-nested-ifs
        self.checkKeyPressed(event)
        super(graphicViewOverride, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.lastMousePosition = event.pos()
        self.mousePosition = self.mapToScene(event.pos())
        self.scenePosChanged.emit(int(self.mousePosition.x()), int(self.mousePosition.y()))
        if self.isConnectingPlug:
            self.tempArrow.updatePosition(self.mapToScene(event.pos()))

    def leftMouseButtonPress(self, event):
        """
            Nel caso in cui si prema CTRL+ LeftMB si può fare il pan della scena
            :param event: default mouse event
            :return: noyhing
        """
        self.selectedItem = self.getItemAtClick(event)
        if isinstance(self.selectedItem, plugGraphic):
            if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
                print(self.selectedItem)
            else:
                self.createArrow(event)

    # LEFT MOUSE OVERRIDES
    def createArrow(self, event):
        # Crea una nuova freccia quando si clicca su un plugs
        self.isConnectingPlug = True
        self.tempArrow = Arrow(self.selectedItem, self.mapToScene(event.pos()))
        self.tempArrow.currentNode = self.selectedItem.parentItem()
        self.tempArrow.setZValue(-1)
        self.scene().addItem(self.tempArrow)

    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)
        if self.isConnectingPlug and type(item) == plugGraphic:
            connection = self.tempArrow.establishConnection(item)
            connection.connect()
            self.scene().removeItem(self.tempArrow)
            self.tempArrow = None
        elif self.tempArrow:
            self.scene().removeItem(self.tempArrow)
            self.tempArrow = None
        self.isConnectingPlug = False

    def checkKeyPressed(self, event):
        """
        Ogni volta che viene premuto un tasto avvia una funzione...
        :param event:
        :return:
        """
        key = event.key()
        if key == Qt.Key.Key_Plus:
            pass
        elif key == Qt.Key.Key_Minus:
            pass
        elif key == Qt.Key.Key_A:
            print("A pressed")
        elif key == Qt.Key.Key_S:
            print("B pressed")
        elif key == Qt.Key.Key_Delete:
            self.deleteObject(self.selectedItem)

    def getItemAtClick(self, event):
        """ Ritorna l'oggetto selezionato cliccandoci sopra"""
        pos = event.pos()
        return self.itemAt(pos)

    def deleteObject(self, obj):
        if isinstance(obj, Connection):
            obj.startPlug.plugInterface.disconnect()
            obj.endPlug.plugInterface.disconnect()
            self.scene().removeItem(obj)
        elif isinstance(obj, AbstractNodeGraphic):
            self.checkForPlugConnection(obj)

            self.scene().removeItem(obj)
        else:
            return

    def checkForPlugConnection(self, node):
        plugs = node.nodeData.dataInPlugs
        connections = []

        for plug in plugs:
            if plug.connectedWith:
                if plug.connection not in connections:
                    connections.append(plug.connection)
                plug.disconnect()
        plugs = node.nodeData.dataOutPlugs
        for plug in plugs:
            if plug.connectedWith:
                if plug.connection not in connections:
                    connections.append(plug.connection)
                plug.disconnect()
        for connection in connections:
            self.scene().removeItem(connection)


class canvas(QWidget):
    mainLayout: QLayout
    graphicView: graphicViewOverride
    filename = "untitled"
    sceneWidth = 5000
    sceneHeight = 5000
    name = "untitled"
    isDebugActive = False

    def __init__(self, parent=None):
        super(canvas, self).__init__(parent)

        self.nodesInTheScene = []
        self.nodeNames = []
        self.initUI()
        self.mainWin = parent

    def initUI(self):
        self.graphicScene = QGraphicsScene()
        self.graphicView = graphicViewOverride(self.graphicScene)
        self.graphicView.canvas = self
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.graphicView)

        self.setGeometry(200, 200, 1200, 800)
        self.setWindowTitle("BiggusPy")

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        contextMenu = QMenu(self)
        contextMenu.addSection("VariableNode")
        _stringNode = contextMenu.addAction("string node")
        _numberNode = contextMenu.addAction("number node")
        _listNode = contextMenu.addAction("list node")
        _dictNode = contextMenu.addAction("dictionary node")
        contextMenu.addSeparator()
        _sumNode = contextMenu.addAction("sum Node")
        _productNode = contextMenu.addAction("product Node")
        _printNode = contextMenu.addAction("print Node")
        contextMenu.addSeparator()

        _mousePosition = self.graphicView.mousePosition
        action = contextMenu.exec(self.mapToGlobal(event.pos()))
        node_interface = None
        if action == _numberNode:
            node_interface = AbstractNodeInterface("NumberNode", value=10, view=self.graphicView)
        elif action == _stringNode:
            node_interface = AbstractNodeInterface("StringNode", value="Hello World!", view=self.graphicView)
        elif action == _listNode:
            node_interface = AbstractNodeInterface("ListNode", value="Hello World!", view=self.graphicView)
        elif action == _dictNode:
            node_interface = AbstractNodeInterface("DictNode", value="", view=self.graphicView)
        elif action == _sumNode:
            node_interface = AbstractNodeInterface("SumNode", view=self.graphicView)
        elif action == _productNode:
            node_interface = AbstractNodeInterface("ProductNode", view=self.graphicView)
        elif action == _printNode:
            node_interface = AbstractNodeInterface("PrintNode", view=self.graphicView)
        else:
            pass
        if node_interface:
            self.addNodeToTheScene(node_interface, _mousePosition)

    def addNodeToTheScene(self, nodeInterface, mousePos):
        index = 0
        self.graphicScene.addItem(nodeInterface.nodeGraphic)
        nodeInterface.nodeGraphic.setPos(mousePos)

        for x in self.nodesInTheScene:
            if nodeInterface.title == x.title:
                index += 1
                nodeInterface.changeIndex(index)

        self.nodesInTheScene.append(nodeInterface)

    def saveScene(self):
        return self.serialize()

    def serialize(self):
        listOfDictionarySerialized = []
        for node in self.nodesInTheScene:
            listOfDictionarySerialized.append(node.serialize())

        dicts = OrderedDict([
            ('name', self.name),
            ('sceneWidth', self.sceneWidth),
            ('sceneHeight', self.sceneHeight),
            ('Nodes', listOfDictionarySerialized)])
        return json.dumps(dicts)

    def deserialize(self, serializedString):
        deserialized = json.loads(serializedString)
        self.name = deserialized['name']
        self.sceneWidth = deserialized['sceneWidth']
        self.sceneHeight = deserialized['sceneHeight']
        nodes = deserialized['Nodes']
        for node in nodes:
            self.deserializeNode(node)

    def deserializeNode(self, serializedJsonDictionary):
        deserialized = json.loads(serializedJsonDictionary)
        _name = deserialized["name"]
        _index = deserialized["index"]
        _type = deserialized["type"]
        _pos = deserialized["pos"]
        _inPlugsNumb = deserialized["inPlugsNumb"]
        _outPlugsNumb = deserialized["outPlugsNumb"]
        node = AbstractNodeInterface(_type, value=10, view=self.graphicView)
        pos = QPointF(float(_pos[0]), float(_pos[1]))
        self.addNodeToTheScene(node, pos)


class MainWindow(QMainWindow):
    canvas: canvas
    statusMousePosition: QLabel
    filename = "untitled"

    def __init__(self):
        super().__init__()
        self.initUI()
        self.createStatusBar()
        self.initMenu()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 800, 600)
        # Imposta il titolo della finestra
        self.setWindowTitle('BiggusPyV0.1.2')
        # Imposta l'icona della finestra
        # self.setWindowIcon(QIcon('path/to/icon.png'))
        self.canvas = canvas()
        self.setCentralWidget(self.canvas)

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.statusMousePosition = QLabel("")
        self.statusBar().addPermanentWidget(self.statusMousePosition)
        self.canvas.graphicView.scenePosChanged.connect(self.onScenePosChanged)

    def onScenePosChanged(self, x, y):
        self.statusMousePosition.setText(f"Scene Pos: {x}:{y}")

    def initMenu(self):
        # Crea il menù
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')

        # Aggiungi un'azione al menù File
        openAction = QAction('open', self)
        saveAction = QAction('save', self)
        exitAction = QAction('Quit', self)
        exitAction.setShortcut('Ctrl+Q')

        openAction.triggered.connect(self.open)
        saveAction.triggered.connect(self.save)
        exitAction.triggered.connect(qApp.quit)

        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        # Aggiungi un'azione al menù Modifica
        cutAction = QAction('Cut', self)
        cutAction.setShortcut('Ctrl+X')
        editMenu.addAction(cutAction)

    def save(self):
        data = self.canvas.saveScene()
        with open("testSave.txt", "w+") as f:
            f.write(data)

    def open(self):
        self.canvas.graphicScene.clear()
        data = ""
        with open("testSave.txt", "r") as f:
            data = f.read()

        self.canvas.deserialize(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
